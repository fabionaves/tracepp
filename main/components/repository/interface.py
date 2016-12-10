class RepositoryInterface:
    dirname = None
    remoteURL = None

    def pull(self):
        raise NotImplementedError
