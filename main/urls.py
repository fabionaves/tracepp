from django.conf.urls import url, include

from main.views import artifacttype_views
from main.views import home_views, project_views, sprint_views, requeriment_views, userstory_views, artifact_views
from django.contrib.auth import views as loginviews
from django.contrib.auth.decorators import login_required

artifact_urls = [
    url(r'^(?P<pk>[0-9]+)/update-activity/',       login_required(artifact_views.ActivityUpdateFormView.as_view()), name='artifact-update-activity'),
    url(r'^(?P<projeto>[0-9]+)/tracecode/',        artifact_views.ArtifactTraceCodeView.as_view(), name='artifact-tracecode'),
    url(r'^(?P<projeto>[0-9]+)/tracebugtracking/', artifact_views.ArtifactTraceBugTrackingView.as_view(), name='artifact-bugtracking'),
    url(r'^(?P<pk>[0-9]+)/download/',              login_required(artifact_views.ArtifactDownloadView), name='artifact-download'),
    url(r'^list-activity/',                        login_required(artifact_views.ActivityListView.as_view()), name='artifact-list-activity'),
    url(r'^add-document/',                         login_required(artifact_views.ArtifactDocumentForm.as_view()), name='artifact-add-document'),
    url(r'^add-activity/',                         login_required(artifact_views.ActivityAddFormView.as_view()), name='artifact-add-document'),
    url(r'^(?P<artifact>[0-9]+)/codeview/',        login_required(artifact_views.ArtifactCodeView.as_view()), name='artifact-codeview'),
    url(r'^(?P<artifact>[0-9]+)/activity/',        login_required(artifact_views.ArtifactActivityView.as_view()), name='artifact-activity'),
    url(r'^(?P<pk>[0-9]+)/delete/',                login_required(artifact_views.ArtifactDeleteView.as_view()), name='artifact-delete'),
    url(r'^tracecode/',                            login_required(artifact_views.ArtifactTraceCodeView.as_view()), name='artifact-tracecode'),
    url(r'^tracecode-confirm/',                    login_required(artifact_views.ArtifactCodeConfirm.as_view()), name='artifact-code-confirm'),
    url(r'^tracebugtracking/',                     login_required(artifact_views.ArtifactTraceBugTrackingView.as_view()), name='artifact-bugtracking'),
    url(r'^tracebugtracking-confirm/',             login_required(artifact_views.ArtifactTraceBugTrackingConfirm.as_view()), name='artifact-bugtracking-confirm'),
    url(r'^$',                                    login_required(artifact_views.ArtifactView.as_view()), name='artifact'),
]

userstory_urls = [
    url(r'^add/',                                   login_required(userstory_views.UserStoryAddFormView.as_view()), name='userstory-add'),
    url(r'^(?P<pk>[0-9]+)/update/',                 login_required(userstory_views.UserStoryUpdateFormView.as_view()),name='userstory-update'),
    url(r'^(?P<userstory>[0-9]+)/detail/artifact/', include(artifact_urls), {'location': 'artifact'}),
    url(r'^(?P<pk>[0-9]+)/detail/graph/',           login_required(userstory_views.UserStoryGraphDetailView.as_view()),name='userstory-graph'),
    url(r'^(?P<pk>[0-9]+)/detail/',                 login_required(userstory_views.UserStoryDetailView.as_view()),name='userstory-detail'),
    url(r'^(?P<pk>[0-9]+)/delete/',                 login_required(userstory_views.UserStoryDeleteView.as_view()),name='userstory-delete'),
    url(r'^$',                                     login_required(userstory_views.UserStoryListView.as_view()), name='userstory'),
]

requeriment_urls = [
    url(r'^(?P<requeriment_id>[0-9]+)/userstory/', include(userstory_urls), {'location': 'userstory'}),
    url(r'^add/',                    login_required(requeriment_views.RequerimentAddFormView.as_view()), name='requeriment-add'),
    url(r'^history/',                login_required(requeriment_views.RequerimentHistoryView.as_view()),name='requeriment-history'),
    url(r'^graph/',                  login_required(requeriment_views.RequerimentGraphView.as_view()),name='requeriment-graph-detail'),
    url(r'^(?P<pk>[0-9]+)/graph/',   login_required(requeriment_views.RequerimentGraphDetailView.as_view()),name='requeriment-graph'),
    url(r'^(?P<pk>[0-9]+)/history/', login_required(requeriment_views.RequerimentHistoryView.as_view()),name='requeriment-history'),
    url(r'^(?P<pk>[0-9]+)/update/',  login_required(requeriment_views.RequerimentUpdateFormView.as_view()),name='requeriment-update'),
    url(r'^(?P<pk>[0-9]+)/delete/',  login_required(requeriment_views.RequerimentDeleteView.as_view()),name='requeriment-delete'),
    url(r'^(?P<requeriment_id>[0-9]+)/artifact/', include(artifact_urls), {'location': 'artifact'}),
    url(r'^(?P<pk>[0-9]+)/',         login_required(requeriment_views.RequerimentDetailView.as_view()),name='requeriment-details'),
    url(r'^$',                      login_required(requeriment_views.RequerimentListView.as_view()), name='requeriment'),

]

sprint_urls = [
    url(r'^(?P<sprint_id>[0-9]+)/requeriment/', include(requeriment_urls), {'location': 'requeriment'}),
    url(r'^(?P<sprint_id>[0-9]+)/userstory/', include(userstory_urls), {'location': 'userstory'}),
    url(r'^add/',                            login_required(sprint_views.SprintAddFormView.as_view()), name='sprint-add'),
    url(r'^(?P<pk>[0-9]+)/update/',          login_required(sprint_views.SprintUpdateFormView.as_view()),name='sprint-update'),
    url(r'^(?P<pk>[0-9]+)/delete/',          login_required(sprint_views.SprintDeleteView.as_view()),name='sprint-delete'),
    url(r'^history/',                        login_required(sprint_views.SprintHistoryView.as_view()), name='sprint-history'),
    url(r'^(?P<sprint_id>[0-9]+)/history/',  login_required(sprint_views.SprintHistoryView.as_view()), name='sprint-history'),
    url(r'^(?P<sprint_id>[0-9]+)/artifact/', include(artifact_urls), {'location': 'artifact'}),
    url(r'^(?P<sprint_id>[0-9]+)/',          login_required(sprint_views.SprintDetailView.as_view()), name='sprint-details'),
    url(r'^$',                              login_required(sprint_views.SprintListView.as_view()), name='sprint'),
]


urlpatterns = [
    url(r'^accounts/login/',                     loginviews.login,{'template_name': 'login/form.html'}, name='login'),
    url(r'^accounts/logout/',                    loginviews.logout,{'template_name': 'login/logout.html'}, name='logout'),
    url(r'^$',                                   login_required(home_views.HomeView.as_view()), name='home'),
    url(r'^project/list/add/',                   login_required(project_views.ProjectAddFormView.as_view()), name='project-add'),
    url(r'^project/list/(?P<pk>[0-9]+)/update/', login_required(project_views.ProjectUpdateFormView.as_view()), name='project-update'),
    url(r'^project/list/(?P<pk>[0-9]+)/delete/', login_required(project_views.ProjectDeleteView.as_view()), name='project-delete'),
    url(r'^project/list/',                       login_required(project_views.ProjectListView.as_view()), name='project-list'),
    url(r'^project/(?P<project_id>[0-9]+)/',     login_required(project_views.ProjectView.as_view()), name='project'),
    url(r'^project/',                            login_required(project_views.ProjectView.as_view()), name='project'),


    url(r'^artifact/',    include(artifact_urls), {'location': 'userstory'}),
    url(r'^userstory/',   include(userstory_urls), {'location': 'artifact'}),
    url(r'^requeriment/', include(requeriment_urls), {'location': 'requeriment'}),
    url(r'^sprint/',      include(sprint_urls), {'location': 'sprint'}),

    url(r'^artifacttype/add/',                       login_required(artifacttype_views.ArtifactTypeAddFormView.as_view()), name='artifacttype-add'),
    url(r'^artifacttype/(?P<pk>[0-9]+)/update/',     login_required(artifacttype_views.ArtifactTypeUpdateFormView.as_view()), name='artifacttype-update'),
    url(r'^artifacttype/(?P<pk>[0-9]+)/delete/',     login_required(artifacttype_views.ArtifactTypeDeleteView.as_view()), name='artifacttype-delete'),
    url(r'^artifacttype/',                           login_required(artifacttype_views.ArtifactTypeView.as_view()), name='artifacttype'),
]