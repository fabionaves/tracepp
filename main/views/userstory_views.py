from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from main.components.lists import ModelListProjectFilter
from main.decorators import require_project
from main.forms import UserStoryForm, SprintUserStoryInlineFormSet
from main.models import Sprint, Project, Requeriment, SprintUserStory, UserStory
from main.components.formviews import AddFormView, UpdateFormView


class UserStoryListView(ModelListProjectFilter):
    model = SprintUserStory
    paginate_by = 20
    list_display = ('userstory', 'sprint','status')
    master = False
    action_template = 'userstory/action.html'
    top_bar = 'userstory/top_bar.html'

    def get_queryset(self):
        if 'sprint_id' in self.kwargs:
            self.master = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=self.request.session.get('project_id', None))
            queryset = self.model.objects.filter(sprint=self.kwargs['sprint_id'])
        elif 'requeriment_id' in self.kwargs:
            self.master = get_object_or_404(Requeriment, pk=self.kwargs['requeriment_id'], project=self.request.session.get('project_id', None))
            queryset = self.model.objects.filter(userstory__requeriment =self.kwargs['requeriment_id'])
        else:
            self.master = get_object_or_404(Project,pk=self.request.session.get('project_id', None))
            queryset = self.model.objects.filter(sprint__project_id=self.request.session.get('project_id', None))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserStoryListView, self).get_context_data()
        context['page_title'] = str(self.master)+' -  '+_('Users Stories')
        if 'sprint_id' in self.kwargs:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
                {'link': reverse_lazy('main:sprint-details',kwargs={'sprint_id':self.kwargs['sprint_id']}), 'class': '', 'name': self.master},
                {'link': '#', 'class': '', 'name': _('User Stories')},
            )
        elif 'requeriment_id' in self.kwargs:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriments')},
                {'link': reverse_lazy('main:requeriment-details',kwargs={'pk':self.kwargs['requeriment_id']}), 'class': '', 'name': self.master},
                {'link': '#', 'class': '', 'name': _('User Stories')},
            )
        else:
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': '#', 'class': '', 'name': _('User Stories')},
            )
        return context


class UserStoryAddFormView(AddFormView):
    page_title = 'UserStory'
    model = UserStory
    form_class = UserStoryForm
    success_message = _('UserStory was created successfully')
    tabs = (
        {"title": "UserStory", "id": "userstory", "class": "active",
         "fields": ('code', 'title', 'description','storypoints_planned', 'storypoints_realized', 'bussinessvalue_planned', 'bussinessvalue_realized')},
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
    page_title = 'UserStory'
    model = UserStory
    form_class = UserStoryForm
    success_message = _('UserStory was created successfully')
    tabs = (
        {"title": "UserStory", "id": "userstory", "class": "active",
         "fields": ('code', 'title', 'description','storypoints_planned', 'storypoints_realized', 'bussinessvalue_planned', 'bussinessvalue_realized')},
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
