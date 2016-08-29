from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView
from main.decorators import require_project

class AddFormView(SuccessMessageMixin, CreateView):
    template_name = 'components/forms/form.html'
    page_title = ''
    head_template = 'components/form/head.html'
    tabs = False

    def get_context_data(self, **kwargs):
        context = super(AddFormView, self).get_context_data(**kwargs)
        if self.tabs:
            self.template_name='components/forms/form_tabs.html'
        context['page_title']=self.page_title
        context['head_template']=self.head_template
        context['tabs']=self.tabs
        return context


class UpdateFormView(SuccessMessageMixin, UpdateView):
    template_name = 'components/forms/form.html'
    page_title = ''
    head_template = 'components/forms/head.html'
    tabs = False

    def get_context_data(self, **kwargs):
        context = super(UpdateFormView, self).get_context_data(**kwargs)
        if self.tabs:
            self.template_name='components/forms/form_tabs.html'
        context['page_title']=self.page_title
        context['head_template']=self.head_template
        context['tabs']=self.tabs
        return context