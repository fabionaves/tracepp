from main.components.bugtracking.interface import *
from redmine import Redmine


class Connection(ConnectionInterface, Redmine):

    def __init__(self, url, username, password, identifier):
        self.connection = Redmine(url, username=username, password=password)
        self.project_id = identifier

    def getIssues(self):
        return self.connection.issue.filter(project_id=self.project_id, status_id='*')

    def getIssue(self, issue_id):
        return self.connection.issue.get(issue_id)

    def getSprints(self):
        return self.connection.version.filter(project_id=self.project_id)

    def getUserStories(self, tracker_id):
        return self.connection.issue.filter(project_id=self.project_id, status_id='*',tracker_id=tracker_id, sort='id:asc')



