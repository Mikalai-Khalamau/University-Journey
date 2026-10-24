from unittest.mock import patch

import pytest
from django.urls import reverse


@pytest.mark.django_db
@patch(
    "insurance.services.branch_weather.weather_for_branch",
    return_value={"ok": True, "lat": 1.0, "lon": 2.0, "weather": {"temperature_c": 5.0}},
)
def test_branch_detail_shows_weather_block(mock_w, client, user_employee_group, branch):
    client.force_login(user_employee_group)
    r = client.get(reverse("insurance:branch-detail", kwargs={"pk": branch.pk}))
    assert r.status_code == 200
    assert "Погода" in r.content.decode("utf-8")
