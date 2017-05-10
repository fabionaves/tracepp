from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from main.components.bugtracking.activityFinder import activityFinder
from main.components.bugtracking.factory import BugTrackingFactory
from main.models import Artifact
from main.models import ArtifactType
from main.models import Requeriment
from main.models import Sprint
from main.models import SprintUserStory
from main.models import UserStory
from main.services.sprint import SprintService
from main.services.userstory import UserStoryService


class ArtifactService:

    @staticmethod
    def get_model():
        return Artifact

    @staticmethod
    def get_artifacts(project_id, userstory_id=False, sprint_id=False, requeriment_id=False):
        if userstory_id:
            userstory = UserStoryService.get_userstory(project_id, userstory_id)
            Artifact.objects.filter(project_id=project_id,
                                    sprint__isnull=True,
                                    userstory=userstory)
        elif sprint_id:
            sprint = SprintService.get_sprint(project_id, sprint_id)

    @staticmethod
    def get_artifact(project_id, pk):
        return get_object_or_404(
                    Artifact.objects.all(),
                    project=project_id,
                    id=pk
                )

    @staticmethod
    def get_bugtrack_activities(project):
        bugtracking = BugTrackingFactory.getConnection(project=project)
        artifactsTypes = ArtifactType.objects.filter(project=project, type=2, )

        tracking_sp_planned_variable = project.tracking_sp_planned_variable
        tracking_sp_realized_variable = project.tracking_sp_realized_variable
        tracking_bv_planned_variable = project.tracking_bv_planned_variable
        tracking_bv_realized_variable = project.tracking_bv_realized_variable
        if tracking_sp_planned_variable == '':
            tracking_sp_planned_variable = False
        if tracking_sp_realized_variable == '':
            tracking_sp_realized_variable = False
        if tracking_bv_planned_variable == '':
            tracking_bv_planned_variable = False
        if tracking_bv_realized_variable == '':
            tracking_bv_realized_variable = False

        acfinder = activityFinder(bugtracking, artifactsTypes,
                                  tracking_sp_planned_variable, tracking_sp_realized_variable,
                                  tracking_bv_planned_variable, tracking_bv_realized_variable,
                                  )

        references = []
        log = []
        for artifact in acfinder.artifactList:
            references.append(artifact['reference'])
            try:
                filterArtifact = Artifact.objects.get(project=project, reference=artifact['reference'])
            except Artifact.DoesNotExist:
                filterArtifact = None

            try:
                if not filterArtifact is None:
                    # upldate a exist artifact
                    if artifact['artifactType'].level == 0:
                        filterArtifact.type = artifact['artifactType']
                        filterArtifact.save()
                    elif artifact['artifactType'].level == 1:
                        requeriment = Requeriment.objects.filter(project=project, code=artifact['code']).get()
                        filterArtifact.type = artifact['artifactType']
                        filterArtifact.requeriment = requeriment
                        filterArtifact.save()
                    elif artifact['artifactType'].level == 2:
                        sprint = Sprint.objects.filter(project=project, code=artifact['code']).get()
                        filterArtifact.type = artifact['artifactType']
                        filterArtifact.sprint = sprint
                        filterArtifact.save()
                    elif artifact['artifactType'].level == 3:
                        userstory = UserStory.objects.filter(project=project, code=artifact['code']).get()
                        filterArtifact.estimated_time = artifact['estimated_time']
                        filterArtifact.spent_time = artifact['spent_time']
                        filterArtifact.type = artifact['artifactType']

                        filterArtifact.estimated_storypoints = artifact['estimated_storypoints']
                        filterArtifact.realized_storypoints = artifact['realized_storypoints']
                        filterArtifact.estimated_businnesvalue = artifact['estimated_businnesvalue']
                        filterArtifact.realized_businnesvalue = artifact['realized_businnesvalue']
                        filterArtifact.userstory = userstory
                        filterArtifact.save()
                        log.append(_('Updated Artifact:')+artifact['code']+' '+_('Reference: ')+str(artifact['reference']))
                else:
                    # create a new artifact
                    if artifact['artifactType'].level == 0:
                        Artifact.objects.create(project=project,
                                                reference=artifact['reference'],
                                                type=artifact['artifactType'])
                    elif artifact['artifactType'].level == 1:
                        requeriment = Requeriment.objects.filter(project=project, code=artifact['code']).get()
                        Artifact.objects.create(project=project,
                                                reference=artifact['reference'],
                                                type=artifact['artifactType'],
                                                requeriment=requeriment)
                    elif artifact['artifactType'].level == 2:
                        sprint = Sprint.objects.filter(project=project, code=artifact['code']).get()
                        Artifact.objects.create(project=project,
                                                reference=artifact['reference'],
                                                type=artifact['artifactType'],
                                                sprint=sprint)
                    elif artifact['artifactType'].level == 3:
                        userstory = UserStory.objects.filter(project=project, code=artifact['code']).get()
                        Artifact.objects.create(project=project,
                                                reference=artifact['reference'],
                                                estimated_time=artifact['estimated_time'],
                                                spent_time=artifact['spent_time'],
                                                estimated_storypoints=artifact['estimated_storypoints'],
                                                realized_storypoints=artifact['realized_storypoints'],
                                                estimated_businnesvalue=artifact['estimated_businnesvalue'],
                                                realized_businnesvalue=artifact['realized_businnesvalue'],
                                                type=artifact['artifactType'],
                                                userstory=userstory)
                    log.append(_('Created Artifact: ')+artifact['code']+' '+_('Reference: ')+str(artifact['reference']))
            except:
                log.append("====>ERRO: "+ str(artifact['reference'])+' '+artifact['code'])
        Artifact.objects.exclude(reference__in=references).filter(
            type__type=2).delete()  # delete the artifacts not detected in bugtracking
        return log

    @staticmethod
    def get_sprints_from_bugtracking(project):
        bugtracking = BugTrackingFactory.getConnection(project=project)
        bugtrackingSprints = bugtracking.getSprints()
        log = []
        for bugtrackingsprint in bugtrackingSprints:
            try:
                sprint = Sprint.objects.get(project=project, reference=bugtrackingsprint.id)
            except Sprint.DoesNotExist:
                sprint = None

            if  sprint is None:
                #create sprint data
                if bugtrackingsprint.status=='Closed':
                    status = 2
                else:
                    status = 1

                Sprint.objects.create(
                    title=bugtrackingsprint.name,
                    reference=bugtrackingsprint.id,
                    status=status,
                    project=project,
                )
                log.append(_('Created Sprint: ') + bugtrackingsprint.name)
            else:
                #update sprint
                # create sprint data
                if bugtrackingsprint.status == 'Closed':
                    status = 2
                else:
                    status = 1
                sprint.title = bugtrackingsprint.name
                sprint.status = status
                sprint.save()
                log.append(_('Updated Sprint: ')+bugtrackingsprint.name)

        return log

    @staticmethod
    def get_userstories_from_bugtracking(project):
        bugtracking = BugTrackingFactory.getConnection(project=project)
        bugtrackingUserStories = bugtracking.getUserStories(project.issueTypesAsUserStory)
        log = []

        for bugtrackuserstory in bugtrackingUserStories:
            try:
                userstory = UserStory.objects.get(project=project, reference=bugtrackuserstory.id)
            except UserStory.DoesNotExist:
                userstory = None

            if userstory is None:
                numUserStories = UserStory.objects.filter(project=project).count()
                UserStory.objects.create(
                    code = 'US'+str(numUserStories+1),
                    reference = bugtrackuserstory.id,
                    title = bugtrackuserstory.subject,
                    description = bugtrackuserstory.description,
                    project=project,
                )
                log.append(_('Created UserStory: ') + 'US'+str(numUserStories+1))


                #ja adiciona como artefato do tipo atividade
                ArtifactService._add_artifact(project, bugtrackuserstory)
            else:
                #update user story
                userstory.title =  bugtrackuserstory.subject
                userstory.description = bugtrackuserstory.description
                userstory.save()
                log.append(_('Updated UserStory: ') + 'US' + userstory.code)

                # ja adiciona ou altera como artefato do tipo atividade
                ArtifactService._add_artifact(project, bugtrackuserstory)

        return log

    @staticmethod
    def sprint_to_userstory(project):
        bugtracking = BugTrackingFactory.getConnection(project=project)
        userStories = UserStory.objects.filter(project=project)
        log = []
        for us in userStories:
            spuss = None
            try:
                issue = bugtracking.getIssue(us.reference)
            except:
                issue = None

            try:
                version = issue.fixed_version
            except:
                version = None

            try:
                issuestatus = issue.status.id
            except:
                issuestatus = None

            if issuestatus is not None and issuestatus == project.issueStatusClosed:
                issuestatus = 1
            else:
                issuestatus = 0



            if issue is not None:
                spuss = SprintUserStory.objects.filter(userstory=us)

                if spuss.count()>0:
                    isNew = False
                    for spus in spuss:
                        if spus.sprint.reference != version.id:
                            isNew = True
                        else:
                           isNew = False
                    if isNew:
                        SprintUserStory.objects.create(
                            sprint=Sprint.objects.get(reference=version),
                            userstory=us,
                            status=issuestatus,
                        )
                        log.append(_('Userstory added to Sprint'))
                    else:
                        sprintUs = SprintUserStory.objects.get(sprint__reference=version, userstory=us)
                        sprintUs.status = issuestatus
                        sprintUs.save()
                        log.append(_('Userstory updated to Sprint'))
                else:
                    if version is not None:
                        SprintUserStory.objects.create(
                            sprint=Sprint.objects.get(reference=version),
                            userstory=us,
                            status=issuestatus,
                        )
                        log.append(_('Userstory added to Sprint'))
        return log




    @staticmethod
    def _add_artifact(project, issue):
        try:
            artifact = Artifact.objects.get(project=project, reference=issue.id)
        except Artifact.DoesNotExist:
            artifact = None

        sp_and_bv = ArtifactService._get_sp_and_bv(project, issue)
        # coloca o artefato no primeiro tipo de artefato de estoria de usuario do projeto
        artifacttype = ArtifactType.objects.filter(project=project, level=3, type=2)[:1].get()
        time = ArtifactService._get_time(project, issue)

        if artifact is None:
            Artifact.objects.create(project=project,
                                    reference=issue.id,
                                    estimated_time=time['estimated_time'],
                                    spent_time=time['spent_time'],
                                    estimated_storypoints=sp_and_bv['sp_planned'],
                                    realized_storypoints=sp_and_bv['sp_realized'],
                                    estimated_businnesvalue=sp_and_bv['bv_planned'],
                                    realized_businnesvalue=sp_and_bv['bv_realized'],
                                    userstory=UserStory.objects.get(reference=issue.id),
                                    type=artifacttype,
                                    )
        else:
            artifact.estimated_time=time['estimated_time']
            artifact.spent_time=time['spent_time']
            artifact.estimated_storypoints=sp_and_bv['sp_planned']
            artifact.realized_storypoints=sp_and_bv['sp_realized']
            artifact.estimated_businnesvalue=sp_and_bv['bv_planned']
            artifact.realized_businnesvalue=sp_and_bv['bv_realized']
            artifact.save()

    @staticmethod
    def _get_time(project, issue):
        spent_time = 0
        for time_entry in issue.time_entries:
            spent_time += time_entry.hours
        try:
            estimated_time = issue.estimated_hours
        except:
            try:
                bugtracking = BugTrackingFactory.getConnection(project=project)
                iss = bugtracking.getIssue(issue.id)
                estimated_time = iss.total_estimated_hours  # bug in python-redmine dont take estimated_hours in getIssues
            except:
                estimated_time = 0
        return {
            'spent_time' : spent_time,
            'estimated_time' : estimated_time,
        }

    @staticmethod
    def _get_sp_and_bv(project, issue):
        sp_variable_planned = project.tracking_sp_planned_variable
        sp_variable_realized = project.tracking_sp_realized_variable
        bv_variable_planned = project.tracking_bv_planned_variable
        bv_variable_realized = project.tracking_bv_realized_variable
        if sp_variable_planned == '':
            sp_variable_planned = False
        if sp_variable_realized == '':
            sp_variable_realized = False
        if bv_variable_planned == '':
            bv_variable_planned = False
        if bv_variable_realized == '':
            bv_variable_realized = False

        bv_realized = 0
        bv_planned = 0
        sp_realized = 0
        sp_planned = 0

        try:
            if sp_variable_planned:
                for custom_field in issue.custom_fields:
                    try:
                        if custom_field['name'] == sp_variable_planned and custom_field['value'] != '':
                            sp_planned = custom_field['value']
                    except:
                        sp_planned = 0

            if sp_variable_realized:
                for custom_field in issue.custom_fields:
                    try:
                        if custom_field['name'] == sp_variable_realized and custom_field['value'] != '':
                            sp_realized = custom_field['value']
                    except:
                        sp_realized = 0

            if bv_variable_planned:
                for custom_field in issue.custom_fields:
                    try:
                        if custom_field['name'] == bv_variable_planned and custom_field['value'] != '':
                            bv_planned = custom_field['value']
                    except:
                        bv_planned = 0

            if bv_variable_realized:
                for custom_field in issue.custom_fields:
                    try:
                        if custom_field['name'] == bv_variable_realized and custom_field['value'] != '':
                            bv_realized = custom_field['value']
                    except:
                        bv_realized = 0
        except:
            bv_realized = 0
            bv_planned = 0
            sp_realized = 0
            sp_planned = 0

        return {
            'bv_realized' : bv_realized,
            'bv_planned': bv_planned,
            'sp_realized': sp_realized,
            'sp_planned': sp_planned,
        }

    @staticmethod
    def total_realized_storyPoints(project):
        return Artifact.objects.values('project_id').annotate(
            realized=Sum('realized_storypoints'),
        ).filter(project=project)[:1].get()


