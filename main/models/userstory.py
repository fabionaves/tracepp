from django.db import models
from django.utils.translation import ugettext as _
from simple_history.models import HistoricalRecords
from main.components.models import MyModel
from .requeriment import Requeriment
from .project import Project


class UserStory(models.Model,MyModel):
    code = models.CharField(_('Code'), max_length=30)
    title = models.CharField(_('Title'), max_length=50)
    description = models.TextField(_('Description'))
    acceptanceCriteria = models.TextField(_('Acceptance Criteria'))
    requeriment = models.ManyToManyField(Requeriment)
    storypoints_planned = models.IntegerField(_('SP (Planned)'), blank=False, default=0)
    storypoints_realized = models.IntegerField(_('SP (Realized)'), blank=False, default=0)
    bussinessvalue_planned = models.IntegerField(_('BV (Planned)'), blank=False, default=0)
    bussinessvalue_realized = models.IntegerField(_('BV (Realized)'), blank=False, default=0)
    project = models.ForeignKey(Project,
                                on_delete=models.PROTECT, verbose_name=_('Project')
                                )
    changed_by = models.ForeignKey('auth.User')
    history = HistoricalRecords()

    @property
    def percentual_of_storypoints_variation(self):
        if self.storypoints_planned != 0:
            return  100 * ( (self.storypoints_realized - self.storypoints_planned) / self.storypoints_planned)
        elif self.storypoints_realized != 0:
            return 0
        else:
            return 0

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return self.code+' - '+self.title




