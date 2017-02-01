from main.models import Artifact
from main.services.sprint import SprintService
from main.services.userstory import UserStoryService


class ArtifactService:

    @staticmethod
    def get_model():
        return Artifact

    @staticmethod
    def get_artifacts(project_id, userstory_id=False, sprint_id=False, requeriment_id=False):
        if userstory_id:
            userstory = UserStoryService.get_userstory(project_id, userstory_id)
            Artifact.objects.filter(project_id=project_id,
                                    sprint__isnull=True,
                                    userstory=userstory)
        elif sprint_id:
            sprint = SprintService.get_sprint(project_id, sprint_id)

