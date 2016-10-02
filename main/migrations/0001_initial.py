# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-30 12:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.components.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
                ('reference', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='upload', verbose_name='File')),
            ],
        ),
        migrations.CreateModel(
            name='ArtifactType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('level', models.IntegerField(choices=[(0, 'Project'), (1, 'Requeriment'), (2, 'Sprint'), (3, 'User Story')], verbose_name='Level')),
                ('type', models.IntegerField(choices=[(0, 'File'), (1, 'Source')], verbose_name='Type')),
                ('trace_code', models.CharField(max_length=100, verbose_name='Trace Code')),
            ],
            bases=(models.Model, main.components.models.MyModel),
        ),
        migrations.CreateModel(
            name='HistoricalRequeriment',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('code', models.CharField(max_length=10, verbose_name='Code')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('description', models.TextField()),
                ('type', models.IntegerField(choices=[(0, 'Functional'), (1, 'Non-Functional')], verbose_name='Type')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'historical requeriment',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalSprint',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Title')),
                ('status', models.IntegerField(choices=[(0, 'Planning'), (1, 'Executing'), (2, 'Close')], verbose_name='Status')),
                ('begin', models.DateField(verbose_name='Begin')),
                ('end', models.DateField(verbose_name='End')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Sprint',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalSprintUserStory',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Story not Completed'), (1, 'Complete story')], default=0, verbose_name='Status')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'historical sprint user story',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalUserStory',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('code', models.CharField(max_length=30, verbose_name='Code')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('acceptanceCriteria', models.TextField(verbose_name='Acceptance Criteria')),
                ('storypoints_planned', models.IntegerField(default=0, verbose_name='Story Points (Planned)')),
                ('storypoints_realized', models.IntegerField(default=0, verbose_name='Story Points (Realized)')),
                ('bussinessvalue_planned', models.IntegerField(default=0, verbose_name='Businnes Value (Planned)')),
                ('bussinessvalue_realized', models.IntegerField(default=0, verbose_name='Businnes Value (Realized)')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'verbose_name': 'historical user story',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('requester', models.CharField(max_length=100, verbose_name='Requester')),
                ('description', models.TextField()),
                ('points_type', models.IntegerField(choices=[(0, 'Functions Points'), (1, 'User Story Points'), (2, 'Use Case Points')], verbose_name='Points Type')),
                ('total_points', models.IntegerField(verbose_name='Total of Points')),
                ('repository_url', models.URLField(verbose_name='Repository URL')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Projects',
                'verbose_name': 'Project',
                'ordering': ['-id'],
            },
            bases=(models.Model, main.components.models.MyModel),
        ),
        migrations.CreateModel(
            name='Requeriment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, verbose_name='Code')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('description', models.TextField()),
                ('type', models.IntegerField(choices=[(0, 'Functional'), (1, 'Non-Functional')], verbose_name='Type')),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('depends_on', models.ManyToManyField(blank=True, to='main.Requeriment')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.Project', verbose_name='Project')),
            ],
            bases=(models.Model, main.components.models.MyModel),
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Title')),
                ('status', models.IntegerField(choices=[(0, 'Planning'), (1, 'Executing'), (2, 'Close')], verbose_name='Status')),
                ('begin', models.DateField(verbose_name='Begin')),
                ('end', models.DateField(verbose_name='End')),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.Project', verbose_name='Project')),
            ],
            options={
                'verbose_name_plural': 'Sprints',
                'verbose_name': 'Sprint',
                'ordering': ['-id'],
            },
            bases=(models.Model, main.components.models.MyModel),
        ),
        migrations.CreateModel(
            name='SprintUserStory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Story not Completed'), (1, 'Complete story')], default=0, verbose_name='Status')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.Sprint', verbose_name='Sprint')),
            ],
            bases=(models.Model, main.components.models.MyModel),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Taks')),
                ('estimated_time', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Estimated Time (Hours)')),
                ('realizated_time', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Realizated Time (Hours)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criated at')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, verbose_name='Code')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('acceptanceCriteria', models.TextField(verbose_name='Acceptance Criteria')),
                ('storypoints_planned', models.IntegerField(default=0, verbose_name='Story Points (Planned)')),
                ('storypoints_realized', models.IntegerField(default=0, verbose_name='Story Points (Realized)')),
                ('bussinessvalue_planned', models.IntegerField(default=0, verbose_name='Businnes Value (Planned)')),
                ('bussinessvalue_realized', models.IntegerField(default=0, verbose_name='Businnes Value (Realized)')),
                ('changed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.Project', verbose_name='Project')),
                ('requeriment', models.ManyToManyField(to='main.Requeriment')),
            ],
            bases=(models.Model, main.components.models.MyModel),
        ),
        migrations.AddField(
            model_name='task',
            name='userstory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UserStory', verbose_name='UserStory'),
        ),
        migrations.AddField(
            model_name='sprintuserstory',
            name='userstory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UserStory', verbose_name='User Story'),
        ),
        migrations.AddField(
            model_name='historicaluserstory',
            name='project',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='main.Project'),
        ),
        migrations.AddField(
            model_name='historicalsprintuserstory',
            name='sprint',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='main.Sprint'),
        ),
        migrations.AddField(
            model_name='historicalsprintuserstory',
            name='userstory',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='main.UserStory'),
        ),
        migrations.AddField(
            model_name='historicalsprint',
            name='project',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='main.Project'),
        ),
        migrations.AddField(
            model_name='historicalrequeriment',
            name='project',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='main.Project'),
        ),
        migrations.AddField(
            model_name='artifacttype',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Project'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Project'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='requeriment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Requeriment'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='sprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Sprint'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.ArtifactType', verbose_name='Artifact type'),
        ),
        migrations.AddField(
            model_name='artifact',
            name='userstory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.UserStory'),
        ),
    ]
