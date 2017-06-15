import os

from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.python import PythonLexer

from main.components.breadcrumbs import userstories_breadcrumbs, activity_sucess_url
from main.components.bugtracking.activityFinder import activityFinder
from main.components.bugtracking.factory import BugTrackingFactory
from main.components.formviews import AddFormView, UpdateFormView
from main.components.lists import TemplateViewProjectFilter
from main.components.repository.factory import RepositoryFactory
from main.components.repository.sourceFinder import SourceFinder
from main.decorators import require_project
from main.forms import ArtifactForm, ActivityUserStoryForm, ActivityRequerimentForm, ActivitySprintForm, \
    ActivityProjectForm
from main.models import  Artifact, ArtifactType, Project, Sprint, Requeriment, UserStory
from main.services.artifact import ArtifactService
from main.services.artifacttype import ArtifactTypeService
from main.services.project import ProjectService
from main.services.requeriment import RequerimentService
from main.services.sprint import SprintService
from main.services.userstory import UserStoryService
from tracepp import settings



class ArtifactView(TemplateViewProjectFilter):
    template_name = 'artifact/list.html'

    def get_context_data(self, **kwargs):
        context = super(ArtifactView, self).get_context_data(**kwargs)
        project = ProjectService.get_project(self.request.session['project_id'])
        context['project'] = project
        context['local_repository'] = settings.REPOSITORY_DIR
        if 'userstory' in self.kwargs:  # userstory
            userstory = UserStoryService.get_userstory(self.request.session['project_id'], self.kwargs['userstory'])
            context['artifacttype'] = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 3, 0)
            context['artifact'] = UserStoryService.get_artifacts(self.request.session['project_id'], userstory)
            context['page_title'] = _('UserStory Artifacts')
            context['breadcrumbs'] = userstories_breadcrumbs(
                self.request.session.get('project_id'),
                self.kwargs.get('requeriment_id'),
                self.kwargs.get('sprint_id'),
                self.kwargs.get('userstory'),
                'Artifacts'
            )
        elif 'sprint_id' in self.kwargs:
            sprint = SprintService.get_sprint(self.request.session['project_id'], self.kwargs['sprint_id'])
            context['artifacttype'] = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 2, 0)
            context['artifact'] = SprintService.get_artifacts(self.request.session['project_id'], sprint)
            context['page_title'] = _('Sprint Artifacts')
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': sprint.id}), 'class': '',
                 'name': sprint},
                {'link': '#', 'class': '', 'name': _('Artifacts')},
            )
        elif 'requeriment_id' in self.kwargs:
            requeriment = RequerimentService.get_requeriment(self.request.session['project_id'],
                                                             self.kwargs['requeriment_id'])
            context['artifacttype'] = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 1, 0)
            context['artifact'] = RequerimentService.get_artifacts(self.request.session['project_id'], requeriment)
            context['page_title'] = _('Requeriment Artifacts')
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
                {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment.id}), 'class': '',
                 'name': requeriment.code},
                {'link': '#', 'class': '', 'name': _('Artifacts')},
            )
        else:
            context['artifact'] = ProjectService.get_artifacts(self.request.session['project_id'])
            context['artifacttype'] = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 0, 0)
            context['page_title'] = _('Project Artifacts')
        return context


class ArtifactDocumentForm(SuccessMessageMixin, CreateView):
    """
    #class:US009
    """
    template_name = 'artifact/add-document.html'
    model = Artifact
    form_class = ArtifactForm

    def get_success_url(self):
        return reverse('main:artifact')

    def get_context_data(self, **kwargs):
        context = super(ArtifactDocumentForm, self).get_context_data(**kwargs)
        project = ProjectService.get_project(self.request.session['project_id'])
        context['project']=project
        context['local_repository']=settings.REPOSITORY_DIR
        if self.request.is_secure():
            url = 'https://'+get_current_site(self.request).domain
        else:
            url = 'http://'+get_current_site(self.request).domain

        if 'userstory' in self.kwargs: #userstory
            userstory = UserStoryService.get_userstory(self.request.session['project_id'], self.kwargs['userstory'])
            context['artifacttype'] = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 3, 0)
            context['artifact'] = UserStoryService.get_artifacts(self.request.session['project_id'], userstory)
            context['page_title'] = _('UserStory Artifacts')
            context['url'] = url+'/userstory/'+str(userstory.id)+'/detail/artifact/'
            context['breadcrumbs'] = userstories_breadcrumbs(
                self.request.session.get('project_id'),
                self.kwargs.get('requeriment_id'),
                self.kwargs.get('sprint_id'),
                self.kwargs.get('userstory'),
                'Artifacts'
            )
        elif 'sprint_id' in self.kwargs:
            sprint = SprintService.get_sprint(self.request.session['project_id'], self.kwargs['sprint_id'])
            context['artifacttype'] = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 2, 0)
            context['artifact'] = SprintService.get_artifacts(self.request.session['project_id'], sprint)
            context['page_title'] = _('Sprint Artifacts')
            context['breadcrumbs'] = (
               {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
               {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
               {'link': reverse_lazy('main:sprint-details',kwargs={'sprint_id':sprint.id}), 'class': '', 'name': sprint},
               {'link': '#', 'class': '', 'name': _('Artifacts')},
            )
        elif 'requeriment_id' in self.kwargs:
            requeriment = RequerimentService.get_requeriment(self.request.session['project_id'], self.kwargs['requeriment_id'])
            context['artifacttype'] = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 1, 0)
            context['artifact'] = RequerimentService.get_artifacts(self.request.session['project_id'], requeriment)
            context['page_title'] = _('Requeriment Artifacts')
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
                {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment.id}), 'class': '',
                 'name': requeriment.code},
                {'link': '#', 'class': '', 'name': _('Artifacts')},
            )
        else:
            context['artifact'] = ProjectService.get_artifacts(self.request.session['project_id'])
            context['artifacttype'] = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 0, 0)
            context['page_title'] = _('Project Artifacts')
        return context

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ArtifactDocumentForm, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        project = ProjectService.get_project(self.request.session['project_id'])
        form.instance.project = project
        if 'userstory' in self.kwargs:
            userstory = UserStoryService.get_userstory(self.request.session['project_id'], self.kwargs['userstory'])
            form.instance.userstory = userstory
        elif 'sprint_id' in self.kwargs:
            sprint = SprintService.get_sprint(self.request.session['project_id'], self.kwargs['sprint_id'])
            form.instance.sprint = sprint
        elif 'requeriment_id' in self.kwargs:
            requeriment = RequerimentService.get_requeriment(self.request.session['project_id'], self.kwargs['requeriment_id'])
            form.instance.requeriment = requeriment
        return super(ArtifactDocumentForm, self).form_valid(form)

class ActivityAddFormView(AddFormView):
    page_title = _('Activity')
    model = ArtifactService.get_model()
    success_message = _('Activity was created successfully')
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
        {'link': '#', 'class': '', 'name': _('Add')},
    )
    form_class = None
    tabs = None

    def get_form_class(self):
        if 'userstory' in self.kwargs:
            self.tabs = (
                {"title": _("Activity"), "id": "activity", "class": "active",
                 "fields": ('user', 'title', 'description', 'type', 'userstory',)},
                {"title": _("Time"), "id": "time",
                 "fields": ('create_date', 'estimated_time', 'closed_date', 'spent_time')},
                {"title": _("Points"), "id": "points",
                 "fields": ('estimated_storypoints', 'realized_storypoints')},
                {"title": "BV", "id": "bv",
                 "fields": ('estimated_businnesvalue', 'realized_businnesvalue')},
            )
            form = ActivityUserStoryForm
        elif 'sprint_id' in self.kwargs and 'requeriment_id' not in self.kwargs:
            self.tabs = (
                {"title": _("Activity"), "id": "activity", "class": "active",
                 "fields": ('user', 'title', 'description', 'type', 'sprint',)},
                {"title": _("Time"), "id": "time",
                 "fields": ('create_date', 'estimated_time', 'closed_date', 'spent_time')},
                {"title": _("Points"), "id": "points",
                 "fields": ('estimated_storypoints', 'realized_storypoints')},
                {"title": "BV", "id": "bv",
                 "fields": ('estimated_businnesvalue', 'realized_businnesvalue')},
            )
            form =  ActivitySprintForm
        elif 'requeriment_id' in self.kwargs:
            self.tabs = (
                {"title": _("Activity"), "id": "activity", "class": "active",
                 "fields": ('user', 'title', 'description', 'type', 'requeriment',)},
                {"title": _("Time"), "id": "time",
                 "fields": ('create_date', 'estimated_time', 'closed_date', 'spent_time')},
                {"title": _("Points"), "id": "points",
                 "fields": ('estimated_storypoints', 'realized_storypoints')},
                {"title": "BV", "id": "bv",
                 "fields": ('estimated_businnesvalue', 'realized_businnesvalue')},
            )
            form = ActivityRequerimentForm
        else:
            self.tabs = (
                {"title": _("Activity"), "id": "activity", "class": "active",
                 "fields": ('user', 'title', 'description', 'type', )},
                {"title": _("Time"), "id": "time",
                 "fields": ('create_date', 'estimated_time', 'closed_date', 'spent_time')},
                {"title": _("Points"), "id": "points",
                 "fields": ('estimated_storypoints', 'realized_storypoints')},
                {"title": "BV", "id": "bv",
                 "fields": ('estimated_businnesvalue', 'realized_businnesvalue')},
            )
            form = ActivityProjectForm
        return form

    def get_form(self, *args, **kwargs):
        form = super(ActivityAddFormView, self).get_form(*args, **kwargs)

        if 'userstory' in self.kwargs:
            form.fields['type'].queryset = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 3,2)
        elif 'sprint_id' in self.kwargs and 'requeriment_id' not in self.kwargs:
            form.fields['type'].queryset = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 2,2)
        elif 'requeriment_id' in self.kwargs:
            form.fields['type'].queryset = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 1,2)
        else:
            form.fields['type'].queryset = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 0,2)

        if self.request.user.is_superuser:
            form.fields['user'].queryset = ProjectService.get_users_from_project(self.request.session['project_id'])
        else:
            form.fields['user'].queryset = User.objects.filter(pk=self.request.user.id)
        return form

    def get_initial(self):
        initial = super(ActivityAddFormView, self).get_initial()
        if 'userstory' in self.kwargs:
            initial['userstory'] = UserStoryService.get_userstory(self.request.session['project_id'],self.kwargs['userstory'])
        initial['user'] = self.request.user
        return initial

    def get_success_url(self):
        requeriment_id = False
        sprint_id = False
        userstory_id = False
        if 'requeriment_id' in self.kwargs:
            requeriment_id = self.kwargs['requeriment_id']
        if 'sprint_id' in self.kwargs:
            sprint_id = self.kwargs['sprint_id']
        if 'userstory' in self.kwargs:
            userstory_id = self.kwargs['userstory']
        return activity_sucess_url(requeriment_id, sprint_id, userstory_id)

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ActivityAddFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = ProjectService.get_project(self.request.session['project_id'])
        #form.instance.changed_by = self.request.user
        form.instance.project = project
        return super(ActivityAddFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ActivityAddFormView, self).get_context_data(**kwargs)
        userstory_id = False
        sprint_id = False
        requeriment_id = False
        if 'userstory' in self.kwargs: #userstory
            userstory_id = self.kwargs['userstory']
        if 'sprint_id' in self.kwargs:
            sprint_id =  self.kwargs['sprint_id']
        if 'requeriment_id' in self.kwargs:
            requeriment_id = self.kwargs['requeriment_id']
        context['breadcrumbs'] = userstories_breadcrumbs(self.request.session['project_id'], requeriment_id, sprint_id, userstory_id, _('Add Activity'))
        return context

class ActivityUpdateFormView(UpdateFormView):
    page_title = _('Activity')
    model = ArtifactService.get_model()
    success_message = _('Activity was updated successfully')
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
        {'link': '#', 'class': '', 'name': _('Add')},
    )
    form_class = None
    tabs = None

    def get_form_class(self):
        if 'userstory' in self.kwargs:
            self.tabs = (
                {"title": _("Activity"), "id": "activity", "class": "active",
                 "fields": ('user', 'title', 'description', 'type', 'userstory',)},
                {"title": _("Time"), "id": "time",
                 "fields": ('create_date', 'estimated_time', 'closed_date', 'spent_time')},
                {"title": _("Points"), "id": "points",
                 "fields": ('estimated_storypoints', 'realized_storypoints')},
                {"title": "BV", "id": "bv",
                 "fields": ('estimated_businnesvalue', 'realized_businnesvalue')},
            )
            form = ActivityUserStoryForm
        elif 'sprint_id' in self.kwargs and 'requeriment_id' not in self.kwargs:
            self.tabs = (
                {"title": _("Activity"), "id": "activity", "class": "active",
                 "fields": ('user', 'title', 'description', 'type', 'sprint',)},
                {"title": _("Time"), "id": "time",
                 "fields": ('create_date', 'estimated_time', 'closed_date', 'spent_time')},
                {"title": _("Points"), "id": "points",
                 "fields": ('estimated_storypoints', 'realized_storypoints')},
                {"title": "BV", "id": "bv",
                 "fields": ('estimated_businnesvalue', 'realized_businnesvalue')},
            )
            form =  ActivitySprintForm
        elif 'requeriment_id' in self.kwargs:
            self.tabs = (
                {"title": _("Activity"), "id": "activity", "class": "active",
                 "fields": ('user', 'title', 'description', 'type', 'requeriment',)},
                {"title": _("Time"), "id": "time",
                 "fields": ('create_date', 'estimated_time', 'closed_date', 'spent_time')},
                {"title": _("Points"), "id": "points",
                 "fields": ('estimated_storypoints', 'realized_storypoints')},
                {"title": "BV", "id": "bv",
                 "fields": ('estimated_businnesvalue', 'realized_businnesvalue')},
            )
            form = ActivityRequerimentForm
        else:
            self.tabs = (
                {"title": _("Activity"), "id": "activity", "class": "active",
                 "fields": ('user', 'title', 'description', 'type', )},
                {"title": _("Time"), "id": "time",
                 "fields": ('create_date', 'estimated_time', 'closed_date', 'spent_time')},
                {"title": _("Points"), "id": "points",
                 "fields": ('estimated_storypoints', 'realized_storypoints')},
                {"title": "BV", "id": "bv",
                 "fields": ('estimated_businnesvalue', 'realized_businnesvalue')},
            )
            form = ActivityProjectForm
        return form

    def get_form(self, *args, **kwargs):
        form = super(ActivityUpdateFormView, self).get_form(*args, **kwargs)
        if 'userstory' in self.kwargs:
            form.fields['type'].queryset = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 3,
                                                                                 2)
        elif 'sprint_id' in self.kwargs and 'requeriment_id' not in self.kwargs:
            form.fields['type'].queryset = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 2,
                                                                                 2)
        elif 'requeriment_id' in self.kwargs:
            form.fields['type'].queryset = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 1,
                                                                                 2)
        else:
            form.fields['type'].queryset = ArtifactTypeService.get_artifactstype(self.request.session['project_id'], 0,
                                                                                 2)
        if self.request.user.is_superuser:
            form.fields['user'].queryset = ProjectService.get_users_from_project(self.request.session['project_id'])
        return form

    def get_success_url(self):
        if 'back' in self.kwargs:
            return reverse_lazy('main:artifact-list-activity')
        requeriment_id = False
        sprint_id = False
        userstory_id = False
        if 'requeriment_id' in self.kwargs:
            requeriment_id = self.kwargs['requeriment_id']
        if 'sprint_id' in self.kwargs:
            sprint_id = self.kwargs['sprint_id']
        if 'userstory' in self.kwargs:
            userstory_id = self.kwargs['userstory']
        return activity_sucess_url(requeriment_id, sprint_id, userstory_id)

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ActivityUpdateFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = ProjectService.get_project(self.request.session['project_id'])
        #form.instance.changed_by = self.request.user
        form.instance.project = project
        return super(ActivityUpdateFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ActivityUpdateFormView, self).get_context_data(**kwargs)
        userstory_id = False
        sprint_id = False
        requeriment_id = False
        if 'userstory' in self.kwargs: #userstory
            userstory_id = self.kwargs['userstory']
        if 'sprint_id' in self.kwargs:
            sprint_id =  self.kwargs['sprint_id']
        if 'requeriment_id' in self.kwargs:
            requeriment_id = self.kwargs['requeriment_id']
        context['breadcrumbs'] = userstories_breadcrumbs(self.request.session['project_id'], requeriment_id, sprint_id, userstory_id, _('Update Activity'))
        return context


class ActivityListView(TemplateViewProjectFilter):
    template_name = 'artifact/activity-list.html'

    def get_context_data(self, **kwargs):
        context = super(ActivityListView, self).get_context_data(**kwargs)
        project = ProjectService.get_project(self.request.session['project_id'])
        context['project'] = project
        context['open_myactivities'] = ArtifactService.get_activities(self.request.session['project_id'], True, self.request.user.id, True)
        context['open_otheractivities'] = ArtifactService.get_activities(self.request.session['project_id'], True, self.request.user.id, False)
        return context

def ArtifactDownloadView(request, pk):
    """
    #class:US009
    Download
    """
    artifact = ArtifactService.get_artifact(request.session.get('project_id', None), pk)
    filename = artifact.file.name.split('/')[-1]
    response = HttpResponse(artifact.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


class ArtifactDeleteView(SuccessMessageMixin, DeleteView):
    """
    #class:US009
    """
    model = ArtifactService.get_model()
    template_name = 'artifact/delete.html'
    fields = ('name', 'type', 'title', 'description', 'reference', 'requeriment','sprint','userstory','file')

    def get_success_url(self):
        requeriment_id = False
        sprint_id = False
        userstory_id = False
        if 'requeriment_id' in self.kwargs:
            requeriment_id = self.kwargs['requeriment_id']
        if 'sprint_id' in self.kwargs:
            sprint_id = self.kwargs['sprint_id']
        if 'userstory' in self.kwargs:
            userstory_id = self.kwargs['userstory']
        return activity_sucess_url(requeriment_id, sprint_id, userstory_id)

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ArtifactDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArtifactDeleteView, self).get_context_data()
        return context


class ArtifactTraceBugTrackingConfirm(TemplateViewProjectFilter):
    """
    #class:US012
    """
    template_name = 'artifact/tracebugtracking-confirm.html'

    def get_context_data(self, **kwargs):
        context = super(ArtifactTraceBugTrackingConfirm, self).get_context_data(**kwargs)
        project = ProjectService.get_project(self.request.session.get('project_id', None))
        if self.request.is_secure():
            context['url']='https://'+get_current_site(self.request).domain+'/'+'artifact/'+str(project.id)+'/tracebugtracking/'
        else:
            context['url'] = 'http://' + get_current_site(
                self.request).domain + '/' + 'artifact/' + str(project.id) + '/tracebugtracking/'

        context['project'] = project
        return context

class ArtifactCodeConfirm(TemplateViewProjectFilter):
    """
    #class:US012
    """
    template_name = 'artifact/tracecode-confirm.html'

    def get_context_data(self, **kwargs):
        context = super(ArtifactCodeConfirm, self).get_context_data(**kwargs)
        project = ProjectService.get_project(self.request.session.get('project_id', None))
        context['local_repository'] = settings.REPOSITORY_DIR
        if self.request.is_secure():
            context['url']='https://'+get_current_site(self.request).domain+'/'+'artifact/'+str(project.id)+'/tracecode/'
        else:
            context['url'] = 'http://' + get_current_site(
                self.request).domain + '/' + 'artifact/' + str(project.id) + '/tracecode/'

        context['project'] = project
        return context



class ArtifactTraceBugTrackingView(TemplateViewProjectFilter):
    """
    #class:US012
    """
    template_name = 'artifact/tracebugtracking.html'

    def dispatch(self, request, *args, **kwargs):
        if 'projeto' in self.kwargs:
            self.request.session['project_id'] = self.kwargs['projeto']
        return super(TemplateViewProjectFilter, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArtifactTraceBugTrackingView, self).get_context_data(**kwargs)

        project = ProjectService.get_project(self.request.session.get('project_id', None))


        if project.versionAsSprint:
            context['sprintImportLogs'] = ArtifactService.get_sprints_from_bugtracking(project)
            context['artifactImportLogs'] = ArtifactService.get_bugtrack_activities(project, True)
        else:
            context['artifactImportLogs'] = ArtifactService.get_bugtrack_activities(project)

        if project.issueTypesAsUserStory:
            context['userStoryImportLogs'] = ArtifactService.get_userstories_from_bugtracking(project)
            context['sprintUsertory'] = ArtifactService.sprint_to_userstory(project)

        context['project'] = project
        return context


class ArtifactTraceCodeView(TemplateViewProjectFilter):
    """
    #class:US010
    """
    template_name = 'artifact/tracecode.html'

    def dispatch(self, request, *args, **kwargs):
        if 'projeto' in self.kwargs:
            self.request.session['project_id'] = self.kwargs['projeto']
        return super(TemplateViewProjectFilter, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArtifactTraceCodeView, self).get_context_data(**kwargs)
        project = ProjectService.get_project(self.request.session.get('project_id', None))
        Artifact.objects.filter(project=project,type__type=1).delete()
        sid = transaction.savepoint()

        artifactsTypes = ArtifactType.objects.filter(project=project, type=1,)
        repo = RepositoryFactory(project)
        repo.repository.pull()
        sf = SourceFinder(project, artifactsTypes)
        for artifact in sf.artifactList:
            try:
                if artifact['artifactType'].level == 0:
                    Artifact.objects.create(project=project, source=artifact['source'], line=artifact['line'], type=artifact['artifactType'])
                elif artifact['artifactType'].level == 1:
                    requeriment = Requeriment.objects.filter(project=project, code=artifact['code']).get()
                    Artifact.objects.create(project=project, source=artifact['source'], line=artifact['line'],
                                            type=artifact['artifactType'], requeriment=requeriment)
                elif artifact['artifactType'].level == 2:
                    sprint = Sprint.objects.filter(project=project, code=artifact['code']).get()
                    Artifact.objects.create(project=project, source=artifact['source'], line=artifact['line'],
                                            type=artifact['artifactType'], sprint=sprint)
                elif artifact['artifactType'].level == 3:
                    userstory = UserStory.objects.filter(project=project, code=artifact['code']).get()
                    Artifact.objects.create(project=project, source=artifact['source'], line=artifact['line'],
                                            type=artifact['artifactType'], userstory=userstory)
            except:
                context['erros']="erros: {} {}", artifact['source'], artifact['line']
        context['project'] = project
        return context


class ArtifactCodeView(TemplateViewProjectFilter):
    """
    #class:US011
    """
    template_name = 'artifact/code.html'

    def get_context_data(self, **kwargs):
        context = super(ArtifactCodeView, self).get_context_data(**kwargs)
        artifact = get_object_or_404(
            Artifact,
            project=self.request.session.get('project_id', None),
            id=self.kwargs['artifact']
        )
        sourcecode = ''
        file = settings.REPOSITORY_DIR+artifact.source
        with open(str(file), 'rb') as f:  # open in binary mode
            linecount = 0
            hl_line = 1
            for line in f:
                linecount += 1
                for cp in ('cp1252', 'cp850'):
                    try:
                        if str(linecount) == artifact.line:
                            sourcecode += line.decode(cp)
                            hl_line = linecount
                        else:
                            sourcecode += line.decode(cp)
                    except UnicodeDecodeError:
                        pass
                    else:
                        break
        context['sourcecode'] = highlight(sourcecode, PythonLexer(), HtmlFormatter(linenos='table', hl_lines=[hl_line]))
        context['source_css'] = HtmlFormatter().get_style_defs('.highlight')

        if 'pk' in self.kwargs:  # userstory
            userstory = get_object_or_404(UserStory, pk=self.kwargs['pk'])
            context['page_title'] = _('Userstory Artifact')
            if 'sprint_id' in self.kwargs:
                sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'])
                context['breadcrumbs'] = (
                    {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                    {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                    {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': self.kwargs['sprint_id']}),
                     'class': '', 'name': sprint},
                    {'link': reverse_lazy('main:sprint-userstory', kwargs={'sprint_id': self.kwargs['sprint_id']}),
                     'class': '',
                     'name': _('User Stories')},
                    {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
                     'name': userstory.code},
                    {'link': reverse_lazy('main:artifact', kwargs={'pk': userstory.pk, 'sprint_id': self.kwargs['sprint_id']}),
                        'class': '', 'name': _('Artifacts')},
                    {'link': '#','class': '', 'name': _('Artifact')},
                )
            elif 'requeriment_id' in self.kwargs:
                requeriment = get_object_or_404(Requeriment, pk=self.kwargs['requeriment_id'])
                context['breadcrumbs'] = (
                    {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                    {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriments')},
                    {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': self.kwargs['requeriment_id']}),
                     'class': '', 'name': requeriment},
                    {'link': reverse_lazy('main:requeriment-userstory',
                                          kwargs={'requeriment_id': self.kwargs['requeriment_id']}), 'class': '',
                     'name': _('User Stories')},
                    {'link': reverse_lazy('main:requeriment-userstory-detail',
                                          kwargs={'requeriment_id': self.kwargs['requeriment_id'], 'pk': userstory.pk}),
                     'class': '',
                     'name': userstory.code},
                    {'link': reverse_lazy('main:artifact',
                                          kwargs={'pk': userstory.pk, 'requeriment_id': self.kwargs['requeriment_id']}),
                     'class': '', 'name': _('Artifacts')},
                    {'link': '#', 'class': '', 'name': _('Artifact')},
                )
            else:
                context['breadcrumbs'] = (
                    {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                    {'link': reverse_lazy('main:userstory'), 'class': '',
                     'name': _('User Stories')},
                    {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
                     'name': userstory.code},
                    {'link': reverse_lazy('main:artifact',
                                          kwargs={'pk': userstory.pk}),
                     'class': '', 'name': _('Artifacts')},
                    {'link': '#', 'class': '', 'name': _('Artifact')},
                )
        elif 'sprint_id' in self.kwargs:
            sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'])
            context['page_title'] = _('Sprint Artifacts')
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': sprint.id}), 'class': '',
                 'name': sprint},
                {'link': '#', 'class': '', 'name': _('Artifact')},
            )
        elif 'requeriment_id' in self.kwargs:
            requeriment = get_object_or_404(Requeriment, pk=self.kwargs['requeriment_id'])
            context['page_title'] = _('Requeriment Artifacts')
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
                {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment.id}), 'class': '',
                 'name': requeriment.code},
                {'link': '#', 'class': '', 'name': _('Artifacts')},
            )
        else:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:artifact'), 'class': '', 'name': _('Project Artifacts')},
                {'link': '#', 'class': '', 'name': _('Artifact')},
            )
            context['page_title'] = _('Project Artifact')

        return context


class ArtifactActivityView(TemplateViewProjectFilter):
    """
    #class:US013
    """
    template_name = 'artifact/activity.html'

    def get_context_data(self, **kwargs):
        context = super(ArtifactActivityView, self).get_context_data(**kwargs)
        artifact = get_object_or_404(
            Artifact,
            project=self.request.session.get('project_id', None),
            id=self.kwargs['artifact']
        )

        project = get_object_or_404(
            Project.objects.all(),
            id=self.request.session.get('project_id', None),
        )
        bugtracking = BugTrackingFactory.getConnection(project=project)
        issue = bugtracking.getIssue(artifact.reference)
        context['artifact']=artifact
        context['issue']=issue
        context['project']=project

        if 'pk' in self.kwargs:  # userstory
            userstory = get_object_or_404(UserStory, pk=self.kwargs['pk'])
            context['page_title'] = _('Userstory Artifact')
            if 'sprint_id' in self.kwargs:
                sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'])
                context['breadcrumbs'] = (
                    {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                    {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                    {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': self.kwargs['sprint_id']}),
                     'class': '', 'name': sprint},
                    {'link': reverse_lazy('main:sprint-userstory', kwargs={'sprint_id': self.kwargs['sprint_id']}),
                     'class': '',
                     'name': _('User Stories')},
                    {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
                     'name': userstory.code},
                    {'link': reverse_lazy('main:artifact', kwargs={'pk': userstory.pk, 'sprint_id': self.kwargs['sprint_id']}),
                        'class': '', 'name': _('Artifacts')},
                    {'link': '#','class': '', 'name': _('Artifact')},
                )
            elif 'requeriment_id' in self.kwargs:
                requeriment = get_object_or_404(Requeriment, pk=self.kwargs['requeriment_id'])
                context['breadcrumbs'] = (
                    {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                    {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriments')},
                    {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': self.kwargs['requeriment_id']}),
                     'class': '', 'name': requeriment},
                    {'link': reverse_lazy('main:requeriment-userstory',
                                          kwargs={'requeriment_id': self.kwargs['requeriment_id']}), 'class': '',
                     'name': _('User Stories')},
                    {'link': reverse_lazy('main:requeriment-userstory-detail',
                                          kwargs={'requeriment_id': self.kwargs['requeriment_id'], 'pk': userstory.pk}),
                     'class': '',
                     'name': userstory.code},
                    {'link': reverse_lazy('main:artifact',
                                          kwargs={'pk': userstory.pk, 'requeriment_id': self.kwargs['requeriment_id']}),
                     'class': '', 'name': _('Artifacts')},
                    {'link': '#', 'class': '', 'name': _('Artifact')},
                )
            else:
                context['breadcrumbs'] = (
                    {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                    {'link': reverse_lazy('main:userstory'), 'class': '',
                     'name': _('User Stories')},
                    {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
                     'name': userstory.code},
                    {'link': reverse_lazy('main:artifact',
                                          kwargs={'pk': userstory.pk}),
                     'class': '', 'name': _('Artifacts')},
                    {'link': '#', 'class': '', 'name': _('Artifact')},
                )
        elif 'sprint_id' in self.kwargs:
            sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'])
            context['page_title'] = _('Sprint Artifacts')
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': sprint.id}), 'class': '',
                 'name': sprint},
                {'link': '#', 'class': '', 'name': _('Artifact')},
            )
        elif 'requeriment_id' in self.kwargs:
            requeriment = get_object_or_404(Requeriment, pk=self.kwargs['requeriment_id'])
            context['page_title'] = _('Requeriment Artifacts')
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
                {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment.id}), 'class': '',
                 'name': requeriment.code},
                {'link': '#', 'class': '', 'name': _('Artifacts')},
            )
        else:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:artifact'), 'class': '', 'name': _('Project Artifacts')},
                {'link': '#', 'class': '', 'name': _('Artifact')},
            )
            context['page_title'] = _('Project Artifact')

        return context

