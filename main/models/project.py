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
    total_points = models.IntegerField(_('Total Planned Points'))
    user = models.ManyToManyField(User)
    REPOSITORY_TYPE = (
        ('Git', 'Git'),
    )
    repository_type = models.CharField(_('Repository Type'), choices=REPOSITORY_TYPE, blank=True, null=True,
                                       max_length=30)
    repository_url = models.CharField(_('Repository URL'), blank=True, null=True,  max_length=200)
    TRACKING_TOOL_TYPE = (
        ('Internal','Internal'),
        ('Redmine', 'Redmine'),
    )
    tracking_tool_type = models.CharField(_('Bug Tracking Tool Type'), choices=TRACKING_TOOL_TYPE, blank=True,
                                          null=True, max_length=50)
    tracking_sp_planned_variable = models.CharField(_('Points Planned Custom Field Name'),
                                                    blank=True,
                                                    null=True,
                                                    max_length=50)
    tracking_sp_realized_variable = models.CharField(_('Points Realized Custom Field Name'),
                                                    blank=True,
                                                    null=True,
                                                    max_length=50)
    tracking_bv_planned_variable = models.CharField(_('Businnes Value Planned Custom Field Name'),
                                                   blank=True,
                                                   null=True,
                                                   max_length=50)
    tracking_bv_realized_variable = models.CharField(_('Businnes Value Realized Custom Field Name'),
                                                     blank=True,
                                                     null=True,
                                                     max_length=50)
    tracking_tool_url = models.URLField(_('Bug Tracking Tool URL'), blank=True, null=True)
    tracking_tool_user = models.CharField(_('Bug Tracking Tool User'), blank=True, null=True, max_length=30)
    tracking_tool_password = models.CharField(_('Bug Tracking Tool Password'), blank=True, null=True, max_length=30)
    tracking_tool_project_id = models.CharField(_('Bug Tracking Tool Project Id'), blank=True, null=True, max_length=30)
    versionAsSprint = models.BooleanField(_('Import Redmine Versions as Sprints?'), default=False)
    issueTypesAsUserStory = models.IntegerField(_('What redmine type of issue is a user story?(Insert redmine issue type ID)'),blank=True, null=True)
    issueStatusClosed =  models.IntegerField(_('What redmine Issue Status is a complete User Story?(Insert redmine issue status ID)'),blank=True, null=True)
    issueOnInsertUserStory = models.IntegerField(_('Insert redmine issue on save new User Story?(Inform redmine issue type ID)'),blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")