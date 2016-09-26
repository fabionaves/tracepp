from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from main.components.lists import TemplateViewProjectFilter
from main.models import Sprint, Requeriment, UserStory, Artifact


class HomeView(TemplateViewProjectFilter):
    template_name = 'home/home.html'
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
    )

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['total_sprints'] = Sprint.objects.filter(project=self.request.session.get('project_id', None)).count()
        context['total_requeriments'] = Requeriment.objects.filter(project=self.request.session.get('project_id', None)).count()
        context['total_userstories'] = UserStory.objects.filter(
            project=self.request.session.get('project_id', None)).count()
        context['total_artifacts'] = Artifact.objects.filter(
            project=self.request.session.get('project_id', None)).count()
        return context
