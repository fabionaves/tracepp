from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
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
    REPOSITORY_TYPE = (
        ('Git', 'Git'),
    )
    repository_type = models.CharField(_('Repository Type'), choices=REPOSITORY_TYPE, blank=True, null=True,
                                       max_length=30)
    repository_url = models.URLField(_('Repository URL'))
    TRACKING_TOOL_TYPE = (
        ('Redmine', 'Redmine'),
    )
    tracking_tool_type = models.CharField(_('Bug Tracking Tool Type'), choices=TRACKING_TOOL_TYPE, blank=True,
                                          null=True, max_length=30)
    tracking_tool_url = models.URLField(_('Bug Tracking Tool URL'), blank=True, null=True)
    tracking_tool_user = models.CharField(_('Bug Tracking Tool User'), blank=True, null=True, max_length=30)
    tracking_tool_password = models.CharField(_('Bug Tracking Tool Password'), blank=True, null=True, max_length=30)
    tracking_tool_project_id = models.CharField(_('Bug Tracking Tool Project Id'), blank=True, null=True, max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")