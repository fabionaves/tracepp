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
from main.models import Sprint, Project, SprintUserStory, Requeriment, Artifact
from main.components.formviews import AddFormView, UpdateFormView


class SprintListView(ModelListProjectFilter):
    """
    #class:US006
    Sprint List
    """
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
    """
    #class:US006
    Details of Sprint
    """
    template_name = 'sprint/detail.html'

    def get_context_data(self, **kwargs):
        context = super(SprintDetailView, self).get_context_data(**kwargs)
        context['sprint'] = get_object_or_404(
                                                Sprint.objects.all(),
                                                project=self.request.session.get('project_id', None),
                                                id=kwargs['sprint_id']
                                              )
        #context['num_requeriment'] = Sprint.objects.filter(pk=kwargs['sprint_id']).aggregate(total=Count('sprintuserstory__userstory__requeriment'))
        #context['num_requeriment'] = Requeriment.objects.filter(userstory__sprintuserstory__sprint=kwargs['sprint_id']).a(total=Count('userstory__requeriment'))
        #context['num_requeriment'] = SprintUserStory.objects.filter(sprint_id=kwargs['sprint_id']).aggregate(total=Count('userstory__requeriment'))
        sprint_user_story = SprintUserStory.objects.filter(sprint_id=kwargs['sprint_id']).values_list('userstory_id')
        context['num_requeriment']=Rqueryset = Requeriment.objects.filter(userstory__in=sprint_user_story).annotate(total=Count('*')).count()
        context['num_userstories'] = SprintUserStory.objects.filter(sprint_id=kwargs['sprint_id']).count()
        context['total_artifacts'] = Artifact.objects.filter(
            project=self.request.session.get('project_id', None), sprint=context['sprint']).count()

        context['breadcrumbs'] = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
            {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id' : context['sprint'].id}), 'class': '', 'name': str(context['sprint'].title)},
         )
        return context


class SprintAddFormView(AddFormView):
    """
    #class:US006
    Add Sprint
    """
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
    """
    #class:US006
    Update Sprint
    """
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
    """
    #class:US006
    Delete Sprint
    """
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
    """
    #class:US006
    Alter History of sprint
    """
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
        if 'sprint_id' in kwargs:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': self.sprint_id}), 'class': '',
                 'name': 'Sprint'},
                {'link': '#', 'class': '', 'name': _('Delete')}
            )
        else:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                {'link': '#', 'class': '', 'name': _('Delete')}
            )
        return context
