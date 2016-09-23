# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-27 01:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20160821_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='points_type',
            field=models.IntegerField(choices=[(0, 'Functions Points'), (1, 'User Story Points'), (2, 'Use Case Points')], default=0, verbose_name='Points Type'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='total_points',
            field=models.IntegerField(default=0, verbose_name='Total of Points'),
            preserve_default=False,
        ),
    ]