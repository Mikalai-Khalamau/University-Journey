import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from insurance.context_processors import access_flags


@pytest.mark.django_db
def test_access_flags_anonymous():
    rf = RequestFactory()
    req = rf.get("/")
    req.user = AnonymousUser()
    ctx = access_flags(req)
    assert ctx["show_crm_tools"] is False
    assert ctx["is_client_group"] is False


@pytest.mark.django_db
def test_access_flags_employee(user_employee_group):
    rf = RequestFactory()
    req = rf.get("/")
    req.user = user_employee_group
    ctx = access_flags(req)
    assert ctx["show_crm_tools"] is True


@pytest.mark.django_db
def test_access_flags_client(user_client_group):
    rf = RequestFactory()
    req = rf.get("/")
    req.user = user_client_group
    ctx = access_flags(req)
    assert ctx["is_client_group"] is True
