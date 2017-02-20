from main.models import Artifact
from main.models import Project, Requeriment
from django.shortcuts import  get_object_or_404

from main.models import Sprint
from main.models import UserStory


class ProjectService:

    @staticmethod
    def get_user_projects(user):
        """
         Super user gets all projects, other users get their projects
        """
        if user.is_superuser:
            return Project.objects.all()
        else:
            return Project.objects.filter(user=user)

    @staticmethod
    def get_project_model():
        return Project

    @staticmethod
    def get_project(project_id):
        return get_object_or_404(Project, pk=project_id)

    @staticmethod
    def get_num_sprints_from_project(project_id):
        return Sprint.objects.filter(project=project_id).count()

    @staticmethod
    def get_num_requeriments_from_project(project_id):
        return Requeriment.objects.filter(project=project_id).count()

    @staticmethod
    def get_num_userstories_from_project(project_id):
        return UserStory.objects.filter(project=project_id).count()

    @staticmethod
    def get_num_artifacts_from_project(project_id):
        return Artifact.objects.filter(
            project=project_id,
            requeriment__isnull=True,
            sprint__isnull=True,
            userstory__isnull=True,
        ).count()

    @staticmethod
    def get_project_requeriments(project_id):
        return Requeriment.objects.filter(project=project_id)


    @staticmethod
    def get_userstories(project_id):
        return UserStory.objects.filter(project=project_id).order_by('code')

    @staticmethod
    def get_artifacts(project_id):
        return Artifact.objects.filter(project_id=project_id,
                                       requeriment__isnull=True,
                                       sprint__isnull=True,
                                       userstory__isnull=True,
                                      )

