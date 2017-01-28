from django.urls import reverse_lazy
from django.utils.translation import ugettext as _

from main.services.requeriment import RequerimentService
from main.services.sprint import SprintService


def requeriments_breadcrumbs(project_id, requeriment_id, sprint_id, last_name=False):
    if sprint_id and requeriment_id:
        sprint = SprintService.get_sprint(project_id, sprint_id)
        requeriment = RequerimentService.get_requeriment(project_id, requeriment_id)
        breadcrumbs = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
            {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': sprint_id}), 'class': '',
             'name': sprint},
            {'link': reverse_lazy('main:sprint-requeriment', kwargs={'sprint_id': sprint_id}), 'class': '',
             'name': _('Requeriments')},
            {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment.id}), 'class': '',
             'name': requeriment.code},
        )
    elif sprint_id:
        sprint = SprintService.get_sprint(project_id, sprint_id)
        breadcrumbs = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
            {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': sprint_id}), 'class': '',
             'name': sprint},
            {'link': reverse_lazy('main:sprint-requeriment', kwargs={'sprint_id': sprint_id}), 'class': '',
             'name': _('Requeriments')},
        )
    elif requeriment_id:
        requeriment = RequerimentService.get_requeriment(project_id, requeriment_id)
        breadcrumbs = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriments')},
            {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment.id}), 'class': '',
             'name': requeriment.code},
        )
    else:
        breadcrumbs = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriments')},
        )
    if last_name:
        breadcrumbs += (
            {'link': '#', 'class': '', 'name': last_name},
        )
    return breadcrumbs


def requeriments_sucess_url(requeriment_id, sprint_id):
    if sprint_id and requeriment_id:
        return '/sprint/'+sprint_id+'/requeriment/'+requeriment_id
    elif sprint_id:
        return '/sprint/'+sprint_id+'/requeriment/'
    elif requeriment_id:
        return '/requeriment/'+requeriment_id
    else:
        return '/requeriment/'

