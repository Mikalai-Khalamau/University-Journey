import pytest
from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group, User


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser("su", "su@example.invalid", "pass12345")


@pytest.fixture
def user_client_group(db):
    u = User.objects.create_user("cuser", password="pass12345", email="c@example.invalid")
    g, _ = Group.objects.get_or_create(name="client")
    u.groups.add(g)
    return u


@pytest.fixture
def user_employee_group(db):
    u = User.objects.create_user("euser", password="pass12345", email="e@example.invalid")
    g, _ = Group.objects.get_or_create(name="employee")
    u.groups.add(g)
    return u


@pytest.fixture
def branch(db):
    from insurance import models

    return models.Branch.objects.create(
        name="Test Branch",
        address="Addr 1",
        city="Minsk",
        phone="+375 (29) 111-22-33",
    )


@pytest.fixture
def insurance_type(db):
    from insurance import models

    return models.InsuranceType.objects.create(
        name="Type A",
        tariff_rate=Decimal("0.04"),
        agent_commission_percent=Decimal("12.00"),
    )


@pytest.fixture
def agent(db, branch):
    from insurance import models

    return models.Agent.objects.create(
        last_name="Ivanov",
        first_name="Ivan",
        patronymic="Ivanovich",
        phone="+375 (29) 222-33-44",
        birth_date=date(1990, 1, 15),
        branch=branch,
    )


@pytest.fixture
def client_record(db):
    from insurance import models

    return models.Client.objects.create(
        full_name="Test Client",
        phone="+375 (29) 333-44-55",
        email="cl@example.invalid",
        birth_date=date(1988, 5, 20),
        address="Minsk",
    )


@pytest.fixture
def contract(db, branch, agent, client_record, insurance_type):
    from insurance import models

    c = models.Contract(
        signed_date=date(2024, 6, 1),
        end_date=date(2025, 6, 1),
        insurance_amount=Decimal("10000.00"),
        branch=branch,
        agent=agent,
        client=client_record,
        insurance_type=insurance_type,
    )
    c.save()
    return c
