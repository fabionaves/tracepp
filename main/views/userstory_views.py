from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView
from django.views.generic import ListView

from main.components.breadcrumbs import userstories_breadcrumbs
from main.components.bugtracking.factory import BugTrackingFactory
from main.components.lists import ModelListProjectFilter, TemplateViewProjectFilter
from main.decorators import require_project
from main.forms import UserStoryForm, SprintUserStoryInlineFormSet, SprintUserStoryInlineFormSetFiltrado
from main.components.formviews import AddFormView, UpdateFormView
from main.models import Artifact
from main.models import ArtifactType
from main.models import UserStory
from main.services.artifact import ArtifactService
from main.services.project import ProjectService
from main.services.requeriment import RequerimentService
from main.services.sprint import SprintService
from main.services.userstory import UserStoryService


class UserStoryListView(ModelListProjectFilter):
    """
    #class:US007
    List of US
    """
    model = UserStoryService.get_userstory_model()
    page_title = _('User Story')
    list_display = ('code', 'title','description')
    action_template = 'userstory/action.html'
    top_bar = 'userstory/top_bar.html'

    def get_queryset(self):

        if 'sprint_id' in self.kwargs and 'requeriment_id' in self.kwargs:
            return RequerimentService.get_userstories_from_requeriment(self.request.session.get('project_id', None),
                                                                       self.kwargs['requeriment_id'])
        elif 'sprint_id' in self.kwargs:
            return SprintService.get_userstories_from_sprint(self.request.session.get('project_id', None),
                                                             self.kwargs['sprint_id'])
        elif 'requeriment_id' in self.kwargs:
            return RequerimentService.get_userstories_from_requeriment(self.request.session.get('project_id', None),
                                                                       self.kwargs['requeriment_id'])
        else:
            return super(UserStoryListView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(UserStoryListView, self).get_context_data()

        context['breadcrumbs'] = userstories_breadcrumbs(
            self.request.session.get('project_id'),
            self.kwargs.get('requeriment_id'),
            self.kwargs.get('sprint_id')
        )
        return context


class UserStoryDetailView(TemplateViewProjectFilter):
    """
    #class:US007
    Detail of US
    """
    template_name = 'userstory/detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserStoryDetailView, self).get_context_data()
        userstory = UserStoryService.get_userstory(self.request.session.get('project_id', None), self.kwargs['pk'])
        context['userstory'] = userstory
        context['total_artifacts'] = UserStoryService.get_num_artifacts_from_userstory(
            self.request.session.get('project_id', None),
            userstory
        )
        context['total_file_artifacts'] = UserStoryService.get_num_file_artifacts_from_userstory(
            self.request.session.get('project_id', None),
            userstory
        )
        context['total_source_artifacts'] = UserStoryService.get_num_source_artifacts_from_userstory(
            self.request.session.get('project_id', None),
            userstory
        )
        context['total_activities'] = UserStoryService.get_num_activity_artifacts_from_userstory(
            self.request.session.get('project_id', None),
            userstory
        )
        context['total_estimated_time'] = UserStoryService.get_total_estimated_time_from_userstory(
            self.request.session.get('project_id', None),
            userstory
        )
        context['total_spent_time'] = UserStoryService.get_total_spent_time_from_userstory(
            self.request.session.get('project_id', None),
            userstory
        )
        context['userstory_storypoints'] = UserStoryService.get_userstory_storypoints(
            self.request.session.get('project_id', None),
            userstory
        )
        context['userstory_businnesvalue'] = UserStoryService.get_userstory_businnesvalue(
            self.request.session.get('project_id', None),
            userstory
        )
        context['breadcrumbs'] = userstories_breadcrumbs(
            self.request.session.get('project_id'),
            self.kwargs.get('requeriment_id'),
            self.kwargs.get('sprint_id'),
            self.kwargs.get('pk')
        )
        return context

class UserStoryHistoryView(ListView):
    """
    Alter History of userstory
    """
    model = UserStoryService.get_userstory_model()
    template_name = 'userstory/history.html'
    list_display = ('history_user',)
    page_title = _('Sprint Change History:')
    sprint_id = False

    def get_context_data(self, **kwargs):
        context = super(UserStoryDetailView, self).get_context_data()
        userstory = UserStoryService.get_userstory(self.request.session.get('project_id', None), self.kwargs['pk'])
        context['breadcrumbs'] = userstories_breadcrumbs(
            self.request.session.get('project_id'),
            self.kwargs.get('requeriment_id'),
            self.kwargs.get('sprint_id'),
            self.kwargs.get('pk')
        )
        return context


class UserStoryAddFormView(AddFormView):
    """
    #class:US007
    Add US
    """
    page_title = 'UserStory'
    model = UserStoryService.get_userstory_model()
    form_class = UserStoryForm
    success_message = _('UserStory was created successfully')
    tabs = (
        {"title": _("UserStory"), "id": "userstory", "class": "active",
         "fields": ('code', 'title', 'description', 'acceptanceCriteria', )},
        {"title": "Sprints", "id": "sprints", "inlines": ("userstory/sprint.html",)},
        {"title": _("Requeriments"), "id": "requeriments", "fields": ('requeriment',)},
    )

    def get_success_url(self):
        if 'sprint_id' in self.kwargs:
            return reverse_lazy('main:userstory', kwargs={'sprint_id':self.kwargs['sprint_id']})
        elif 'requeriment_id' in self.kwargs:
            return reverse_lazy('main:userstory', kwargs={'requeriment_id':self.kwargs['requeriment_id']})
        else:
            return reverse_lazy('main:userstory')

    def get_form(self, form=False):
        return self.form_class(request=self.request, **self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        sprint_userstory_form = SprintUserStoryInlineFormSet(self.request.POST)
        if form.is_valid() and sprint_userstory_form.is_valid():
            return self.form_valid(form, sprint_userstory_form)
        else:
            return self.form_invalid(form, sprint_userstory_form)

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(UserStoryAddFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form, sprint_userstory_form):
        project = ProjectService.get_project(self.request.session['project_id'])
        form.instance.changed_by = self.request.user
        form.instance.project = project
        self.object = form.save()
        sprint_userstory_form.instance = self.object
        spus = sprint_userstory_form.save()

        #save new redmine issue related to userstory and artifact related
        if project.issueOnInsertUserStory:
            ArtifactService.add_redmine_activity(project,spus, self.request, self.object)


        return HttpResponseRedirect(self.get_success_url())


    def get_context_data(self, **kwargs):
        context = super(UserStoryAddFormView, self).get_context_data()
        context['SprintUserStoryInline']=SprintUserStoryInlineFormSetFiltrado(project=self.request.session['project_id'])
        context['breadcrumbs'] = userstories_breadcrumbs(
            self.request.session.get('project_id'),
            self.kwargs.get('requeriment_id'),
            self.kwargs.get('sprint_id'),
            self.kwargs.get('pk'),
            _('Add')
        )
        return context


class UserStoryUpdateFormView(UpdateFormView):
    """
    #class:US007
    Update US
    """
    page_title = 'UserStory'
    model = UserStoryService.get_userstory_model()
    form_class = UserStoryForm
    success_message = _('UserStory was created successfully')
    tabs = (
        {"title": _("UserStory"), "id": "userstory", "class": "active",
         "fields": ('code', 'title', 'description', 'acceptanceCriteria')},
        {"title": "Sprints", "id": "sprints", "inlines": ("userstory/sprint.html",)},
        {"title": _("Requeriments"), "id": "requeriments", "fields": ('requeriment',)},
    )
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
        {'link': '#', 'class': '', 'name': _('Add')},
    )

    def get_success_url(self):
        if 'sprint_id' in self.kwargs:
            return reverse_lazy('main:userstory', kwargs={'sprint_id':self.kwargs['sprint_id']})
        elif 'requeriment_id' in self.kwargs:
            return reverse_lazy('main:userstory', kwargs={'requeriment_id':self.kwargs['requeriment_id']})
        else:
            return reverse_lazy('main:userstory')

    def get_form(self, form=False):
        return self.form_class(request=self.request, **self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        sprint_userstory_form = SprintUserStoryInlineFormSet(self.request.POST, instance=self.object)
        if form.is_valid() and sprint_userstory_form.is_valid():
            return self.form_valid(form, sprint_userstory_form)
        else:
            return self.form_invalid(form, sprint_userstory_form)

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(UserStoryUpdateFormView, self).dispatch(request, *args, **kwargs)



    def form_valid(self, form, sprint_userstory_form):
        project = ProjectService.get_project(self.request.session.get('project_id'))
        form.instance.changed_by = self.request.user
        form.instance.project = project
        self.object = form.save()
        sprint_userstory_form.instance = self.object
        sprint_userstory_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(UserStoryUpdateFormView, self).get_context_data()
        sprint_userstory = UserStoryService.get_sprints_from_userstory(self.object)
        context['SprintUserStoryInline']=SprintUserStoryInlineFormSetFiltrado(project=self.request.session.get('project_id'), instance=self.object)
        context['breadcrumbs'] = userstories_breadcrumbs(
            self.request.session.get('project_id'),
            self.kwargs.get('requeriment_id'),
            self.kwargs.get('sprint_id'),
            self.kwargs.get('pk'),
            _('Add')
        )
        return context


class UserStoryDeleteView(SuccessMessageMixin, DeleteView):
    """
    #class:US007
    Delete US
    """
    model = UserStoryService.get_userstory_model()
    template_name = 'userstory/delete.html'
    list_display = ('code', 'title', 'description')

    def get_success_url(self):
        if 'sprint_id' in self.kwargs:
            return reverse_lazy('main:userstory', kwargs={'sprint_id': self.kwargs['sprint_id']})
        elif 'requeriment_id' in self.kwargs:
            return reverse_lazy('main:userstory', kwargs={'requeriment_id': self.kwargs['requeriment_id']})
        else:
            return reverse_lazy('main:userstory')

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(UserStoryDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserStoryDeleteView, self).get_context_data()
        #sprint_userstory = SprintUserStory.objects.filter(userstory=self.object)
        #context['SprintUserStoryInline']=SprintUserStoryInlineFormSet(instance=self.object)
        context['breadcrumbs'] = userstories_breadcrumbs(
            self.request.session.get('project_id'),
            self.kwargs.get('requeriment_id'),
            self.kwargs.get('sprint_id'),
            self.kwargs.get('pk'),
            _('Delete')
        )
        return context


class UserStoryGraphDetailView(TemplateViewProjectFilter):
    """
    #class:US014
    """
    template_name = 'userstory/graph_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserStoryGraphDetailView, self).get_context_data(**kwargs)
        userstory = UserStoryService.get_userstory(self.request.session.get('project_id', None), self.kwargs['pk'])
        context['breadcrumbs'] = userstories_breadcrumbs(
            self.request.session.get('project_id'),
            self.kwargs.get('requeriment_id'),
            self.kwargs.get('sprint_id'),
            self.kwargs.get('pk'),
            _('Delete')
        )
        context['userstory'] = userstory
        return context
