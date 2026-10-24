import pytest
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError

from insurance import models


@pytest.mark.django_db
def test_contract_premium_and_commission(contract):
    assert contract.premium_amount == Decimal("400.00")
    assert contract.commission_amount == Decimal("48.00")


@pytest.mark.django_db
def test_contract_agent_branch_mismatch(branch, insurance_type, client_record):
    b2 = models.Branch.objects.create(
        name="Other",
        address="x",
        city="Grodno",
        phone="+375 (29) 444-55-66",
    )
    agent = models.Agent.objects.create(
        last_name="A",
        first_name="B",
        phone="+375 (29) 555-66-77",
        birth_date=date(1991, 1, 1),
        branch=b2,
    )
    c = models.Contract(
        signed_date=date(2024, 1, 1),
        end_date=date(2025, 1, 1),
        insurance_amount=Decimal("5000"),
        branch=branch,
        agent=agent,
        client=client_record,
        insurance_type=insurance_type,
    )
    with pytest.raises(ValidationError):
        c.full_clean()


@pytest.mark.django_db
def test_promo_dates():
    p = models.PromoCode(
        code="X1",
        discount_percent=Decimal("5"),
        valid_from=date(2025, 1, 10),
        valid_until=date(2025, 1, 1),
    )
    with pytest.raises(ValidationError):
        p.full_clean()


@pytest.mark.django_db
def test_client_str(client_record):
    assert "Test" in str(client_record)
