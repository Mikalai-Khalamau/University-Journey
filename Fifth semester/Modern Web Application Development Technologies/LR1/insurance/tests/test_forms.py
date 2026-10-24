import pytest
from datetime import date
from decimal import Decimal

from insurance.forms import (
    AgentForm,
    BranchForm,
    ClientOnboardingForm,
    InsuranceTypeForm,
    ReviewForm,
)


@pytest.mark.django_db
def test_branch_form_valid():
    f = BranchForm(
        {
            "name": "N",
            "address": "A",
            "city": "C",
            "phone": "+375 (29) 100-00-01",
        }
    )
    assert f.is_valid()


@pytest.mark.django_db
def test_insurance_type_form_valid():
    f = InsuranceTypeForm(
        {
            "name": "Z",
            "tariff_rate": "0.03",
            "agent_commission_percent": "10",
        }
    )
    assert f.is_valid()


@pytest.mark.django_db
def test_agent_form_requires_branch(db, branch):
    f = AgentForm(
        {
            "last_name": "L",
            "first_name": "F",
            "patronymic": "",
            "phone": "+375 (29) 200-00-02",
            "birth_date": date(1992, 2, 2),
            "branch": branch.pk,
        }
    )
    assert f.is_valid(), f.errors


@pytest.mark.django_db
def test_review_form_short_text():
    f = ReviewForm({"rating": 5, "text": "short"})
    assert not f.is_valid()


@pytest.mark.django_db
def test_review_form_ok():
    f = ReviewForm({"rating": 4, "text": "Good service here thanks"})
    assert f.is_valid()


@pytest.mark.django_db
def test_client_onboarding_form():
    f = ClientOnboardingForm(
        {
            "full_name": "FN",
            "phone": "+375 (29) 300-00-03",
            "email": "a@b.co",
            "birth_date": date(1993, 3, 3),
            "address": "Addr",
        }
    )
    assert f.is_valid()
