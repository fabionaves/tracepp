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
    source = models.CharField(_('Name'), max_length=100, blank=True, null=True)
    line = models.CharField(_('Name'), max_length=100, blank=True, null=True)

    type = models.ForeignKey(
        ArtifactType,
        verbose_name=_('Artifact type'),
        null=True,
        blank=True,
    )
    reference = models.CharField( max_length=100, blank=False, null=False)
    project = models.ForeignKey(
        Project,
    )
    requeriment = models.ForeignKey(
        Requeriment,
        blank=True,
        null=True,
    )
    sprint = models.ForeignKey(
        Sprint,
        blank=True,
        null=True,
    )
    userstory = models.ForeignKey(
        UserStory,
        blank=True,
        null=True,
    )
    estimated_time = models.IntegerField(_('Estimated Time'), null=True, blank=True)
    spent_time = models.IntegerField(_('Spent Time'), null=True, blank=True)
    file = models.FileField(_('File'), upload_to=settings.UPLOAD_DIR)
    objects = models.Manager()
    file_objects = FileArtifactsManager()
    source_objects = SourceArtifactsManager()
    activity_objects = ActivityArtifactsManager()


