from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView
from main.components.lists import ModelList, ModelListProjectFilter, TemplateViewProjectFilter
from main.decorators import require_project
from main.forms import ProjectForm, RequerimentForm
from main.models import Sprint, Project, Requeriment
from main.components.formviews import AddFormView, UpdateFormView


class ProjectView(ModelList):
    model = Project
    list_display = ('name', )
    page_title = _('Choose a project:')
    action_template = 'project/choose_action.html'

    def dispatch(self, request, *args, **kwargs):
        if 'project_id' in self.kwargs:
            self.request.session['project_id'] = self.kwargs['project_id']
            return redirect('/')
        else:
            return super(ProjectView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Project.objects.all()
        else:
            return Project.objects.filter(user=user)


class ProjectListView(ProjectView):
    model = Project
    page_title = 'Projects'
    list_display = ('name', 'requester', 'points_type')
    action_template = "components/lists/action.html"
    top_bar = 'project/top_bar.html'
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:project-list'), 'class': 'active', 'name': _('Project')},
    )


class ProjectAddFormView(AddFormView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/form.html'
    success_url = '/project/list/'
    success_message = _('Project was created successfully')
    tabs = (
        {"title" : "Project", "id" : "project","class" : "active", "fields" : ("name","requester","description","points_type","total_points")},
        {"title" : "Users", "id" : "user", "fields" : ("user",)},
    )
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:project-list'), 'class': 'active', 'name': _('Project')},
        {'link': '#', 'class': 'active', 'name': _('Add')},
    )


class ProjectUpdateFormView(UpdateFormView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/form.html'
    success_url = '/project/list/'
    success_message = _('Project was saved successfully')
    tabs = (
        {"title": "Project", "id": "project", "class": "active",
         "fields": ("name", "requester", "description", "points_type", "total_points")},
        {"title": "Users", "id": "user", "fields": ("user",)},
    )
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:project-list'), 'class': 'active', 'name': _('Project')},
        {'link': '#', 'class': 'active', 'name': _('Update')},
    )


class HomeView(TemplateViewProjectFilter):
    template_name = 'home/home.html'
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
    )

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['total_sprints'] = Sprint.objects.filter(project=self.request.session.get('project_id', None)).count()
        context['total_requeriments'] = Requeriment.objects.filter(project=self.request.session.get('project_id', None)).count()
        return context


class SprintListView(ModelListProjectFilter):
    model = Sprint
    paginate_by = 20
    list_display = ('title', 'status', 'begin', 'end')
    action_template = 'sprint/choose_action.html'
    top_bar = 'sprint/top_bar.html'
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
    )


class SprintDetailView(TemplateViewProjectFilter):
    template_name = 'sprint/detail.html'

    def get_context_data(self, **kwargs):
        context = super(SprintDetailView, self).get_context_data(**kwargs)
        context['sprint'] = get_object_or_404(
                                                Sprint.objects.all(),
                                                project=self.request.session.get('project_id', None),
                                                id=kwargs['sprint_id']
                                              )
        context['breadcrumbs'] = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
            {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id' : context['sprint'].id}), 'class': '', 'name': str(context['sprint'].title)},
         )
        return context


class SprintAddFormView(AddFormView):
    page_title = 'Sprint'
    model = Sprint
    head_template = 'sprint/form_head.html'
    fields = ('title', 'status', 'begin', 'end')
    success_url = '/sprint/'
    success_message = _('Sprint was created successfully')
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
        {'link': '#', 'class': '', 'name': _('Add')},
    )

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(SprintAddFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.request.session['project_id'])
        form.instance.changed_by = self.request.user
        form.instance.project = project
        return super(SprintAddFormView, self).form_valid(form)



class SprintUpdateFormView(UpdateFormView):
    page_title = 'Sprint'
    model = Sprint
    head_template = 'sprint/form_head.html'
    fields = ('title', 'status', 'begin', 'end')
    success_message = _('Sprint was saved successfully')

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(SprintUpdateFormView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return "/sprint/%d/" % self.object.id

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.request.session['project_id'])
        form.instance.project = project
        return super(SprintUpdateFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SprintUpdateFormView, self).get_context_data()
        context['breadcrumbs'] = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
            {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': context['sprint'].id}), 'class': '',
             'name': str(context['sprint'].title)},
            {'link': '#', 'class': '', 'name': _('Update')}
        )
        return context


class SprintDeleteView(SuccessMessageMixin, DeleteView):
    model = Sprint
    template_name = 'sprint/delete.html'
    fields = ('title', 'status', 'begin', 'end')
    success_url = '/sprint/'

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(SprintDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SprintDeleteView, self).get_context_data()
        context['breadcrumbs'] = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
            {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': context['sprint'].id}), 'class': '',
             'name': str(context['sprint'].title)},
            {'link': '#', 'class': '', 'name': _('Delete')}
        )
        return context


class SprintHistoryView(ListView):
    model = Sprint
    template_name = 'sprint/history.html'
    list_display = ('history_user',)
    page_title = _('Sprint Change History:')
    sprint_id = False

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        if 'sprint_id' in kwargs:
            self.sprint_id = kwargs['sprint_id']
        return super(SprintHistoryView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.sprint_id:
            queryset = self.model.history.filter(project=self.request.session.get('project_id', None), id=self.sprint_id)
        else:
            queryset = self.model.history.filter(project=self.request.session.get('project_id', None))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SprintHistoryView, self).get_context_data()
        context['breadcrumbs'] = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
            {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': self.sprint_id}), 'class': '',
             'name': 'Sprint'},
            {'link': '#', 'class': '', 'name': _('Delete')}
        )
        return context


class RequerimentListView(ModelListProjectFilter):
    model = Requeriment
    paginate_by = 20
    list_display = ('code','title', 'description','type')
    action_template = 'requeriment/choose_action.html'
    top_bar = 'requeriment/top_bar.html'
    page_title = 'Requeriments'
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
    )


class RequerimentAddFormView(AddFormView):
    page_title = 'Requeriment'
    model = Requeriment
    form_class = RequerimentForm
    success_url = '/requeriment/'
    success_message = _('Requeriment was created successfully')
    tabs = (
        {"title": "Requirement", "id": "requeriment", "class": "active",
         "fields": ('code', 'title', 'description', 'type')},
        {"title": "Depends On", "id": "depends_on", "fields": ("depends_on",)},
    )
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
        {'link': '#', 'class': '', 'name': _('Add')},
    )

    def get_form(self):
        return self.form_class(request=self.request,**self.get_form_kwargs())

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(RequerimentAddFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.request.session['project_id'])
        form.instance.changed_by = self.request.user
        form.instance.project = project
        return super(RequerimentAddFormView, self).form_valid(form)


class RequerimentUpdateFormView(UpdateFormView):
    page_title = 'Requeriment'
    model = Requeriment
    form_class = RequerimentForm
    success_url = '/requeriment/'
    success_message = _('Requeriment was created successfully')
    tabs = (
        {"title": "Requirement", "id": "requeriment", "class": "active",
         "fields": ('code', 'title', 'description', 'type')},
        {"title": "Depends On", "id": "depends_on", "fields": ("depends_on",)},
    )

    def get_form(self):
        return self.form_class(request=self.request,**self.get_form_kwargs())

    def get_success_url(self):
        return "/requeriment/%d/" % self.object.id


    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(RequerimentUpdateFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.request.session['project_id'])
        form.instance.changed_by = self.request.user
        form.instance.project = project
        return super(RequerimentUpdateFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimentUpdateFormView, self).get_context_data()
        context['breadcrumbs'] = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
            {'link': reverse_lazy('main:requeriment-details', kwargs={'pk' : self.object.id}), 'class': '', 'name': self.object.code},
            {'link': '#', 'class': '', 'name': _('Add')},
        )
        return context


class RequerimentDetailView(TemplateViewProjectFilter):
    template_name = 'requeriment/detail.html'


    def get_context_data(self, **kwargs):
        context = super(RequerimentDetailView, self).get_context_data(**kwargs)
        requeriment = get_object_or_404(
                                                Requeriment.objects.all(),
                                                project=self.request.session.get('project_id', None),
                                                id=kwargs['pk']
                                              )
        context['breadcrumbs'] = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
            {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment.id}), 'class': '',
             'name': requeriment.code},
        )
        context['dependent_requeriments'] = Requeriment.objects.filter(depends_on=requeriment)
        context['depends_on'] = requeriment.depends_on.all()
        context['requeriment']=requeriment
        return context

class RequerimentHistoryView(ListView):
    model = Requeriment
    template_name = 'requeriment/history.html'
    list_display = ('history_user',)
    page_title = _('Requeriment Change History:')
    pk = False

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            self.pk = kwargs['pk']
        return super(RequerimentHistoryView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.pk:
            queryset = self.model.history.filter(project=self.request.session.get('project_id', None), id=self.pk)
        else:
            queryset = self.model.history.filter(project=self.request.session.get('project_id', None))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RequerimentHistoryView, self).get_context_data()
        context['breadcrumbs'] = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
            {'link': '#', 'class': '', 'name': _('History')},
        )
        return context


class RequerimentGraphView(TemplateViewProjectFilter):
    template_name = 'requeriment/graph.html'

    def get_context_data(self, **kwargs):
        context = super(RequerimentGraphView, self).get_context_data(**kwargs)
        requeriments = Requeriment.objects.filter(project=self.request.session.get('project_id', None))
        context['requeriments']=requeriments

        context['breadcrumbs'] = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
            {'link': '#', 'class': '', 'name': _('Graph')},
        )
        return context