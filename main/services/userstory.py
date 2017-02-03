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
    def get_task_effor_per_userstory(project_id):
        resultsets =  Artifact.objects.values('userstory','userstory__code').annotate(
            estimated_time=Sum('estimated_time'),
            realizated_time=Sum('spent_time'),
        ).filter(project=project_id, userstory__code__isnull=False).order_by('userstory__code')
        retorno = []
        for resultset in resultsets:
            if resultset['estimated_time'] and resultset['estimated_time'] != 0:
                retorno.append({
                    'userstory__code': resultset['userstory__code'],
                    'estimated_time': resultset['estimated_time'],
                    'spent_time': resultset['realizated_time'],
                    'percentual': 100*((resultset['realizated_time']-resultset['estimated_time'])/resultset['estimated_time'])
                })
            else:
                retorno.append({
                    'userstory__code': resultset['userstory__code'],
                    'estimated_time': resultset['estimated_time'],
                    'spent_time': resultset['realizated_time'],
                    'percentual': 0
                })
        return retorno



    @staticmethod
    def get_sprints_from_userstory(userstory_id):
        return SprintUserStory.objects.filter(userstory=userstory_id)

    @staticmethod
    def get_artifacts(project_id, userstory_id):
        return Artifact.objects.filter(project_id=project_id, sprint__isnull=True, userstory=userstory_id)