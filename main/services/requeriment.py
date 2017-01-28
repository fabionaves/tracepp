from django.db.models import Count
from django.shortcuts import get_object_or_404

from main.models import Artifact
from main.models import Requeriment
from main.models import UserStory


class RequerimentService:

    @staticmethod
    def get_requeriment_model():
        return Requeriment

    @staticmethod
    def get_requeriment(project_id, requeriment_id):
        return get_object_or_404(
            Requeriment.objects.all(),
            project=project_id,
            id=requeriment_id
        )

    @staticmethod
    def get_num_userstories_from_requeriment(requeriment_id):
        return UserStory.objects.filter(requeriment=requeriment_id).aggregate(total=Count('*'))

    @staticmethod
    def get_num_artifacts_from_requeriment(project_id, requeriment_id):
        return Artifact.objects.filter(
            project=project_id, requeriment=requeriment_id).count()

    @staticmethod
    def get_dependent_requeriments(requeriment):
        return Requeriment.objects.filter(depends_on=requeriment)


