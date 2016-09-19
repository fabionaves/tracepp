from django.conf.urls import url

from main.views import artifacttype_views
from main.views import home_views, project_views, sprint_views, requeriment_views, userstory_views
from django.contrib.auth import views as loginviews
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^accounts/login/', loginviews.login,{'template_name': 'login/form.html'}, name='login'),
    url(r'^$',                                   login_required(home_views.HomeView.as_view()), name='home'),
    url(r'^project/list/add/',                   login_required(project_views.ProjectAddFormView.as_view()), name='project-add'),
    url(r'^project/list/(?P<pk>[0-9]+)/update/', login_required(project_views.ProjectUpdateFormView.as_view()), name='project-update'),
    url(r'^project/list/',                       login_required(project_views.ProjectListView.as_view()), name='project-list'),
    url(r'^project/(?P<project_id>[0-9]+)/',     login_required(project_views.ProjectView.as_view()), name='project'),
    url(r'^project/',                            login_required(project_views.ProjectView.as_view()), name='project'),

    url(r'^userstory/add/',                                                login_required(userstory_views.UserStoryAddFormView.as_view()), name='userstory-add'),
    url(r'^userstory/(?P<pk>[0-9]+)/update/',                              login_required(userstory_views.UserStoryUpdateFormView.as_view()),name='userstory-update'),
    url(r'^userstory/(?P<pk>[0-9]+)/detail/',                              login_required(userstory_views.UserStoryDetailView.as_view()),name='userstory-detail'),
    url(r'^userstory/(?P<pk>[0-9]+)/delete/',                              login_required(userstory_views.UserStoryDeleteView.as_view()),name='userstory-delete'),
    url(r'^userstory/',                                                    login_required(userstory_views.UserStoryListView.as_view()), name='userstory'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/userstory/(?P<pk>[0-9]+)/detail/',login_required(userstory_views.UserStoryDetailView.as_view()),name='userstory-detail'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/userstory/(?P<pk>[0-9]+)/update/', login_required(userstory_views.UserStoryUpdateFormView.as_view()), name='userstory-update'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/userstory/add/',                   login_required(userstory_views.UserStoryAddFormView.as_view()), name='sprint-userstory-add'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/userstory/(?P<pk>[0-9]+)/update/', login_required(userstory_views.UserStoryUpdateFormView.as_view()), name='sprint-userstory-update'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/userstory/(?P<pk>[0-9]+)/delete/', login_required(userstory_views.UserStoryDeleteView.as_view()), name='sprint-userstory-delete'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/userstory/',                       login_required(userstory_views.UserStoryListView.as_view()), name='sprint-userstory'),
    url(r'^requeriment/(?P<requeriment_id>[0-9]+)/userstory/(?P<pk>[0-9]+)/detail/', login_required(userstory_views.UserStoryDetailView.as_view()),name='userstory-detail'),
    url(r'^requeriment/(?P<requeriment_id>[0-9]+)/userstory/(?P<pk>[0-9]+)/update/', login_required(userstory_views.UserStoryUpdateFormView.as_view()), name='userstory-update'),
    url(r'^requeriment/(?P<requeriment_id>[0-9]+)/userstory/(?P<pk>[0-9]+)/delete/', login_required(userstory_views.UserStoryDeleteView.as_view()), name='userstory-delete'),
    url(r'^requeriment/(?P<requeriment_id>[0-9]+)/userstory/add/',         login_required(userstory_views.UserStoryAddFormView.as_view()), name='requeriment-userstory-add'),
    url(r'^requeriment/(?P<requeriment_id>[0-9]+)/userstory/(?P<pk>[0-9]+)/update/',         login_required(userstory_views.UserStoryUpdateFormView.as_view()), name='requeriment-userstory-update'),
    url(r'^requeriment/(?P<requeriment_id>[0-9]+)/userstory/',             login_required(userstory_views.UserStoryListView.as_view()), name='requeriment-userstory'),

    url(r'^sprint/add/',                            login_required(sprint_views.SprintAddFormView.as_view()), name='sprint-add'),
    url(r'^sprint/(?P<pk>[0-9]+)/update/',          login_required(sprint_views.SprintUpdateFormView.as_view()), name='sprint-update'),
    url(r'^sprint/(?P<pk>[0-9]+)/delete/',          login_required(sprint_views.SprintDeleteView.as_view()), name='sprint-delete'),
    url(r'^sprint/history/',                        login_required(sprint_views.SprintHistoryView.as_view()), name='sprint-history'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/history/',  login_required(sprint_views.SprintHistoryView.as_view()), name='sprint-history'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/requeriment/', login_required(requeriment_views.RequerimentListView.as_view()), name='sprint-requeriment'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/',          login_required(sprint_views.SprintDetailView.as_view()), name='sprint-details'),
    url(r'^sprint/',                                login_required(sprint_views.SprintListView.as_view()), name='sprint'),

    url(r'^requeriment/add/',                       login_required(requeriment_views.RequerimentAddFormView.as_view()), name='requeriment-add'),
    url(r'^requeriment/history/',                   login_required(requeriment_views.RequerimentHistoryView.as_view()), name='requeriment-history'),
    url(r'^requeriment/graph/',                     login_required(requeriment_views.RequerimentGraphView.as_view()), name='requeriment-graph-detail'),
    url(r'^requeriment/(?P<pk>[0-9]+)/graph/',      login_required(requeriment_views.RequerimentGraphDetailView.as_view()), name='requeriment-graph'),
    url(r'^requeriment/(?P<pk>[0-9]+)/history/',    login_required(requeriment_views.RequerimentHistoryView.as_view()), name='requeriment-history'),
    url(r'^requeriment/(?P<pk>[0-9]+)/update/',     login_required(requeriment_views.RequerimentUpdateFormView.as_view()), name='requeriment-update'),
    url(r'^requeriment/(?P<pk>[0-9]+)/',            login_required(requeriment_views.RequerimentDetailView.as_view()), name='requeriment-details'),
    url(r'^requeriment/',                           login_required(requeriment_views.RequerimentListView.as_view()), name='requeriment'),

    url(r'^artifacttype/add/',                       login_required(artifacttype_views.ArtifactTypeAddFormView.as_view()), name='artifacttype-add'),
    url(r'^artifacttype/(?P<pk>[0-9]+)/update/',     login_required(artifacttype_views.ArtifactTypeUpdateFormView.as_view()), name='artifacttype-update'),
    url(r'^artifacttype/(?P<pk>[0-9]+)/delete/',     login_required(artifacttype_views.ArtifactTypeDeleteView.as_view()), name='artifacttype-delete'),
    url(r'^artifacttype/',                           login_required(artifacttype_views.ArtifactTypeView.as_view()), name='artifacttype'),
]