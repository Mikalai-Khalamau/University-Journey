import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    "name,kwargs",
    [
        ("home", {}),
        ("branch-list", {}),
        ("register", {}),
        ("stats-dashboard", {}),
        ("api-holidays", {"year": 2026}),
        ("api-branch-weather", {"pk": 1}),
        ("news-list", {}),
        ("contract-list", {}),
    ],
)
def test_reverse_named_routes(name, kwargs):
    reverse(f"insurance:{name}", kwargs=kwargs)
