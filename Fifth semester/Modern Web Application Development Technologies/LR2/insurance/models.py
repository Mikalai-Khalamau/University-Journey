from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from .validators import validate_age_at_least_18, validate_by_mobile_phone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Branch(TimeStampedModel):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, validators=[validate_by_mobile_phone])

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class InsuranceType(TimeStampedModel):
    name = models.CharField(max_length=200, unique=True)
    tariff_rate = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        help_text="Fraction of sum per period, e.g. 0.035 for 3.5%",
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("1"))],
    )
    agent_commission_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("100"))],
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Agent(TimeStampedModel):
    last_name = models.CharField(max_length=80)
    first_name = models.CharField(max_length=80)
    patronymic = models.CharField(max_length=80, blank=True)
    phone = models.CharField(max_length=30, validators=[validate_by_mobile_phone])
    birth_date = models.DateField()
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="agents",
    )

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        initial = f"{self.first_name[:1]}." if self.first_name else ""
        return f"{self.last_name} {initial}".strip()

    def clean(self):
        super().clean()
        validate_age_at_least_18(self.birth_date)


class Client(TimeStampedModel):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, validators=[validate_by_mobile_phone])
    email = models.EmailField()
    birth_date = models.DateField()
    address = models.CharField(max_length=500)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_profile",
    )

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name

    def clean(self):
        super().clean()
        validate_age_at_least_18(self.birth_date)


class ClientIdentity(models.Model):
    """Extra identity record; satisfies OneToOneField requirement in domain."""

    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="identity",
    )
    document_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.document_id


class InsuredObject(TimeStampedModel):
    class ObjectKind(models.TextChoices):
        AUTO = "auto", "Vehicle"
        PROPERTY = "property", "Property"
        LIFE = "life", "Life"
        HEALTH = "health", "Health"
        OTHER = "other", "Other"

    object_type = models.CharField(max_length=32, choices=ObjectKind.choices)
    description = models.CharField(max_length=500)
    value = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_object_type_display()}: {self.description[:40]}"


class Contract(TimeStampedModel):
    signed_date = models.DateField()
    end_date = models.DateField()
    insurance_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    premium_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0"),
        editable=False,
    )
    commission_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0"),
        editable=False,
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="contracts",
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.PROTECT,
        related_name="contracts",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="contracts",
    )
    insurance_type = models.ForeignKey(
        InsuranceType,
        on_delete=models.PROTECT,
        related_name="contracts",
    )
    insured_objects = models.ManyToManyField(
        InsuredObject,
        related_name="contracts",
        blank=True,
    )

    class Meta:
        ordering = ["-signed_date", "-id"]

    def __str__(self):
        label = ""
        if self.insurance_type_id:
            label = getattr(self.insurance_type, "name", "") or ""
        return f"Contract #{self.pk or 'new'} ({label or '—'})"

    @property
    def insurance_payment(self):
        """Premium = sum * tariff (stored after save)."""
        return self.premium_amount

    @property
    def agent_commission(self):
        """Agent cut from premium (stored after save)."""
        return self.commission_amount

    def clean(self):
        super().clean()
        if self.signed_date and self.end_date and self.end_date < self.signed_date:
            raise ValidationError({"end_date": "End date must be on or after signed date."})
        if self.agent_id and self.branch_id and self.agent.branch_id != self.branch_id:
            raise ValidationError("Agent must belong to the selected branch.")

    def save(self, *args, **kwargs):
        if self.insurance_type_id:
            t = self.insurance_type
            prem = (self.insurance_amount * t.tariff_rate).quantize(Decimal("0.01"))
            self.premium_amount = prem
            self.commission_amount = (
                prem * (t.agent_commission_percent / Decimal("100"))
            ).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)

    def refresh_financials(self):
        """Recalculate denormalized amounts from current type and sum."""
        self.save(update_fields=["premium_amount", "commission_amount", "updated_at"])


# --- CMS / lab mandatory pages ---


class CompanyProfile(TimeStampedModel):
    title = models.CharField(max_length=200, default="About us")
    about_text = models.TextField()

    def __str__(self):
        return self.title


class CompanyRequisite(TimeStampedModel):
    profile = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name="requisites",
    )
    label = models.CharField(max_length=200)
    value = models.CharField(max_length=500)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.label}: {self.value[:30]}"


class NewsArticle(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    summary = models.CharField(max_length=300)
    image_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="https://… or static path insurance/images/…",
    )
    body = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class FAQEntry(TimeStampedModel):
    question = models.CharField(max_length=500)
    answer = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.question[:60]


class ContactPerson(TimeStampedModel):
    full_name = models.CharField(max_length=200)
    role_title = models.CharField(max_length=200)
    photo_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="https://… or static path insurance/images/…",
    )
    phone = models.CharField(max_length=30, validators=[validate_by_mobile_phone])
    email = models.EmailField()
    bio = models.TextField(blank=True)
    birth_date = models.DateField()
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_staff",
    )

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name

    def clean(self):
        super().clean()
        validate_age_at_least_18(self.birth_date)


class Vacancy(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Review(TimeStampedModel):
    guest_name = models.CharField(max_length=120, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        name = self.guest_name or (self.user.get_username() if self.user_id else "?")
        return f"{name} ({self.rating})"


class PromoCode(TimeStampedModel):
    code = models.CharField(max_length=64, unique=True)
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("100"))],
    )
    valid_from = models.DateField()
    valid_until = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-valid_from"]

    def __str__(self):
        return self.code

    def clean(self):
        super().clean()
        if self.valid_from and self.valid_until and self.valid_until < self.valid_from:
            raise ValidationError({"valid_until": "valid_until must be >= valid_from."})


class Partner(TimeStampedModel):
    name = models.CharField(max_length=200)
    logo = models.CharField(max_length=500, blank=True, help_text="Image path or URL")
    website_url = models.URLField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class GlossaryItem(TimeStampedModel):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    added_at = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["-added_at"]

    def __str__(self):
        return self.question
