import pytest
from datetime import date

from django.core.exceptions import ValidationError

from insurance.validators import validate_age_at_least_18, validate_by_mobile_phone


def test_phone_validator_ok():
    validate_by_mobile_phone("+375 (29) 123-45-67")


def test_phone_validator_bad():
    with pytest.raises(ValidationError):
        validate_by_mobile_phone("+375 (33) 123-45-67")


def test_age_ok():
    validate_age_at_least_18(date(1990, 1, 1))


def test_age_minor():
    with pytest.raises(ValidationError):
        validate_age_at_least_18(date.today().replace(year=date.today().year - 10))
