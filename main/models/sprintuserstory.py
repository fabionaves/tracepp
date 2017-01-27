from django.db import models
from django.utils.translation import ugettext as _
from simple_history.models import HistoricalRecords
from main.components.models import MyModel
from .userstory import UserStory
from .sprint import Sprint


class SprintUserStory(models.Model, MyModel):
    userstory = models.ForeignKey(
        UserStory,
        verbose_name=_('User Story'),
    )
    sprint = models.ForeignKey(
       Sprint,
       verbose_name=_('Sprint'),
       on_delete=models.PROTECT,
    )
    USERSTORY_STATUS_IN_SPRINT_OPTIONS = (
        (0, _('Story not Completed')),
        (1, _('Complete story')),
    )
    status = models.IntegerField(
        _('Status'), choices=USERSTORY_STATUS_IN_SPRINT_OPTIONS, blank=False,default=0,
    )
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
