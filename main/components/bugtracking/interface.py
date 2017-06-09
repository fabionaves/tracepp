

class ConnectionInterface:
    connection = False
    project_id = None

    def __init__(self, url, username, password, project_id):
        '''
        Interface to Implement the connection to the bug tracking REST api"
        '''
        raise NotImplementedError("Connect to Bug Tracking must me implemented")

    def getIssues(self):
        raise NotImplementedError("getIssues to Bug Tracking must me implemented")

    def getIssue(self, issue_id):
        raise NotImplementedError("getIssue to Bug Tracking must me implemented")

    def getSprints(self):
        raise NotImplementedError("getSprints to Bug Tracking must me implemented")

    def getUserStories(self):
        raise NotImplementedError("getUserStories to Bug Tracking must me implemented")

    def addIssueFromUserStory(self, project_id, subject, tracker_id, description, fixed_version_id, status_id=1, priority_id=2):
        raise NotImplementedError("addIssueFromUserStory to Bug Tracking must me implemented")