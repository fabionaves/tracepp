from django.db.models import Sum
from django.shortcuts import get_object_or_404

from main.models import Artifact
from main.models import SprintUserStory
from main.models import UserStory

class UserStoryService:

    @staticmethod
    def get_userstory_model():
        return UserStory

    @staticmethod
    def get_userstory(project_id, userstory_id):
        return get_object_or_404(
            UserStory.objects.all(),
            project=project_id,
            id=userstory_id
        )

    @staticmethod
    def get_num_artifacts_from_userstory(project_id, userstory_id):
        return Artifact.objects.filter(
            project=project_id, userstory=userstory_id).count()

    @staticmethod
    def get_num_file_artifacts_from_userstory(project_id, userstory_id):
        return Artifact.file_objects.filter(
            project=project_id, userstory=userstory_id).count()

    @staticmethod
    def get_num_source_artifacts_from_userstory(project_id, userstory_id):
        return Artifact.source_objects.filter(
            project=project_id, userstory=userstory_id).count()

    @staticmethod
    def get_num_activity_artifacts_from_userstory(project_id, userstory_id):
        return Artifact.activity_objects.filter(
            project=project_id, userstory=userstory_id).count()

    @staticmethod
    def get_total_estimated_time_from_userstory(project_id, userstory_id):
        return Artifact.activity_objects.filter(
            project=project_id, userstory=userstory_id).aggregate(time = Sum('estimated_time'))

    @staticmethod
    def get_total_spent_time_from_userstory(project_id, userstory_id):
        return Artifact.activity_objects.filter(
            project=project_id, userstory=userstory_id).aggregate(time=Sum('spent_time'))

    @staticmethod
    def get_sprints_from_userstory(userstory_id):
        return SprintUserStory.objects.filter(userstory=userstory_id)