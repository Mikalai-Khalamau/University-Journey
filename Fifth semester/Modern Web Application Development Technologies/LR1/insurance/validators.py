import re
from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Belarus mobile format required by assignment
BY_MOBILE_REGEX = re.compile(r"^\+375\s\(29\)\s\d{3}-\d{2}-\d{2}$")

validate_by_mobile_phone = RegexValidator(
    BY_MOBILE_REGEX,
    "Use format: +375 (29) XXX-XX-XX",
)


def validate_age_at_least_18(birth_date):
    if birth_date is None:
        return
    today = date.today()
    age = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
    if age < 18:
        raise ValidationError("Age must be 18 or older.")
