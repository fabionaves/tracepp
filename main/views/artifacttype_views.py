from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView
from main.components.formviews import AddFormView, UpdateFormView
from main.components.lists import ModelListProjectFilter
from main.forms import ArtifactTypeForm
from main.decorators import require_project
from main.services.artifacttype import ArtifactTypeService
from main.services.project import ProjectService


class ArtifactTypeView(ModelListProjectFilter):
    """
    #class:US008
    """
    model = ArtifactTypeService.get_artifacttype_model()
    paginate_by = 20
    list_display = ('name', 'level', 'type', 'trace_code')
    top_bar = 'artifacttype/top_bar.html'
    page_title = _('Artifact type')
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:artifacttype'), 'class': '', 'name': _('Artifact type')},
    )


class ArtifactTypeAddFormView(AddFormView):
    """
    #class:US008
    """
    page_title = _('Artifact type')
    model = ArtifactTypeService.get_artifacttype_model()
    form_class = ArtifactTypeForm

    success_message = _('Artifacty Type was created successfully')
    tabs = (
        {"title": _('Artifact type'), "id": "artifacttype", "class": "active",
         "fields": ('name', 'level', 'type', 'trace_code')},
    )
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:artifacttype'), 'class': '', 'name': _('Artifact type')},
    )

    def get_success_url(self):
        return reverse('main:artifacttype')

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ArtifactTypeAddFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = ProjectService.get_project(self.request.session['project_id'])
        #form.instance.changed_by = self.request.user
        form.instance.project = project
        return super(ArtifactTypeAddFormView, self).form_valid(form)


class ArtifactTypeUpdateFormView(UpdateFormView):
    """
    #class:US008
    """
    page_title = _('Artifact type')
    model = ArtifactTypeService.get_artifacttype_model()
    form_class = ArtifactTypeForm

    success_message = _('Artifacty Type was updated successfully')
    tabs = (
        {"title": _('Artifact type'), "id": "artifacttype", "class": "active",
         "fields": ('name', 'level', 'type', 'trace_code')},
    )
    breadcrumbs = (
        {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
        {'link': reverse_lazy('main:artifacttype'), 'class': '', 'name': _('Artifact Type')},
    )

    def get_success_url(self):
        return reverse('main:artifacttype')

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ArtifactTypeUpdateFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = ProjectService.get_project(self.request.session['project_id'])
        #form.instance.changed_by = self.request.user
        form.instance.project = project
        return super(ArtifactTypeUpdateFormView, self).form_valid(form)


class ArtifactTypeDeleteView(SuccessMessageMixin, DeleteView):
    """
    #class:US008
    """
    model = ArtifactTypeService.get_artifacttype_model()
    template_name = 'artifacttype/delete.html'
    list_display = ('name', 'level', 'type', 'trace_code')

    def get_success_url(self):
        return reverse('main:artifacttype')

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ArtifactTypeDeleteView, self).dispatch(request, *args, **kwargs)