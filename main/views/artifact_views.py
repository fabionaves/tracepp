import os
from django.core.files import File

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import CreateView

from main.components.lists import TemplateViewProjectFilter
from main.forms import ArtifactForm
from main.models import  Artifact, ArtifactType, Project
from main.decorators import require_project


class ArtifactView(SuccessMessageMixin, CreateView):
    template_name = 'artifact/form.html'
    page_title = 'Artifact'
    model = Artifact
    form_class = ArtifactForm
    success_url = '/artifact/'

    def get_context_data(self, **kwargs):
        context = super(ArtifactView, self).get_context_data(**kwargs)
        context['artifacttype'] = ArtifactType.objects.filter(project_id=self.request.session['project_id'], level=0)
        context['artifact'] = Artifact.objects.filter(project_id=self.request.session['project_id'])
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
        #artifacttype = get_object_or_404(ArtifactType, pk=1)
        #form.instance.type = artifacttype
        form.instance.project = project
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



