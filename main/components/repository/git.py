import git

from main.components.repository.interface import RepositoryInterface


class GitImplementation(RepositoryInterface):
    """
    Git implementation of Repository Interface, use RepositoryFactory to instance this
    #class:US010

    """
    def pull(self):
        try:
            repo = git.Repo.init(self.dirname)
            origin = repo.create_remote('origin', self.remoteURL)
        except git.GitCommandError:
            origin = repo.remotes.origin
        finally:
            try:
                origin.fetch()
            except:
                repo = git.Repo.init(self.dirname)
                origin = repo.create_remote('origin', 'localhost')
                ssh_cmd = 'ssh -i id_dsa.pub'
                with repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
                    origin.fetch()
            origin.pull(origin.refs[0].remote_head)

"""def pull(project: Project):
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
"""