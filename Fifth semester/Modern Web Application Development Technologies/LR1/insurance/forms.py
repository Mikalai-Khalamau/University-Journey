from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from . import models
from .validators import validate_age_at_least_18

User = get_user_model()


def _clean_birth_date_field(form, field_name="birth_date"):
    bd = form.cleaned_data.get(field_name)
    if bd:
        validate_age_at_least_18(bd)
    return bd

_PHONE_ATTRS = {
    "pattern": r"\+375 \(29\) [0-9]{3}-[0-9]{2}-[0-9]{2}",
    "title": "+375 (29) XXX-XX-XX",
    "placeholder": "+375 (29) 123-45-67",
}


class BranchForm(forms.ModelForm):
    class Meta:
        model = models.Branch
        fields = ("name", "address", "city", "phone")
        widgets = {
            "name": forms.TextInput(
                attrs={"required": True, "maxlength": "200", "placeholder": "Branch name"}
            ),
            "address": forms.TextInput(
                attrs={"required": True, "maxlength": "500"}
            ),
            "city": forms.TextInput(
                attrs={"required": True, "maxlength": "120"}
            ),
            "phone": forms.TextInput(attrs={**_PHONE_ATTRS, "required": True}),
        }


class InsuranceTypeForm(forms.ModelForm):
    class Meta:
        model = models.InsuranceType
        fields = ("name", "tariff_rate", "agent_commission_percent")
        widgets = {
            "name": forms.TextInput(attrs={"required": True, "maxlength": "200"}),
            "tariff_rate": forms.NumberInput(
                attrs={"required": True, "min": "0", "max": "1", "step": "0.000001"}
            ),
            "agent_commission_percent": forms.NumberInput(
                attrs={"required": True, "min": "0", "max": "100", "step": "0.01"}
            ),
        }


class AgentForm(forms.ModelForm):
    class Meta:
        model = models.Agent
        fields = (
            "last_name",
            "first_name",
            "patronymic",
            "phone",
            "birth_date",
            "branch",
        )
        widgets = {
            "last_name": forms.TextInput(attrs={"required": True, "maxlength": "80"}),
            "first_name": forms.TextInput(attrs={"required": True, "maxlength": "80"}),
            "patronymic": forms.TextInput(attrs={"maxlength": "80"}),
            "phone": forms.TextInput(attrs={**_PHONE_ATTRS, "required": True}),
            "birth_date": forms.DateInput(attrs={"type": "date", "required": True}),
        }

    def clean_birth_date(self):
        return _clean_birth_date_field(self)


class ClientForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.order_by("username"),
        required=False,
    )

    class Meta:
        model = models.Client
        fields = ("full_name", "phone", "email", "birth_date", "address", "user")
        widgets = {
            "full_name": forms.TextInput(attrs={"required": True, "maxlength": "255"}),
            "phone": forms.TextInput(attrs={**_PHONE_ATTRS, "required": True}),
            "email": forms.EmailInput(attrs={"required": True, "maxlength": "254"}),
            "birth_date": forms.DateInput(attrs={"type": "date", "required": True}),
            "address": forms.TextInput(attrs={"required": True, "maxlength": "500"}),
        }

    def clean_birth_date(self):
        return _clean_birth_date_field(self)


class InsuredObjectForm(forms.ModelForm):
    class Meta:
        model = models.InsuredObject
        fields = ("object_type", "description", "value")
        widgets = {
            "object_type": forms.Select(attrs={"required": True}),
            "description": forms.TextInput(attrs={"required": True, "maxlength": "500"}),
            "value": forms.NumberInput(
                attrs={"required": True, "min": "0", "step": "0.01"}
            ),
        }


class ContractForm(forms.ModelForm):
    class Meta:
        model = models.Contract
        fields = (
            "signed_date",
            "end_date",
            "insurance_amount",
            "insurance_type",
            "branch",
            "agent",
            "client",
            "insured_objects",
        )
        widgets = {
            "signed_date": forms.DateInput(attrs={"type": "date", "required": True}),
            "end_date": forms.DateInput(attrs={"type": "date", "required": True}),
            "insurance_amount": forms.NumberInput(
                attrs={"required": True, "min": "0.01", "step": "0.01"}
            ),
            "insured_objects": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["insured_objects"].queryset = models.InsuredObject.objects.order_by(
            "-created_at"
        )
        self.fields["insured_objects"].required = False
        self.fields["agent"].queryset = models.Agent.objects.select_related("branch")
        self.fields["client"].queryset = models.Client.objects.order_by("full_name")
        self.fields["branch"].queryset = models.Branch.objects.order_by("name")
        self.fields["insurance_type"].queryset = models.InsuranceType.objects.order_by(
            "name"
        )
        for fname in (
            "signed_date",
            "end_date",
            "insurance_amount",
            "insurance_type",
            "branch",
            "agent",
            "client",
        ):
            self.fields[fname].widget.attrs.setdefault("required", "")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ("rating", "text")
        widgets = {
            "rating": forms.NumberInput(
                attrs={"min": "1", "max": "5", "required": True, "step": "1"}
            ),
            "text": forms.Textarea(
                attrs={
                    "required": True,
                    "minlength": 10,
                    "maxlength": 2000,
                    "rows": 5,
                    "cols": 56,
                }
            ),
        }

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if len(text) < 10:
            raise ValidationError("Please enter at least 10 characters.")
        return text

    def clean_rating(self):
        raw = self.cleaned_data.get("rating")
        if raw in (None, ""):
            raise ValidationError("Rating is required.")
        try:
            r = int(raw)
        except (TypeError, ValueError) as exc:
            raise ValidationError("Invalid rating.") from exc
        if r < 1 or r > 5:
            raise ValidationError("Rating must be between 1 and 5.")
        return r


class ClientOnboardingForm(forms.ModelForm):
    """Client profile linked to the logged-in user (no user field in UI)."""

    class Meta:
        model = models.Client
        fields = ("full_name", "phone", "email", "birth_date", "address")
        widgets = {
            "full_name": forms.TextInput(attrs={"required": True, "maxlength": "255"}),
            "phone": forms.TextInput(attrs={**_PHONE_ATTRS, "required": True}),
            "email": forms.EmailInput(attrs={"required": True, "maxlength": "254"}),
            "birth_date": forms.DateInput(attrs={"type": "date", "required": True}),
            "address": forms.TextInput(attrs={"required": True, "maxlength": "500"}),
        }

    def clean_birth_date(self):
        return _clean_birth_date_field(self)


class ClientPortalContractForm(forms.ModelForm):
    """Client orders a contract; agent is auto-picked from the selected branch."""

    class Meta:
        model = models.Contract
        fields = (
            "signed_date",
            "end_date",
            "insurance_amount",
            "insurance_type",
            "branch",
            "insured_objects",
        )
        widgets = {
            "signed_date": forms.DateInput(attrs={"type": "date", "required": True}),
            "end_date": forms.DateInput(attrs={"type": "date", "required": True}),
            "insurance_amount": forms.NumberInput(
                attrs={"required": True, "min": "0.01", "step": "0.01"}
            ),
            "insured_objects": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["insured_objects"].queryset = models.InsuredObject.objects.order_by(
            "-created_at"
        )
        self.fields["insured_objects"].required = False
        self.fields["branch"].queryset = models.Branch.objects.order_by("name")
        self.fields["insurance_type"].queryset = models.InsuranceType.objects.order_by(
            "name"
        )
        for fname in (
            "signed_date",
            "end_date",
            "insurance_amount",
            "insurance_type",
            "branch",
        ):
            self.fields[fname].widget.attrs.setdefault("required", "")
