import os
from main.components.repository.git import GitImplementation
from main.models import Project
from tracepp import settings


class RepositoryFactory:
    repository = None

    def __init__(self, project: Project):
        if project.repository_type == 'Git':
            self.repository = GitImplementation()
            self.repository.remoteURL = project.repository_url

        if project.id:
            self.repository.dirname = os.path.join(os.path.join(settings.REPOSITORY_DIR), str(project.id))
        else:
            return False

        if project.repository_url:
            self.repository.remoteURL = project.repository_url
        else:
            return False

        if not os.path.isdir(self.repository.dirname):
            os.mkdir(self.repository.dirname)



