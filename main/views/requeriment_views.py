from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.shortcuts import  get_object_or_404
from django.views.generic import DeleteView
from django.views.generic import ListView
from main.components.lists import  ModelListProjectFilter, TemplateViewProjectFilter
from main.decorators import require_project
from main.forms import RequerimentForm
from main.models import Project, Requeriment, SprintUserStory, Sprint, UserStory, Artifact
from main.components.formviews import AddFormView, UpdateFormView


class RequerimentListView(ModelListProjectFilter):
    model = Requeriment
    paginate_by = 20
    list_display = ('code','title', 'description','type')
    action_template = 'requeriment/choose_action.html'
    top_bar = 'requeriment/top_bar.html'
    page_title = _('Requeriments')
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
    )

    def get_queryset(self):
        queryset = super(RequerimentListView, self).get_queryset()
        if 'sprint_id' in self.kwargs:
            sprint_user_story = SprintUserStory.objects.filter(sprint_id=self.kwargs['sprint_id']).values_list('userstory_id')
            queryset = Requeriment.objects.filter(userstory__in=sprint_user_story).annotate(total=Count('*'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RequerimentListView, self).get_context_data()
        if 'sprint_id' in self.kwargs:
            sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'])
            context['breadcrumbs'] = (
               {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
               {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
               {'link': reverse_lazy('main:sprint-details',kwargs={'sprint_id':sprint.id}), 'class': '', 'name': sprint},
               {'link': '#', 'class': '', 'name': _('Requeriment')},
            )
        return context


class RequerimentAddFormView(AddFormView):
    page_title = _('Requeriment')
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
        context['num_userstories']= UserStory.objects.filter(requeriment=requeriment).aggregate(total=Count('*'))
        context['total_artifacts'] = Artifact.objects.filter(
            project=self.request.session.get('project_id', None),requeriment=requeriment).count()
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


class RequerimentDeleteView(SuccessMessageMixin, DeleteView):
    model = Requeriment
    template_name = 'requeriment/delete.html'
    fields = ('code', 'title', 'description')
    success_url = '/requeriment/'

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(RequerimentDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RequerimentDeleteView, self).get_context_data()
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


class RequerimentGraphDetailView(TemplateViewProjectFilter):
    template_name = 'requeriment/graph_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RequerimentGraphDetailView, self).get_context_data(**kwargs)
        requeriment = get_object_or_404(Requeriment,  project=self.request.session.get('project_id', None), pk=self.kwargs['pk'])
        context['breadcrumbs'] = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
            {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment.id}), 'class': '',
             'name': requeriment.code},
            {'link':'#', 'class': '','name':_('Graph')},
        )
        context['dependent_requeriments'] = Requeriment.objects.filter(depends_on=requeriment)
        context['depends_on'] = requeriment.depends_on.all()
        context['requeriment'] = requeriment

        return context
