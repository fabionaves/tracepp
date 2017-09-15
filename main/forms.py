from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.utils.translation import ugettext as _


from main.models import Project, Requeriment, UserStory, SprintUserStory, ArtifactType, Artifact
from main.services.artifacttype import ArtifactTypeService


class ProjectForm(forms.ModelForm):

    user = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                          required=False,
                                          widget=FilteredSelectMultiple("User", is_stacked=False))

    class Meta:
        model = Project
        fields = ['name', 'requester', 'description', 'points_type', 'total_points',
                  'repository_type', 'repository_url','tracking_tool_type',
                  'tracking_tool_url',
                  'tracking_sp_planned_variable', 'tracking_sp_realized_variable',
                  'tracking_bv_planned_variable', 'tracking_bv_realized_variable',
                  'tracking_tool_user', 'tracking_tool_password', 'tracking_tool_project_id','versionAsSprint','issueTypesAsUserStory','issueStatusClosed','issueOnInsertUserStory',
                  'user']


class RequerimentForm(forms.ModelForm):

    def __init__(self, request, *args, **kwargs):
        super(RequerimentForm, self).__init__(*args, **kwargs)

        self.fields['depends_on'] = forms.ModelMultipleChoiceField(
            queryset=Requeriment.objects.filter(project_id=request.session.get('project_id', None)),
            required=False,
            widget=FilteredSelectMultiple(_("Depends on"), is_stacked=False),
        )

    class Meta:
        model = Requeriment
        fields = ('code', 'title', 'description', 'type', 'depends_on',)


class SprintUserStoryForm(forms.ModelForm):

    class Meta:
        model = SprintUserStory
        fields = ('sprint', 'status',)


class UserStoryForm(forms.ModelForm):

    def __init__(self, request, *args, **kwargs):
        super(UserStoryForm, self).__init__(*args, **kwargs)
        self.fields['requeriment'] = forms.ModelMultipleChoiceField(queryset=Requeriment.objects.filter(project_id= request.session['project_id']),
                                          required=False,
                                          widget=FilteredSelectMultiple(_("Requeriments"), is_stacked=False))
    class Meta:
        model = UserStory
        fields = ('code', 'title', 'description', 'acceptanceCriteria', 'requeriment')

SprintUserStoryInlineFormSet = inlineformset_factory(UserStory,
                                                     SprintUserStory,
                                                     form=SprintUserStoryForm,
                                                     extra=2,
                                                     can_delete=True,
                                                     )

class SprintUserStoryInlineFormSetFiltrado(SprintUserStoryInlineFormSet):
    def __init__(self, project, *args, **kwargs):
        super(SprintUserStoryInlineFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
              form.fields['sprint'].queryset = form.fields['sprint'].queryset.filter(
              project=project
         )


class ArtifactTypeForm(forms.ModelForm):

    class Meta:
        model = ArtifactType
        fields = ('name', 'level', 'type', 'trace_code')


class ArtifactForm(forms.ModelForm):

    class Meta:
        model = Artifact
        fields = ('type','file')

class ActivityUserStoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActivityUserStoryForm, self).__init__(*args, **kwargs)
        self.fields['type'].required=True
        self.fields['user'].required = True
        self.fields['title'].required = True
        self.fields['userstory'].required = True
    class Meta:
        model = Artifact
        fields = ('user', 'title', 'description', 'type', 'userstory','create_date',
                  'estimated_time', 'closed_date', 'spent_time', 'estimated_storypoints', 'realized_storypoints',
                  'estimated_businnesvalue', 'realized_businnesvalue')


class ActivityRequerimentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActivityRequerimentForm, self).__init__(*args, **kwargs)
        self.fields['type'].required=True
        self.fields['user'].required = True
        self.fields['title'].required = True
        self.fields['requeriment'].required = True
    class Meta:
        model = Artifact
        fields = ('user', 'title', 'description', 'type', 'requeriment','create_date',
                  'estimated_time', 'closed_date', 'spent_time', 'estimated_storypoints', 'realized_storypoints',
                  'estimated_businnesvalue', 'realized_businnesvalue')


class ActivitySprintForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActivitySprintForm, self).__init__(*args, **kwargs)
        self.fields['type'].required=True
        self.fields['user'].required = True
        self.fields['title'].required = True
        self.fields['sprint'].required = True
    class Meta:
        model = Artifact
        fields = ('user', 'title', 'description', 'type', 'sprint', 'create_date',
                  'estimated_time', 'closed_date', 'spent_time', 'estimated_storypoints', 'realized_storypoints',
                  'estimated_businnesvalue', 'realized_businnesvalue')

class ActivityProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ActivityProjectForm, self).__init__(*args, **kwargs)
        self.fields['type'].required=True
        self.fields['user'].required = True
        self.fields['title'].required = True
    class Meta:
        model = Artifact
        fields = ('user', 'title', 'description', 'type','create_date',
                  'estimated_time', 'closed_date', 'spent_time', 'estimated_storypoints', 'realized_storypoints',
                  'estimated_businnesvalue', 'realized_businnesvalue')