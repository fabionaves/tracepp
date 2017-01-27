from django.db import models
from django.utils.translation import ugettext as _
from simple_history.models import HistoricalRecords
from main.components.models import MyModel
from .project import Project


class Requeriment(models.Model, MyModel):
    code = models.CharField(_('Code'), max_length=10, blank=False, null=False)
    title = models.CharField(_('Title'), max_length=100, blank=False, null=False)
    description = models.TextField()
    REQUIREMENT_TYPE_OPTIONS = (
        (0, _('Functional')),
        (1, _('Non-Functional')),
    )
    type = models.IntegerField(
        _('Type'), choices=REQUIREMENT_TYPE_OPTIONS, blank=False
    )
    project = models.ForeignKey(
        Project,
        verbose_name=_('Project'),
        on_delete=models.PROTECT,
    )
    changed_by = models.ForeignKey('auth.User')
    history = HistoricalRecords()
    depends_on = models.ManyToManyField("self", symmetrical=False, blank=True)  #depende de

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return self.code+' - '+self.title
