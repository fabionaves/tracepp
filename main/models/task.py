from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from .userstory import UserStory


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