from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from main.components.lists import TemplateViewProjectFilter
from main.models import Sprint, Requeriment, UserStory, Artifact
from main.services.project import ProjectService
from main.services.userstory import UserStoryService


class HomeView(TemplateViewProjectFilter):
    template_name = 'home/home.html'
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
    )

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['total_sprints'] = Sprint.objects.filter(project=self.request.session.get('project_id', None)).count()
        context['total_requeriments'] = Requeriment.objects.filter(project=self.request.session.get('project_id', None)).count()
        context['task_effort'] = UserStoryService.get_task_effor_per_userstory(self.request.session.get('project_id', None))
        context['storypoints_variation'] = ProjectService.get_userstories(self.request.session.get('project_id', None))
        context['total_userstories'] = UserStory.objects.filter(
            project=self.request.session.get('project_id', None)).count()
        context['total_artifacts'] = Artifact.objects.filter(
            project=self.request.session.get('project_id', None),
            requeriment__isnull=True,
            sprint__isnull=True,
            userstory__isnull=True,
        ).count()
        return context
