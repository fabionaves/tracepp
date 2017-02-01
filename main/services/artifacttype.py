from main.models import ArtifactType

class ArtifactTypeService:

    @staticmethod
    def get_artifacttype_model():
        return ArtifactType

    @staticmethod
    def get_artifactstype(project_id, level, type):
        return ArtifactType.objects.filter(project_id=project_id, level=level, type=type)