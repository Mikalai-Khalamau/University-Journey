from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from . import models


class EmployeeOrSuperuserMixin(UserPassesTestMixin):
    """CRM access: employees group or Django superuser."""

    login_url = reverse_lazy("login")

    def test_func(self):
        u = self.request.user
        if not u.is_authenticated:
            return False
        if u.is_superuser:
            return True
        return u.groups.filter(name="employee").exists()


class ClientGroupMixin(UserPassesTestMixin):
    """Registered client (lab group name: client)."""

    login_url = reverse_lazy("login")

    def test_func(self):
        u = self.request.user
        if not u.is_authenticated:
            return False
        if u.is_superuser:
            return True
        return u.groups.filter(name="client").exists()


class ContractAccessMixin(UserPassesTestMixin):
    """Employee/superuser or client who owns the contract."""

    login_url = reverse_lazy("login")

    def test_func(self):
        u = self.request.user
        if not u.is_authenticated:
            return False
        if u.is_superuser or u.groups.filter(name="employee").exists():
            return True
        if u.groups.filter(name="client").exists():
            pk = self.kwargs.get("pk")
            if not pk:
                return False
            return models.Contract.objects.filter(pk=pk, client__user=u).exists()
        return False
