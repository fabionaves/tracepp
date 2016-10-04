import git, os, shutil
from django.conf import settings

from main.models import Project


def pull(project: Project):
    if project.id:
        DIR_NAME = os.path.join(settings.REPOSITORY_DIR, str(project.id))
    else:
        return False

    if project.repository_url:
        REMOTE_URL = project.repository_url
    else:
        return False

    if not os.path.isdir(DIR_NAME):
        os.mkdir(DIR_NAME)

    try:
        repo = git.Repo.init(DIR_NAME)
        origin = repo.create_remote('origin', REMOTE_URL)
    except git.GitCommandError:
        origin = repo.remotes.origin
    finally:
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)