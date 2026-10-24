from unittest.mock import patch

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_branch_weather_api_requires_login(client, branch):
    url = reverse("insurance:api-branch-weather", kwargs={"pk": branch.pk})
    assert client.get(url).status_code == 302


@pytest.mark.django_db
@patch(
    "insurance.services.branch_weather.current_weather",
    return_value={
        "temperature_c": 1.0,
        "humidity_pct": 50,
        "wind_kmh": 3.0,
        "time": "t",
    },
)
@patch("insurance.services.branch_weather.geocode_city", return_value=(53.0, 27.0))
def test_branch_weather_api_ok(mock_geo, mock_w, client, user_employee_group, branch):
    client.force_login(user_employee_group)
    url = reverse("insurance:api-branch-weather", kwargs={"pk": branch.pk})
    r = client.get(url)
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["weather"]["temperature_c"] == 1.0


@pytest.mark.django_db
@patch("insurance.services.nager_holidays.http_get_json", return_value=[])
def test_holidays_api_empty(mock_get, client, user_employee_group):
    client.force_login(user_employee_group)
    url = reverse("insurance:api-holidays", kwargs={"year": 2026})
    r = client.get(url)
    assert r.status_code == 200
    assert r.json()["count"] == 0


@pytest.mark.django_db
@patch(
    "insurance.services.nager_holidays.http_get_json",
    return_value=[
        {"date": "2026-01-01", "name": "New Year", "localName": "Новый год"},
    ],
)
def test_holidays_api_with_rows(mock_get, client, user_employee_group):
    client.force_login(user_employee_group)
    r = client.get(reverse("insurance:api-holidays", kwargs={"year": 2026}))
    body = r.json()
    assert body["count"] == 1
    assert body["holidays"][0]["date"] == "2026-01-01"
