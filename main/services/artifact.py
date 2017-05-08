from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from main.components.bugtracking.activityFinder import activityFinder
from main.components.bugtracking.factory import BugTrackingFactory
from main.models import Artifact
from main.models import ArtifactType
from main.models import Requeriment
from main.models import Sprint
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

        for bubtrackuserstory in bugtrackingUserStories:
            try:
                userstory = UserStory.objects.get(project=project, reference=bubtrackuserstory.id)
            except UserStory.DoesNotExist:
                userstory = None

            if userstory is None:
                #create user story
                pass
            else:
                #update user story
                pass
        log = []

        return log


