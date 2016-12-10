from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect
from main.components.lists import ModelList
from main.forms import ProjectForm
from main.models import Project
from main.components.formviews import AddFormView, UpdateFormView

#class:US004
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
    action_template = "project/action.html"
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
        {"title" : "Repository", "id" : "repository", "fields" : ("repository_type","repository_url")},
        {"title": "Bug Tracking Tool", "id": "tracking","fields": ('tracking_tool_type', 'tracking_tool_url', 'tracking_tool_user', 'tracking_tool_password','tracking_tool_project_id')},
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
        {"title": "Repository", "id": "repository", "fields": ("repository_type", "repository_url")},
        {"title": "Bug Tracking Tool", "id": "tracking",
         "fields": ('tracking_tool_type', 'tracking_tool_url', 'tracking_tool_user', 'tracking_tool_password','tracking_tool_project_id')},
        {"title": "Users", "id": "user", "fields": ("user",)},
    )
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:project-list'), 'class': 'active', 'name': _('Project')},
        {'link': '#', 'class': 'active', 'name': _('Update')},
    )