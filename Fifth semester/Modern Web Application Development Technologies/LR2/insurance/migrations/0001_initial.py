# Initial schema for insurance app (stage 2).

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal

from django.conf import settings
from django.db import migrations, models

_BY_PHONE_VALIDATOR = django.core.validators.RegexValidator(
    r"^\+375\s\(29\)\s\d{3}-\d{2}-\d{2}$",
    "Use format: +375 (29) XXX-XX-XX",
)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Branch",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=200)),
                ("address", models.CharField(max_length=500)),
                ("city", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=30, validators=[_BY_PHONE_VALIDATOR])),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="InsuranceType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=200, unique=True)),
                (
                    "tariff_rate",
                    models.DecimalField(
                        decimal_places=6,
                        help_text="Fraction of sum per period, e.g. 0.035 for 3.5%",
                        max_digits=8,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0")),
                            django.core.validators.MaxValueValidator(Decimal("1")),
                        ],
                    ),
                ),
                (
                    "agent_commission_percent",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=5,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0")),
                            django.core.validators.MaxValueValidator(Decimal("100")),
                        ],
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="InsuredObject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "object_type",
                    models.CharField(
                        choices=[
                            ("auto", "Vehicle"),
                            ("property", "Property"),
                            ("life", "Life"),
                            ("health", "Health"),
                            ("other", "Other"),
                        ],
                        max_length=32,
                    ),
                ),
                ("description", models.CharField(max_length=500)),
                (
                    "value",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=14,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0")),
                        ],
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="CompanyProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(default="About us", max_length=200)),
                ("about_text", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="NewsArticle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("summary", models.CharField(max_length=300)),
                ("image_url", models.URLField(blank=True)),
                ("body", models.TextField(blank=True)),
                ("is_published", models.BooleanField(default=False)),
                (
                    "published_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={
                "ordering": ["-published_at"],
            },
        ),
        migrations.CreateModel(
            name="FAQEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("question", models.CharField(max_length=500)),
                ("answer", models.TextField()),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Vacancy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="PromoCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=64, unique=True)),
                (
                    "discount_percent",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=5,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0")),
                            django.core.validators.MaxValueValidator(Decimal("100")),
                        ],
                    ),
                ),
                ("valid_from", models.DateField()),
                ("valid_until", models.DateField()),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["-valid_from"],
            },
        ),
        migrations.CreateModel(
            name="Agent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("last_name", models.CharField(max_length=80)),
                ("first_name", models.CharField(max_length=80)),
                ("patronymic", models.CharField(blank=True, max_length=80)),
                ("phone", models.CharField(max_length=30, validators=[_BY_PHONE_VALIDATOR])),
                ("birth_date", models.DateField()),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="agents",
                        to="insurance.branch",
                    ),
                ),
            ],
            options={
                "ordering": ["last_name", "first_name"],
            },
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("full_name", models.CharField(max_length=255)),
                ("phone", models.CharField(max_length=30, validators=[_BY_PHONE_VALIDATOR])),
                ("email", models.EmailField(max_length=254)),
                ("birth_date", models.DateField()),
                ("address", models.CharField(max_length=500)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="client_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["full_name"],
            },
        ),
        migrations.CreateModel(
            name="ClientIdentity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("document_id", models.CharField(max_length=64, unique=True)),
                (
                    "client",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="identity",
                        to="insurance.client",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ContactPerson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("full_name", models.CharField(max_length=200)),
                ("role_title", models.CharField(max_length=200)),
                ("photo_url", models.URLField(blank=True)),
                ("phone", models.CharField(max_length=30, validators=[_BY_PHONE_VALIDATOR])),
                ("email", models.EmailField(max_length=254)),
                ("bio", models.TextField(blank=True)),
                ("birth_date", models.DateField()),
                (
                    "branch",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="contact_staff",
                        to="insurance.branch",
                    ),
                ),
            ],
            options={
                "ordering": ["full_name"],
            },
        ),
        migrations.CreateModel(
            name="Contract",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("signed_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "insurance_amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=14,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01")),
                        ],
                    ),
                ),
                (
                    "premium_amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0"),
                        editable=False,
                        max_digits=14,
                    ),
                ),
                (
                    "commission_amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0"),
                        editable=False,
                        max_digits=14,
                    ),
                ),
                (
                    "agent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contracts",
                        to="insurance.agent",
                    ),
                ),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contracts",
                        to="insurance.branch",
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contracts",
                        to="insurance.client",
                    ),
                ),
                (
                    "insurance_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="contracts",
                        to="insurance.insurancetype",
                    ),
                ),
            ],
            options={
                "ordering": ["-signed_date", "-id"],
            },
        ),
        migrations.AddField(
            model_name="contract",
            name="insured_objects",
            field=models.ManyToManyField(
                blank=True,
                related_name="contracts",
                to="insurance.insuredobject",
            ),
        ),
        migrations.CreateModel(
            name="CompanyRequisite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("label", models.CharField(max_length=200)),
                ("value", models.CharField(max_length=500)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="requisites",
                        to="insurance.companyprofile",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order", "id"],
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("guest_name", models.CharField(blank=True, max_length=120)),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                    ),
                ),
                ("text", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reviews",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
