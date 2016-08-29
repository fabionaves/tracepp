from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from simple_history.models import HistoricalRecords
from main.components.models import MyModel


class Project(models.Model, MyModel):
    name = models.CharField(_('Name'), max_length=100, blank=False, null=False)
    requester = models.CharField(_('Requester'), max_length=100)
    description = models.TextField()
    POINTS_TYPE_OPTIONS = (
        (0, _('Functions Points')),
        (1, _('User Story Points')),
        (2, _('Use Case Points')),
    )
    points_type = models.IntegerField(
        _('Points Type'), choices=POINTS_TYPE_OPTIONS, blank=False
    )
    total_points = models.IntegerField(_('Total of Points'))
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-id"]
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class Sprint(models.Model,MyModel):
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
    changed_by = models.ForeignKey('auth.User')
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
        
    def __str__(self):
        return self.title



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


