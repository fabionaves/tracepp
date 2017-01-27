from django.db import models
from django.utils.translation import ugettext as _
from simple_history.models import HistoricalRecords
from main.components.models import MyModel
from .project import Project


class Sprint(models.Model, MyModel):
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
        on_delete=models.PROTECT,
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
