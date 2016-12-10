class ConnectionInterface:
    connection = False
    project = False

    def connect(self, url, username, password):
        '''
        Interface to Implement the connection to the bug tracking REST api"
        '''
        raise NotImplementedError("Connect to Bug Tracking must me implemented")


class ProjectInterface:
    connection = False
    id = False
    identifier = False
    activities = False

    def __init__(self, connection, identifier):
        raise NotImplementedError("Activities of Bug Tracking must me implemented")

    def getActivities(self):
        '''
        Interface to implement the get activities from project
        :return:
        '''
        raise NotImplementedError("Activities of Bug Tracking must me implemented")


class ActivityInterface:
    title = ""
    description = ""
    attachments = False
    estimated_time = 0
    spent_time = 0