from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from main.components.lists import ModelList
from main.forms import ProjectForm
from main.components.formviews import AddFormView, UpdateFormView
from main.services.project import ProjectService


class ProjectView(ModelList):
    """
    #class:US004
    #class:US003
    Projects Choose Page.
    """
    model = ProjectService.get_project_model()
    list_display = ('name', )
    page_title = _('Choose a project:')
    action_template = 'project/choose_action.html'

    def dispatch(self, request, *args, **kwargs):
        if 'project_id' in self.kwargs:
            self.request.session['project_id'] = self.kwargs['project_id']
            return redirect(reverse('main:home'))
        else:
            return super(ProjectView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return ProjectService.get_user_projects(user)


class ProjectListView(ProjectView):
    """
    #class:US002
    List of projects for options for choosing, adding, changing, or deleting
    """
    model = ProjectService.get_project_model()
    page_title = 'Projects'
    list_display = ('name', 'requester', 'points_type')
    action_template = "project/action.html"
    top_bar = 'project/top_bar.html'
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:project-list'), 'class': 'active', 'name': _('Project')},
    )


class ProjectAddFormView(AddFormView):
    """
    #class:US002
    Add project form
    """
    model = ProjectService.get_project_model()
    form_class = ProjectForm
    template_name = 'project/form.html'
    success_url = '/project/list/'
    success_message = _('Project was created successfully')
    tabs = (
        {"title": "Project", "id": "project", "class": "active",
         "fields": ("name", "requester", "description", "points_type", "total_points")},
        {"title": "Repository", "id": "repository", "fields": ("repository_type", "repository_url")},
        {"title": "Bug Tracking Tool", "id": "tracking",
         "fields": ('tracking_tool_type', 'tracking_tool_url', 'tracking_tool_user',
                    'tracking_tool_password', 'tracking_tool_project_id')},
        {"title": "Story Points", "id": "sp",
         "fields": ('tracking_sp_planned_variable', 'tracking_sp_realized_variable',)},
        {"title": "Business Value", "id": "bv",
         "fields": ('tracking_bv_planned_variable', 'tracking_bv_realized_variable',)},
        {"title": "Users", "id": "user", "fields": ("user",)},
    )
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:project-list'), 'class': 'active', 'name': _('Project')},
        {'link': '#', 'class': 'active', 'name': _('Add')},
    )


class ProjectUpdateFormView(UpdateFormView):
    """
    #class:US002
    Edit project form
    """
    model = ProjectService.get_project_model()
    form_class = ProjectForm
    template_name = 'project/form.html'
    success_url = '/project/list/'
    success_message = _('Project was saved successfully')
    tabs = (
        {"title": "Project", "id": "project", "class": "active",
         "fields": ("name", "requester", "description", "points_type", "total_points")},
        {"title": "Repository", "id": "repository", "fields": ("repository_type", "repository_url")},
        {"title": "Bug Tracking Tool", "id": "tracking",
         "fields": ('tracking_tool_type', 'tracking_tool_url', 'tracking_tool_user',
                    'tracking_tool_password', 'tracking_tool_project_id')},
        {"title": "Story Points", "id": "sp",
         "fields": ('tracking_sp_planned_variable', 'tracking_sp_realized_variable',)},
        {"title": "Business Value", "id": "bv",
         "fields": ('tracking_bv_planned_variable', 'tracking_bv_realized_variable',)},
        {"title": "Users", "id": "user", "fields": ("user",)},
    )
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:project-list'), 'class': 'active', 'name': _('Project')},
        {'link': '#', 'class': 'active', 'name': _('Update')},
    )