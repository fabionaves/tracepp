from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from .artifacttype import ArtifactType
from .project import Project
from .sprint import Sprint
from .requeriment import Requeriment
from .userstory import UserStory


class FileArtifactsManager(models.Manager):
    def get_queryset(self):
        return super(FileArtifactsManager, self).get_queryset().filter(type__type=0)


class SourceArtifactsManager(models.Manager):
    def get_queryset(self):
        return super(SourceArtifactsManager, self).get_queryset().filter(type__type=1)


class ActivityArtifactsManager(models.Manager):
    def get_queryset(self):
        return super(ActivityArtifactsManager, self).get_queryset().filter(type__type=2)


class Artifact(models.Model):
    title = models.CharField(_('Title'), max_length=100, blank=True, null=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=False
    )
    create_date = models.DateField(_('Create Date'), blank=True, null=True)
    closed_date = models.DateField(_('Closed Date'), blank=True, null=True)

    source = models.CharField(_('Source'), max_length=100, blank=True, null=True)
    line = models.CharField(_('Name'), max_length=100, blank=True, null=True)

    type = models.ForeignKey(
        ArtifactType,
        verbose_name=_('Artifact type'),
        null=True,
        blank=True,
        on_delete=False
    )
    reference = models.CharField( max_length=100, blank=False, null=False)
    project = models.ForeignKey(
        Project,
        on_delete=False
    )
    requeriment = models.ForeignKey(
        Requeriment,
        blank=True,
        null=True,
        on_delete=False
    )
    sprint = models.ForeignKey(
        Sprint,
        blank=True,
        null=True,
        on_delete=False
    )
    userstory = models.ForeignKey(
        UserStory,
        blank=True,
        null=True,
        on_delete=False
    )
    estimated_time = models.IntegerField(_('Estimated Time'), null=True, blank=True)
    spent_time = models.IntegerField(_('Spent Time'), null=True, blank=True)
    estimated_storypoints = models.IntegerField(_('Estimated Points'), null=True, blank=True)
    realized_storypoints = models.IntegerField(_('Realized Points'), null=True, blank=True)
    estimated_businnesvalue = models.IntegerField(_('Estimated Businnes Value'), null=True, blank=True)
    realized_businnesvalue = models.IntegerField(_('Realized Businnes Value'), null=True, blank=True)
    file = models.FileField(_('File'), upload_to=settings.UPLOAD_DIR)
    objects = models.Manager()
    file_objects = FileArtifactsManager()
    source_objects = SourceArtifactsManager()
    activity_objects = ActivityArtifactsManager()
