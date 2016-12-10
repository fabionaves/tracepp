from main.components.bugtracking.interface import *
from redmine import Redmine


class Connection(ConnectionInterface, Redmine):

    def connect(self, url, username, password):
        self.connection = Redmine(url, username, password)

    def get(self, identifier):
        self.project = self.connection.project.get(identifier)


class Project(ProjectInterface):

    def __init__(self, connection, identifier):
        self.connection = connection
        return self.connection.project.get(identifier)

    def getActivities(self):
        return self.issues
