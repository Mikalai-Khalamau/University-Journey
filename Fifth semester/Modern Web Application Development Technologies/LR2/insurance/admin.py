from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


class AgentInline(admin.TabularInline):
    model = models.Agent
    extra = 0
    show_change_link = True


class ContractBranchInline(admin.TabularInline):
    model = models.Contract
    fk_name = "branch"
    extra = 0
    readonly_fields = ("premium_amount", "commission_amount")
    autocomplete_fields = ("agent", "client", "insurance_type")
    show_change_link = True


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "phone", "created_at")
    list_filter = ("city",)
    search_fields = ("name", "address", "city", "phone")
    date_hierarchy = "created_at"
    inlines = [AgentInline, ContractBranchInline]


@admin.register(models.InsuranceType)
class InsuranceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "tariff_rate", "agent_commission_percent", "updated_at")
    list_filter = ("created_at",)
    search_fields = ("name",)
    date_hierarchy = "created_at"


@admin.register(models.Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "branch", "phone", "birth_date")
    list_filter = ("branch", "birth_date")
    search_fields = ("last_name", "first_name", "patronymic", "phone")
    autocomplete_fields = ("branch",)
    date_hierarchy = "created_at"


class ClientIdentityInline(admin.StackedInline):
    model = models.ClientIdentity
    extra = 0
    max_num = 1


class ContractClientInline(admin.TabularInline):
    model = models.Contract
    fk_name = "client"
    extra = 0
    readonly_fields = ("premium_amount", "commission_amount")
    autocomplete_fields = ("branch", "agent", "insurance_type")
    show_change_link = True


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "email", "birth_date", "user")
    list_filter = ("birth_date",)
    search_fields = ("full_name", "phone", "email", "address")
    autocomplete_fields = ("user",)
    date_hierarchy = "created_at"
    inlines = [ClientIdentityInline, ContractClientInline]


@admin.register(models.ClientIdentity)
class ClientIdentityAdmin(admin.ModelAdmin):
    list_display = ("document_id", "client")
    search_fields = ("document_id", "client__full_name")
    autocomplete_fields = ("client",)


@admin.register(models.InsuredObject)
class InsuredObjectAdmin(admin.ModelAdmin):
    list_display = ("object_type", "description", "value", "created_at")
    list_filter = ("object_type",)
    search_fields = ("description",)
    date_hierarchy = "created_at"


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "signed_date",
        "end_date",
        "insurance_type",
        "insurance_amount",
        "premium_amount",
        "commission_amount",
        "branch",
        "agent",
        "client",
    )
    list_filter = ("insurance_type", "branch", "signed_date")
    search_fields = (
        "client__full_name",
        "agent__last_name",
        "agent__first_name",
        "branch__name",
    )
    date_hierarchy = "signed_date"
    readonly_fields = ("premium_amount", "commission_amount", "created_at", "updated_at")
    autocomplete_fields = ("branch", "agent", "client", "insurance_type")
    filter_horizontal = ("insured_objects",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "signed_date",
                    "end_date",
                    "insurance_amount",
                    "insurance_type",
                    "branch",
                    "agent",
                    "client",
                )
            },
        ),
        (_("Objects"), {"fields": ("insured_objects",)}),
        (
            _("Computed"),
            {"fields": ("premium_amount", "commission_amount")},
        ),
        (_("Audit"), {"fields": ("created_at", "updated_at")}),
    )


class CompanyRequisiteInline(admin.TabularInline):
    model = models.CompanyRequisite
    extra = 1
    ordering = ("sort_order",)


@admin.register(models.CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    search_fields = ("title", "about_text")
    date_hierarchy = "created_at"
    inlines = [CompanyRequisiteInline]


@admin.register(models.CompanyRequisite)
class CompanyRequisiteAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "sort_order", "profile")
    list_filter = ("profile",)
    search_fields = ("label", "value")
    autocomplete_fields = ("profile",)


@admin.register(models.NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_at", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "summary", "slug")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


@admin.register(models.FAQEntry)
class FAQEntryAdmin(admin.ModelAdmin):
    list_display = ("question", "created_at")
    search_fields = ("question", "answer")
    date_hierarchy = "created_at"


@admin.register(models.ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role_title", "branch", "phone", "email")
    list_filter = ("branch",)
    search_fields = ("full_name", "role_title", "email", "phone")
    autocomplete_fields = ("branch",)
    date_hierarchy = "created_at"


@admin.register(models.Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    date_hierarchy = "created_at"


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("guest_name", "user", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("guest_name", "text", "user__username")
    autocomplete_fields = ("user",)
    date_hierarchy = "created_at"


@admin.register(models.PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "valid_from", "valid_until", "is_active")
    list_filter = ("is_active", "valid_from", "valid_until")
    search_fields = ("code",)
    date_hierarchy = "valid_from"


@admin.register(models.Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "website_url", "created_at")
    search_fields = ("name", "website_url", "description")
    date_hierarchy = "created_at"


@admin.register(models.GlossaryItem)
class GlossaryItemAdmin(admin.ModelAdmin):
    list_display = ("question", "added_at", "created_at")
    search_fields = ("question", "answer")
    date_hierarchy = "added_at"
