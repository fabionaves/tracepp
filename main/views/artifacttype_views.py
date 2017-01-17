from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView

from main.components.formviews import AddFormView, UpdateFormView
from main.components.lists import ModelListProjectFilter
from main.forms import ArtifactTypeForm
from main.models import ArtifactType, Project
from main.decorators import require_project


class ArtifactTypeView(ModelListProjectFilter):
    model = ArtifactType
    paginate_by = 20
    list_display = ('name', 'level', 'type', 'trace_code')
    top_bar = 'artifacttype/top_bar.html'
    page_title = _('Artifact type')
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:artifacttype'), 'class': '', 'name': _('Artifact type')},
    )


class ArtifactTypeAddFormView(AddFormView):
    page_title = _('Artifact type')
    model = ArtifactType
    form_class = ArtifactTypeForm
    success_url = '/artifacttype/'
    success_message = _('Artifacty Type was created successfully')
    tabs = (
        {"title": _('Artifact type'), "id": "artifacttype", "class": "active",
         "fields": ('name', 'level', 'type', 'trace_code')},
    )
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:artifacttype'), 'class': '', 'name': _('Artifact type')},
    )

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ArtifactTypeAddFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.request.session['project_id'])
        #form.instance.changed_by = self.request.user
        form.instance.project = project
        return super(ArtifactTypeAddFormView, self).form_valid(form)


class ArtifactTypeUpdateFormView(UpdateFormView):
    page_title = _('Artifact type')
    model = ArtifactType
    form_class = ArtifactTypeForm
    success_url = '/artifacttype/'
    success_message = _('Artifacty Type was updated successfully')
    tabs = (
        {"title": _('Artifact type'), "id": "artifacttype", "class": "active",
         "fields": ('name', 'level', 'type', 'trace_code')},
    )
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:artifacttype'), 'class': '', 'name': _('Artifact Type')},
    )

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ArtifactTypeUpdateFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.request.session['project_id'])
        #form.instance.changed_by = self.request.user
        form.instance.project = project
        return super(ArtifactTypeUpdateFormView, self).form_valid(form)


class ArtifactTypeDeleteView(SuccessMessageMixin, DeleteView):
    model = ArtifactType
    template_name = 'artifacttype/delete.html'
    list_display = ('name', 'level', 'type', 'trace_code')
    success_url = '/artifacttype/'

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ArtifactTypeDeleteView, self).dispatch(request, *args, **kwargs)