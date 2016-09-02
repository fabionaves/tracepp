from django.conf.urls import url
from main import views as mainviews
from django.contrib.auth import views as loginviews
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^accounts/login/', loginviews.login,
        {'template_name': 'login/form.html'}, name='login'),
    #url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(r'^$', login_required(mainviews.HomeView.as_view()), name='home'),
    url(r'^project/list/add/', login_required(mainviews.ProjectAddFormView.as_view()), name='project-add'),
    url(r'^project/list/(?P<pk>[0-9]+)/update/', login_required(mainviews.ProjectUpdateFormView.as_view()), name='project-update'),
    url(r'^project/list/', login_required(mainviews.ProjectListView.as_view()), name='project-list'),
    url(r'^project/(?P<project_id>[0-9]+)/', login_required(mainviews.ProjectView.as_view()), name='project'),
    url(r'^project/', login_required(mainviews.ProjectView.as_view()), name='project'),

    url(r'^userstory/', login_required(mainviews.UserStoryListView.as_view()), name='userstory'),

    url(r'^sprint/add/', login_required(mainviews.SprintAddFormView.as_view()), name='sprint-add'),
    url(r'^sprint/(?P<pk>[0-9]+)/update/', login_required(mainviews.SprintUpdateFormView.as_view()), name='sprint-update'),
    url(r'^sprint/(?P<pk>[0-9]+)/delete/', login_required(mainviews.SprintDeleteView.as_view()), name='sprint-delete'),
    url(r'^sprint/history/', login_required(mainviews.SprintHistoryView.as_view()), name='sprint-history'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/history/', login_required(mainviews.SprintHistoryView.as_view()), name='sprint-history'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/userstory/', login_required(mainviews.UserStoryListView.as_view()), name='sprint-userstory'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/', login_required(mainviews.SprintDetailView.as_view()), name='sprint-details'),
    url(r'^sprint/', login_required(mainviews.SprintListView.as_view()), name='sprint'),

    url(r'^requeriment/add/', login_required(mainviews.RequerimentAddFormView.as_view()), name='requeriment-add'),
    url(r'^requeriment/history/', login_required(mainviews.RequerimentHistoryView.as_view()), name='requeriment-history'),
    url(r'^requeriment/graph/', login_required(mainviews.RequerimentGraphView.as_view()), name='requeriment-graph'),
    url(r'^requeriment/(?P<pk>[0-9]+)/history/', login_required(mainviews.RequerimentHistoryView.as_view()), name='requeriment-history'),
    url(r'^requeriment/(?P<requeriment_id>[0-9]+)/userstory/add/', login_required(mainviews.UserStoryAddFormView.as_view()), name='requeriment-userstory-add'),
    url(r'^requeriment/(?P<requeriment_id>[0-9]+)/userstory/', login_required(mainviews.UserStoryListView.as_view()), name='requeriment-userstory'),
    url(r'^requeriment/(?P<pk>[0-9]+)/update/', login_required(mainviews.RequerimentUpdateFormView.as_view()), name='requeriment-update'),
    url(r'^requeriment/(?P<pk>[0-9]+)/', login_required(mainviews.RequerimentDetailView.as_view()), name='requeriment-details'),
    url(r'^requeriment/', login_required(mainviews.RequerimentListView.as_view()), name='requeriment'),
]