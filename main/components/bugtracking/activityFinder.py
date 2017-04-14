
class activityFinder:
    artifactList = list()
    artifactTypes = False
    issues = False

    def __init__(self, bugtracking, artifactTypes, sp_variable_planned, sp_variable_realized,  bv_variable_planned, bv_variable_realized):
        self.artifactList = list()
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

                    sp_planned = 0
                    sp_realized = 0
                    bv_planned = 0
                    bv_realized = 0

                    if sp_variable_planned  and sp_variable_realized and bv_variable_planned and bv_variable_realized:
                        for custom_field in issue.custom_fields:
                            try:
                                if custom_field['name'] == sp_variable_planned and custom_field['value'] != '':
                                    sp_planned = custom_field['value']
                                elif custom_field['name'] == sp_variable_realized and custom_field['value'] != '':
                                    sp_realized = custom_field['value']
                                elif custom_field['name'] == bv_variable_planned and custom_field['value'] != '':
                                    bv_planned = custom_field['value']
                                elif custom_field['name'] == bv_variable_realized and custom_field['value'] != '':
                                    bv_realized = custom_field['value']
                            except:
                                sp_planned = 0
                                sp_realized = 0
                                bv_planned = 0
                                bv_realized = 0

                    self.artifactList.append(
                            {'reference': issue.id,
                             'estimated_time': estimated_time,
                             'spent_time': spent_time,
                             'artifactType': artifactType,
                             'estimated_storypoints': sp_planned,
                             'realized_storypoints': sp_realized,
                             'estimated_businnesvalue': bv_planned,
                             'realized_businnesvalue': bv_realized,
                             'code': str(issue)[str(issue).find(trace_code):][len(artifactType.trace_code):]
                             }
                        )
