from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from main.components.lists import TemplateViewProjectFilter
from main.models import Sprint, Requeriment, UserStory, Artifact
from main.services.project import ProjectService
from main.services.sprint import SprintService
from main.services.userstory import UserStoryService


class HomeView(TemplateViewProjectFilter):
    template_name = 'home/home.html'
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
    )

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['total_sprints'] = ProjectService.get_num_sprints_from_project(self.request.session.get('project_id', None))
        context['total_requeriments'] = ProjectService.get_num_requeriments_from_project(self.request.session.get('project_id', None))
        context['task_effort'] = SprintService.task_effort(self.request.session.get('project_id', None))
        context['storypoints_variation'] = SprintService.storypoint(self.request.session.get('project_id', None))
        context['total_userstories'] = ProjectService.get_num_userstories_from_project(self.request.session.get('project_id', None))
        context['total_artifacts'] = ProjectService.get_num_artifacts_from_project(self.request.session.get('project_id', None))
        return context
