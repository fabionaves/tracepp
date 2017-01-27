from main.models import Project
from django.shortcuts import  get_object_or_404


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
