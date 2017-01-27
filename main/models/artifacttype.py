from django.db import models
from django.utils.translation import ugettext as _
from main.components.models import MyModel
from .project import Project


class ArtifactType(models.Model, MyModel):
    name = models.CharField(_('Name'), max_length=100, blank=False, null=False)
    ARTIFACT_LEVEL = (
        (0, _('Project')),
        (1, _('Requeriment')),
        (2, _('Sprint')),
        (3, _('User Story')),
    )
    level = models.IntegerField(_('Level'), choices=ARTIFACT_LEVEL)
    ARTIFACT_TYPE = (
        (0, _('File')),
        (1, _('Source')),
        (2, _('Activity')),
    )
    type = models.IntegerField(_('Type'), choices=ARTIFACT_TYPE)
    trace_code = models.CharField(_('Trace Code'), max_length=100, blank=False, null=False)
    project = models.ForeignKey(
        Project
    )