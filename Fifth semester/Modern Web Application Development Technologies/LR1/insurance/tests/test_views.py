import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_ok(client):
    r = client.get(reverse("insurance:home"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_branch_list_anonymous(client):
    r = client.get(reverse("insurance:branch-list"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_branch_create_redirects_anonymous(client):
    r = client.get(reverse("insurance:branch-create"))
    assert r.status_code == 302


@pytest.mark.django_db
def test_branch_create_employee(client, user_employee_group, branch):
    client.force_login(user_employee_group)
    r = client.get(reverse("insurance:branch-create"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_stats_dashboard_forbidden_guest(client):
    r = client.get(reverse("insurance:stats-dashboard"))
    assert r.status_code == 302


@pytest.mark.django_db
def test_stats_dashboard_employee(client, user_employee_group, contract):
    client.force_login(user_employee_group)
    r = client.get(reverse("insurance:stats-dashboard"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_stats_dashboard_has_matplotlib_chart(client, user_employee_group, contract):
    client.force_login(user_employee_group)
    r = client.get(reverse("insurance:stats-dashboard"))
    assert r.status_code == 200
    assert b"data:image/png;base64," in r.content


@pytest.mark.django_db
def test_client_dashboard_requires_client_group(client, user_employee_group):
    client.force_login(user_employee_group)
    r = client.get(reverse("insurance:client-dashboard"))
    assert r.status_code == 403


@pytest.mark.django_db
def test_client_dashboard_ok(client, user_client_group):
    client.force_login(user_client_group)
    r = client.get(reverse("insurance:client-dashboard"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_register_get(client):
    r = client.get(reverse("insurance:register"))
    assert r.status_code == 200


@pytest.mark.django_db
def test_review_list(client):
    r = client.get(reverse("insurance:review-list"))
    assert r.status_code == 200
