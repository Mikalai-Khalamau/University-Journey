"""Function-based access checks (lab: backend access control)."""
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from . import models


def _is_employee(user):
    return user.is_superuser or user.groups.filter(name="employee").exists()


def employee_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not _is_employee(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped


def client_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        u = request.user
        if u.is_superuser or u.groups.filter(name="client").exists():
            return view_func(request, *args, **kwargs)
        raise PermissionDenied

    return _wrapped


def contract_access_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        u = request.user
        if _is_employee(u):
            return view_func(request, *args, **kwargs)
        if u.groups.filter(name="client").exists():
            pk = kwargs.get("pk")
            if pk and models.Contract.objects.filter(pk=pk, client__user=u).exists():
                return view_func(request, *args, **kwargs)
        raise PermissionDenied

    return _wrapped
