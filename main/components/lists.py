from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from main.decorators import require_project


class ModelList(ListView):
    template_name = 'components/lists/list.html'
    page_title = False
    action_template = "components/lists/action.html"
    top_bar = False
    breadcrumbs = False

    def get_context_data(self, **kwargs):
        context = super(ModelList, self).get_context_data(**kwargs)
        context['breadcrumbs'] = self.breadcrumbs
        context['top_bar'] = self.top_bar
        context['list_display'] = self.list_display
        titles = []
        for item in self.list_display:
            titles.append(self.model._meta.get_field(item).verbose_name)
        context['titles'] = titles
        if not self.page_title:
            context['page_title'] = self.model._meta.verbose_name_plural
        else:
            context['page_title'] = self.page_title
        context['action_template'] = self.action_template
        return context


class ModelListProjectFilter(ModelList):

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(ModelListProjectFilter, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(ModelListProjectFilter, self).get_queryset()
        return queryset.filter(project=self.request.session.get('project_id', None))


class TemplateViewProjectFilter(TemplateView):
    breadcrumbs = False

    @method_decorator(require_project())
    def dispatch(self, request, *args, **kwargs):
        return super(TemplateViewProjectFilter, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TemplateViewProjectFilter, self).get_context_data()
        context['breadcrumbs']=self.breadcrumbs
        return context