from main.models import Sprint, SprintUserStory, Requeriment, Artifact
from django.shortcuts import  get_object_or_404
from django.db.models import Count, Sum

from main.models import UserStory


class SprintService:

    @staticmethod
    def get_sprint_model():
        return Sprint

    @staticmethod
    def get_sprint(project_id, sprint_id):
        return get_object_or_404(
                                    Sprint.objects.all(),
                                    project=project_id,
                                    id=sprint_id
                                )

    @staticmethod
    def get_userstories_from_sprint(project_id, sprint_id):
        return UserStory.objects.filter(project=project_id, sprintuserstory__sprint =sprint_id)

    @staticmethod
    def get_requeriments_from_sprint(sprint_user_story_list):
        return Requeriment.objects.filter(userstory__in=sprint_user_story_list).annotate(total=Count('*'))

    @staticmethod
    def get_num_requeriments_from_sprint(sprint_user_story_list):
        return Requeriment.objects.filter(userstory__in=sprint_user_story_list).annotate(total=Count('*')).count()

    @staticmethod
    def get_num_userstories_from_sprint(sprint_id):
        return SprintUserStory.objects.filter(sprint_id=sprint_id).count()

    @staticmethod
    def get_num_artifacts_from_sprint(project_id, sprint_id):
        return Artifact.objects.filter(
            project=project_id, sprint=sprint_id).count()

    @staticmethod
    def get_artifacts(project_id, sprint_id):
        return Artifact.objects.filter(project_id=project_id, sprint=sprint_id, userstory__isnull=True)

    @staticmethod
    def task_effort_per_sprint(sprint_id):
        return SprintUserStory.objects.values('sprint_id').annotate(
            estimated_time=Sum('userstory__artifact__estimated_time'),
            realizated_time=Sum('userstory__artifact__spent_time'),
            percentual=100 * (Sum('userstory__artifact__spent_time') - Sum('userstory__artifact__estimated_time')) / Sum('userstory__artifact__estimated_time')
        ).filter(sprint=sprint_id)

    @staticmethod
    def storypoint_per_sprint(sprint_id):
        return SprintUserStory.objects.values('sprint_id').annotate(
            estimated = Sum('userstory__artifact__estimated_storypoints'),
            realized = Sum('userstory__artifact__realized_storypoints'),
            percentual=100 * (
                                Sum('userstory__artifact__realized_storypoints') - Sum('userstory__artifact__estimated_storypoints')) / Sum(
                                    'userstory__artifact__estimated_storypoints')
                            ).filter(sprint=sprint_id)
