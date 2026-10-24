"""Client / employee dashboards (lab stage 6)."""
from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.views.generic.list import ListView

from . import models
from .forms import ClientOnboardingForm, ClientPortalContractForm
from .mixins import ClientGroupMixin, EmployeeOrSuperuserMixin


class ClientDashboardView(LoginRequiredMixin, ClientGroupMixin, TemplateView):
    template_name = "insurance/portal/client_dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile = models.Client.objects.filter(user=self.request.user).first()
        ctx["profile"] = profile
        if profile:
            ctx["contracts"] = (
                models.Contract.objects.filter(client=profile)
                .select_related("branch", "insurance_type", "agent")
                .order_by("-signed_date")
            )
        today = date.today()
        ctx["promo_highlights"] = models.PromoCode.objects.filter(
            is_active=True,
            valid_from__lte=today,
            valid_until__gte=today,
        ).order_by("-valid_until")[:8]
        return ctx


class ClientProfileCreateView(LoginRequiredMixin, ClientGroupMixin, CreateView):
    model = models.Client
    form_class = ClientOnboardingForm
    template_name = "insurance/portal/client_profile_form.html"
    success_url = reverse_lazy("insurance:client-dashboard")

    def dispatch(self, request, *args, **kwargs):
        if models.Client.objects.filter(user=request.user).exists():
            messages.info(request, "Profile already exists.")
            return redirect("insurance:client-dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientProfileUpdateView(LoginRequiredMixin, ClientGroupMixin, UpdateView):
    model = models.Client
    form_class = ClientOnboardingForm
    template_name = "insurance/portal/client_profile_form.html"
    success_url = reverse_lazy("insurance:client-dashboard")

    def get_object(self, queryset=None):
        return get_object_or_404(models.Client, user=self.request.user)


class ClientPortalContractCreateView(LoginRequiredMixin, ClientGroupMixin, CreateView):
    model = models.Contract
    form_class = ClientPortalContractForm
    template_name = "insurance/portal/client_contract_form.html"

    def get_success_url(self):
        from django.urls import reverse

        return reverse("insurance:contract-detail", kwargs={"pk": self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        if not models.Client.objects.filter(user=request.user).exists():
            messages.warning(request, "Complete your client profile first.")
            return redirect("insurance:client-profile-create")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        client = models.Client.objects.get(user=self.request.user)
        branch = form.cleaned_data["branch"]
        agent = (
            models.Agent.objects.filter(branch=branch).order_by("id").first()
        )
        if not agent:
            form.add_error("branch", "No agent is assigned to this branch yet.")
            return self.form_invalid(form)
        form.instance.client = client
        form.instance.agent = agent
        return super().form_valid(form)


class EmployeeDashboardView(LoginRequiredMixin, EmployeeOrSuperuserMixin, TemplateView):
    template_name = "insurance/portal/employee_dashboard.html"


class EmployeeContractListView(LoginRequiredMixin, EmployeeOrSuperuserMixin, ListView):
    model = models.Contract
    template_name = "insurance/portal/employee_contract_list.html"
    context_object_name = "contracts"
    paginate_by = 20

    def get_queryset(self):
        qs = (
            models.Contract.objects.select_related(
                "branch", "agent", "client", "insurance_type"
            )
            .prefetch_related("insured_objects")
            .order_by("-signed_date", "-id")
        )
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(client__full_name__icontains=q)
                | Q(branch__name__icontains=q)
                | Q(insurance_type__name__icontains=q)
            )
        sort = self.request.GET.get("sort", "signed_date_desc")
        mapping = {
            "signed_date_desc": ("-signed_date", "-id"),
            "signed_date_asc": ("signed_date", "id"),
            "amount_desc": ("-insurance_amount",),
            "amount_asc": ("insurance_amount",),
        }
        return qs.order_by(*mapping.get(sort, ("-signed_date", "-id")))
