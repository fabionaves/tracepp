

class ConnectionInterface:
    connection = False
    project_id = None

    def __init__(self, url, username, password, project_id):
        '''
        Interface to Implement the connection to the bug tracking REST api"
        '''
        raise NotImplementedError("Connect to Bug Tracking must me implemented")

    def getIssues(self):
        raise NotImplementedError("Connect to Bug Tracking must me implemented")

    def getIssue(self, issue_id):
        raise NotImplementedError("Connect to Bug Tracking must me implemented")

