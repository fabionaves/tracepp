from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Project(models.Model):
    name = models.CharField(_('Name'), max_length=100, blank=False, null=False)
    requester = models.CharField(_('Requester'), max_length=100)
    description = models.TextField()
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_all_fields(self):
        fields = []
        for f in self._meta.fields:
            fname = f.name
            # resolve picklists/choices, with get_xyz_display() function
            get_choice = 'get_' + fname + '_display'
            if hasattr(self, get_choice):
                value = getattr(self, get_choice)()
            else:
                try:
                    value = getattr(self, fname)
                except User.DoesNotExist:
                    value = None

            # only display fields with values and skip some fields entirely
            if f.editable and f.name not in ('id', 'created_at', 'updated_at', 'applicant'):
                fields.append(
                    {
                        'label': f.verbose_name,
                        'name': f.name,
                        'value': value,
                    }
                )
        return fields

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class Sprint(models.Model):
    title = models.CharField(_('Title'), max_length=30)
    SPRINT_STATUS_OPTIONS = (
        (0, _('Planning')),
        (1, _('Executing')),
        (2, _('Close')),
    )
    status = models.IntegerField(
        _('Status'), choices=SPRINT_STATUS_OPTIONS, blank=False
    )
    begin = models.DateField(_('Begin'))
    end = models.DateField(_('End'))
    project = models.ForeignKey(
        Project,
        verbose_name=_('Project'),
    )

    def __str__(self):
        return self.title

    def get_all_fields(self):
        fields = []
        for f in self._meta.fields:
            fname = f.name
            # resolve picklists/choices, with get_xyz_display() function
            get_choice = 'get_' + fname + '_display'
            if hasattr(self, get_choice):
                value = getattr(self, get_choice)()
            else:
                try:
                    value = getattr(self, fname)
                except User.DoesNotExist:
                    value = None

            # only display fields with values and skip some fields entirely
            if f.editable and f.name not in ('id', 'created_at', 'updated_at', 'applicant'):
                fields.append(
                    {
                        'label': f.verbose_name,
                        'name': f.name,
                        'value': value,
                    }
                )
        return fields

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Sprint")
        verbose_name_plural = _("Sprints")



class UserStory(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    description = models.TextField(_('Description'))


class SprintUserStory(models.Model):
    sprint = models.ForeignKey(
        Sprint,
        verbose_name=_('Sprint'),
    )
    userstory = models.ForeignKey(
        UserStory,
        verbose_name=_('User Story'),
    )
    USERSTORY_STATUS_IN_SPRINT_OPTIONS = (
        (0, _('Story not Completed')),
        (1, _('Complete story')),
    )
    status = models.IntegerField(
        _('Status'), choices=USERSTORY_STATUS_IN_SPRINT_OPTIONS, blank=False,default=0,
    )


class Task(models.Model):
    userstory = models.ForeignKey(
        UserStory,
        verbose_name=_('UserStory'),
    )
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='User',
    )
    description = models.CharField(_('Taks'), max_length=100)
    estimated_time = models.DecimalField(_('Estimated Time (Hours)'), max_digits=4, decimal_places=2)
    realizated_time = models.DecimalField(_('Realizated Time (Hours)'), blank=True, null=True, max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(_('Criated at'), auto_now_add=True)


class ArtifactType(models.Model):
    name = models.CharField(_('Name'), max_length=100, blank=False, null=False)
    ARTIFACT_LEVEL = (
        (0, _('Project')),
        (1, _('Sprint')),
        (2, _('User Story')),
    )
    level = models.IntegerField(_('Level'), choices=ARTIFACT_LEVEL)
    ARTIFACT_TYPE = (
        (0, _('File')),
        (1, _('Source')),
    )
    type = models.IntegerField(_('Type'), choices=ARTIFACT_TYPE)
    trace_code = models.CharField(_('Trace Code'), max_length=100, blank=False, null=False)


class Artifact(models.Model):
    name = models.CharField(_('Name'), max_length=100, blank=False, null=False)
    type = models.ForeignKey(
        ArtifactType,
        verbose_name=_('Artifact type'),
    )
    reference = models.CharField( max_length=100, blank=False, null=False)


