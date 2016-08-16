from django.shortcuts import redirect
from django.utils.decorators import available_attrs
from django.utils.six import wraps


def require_project():
    def decorator(func):
        def inner(request, *args, **kwargs):
            if not 'project_id' in request.session:
               return redirect('/project/')
            return func(request, *args, **kwargs)
        return wraps(func, assigned=available_attrs(func))(inner)
    return decorator
