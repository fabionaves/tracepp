from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User

from main.models import Project, Requeriment, UserStory


class ProjectForm(forms.ModelForm):

    user = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                          required=False,
                                          widget=FilteredSelectMultiple("User", is_stacked=False))

    class Media:
        css = {
            'all': ['admin/css/widgets.css',
                    'css/uid-manage-form.css'],
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']

    class Meta:
        model = Project
        fields = ['name','requester','description','points_type','total_points','user']


class RequerimentForm(forms.ModelForm):

    def __init__(self, request, *args, **kwargs):
        super(RequerimentForm, self).__init__(*args, **kwargs)
        self.fields['depends_on'] = forms.ModelMultipleChoiceField(queryset=Requeriment.objects.filter(project_id= request.session.get('project_id', None)),
                                          required=False,
                                          widget=FilteredSelectMultiple("Depends on", is_stacked=False))


    class Media:
        css = {
            'all': ['admin/css/widgets.css',
                    'css/uid-manage-form.css'],
        }
        # Adding this javascript is crucial
        js = ['/admin/jsi18n/']

    class Meta:
        model = Requeriment
        fields = ('code', 'title', 'description', 'type', 'depends_on')


class UserStoryForm(forms.ModelForm):

    class Meta:
        model = UserStory
        fields = ('code', 'title', 'description')
