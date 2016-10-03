import  os

from pathlib import Path

from django.db import transaction

from main.models import Project, ArtifactType, Artifact
from tracepp import settings


class SourceFinder:
    dir = False
    files = False
    project = False
    artifactList = list()
    artifactTypes = False
    project_local_repository = ""

    def __init__(self, project: Project, artifactTypes: ArtifactType):
        self.project = project
        self.project_local_repository = '{0}{1}'.format(settings.REPOSITORY_DIR, project.id)
        self.artifactTypes = artifactTypes
        self.__navigate__()
        self.__compare__()

    def __navigate__(self):
        p = Path(self.project_local_repository)
        self.dir = [x for x in p.iterdir() if x.is_dir()]
        self.files = [x for x in p.iterdir() if x.is_file()]
        for file in self.dir:
            if file.name != '.git':
                p = Path(file)
                self.dir += [x for x in p.iterdir() if x.is_dir()]
                self.files += [x for x in p.iterdir() if x.is_file()]

    def __compare__(self):
        self.artifactList = list()
        for file in self.files:
            with open(str(file), 'rb') as f:  # open in binary mode
                linecount = 0
                for line in f:
                    linecount += 1
                    for cp in ('cp1252', 'cp850'):
                        try:
                            s = line.decode(cp)
                        except UnicodeDecodeError:
                            pass
                        else:
                            for artifactType in self.artifactTypes:
                                if s[:-2] == artifactType.trace_code:
                                    self.artifactList.append({'source': str(file), 'line': linecount, 'artifactType': artifactType})
                                    break
                            break
