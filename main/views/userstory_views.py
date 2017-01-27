from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.views.generic import DeleteView
from django.views.generic import ListView

from main.components.lists import ModelListProjectFilter, TemplateViewProjectFilter
from main.decorators import require_project
from main.forms import UserStoryForm, SprintUserStoryInlineFormSet
from main.models import Sprint, Project, Requeriment, SprintUserStory, UserStory, Artifact
from main.components.formviews import AddFormView, UpdateFormView


class UserStoryListView(ModelListProjectFilter):
    """
    #class:US007
    List of US
    """
    model = UserStory
    paginate_by = 30
    page_title = _('User Story')
    list_display = ('code', 'title','description','storypoints_planned','bussinessvalue_planned','storypoints_realized','bussinessvalue_realized')
    action_template = 'userstory/action.html'
    top_bar = 'userstory/top_bar.html'

    def get_queryset(self):
        if 'sprint_id' in self.kwargs:
            return UserStory.objects.filter(project=self.request.session.get('project_id', None),
                                            sprintuserstory__sprint =self.kwargs['sprint_id'])
        elif 'requeriment_id' in self.kwargs:
            return UserStory.objects.filter(project=self.request.session.get('project_id', None), requeriment=self.kwargs['requeriment_id'])
        else:
            return UserStory.objects.filter(project=self.request.session.get('project_id', None))

    def get_context_data(self, **kwargs):
        context = super(UserStoryListView, self).get_context_data()

        if 'sprint_id' in self.kwargs:
            sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'])
            context['page_title']= '%s - User Stories' % str(sprint)
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': self.kwargs['sprint_id']}),
                 'class': '', 'name': sprint},
                {'link': '#', 'class': '', 'name': _('User Stories')},
            )
        elif 'requeriment_id' in self.kwargs:
            requeriment = get_object_or_404(Requeriment, pk=self.kwargs['requeriment_id'])
            context['page_title'] = '%s - User Stories' % str(requeriment)
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriments')},
                {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': self.kwargs['requeriment_id']}),
                 'class': '', 'name': requeriment},
                {'link': '#', 'class': '', 'name': _('User Stories')},
            )
        else:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': '#', 'class': '', 'name': _('User Stories')},
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
        userstory = get_object_or_404(UserStory, pk=self.kwargs['pk'])
        context['userstory'] = userstory
        context['total_artifacts'] = Artifact.objects.filter(
            project=self.request.session.get('project_id', None), userstory=userstory).count()
        context['total_file_artifacts'] = Artifact.file_objects.filter(
            project=self.request.session.get('project_id', None), userstory=userstory).count()
        context['total_source_artifacts'] = Artifact.source_objects.filter(
            project=self.request.session.get('project_id', None), userstory=userstory).count()
        context['total_activities']=Artifact.activity_objects.filter(
            project=self.request.session.get('project_id', None), userstory=userstory).count()
        context['total_estimated_time']=Artifact.activity_objects.filter(
            project=self.request.session.get('project_id', None), userstory=userstory).aggregate(time = Sum('estimated_time'))
        context['total_spent_time'] = Artifact.activity_objects.filter(
            project=self.request.session.get('project_id', None), userstory=userstory).aggregate(time = Sum('spent_time'))
        if 'sprint_id' in self.kwargs:
            sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'])
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': self.kwargs['sprint_id']}),
                 'class': '', 'name': sprint},
                {'link': reverse_lazy('main:sprint-userstory',kwargs={'sprint_id': self.kwargs['sprint_id']}), 'class': '',
                 'name': _('User Stories')},
                {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
                 'name': userstory.code},
            )
        elif 'requeriment_id' in self.kwargs:
            requeriment = get_object_or_404(Requeriment, pk=self.kwargs['requeriment_id'])
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriments')},
                {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': self.kwargs['requeriment_id']}),
                 'class': '', 'name': requeriment},
                {'link': reverse_lazy('main:requeriment-userstory', kwargs={'requeriment_id': self.kwargs['requeriment_id']}), 'class': '', 'name': _('User Stories')},
                {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
                 'name': userstory.code},
            )
        else:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:userstory'), 'class': '',
                 'name': _('User Stories')},
                {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
                 'name':userstory.code},
            )
        return context


class UserStoryAddFormView(AddFormView):
    """
    #class:US007
    Add US
    """
    page_title = 'UserStory'
    model = UserStory
    form_class = UserStoryForm
    success_message = _('UserStory was created successfully')
    tabs = (
        {"title": "UserStory", "id": "userstory", "class": "active",
         "fields": ('code', 'title', 'description', 'acceptanceCriteria', 'storypoints_planned', 'storypoints_realized', 'bussinessvalue_planned', 'bussinessvalue_realized')},
        {"title": "Sprints", "id": "sprints", "inlines": ("userstory/sprint.html",)},
        {"title": "Requeriments", "id": "requeriments", "fields": ('requeriment',)},
    )

    def get_success_url(self):
        if 'sprint_id' in self.kwargs:
            return reverse_lazy('main:sprint-userstory', kwargs={'sprint_id':self.kwargs['sprint_id']})
        elif 'requeriment_id' in self.kwargs:
            return reverse_lazy('main:requeriment-userstory', kwargs={'requeriment_id':self.kwargs['requeriment_id']})
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
        project = get_object_or_404(Project, pk=self.request.session['project_id'])
        form.instance.changed_by = self.request.user
        form.instance.project = project
        self.object = form.save()
        sprint_userstory_form.instance = self.object
        sprint_userstory_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(UserStoryAddFormView, self).get_context_data()
        context['SprintUserStoryInline']=SprintUserStoryInlineFormSet()
        if 'sprint_id' in self.kwargs:
            sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'])
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': self.kwargs['sprint_id']}),'class': '', 'name':sprint},
                {'link': '#', 'class': '', 'name': _('User Stories')},
            )
        elif 'requeriment_id' in self.kwargs:
            requeriment = get_object_or_404(Requeriment, pk=self.kwargs['requeriment_id'])
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriments')},
                {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment.id}), 'class': '', 'name': requeriment},
                {'link': '#', 'class': '', 'name': _('User Stories')},
            )
        else:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:userstory'), 'class': '', 'name': _('User Stories')},
            )
        return context


class UserStoryUpdateFormView(UpdateFormView):
    """
    #class:US007
    Update US
    """
    page_title = 'UserStory'
    model = UserStory
    form_class = UserStoryForm
    success_message = _('UserStory was created successfully')
    tabs = (
        {"title": "UserStory", "id": "userstory", "class": "active",
         "fields": ('code', 'title', 'description', 'acceptanceCriteria', 'storypoints_planned', 'storypoints_realized', 'bussinessvalue_planned', 'bussinessvalue_realized')},
        {"title": "Sprints", "id": "sprints", "inlines": ("userstory/sprint.html",)},
        {"title": "Requeriments", "id": "requeriments", "fields": ('requeriment',)},
    )
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
        {'link': '#', 'class': '', 'name': _('Add')},
    )

    def get_success_url(self):
        if 'sprint_id' in self.kwargs:
            return reverse_lazy('main:sprint-userstory', kwargs={'sprint_id':self.kwargs['sprint_id']})
        elif 'requeriment_id' in self.kwargs:
            return reverse_lazy('main:requeriment-userstory', kwargs={'requeriment_id':self.kwargs['requeriment_id']})
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
        project = get_object_or_404(Project, pk=self.request.session['project_id'])
        form.instance.changed_by = self.request.user
        form.instance.project = project
        self.object = form.save()
        sprint_userstory_form.instance = self.object
        sprint_userstory_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(UserStoryUpdateFormView, self).get_context_data()
        sprint_userstory = SprintUserStory.objects.filter(userstory=self.object)
        context['SprintUserStoryInline']=SprintUserStoryInlineFormSet(instance=self.object)
        if 'sprint_id' in self.kwargs:
            sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'])
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': self.kwargs['sprint_id']}),'class': '', 'name': sprint.name},
                {'link': '#', 'class': '', 'name': _('User Stories')},
            )
        elif 'requeriment_id' in self.kwargs:
            requeriment = get_object_or_404(Requeriment, pk=self.kwargs['requeriment_id'])
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriments')},
                {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment.id}), 'class': '',
                 'name': requeriment},
                {'link': '#', 'class': '', 'name': _('User Stories')},
            )
        else:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:userstory'), 'class': '', 'name': _('User Stories')},
            )
        return context


class UserStoryDeleteView(SuccessMessageMixin, DeleteView):
    """
    #class:US007
    Delete US
    """
    model = UserStory
    template_name = 'userstory/delete.html'
    list_display = ('code', 'title', 'description')
    success_url = '/userstory/'

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(UserStoryDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserStoryDeleteView, self).get_context_data()
        sprint_userstory = SprintUserStory.objects.filter(userstory=self.object)
        context['SprintUserStoryInline']=SprintUserStoryInlineFormSet(instance=self.object)
        if 'sprint_id' in self.kwargs:
            sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'])
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': self.kwargs['sprint_id']}),'class': '', 'name': sprint},
                {'link': '#', 'class': '', 'name': _('User Stories')},
            )
        elif 'requeriment_id' in self.kwargs:
            requeriment = get_object_or_404(Requeriment, pk=self.kwargs['requeriment_id'])
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriments')},
                {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment.id}), 'class': '',
                 'name': requeriment},
                {'link': '#', 'class': '', 'name': _('User Stories')},
            )
        else:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:userstory'), 'class': '', 'name': _('User Stories')},
            )
        return context


class UserStoryGraphDetailView(TemplateViewProjectFilter):
    """
    #class:US014
    """
    template_name = 'userstory/graph_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserStoryGraphDetailView, self).get_context_data(**kwargs)
        userstory = get_object_or_404(UserStory,  project=self.request.session.get('project_id', None), pk=self.kwargs['pk'])


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
                {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
                 'name': userstory.code},
            )
        else:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:userstory'), 'class': '',
                 'name': _('User Stories')},
                {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
                 'name': userstory.code},
            )

        context['userstory'] = userstory


        return context