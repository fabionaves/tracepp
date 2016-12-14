
class activityFinder:
    artifactList = list()
    artifactTypes = False
    issues = False

    def __init__(self, bugtracking, artifactTypes):

        for issue in bugtracking.getIssues():
            for artifactType in artifactTypes:
                trace_code = artifactType.trace_code
                if str(issue).find(trace_code) > -1:
                    spent_time = 0
                    for time_entry in issue.time_entries:
                        spent_time += time_entry.hours
                    try:
                        estimated_time = issue.estimated_hours
                    except:
                        estimated_time = 0

                    self.artifactList.append(
                            {'reference': issue.id,
                             'estimated_time': estimated_time,
                             'spent_time': spent_time,
                             'artifactType': artifactType,
                             'code': str(issue)[str(issue).find(trace_code):][len(artifactType.trace_code)+1:]
                             }
                        )
