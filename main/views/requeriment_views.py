from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView
from django.views.generic import ListView

from main.components.breadcrumbs import requeriments_breadcrumbs, requeriments_sucess_url
from main.components.lists import  ModelListProjectFilter, TemplateViewProjectFilter
from main.decorators import require_project
from main.forms import RequerimentForm
from main.components.formviews import AddFormView, UpdateFormView
from main.services.project import ProjectService
from main.services.requeriment import RequerimentService
from main.services.sprint import SprintService


class RequerimentListView(ModelListProjectFilter):
    """
    #class:US005
    List of project's requeriments
    """
    model = RequerimentService.get_requeriment_model()
    paginate_by = 20
    list_display = ('code','title', 'description','type')
    action_template = 'requeriment/choose_action.html'
    top_bar = 'requeriment/top_bar.html'
    page_title = _('Requeriments')
    ordering = 'code'

    def get_queryset(self):
        queryset = super(RequerimentListView, self).get_queryset()
        if 'sprint_id' in self.kwargs:
            sprint_user_story_list = SprintService.get_userstories_from_sprint(self.request.session['project_id'], self.kwargs['sprint_id']).values_list('id')
            queryset = SprintService.get_requeriments_from_sprint(sprint_user_story_list)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(RequerimentListView, self).get_context_data()
        context['breadcrumbs'] = requeriments_breadcrumbs(
            self.request.session['project_id'],
            self.kwargs.get('pk'),
            self.kwargs.get('sprint_id')
        )
        return context


class RequerimentAddFormView(AddFormView):
    """
    #class:US005
    Requeriment add
    """
    page_title = _('Requeriment')
    model = RequerimentService.get_requeriment_model()
    form_class = RequerimentForm
    success_message = _('Requeriment was created successfully')
    tabs = (
        {"title": _("Requirement"), "id": "requeriment", "class": "active",
         "fields": ('code', 'title', 'description', 'type')},
        {"title": _("Depends on"), "id": "depends_on", "fields": ("depends_on",)},
    )
    breadcrumbs = False

    def get_success_url(self):
        return requeriments_sucess_url(False, False)

    def get_form(self):
        return self.form_class(request=self.request,**self.get_form_kwargs())

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(RequerimentAddFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = ProjectService.get_project(self.request.session['project_id'])
        form.instance.changed_by = self.request.user
        form.instance.project = project
        return super(RequerimentAddFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimentAddFormView, self).get_context_data()
        context['breadcrumbs'] = requeriments_breadcrumbs(
            self.request.session['project_id'],
            self.kwargs.get('pk'),
            self.kwargs.get('sprint_id'),
            _('Add')
        )
        return context


class RequerimentUpdateFormView(UpdateFormView):
    """
    #class:US005
    Edit requeriment
    """
    page_title = _('Requeriment')
    model = RequerimentService.get_requeriment_model()
    form_class = RequerimentForm
    success_message = _('Requeriment was updated successfully')
    tabs = (
        {"title": _("Requirement"), "id": "requeriment", "class": "active",
         "fields": ('code', 'title', 'description', 'type')},
        {"title": _("Depends on"), "id": "depends_on", "fields": ("depends_on",)},
    )

    def get_form(self):
        return self.form_class(request=self.request,**self.get_form_kwargs())

    def get_success_url(self):
        return requeriments_sucess_url(self.kwargs.get('pk'), self.kwargs.get('sprint_id'))

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(RequerimentUpdateFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = ProjectService.get_project(self.request.session['project_id'])
        form.instance.changed_by = self.request.user
        form.instance.project = project
        return super(RequerimentUpdateFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequerimentUpdateFormView, self).get_context_data()
        context['breadcrumbs'] = requeriments_breadcrumbs(
            self.request.session['project_id'],
            self.kwargs.get('pk'),
            self.kwargs.get('sprint_id'),
            _('Update')
        )
        return context


class RequerimentDetailView(TemplateViewProjectFilter):
    """
    #class:US005
    Detail of requeriment
    """
    template_name = 'requeriment/detail.html'

    def get_context_data(self, **kwargs):
        context = super(RequerimentDetailView, self).get_context_data(**kwargs)
        requeriment = RequerimentService.get_requeriment(self.request.session.get('project_id', None), self.kwargs['pk'])
        context['breadcrumbs'] = requeriments_breadcrumbs(
            self.request.session['project_id'],
            self.kwargs['pk'],
            self.kwargs.get('sprint_id')
        )
        context['num_userstories']= RequerimentService.get_num_userstories_from_requeriment(requeriment)
        context['total_artifacts'] = RequerimentService.get_num_artifacts_from_requeriment(self.request.session.get('project_id', None),
                                                                                           requeriment
                                                                                           )
        context['dependent_requeriments'] = RequerimentService.get_dependent_requeriments(requeriment)
        context['depends_on'] = requeriment.depends_on.all()
        context['requeriment']=requeriment
        return context


class RequerimentHistoryView(ListView):
    """
    #class:US005
    Alter history of the requeriment
    """
    model = RequerimentService.get_requeriment_model()
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
        context['breadcrumbs'] = requeriments_breadcrumbs(
            self.request.session['project_id'],
            self.kwargs.get('pk'),
            self.kwargs.get('sprint_id'),
            _('Change History')
        )
        return context


class RequerimentDeleteView(SuccessMessageMixin, DeleteView):
    """
    #class:US005
    Delete requeriment
    """
    model = RequerimentService.get_requeriment_model()
    template_name = 'requeriment/delete.html'
    fields = ('code', 'title', 'description')

    def get_success_url(self):
        return reverse('main:requeriment')

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(RequerimentDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RequerimentDeleteView, self).get_context_data()
        context['breadcrumbs'] = requeriments_breadcrumbs(
            self.request.session['project_id'],
            self.kwargs.get('pk'),
            self.kwargs.get('sprint_id'),
            _("Delete")
        )
        return context

class RequerimentGraphView(TemplateViewProjectFilter):
    """
    #class:US014
    """
    template_name = 'requeriment/graph.html'

    def get_context_data(self, **kwargs):
        context = super(RequerimentGraphView, self).get_context_data(**kwargs)
        requeriments = ProjectService.get_project_requeriments(self.request.session.get('project_id', None))
        context['requeriments']=requeriments
        context['breadcrumbs'] = requeriments_breadcrumbs(
            self.request.session['project_id'],
            self.kwargs.get('requeriment_id'),
            self.kwargs.get('sprint_id'),
            _('Graph'),
        )
        return context


class RequerimentGraphDetailView(TemplateViewProjectFilter):
    """
    #class:US014
    """
    template_name = 'requeriment/graph_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RequerimentGraphDetailView, self).get_context_data(**kwargs)
        requeriment = RequerimentService.get_requeriment(self.request.session.get('project_id', None), self.kwargs['pk'])

        context['breadcrumbs'] = requeriments_breadcrumbs(
            self.request.session['project_id'],
            self.kwargs.get('pk'),
            self.kwargs.get('sprint_id'),
            _('Graph'),
        )
        context['dependent_requeriments'] = RequerimentService.get_dependent_requeriments(requeriment)
        context['depends_on'] = requeriment.depends_on.all()
        context['requeriment'] = requeriment

        return context
