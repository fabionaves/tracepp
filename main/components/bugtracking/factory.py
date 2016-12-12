from main.models import Project


class BugTrackingFactory:

    def getConnection(project: Project):
        if project.tracking_tool_type == 'Redmine':
            from main.components.bugtracking.redmine import Connection
            return Connection(project.tracking_tool_url,
                              project.tracking_tool_user,
                              project.tracking_tool_password,
                              project.tracking_tool_project_id)







