import  os

from main.models import Project
from tracepp import settings


class SourceFinder:
    caminhos = False
    arquivos = False
    project = False
    project_local_repository = False

    def __init__(self,project: Project,):
        self.project = project
        self.project_local_repository = settings.REPOSITORY_DIR, str(project.id)
        self.caminhos = [os.path.join(self.project_local_repositoryself.project_local_repository, nome)





