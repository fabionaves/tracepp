import os
from django.core.files import File
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from django.views.generic import DeleteView

from main.components.git import pull
from main.components.lists import TemplateViewProjectFilter
from main.forms import ArtifactForm
from main.models import  Artifact, ArtifactType, Project, Sprint, Requeriment, UserStory
from main.decorators import require_project


class ArtifactView(SuccessMessageMixin, CreateView):
    template_name = 'artifact/form.html'
    model = Artifact
    form_class = ArtifactForm
    success_url = '/artifact/'

    def get_context_data(self, **kwargs):
        context = super(ArtifactView, self).get_context_data(**kwargs)

        if 'pk' in self.kwargs: #userstory
            userstory = get_object_or_404(UserStory,pk=self.kwargs['pk'])
            context['artifacttype'] = ArtifactType.objects.filter(project_id=self.request.session['project_id'],
                                                                  level=3)
            context['artifact'] = Artifact.objects.filter(project_id=self.request.session['project_id'],
                                                          sprint__isnull=True,
                                                          userstory=userstory)
            context['page_title'] = _('UserStory Artifacts')
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
                    {'link': '#', 'class': '', 'name': _('Artifact')},
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
                    {'link': reverse_lazy('main:requeriment-userstory-detail', kwargs={'requeriment_id': self.kwargs['requeriment_id'],'pk': userstory.pk}), 'class': '',
                     'name': userstory.code},
                    {'link': '#', 'class': '', 'name': _('Artifact')},
                )
            else:
                context['breadcrumbs'] = (
                    {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                    {'link': reverse_lazy('main:userstory'), 'class': '',
                     'name': _('User Stories')},
                    {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
                     'name': userstory.code},
                    {'link': '#', 'class': '', 'name': _('Artifact')},
                )
        elif 'sprint_id' in self.kwargs:
            sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'])
            context['artifacttype'] = ArtifactType.objects.filter(project_id=self.request.session['project_id'],
                                                                  level=2)
            context['artifact'] = Artifact.objects.filter(project_id=self.request.session['project_id'],
                                                          sprint=sprint,
                                                          userstory__isnull=True)
            context['page_title'] = _('Sprint Artifacts')
            context['breadcrumbs'] = (
               {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
               {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
               {'link': reverse_lazy('main:sprint-details',kwargs={'sprint_id':sprint.id}), 'class': '', 'name': sprint},
               {'link': '#', 'class': '', 'name': _('Artifact')},
            )
        elif 'requeriment_id' in self.kwargs:
            requeriment = get_object_or_404(Requeriment, pk=self.kwargs['requeriment_id'])
            context['artifacttype'] = ArtifactType.objects.filter(project_id=self.request.session['project_id'],
                                                                  level=1)
            context['artifact'] = Artifact.objects.filter(project_id=self.request.session['project_id'],
                                                          requeriment=requeriment
                                                          )
            context['page_title'] = _('Requeriment Artifacts')
            context['breadcrumbs'] = (
                {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
                {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
                {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment.id}), 'class': '',
                 'name': requeriment.code},
                {'link': '#', 'class': '', 'name': _('Artifacts')},
            )
        else:
            context['artifact'] = Artifact.objects.filter(project_id=self.request.session['project_id'],
                                                          requeriment__isnull=True,
                                                          sprint__isnull=True,
                                                          userstory__isnull=True,
                                                          )
            context['artifacttype'] = ArtifactType.objects.filter(project_id=self.request.session['project_id'],
                                                                  level=0)
            context['page_title'] = _('Project Artifacts')
        return context

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ArtifactView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.request.session['project_id'])
        form.instance.project = project
        if 'pk' in self.kwargs:
            userstory = get_object_or_404(UserStory, pk=self.kwargs['pk'])
            form.instance.userstory = userstory
        elif 'sprint_id' in self.kwargs:
            sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'])
            form.instance.sprint = sprint
        elif 'requeriment_id' in self.kwargs:
            requeriment = get_object_or_404(Requeriment,pk=self.kwargs['requeriment_id'])
            form.instance.requeriment = requeriment
        return super(ArtifactView, self).form_valid(form)


def ArtifactDownloadView(request,pk):
    artifact = get_object_or_404(
        Artifact,
        project=request.session.get('project_id', None),
        id= pk
    )
    filename = artifact.file.name.split('/')[-1]
    response = HttpResponse(artifact.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


class ArtifactDeleteView(SuccessMessageMixin, DeleteView):
    model = Artifact
    template_name = 'artifact/delete.html'
    fields = ('name', 'type', 'reference', 'requeriment','sprint','userstory','file')
    success_url = '/artifact/'

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ArtifactDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArtifactDeleteView, self).get_context_data()
        return context


class ArtifactTraceCodeView(TemplateViewProjectFilter):
    template_name = 'artifact/tracecode.html'

    def get_context_data(self, **kwargs):
        context = super(ArtifactTraceCodeView, self).get_context_data(**kwargs)
        project = get_object_or_404(
                                                Project.objects.all(),
                                                id=self.request.session.get('project_id', None),
                                              )
        pull(project)
        
        context['project']=project
        return context
