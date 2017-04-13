from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _

from main.services.requeriment import RequerimentService
from main.services.sprint import SprintService
from main.services.userstory import UserStoryService


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
        return reverse("main:requeriment-details",kwargs={'sprint_id':sprint_id, 'pk':requeriment_id})
    elif sprint_id:
        return reverse("main:sprint-requeriment", kwargs={'sprint_id':sprint_id})
    elif requeriment_id:
        return reverse("main:requeriment-details", kwargs={'pk':requeriment_id})
    else:
        return reverse("main:requeriment")


def userstories_breadcrumbs(project_id=False, requeriment_id=False, sprint_id=False, userstory_id=False, last_name=False):
    if sprint_id and userstory_id and requeriment_id:
        sprint = SprintService.get_sprint(project_id, sprint_id)
        requeriment = RequerimentService.get_requeriment(project_id, requeriment_id)
        userstory = UserStoryService.get_userstory(project_id, userstory_id)
        breadcrumbs = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
            {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': sprint_id}),
             'class': '', 'name': sprint},
            {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
            {'link': reverse_lazy('main:requeriment-details',  kwargs={'pk': requeriment_id, 'sprint_id': sprint_id}),
             'class': '', 'name': sprint},
            {'link': reverse_lazy('main:sprint-requeriment-userstory', kwargs={'sprint_id': sprint_id, 'requeriment_id': requeriment_id}), 'class': '',
             'name': _('User Stories')},
            {'link': reverse_lazy('main:sprint-requeriment-userstory-detail', kwargs={'sprint_id': sprint_id, 'requeriment_id': requeriment_id, 'pk': userstory.pk}), 'class': '',
             'name': userstory.code}
        )
    elif sprint_id and requeriment_id:
        sprint = SprintService.get_sprint(project_id, sprint_id)
        requeriment = RequerimentService.get_requeriment(project_id, requeriment_id)

        breadcrumbs = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
            {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': sprint_id}),
             'class': '', 'name': sprint},
            {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriment')},
            {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment_id, 'sprint_id': sprint_id}),
             'class': '', 'name': requeriment.code}
        )
    elif sprint_id and userstory_id:
        sprint = SprintService.get_sprint(project_id, sprint_id)
        userstory = UserStoryService.get_userstory(project_id, userstory_id)
        breadcrumbs = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
            {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': sprint_id}),
             'class': '', 'name': sprint},
            {'link': reverse_lazy('main:sprint-userstory', kwargs={'sprint_id': sprint_id}), 'class': '',
             'name': _('User Stories')},
            {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
             'name': userstory.code}
        )
    elif requeriment_id and userstory_id:
        requeriment = RequerimentService.get_requeriment(project_id, requeriment_id)
        userstory = UserStoryService.get_userstory(project_id, userstory_id)
        breadcrumbs = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriments')},
            {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment_id}),
             'class': '', 'name': requeriment},
            {'link': reverse_lazy('main:requeriment-userstory',
                                  kwargs={'requeriment_id': requeriment_id}), 'class': '',
             'name': _('User Stories')},
            {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
             'name': userstory.code},
        )
    elif userstory_id:
        userstory = UserStoryService.get_userstory(project_id, userstory_id)
        breadcrumbs = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:userstory'), 'class': '',
             'name': _('User Stories')},
            {'link': reverse_lazy('main:userstory-detail', kwargs={'pk': userstory.pk}), 'class': '',
             'name': userstory.code},
        )
    elif sprint_id:
        sprint = SprintService.get_sprint(project_id, sprint_id)
        breadcrumbs = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:sprint'), 'class': '', 'name': _('Sprint')},
            {'link': reverse_lazy('main:sprint-details', kwargs={'sprint_id': sprint_id}),
             'class': '', 'name': sprint},
            {'link': '#', 'class': '', 'name': _('User Stories')},
        )
    elif requeriment_id:
        requeriment = RequerimentService.get_requeriment(project_id, requeriment_id)
        breadcrumbs = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': reverse_lazy('main:requeriment'), 'class': '', 'name': _('Requeriments')},
            {'link': reverse_lazy('main:requeriment-details', kwargs={'pk': requeriment_id}),
             'class': '', 'name': requeriment},
            {'link': '#', 'class': '', 'name': _('User Stories')},
        )
    else:
        breadcrumbs = (
            {'link': reverse_lazy('main:home'), 'class': '', 'name': _('Home')},
            {'link': '#', 'class': '', 'name': _('User Stories')},
        )

    if last_name:
        breadcrumbs += (
            {'link': '#', 'class': '', 'name': last_name},
        )
    return breadcrumbs


