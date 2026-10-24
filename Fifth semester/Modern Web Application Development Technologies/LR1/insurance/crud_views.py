"""
CRM CRUD via Function-Based Views (lab requirement).
Pattern matches assignment example: list / detail / create / update / delete.
"""
import logging

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from . import models
from .access import contract_access_required, employee_required
from .forms import (
    AgentForm,
    BranchForm,
    ClientForm,
    ContractForm,
    InsuredObjectForm,
    InsuranceTypeForm,
)

log = logging.getLogger("insurance")
PAGE_SIZE = 15


def _page(request, queryset, context_name):
    paginator = Paginator(queryset, PAGE_SIZE)
    page = paginator.get_page(request.GET.get("page"))
    return {
        context_name: page.object_list,
        "page_obj": page,
        "is_paginated": page.has_other_pages(),
    }


# --- Branch ---


def branch_list(request):
    qs = models.Branch.objects.order_by("name")
    ctx = _page(request, qs, "branches")
    return render(request, "insurance/branch_list.html", ctx)


def branch_detail(request, pk):
    branch = get_object_or_404(models.Branch, pk=pk)
    ctx = {"branch": branch}
    if request.user.is_authenticated:
        from .services.branch_weather import weather_for_branch

        try:
            ctx["branch_weather"] = weather_for_branch(branch)
        except Exception as exc:
            logging.getLogger("insurance.external").warning("weather skip: %s", exc)
            ctx["branch_weather"] = {"ok": False, "error": "unavailable"}
    return render(request, "insurance/branch_detail.html", ctx)


@employee_required
def branch_create(request):
    if request.method == "POST":
        form = BranchForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Филиал создан.")
            return redirect("insurance:branch-detail", pk=obj.pk)
    else:
        form = BranchForm()
    return render(request, "insurance/branch_form.html", {"form": form, "object": None})


@employee_required
def branch_update(request, pk):
    branch = get_object_or_404(models.Branch, pk=pk)
    if request.method == "POST":
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request, "Филиал обновлён.")
            return redirect("insurance:branch-detail", pk=pk)
    else:
        form = BranchForm(instance=branch)
    return render(request, "insurance/branch_form.html", {"form": form, "object": branch})


@employee_required
def branch_delete(request, pk):
    branch = get_object_or_404(models.Branch, pk=pk)
    if request.method == "POST":
        branch.delete()
        messages.success(request, "Филиал удалён.")
        return redirect("insurance:branch-list")
    return render(request, "insurance/branch_confirm_delete.html", {"object": branch})


# --- InsuranceType ---


def insurancetype_list(request):
    qs = models.InsuranceType.objects.order_by("name")
    ctx = _page(request, qs, "insurance_types")
    return render(request, "insurance/insurancetype_list.html", ctx)


def insurancetype_detail(request, pk):
    insurance_type = get_object_or_404(models.InsuranceType, pk=pk)
    return render(
        request,
        "insurance/insurancetype_detail.html",
        {"insurance_type": insurance_type},
    )


@employee_required
def insurancetype_create(request):
    if request.method == "POST":
        form = InsuranceTypeForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Вид страхования создан.")
            return redirect("insurance:insurancetype-detail", pk=obj.pk)
    else:
        form = InsuranceTypeForm()
    return render(
        request, "insurance/insurancetype_form.html", {"form": form, "object": None}
    )


@employee_required
def insurancetype_update(request, pk):
    insurance_type = get_object_or_404(models.InsuranceType, pk=pk)
    if request.method == "POST":
        form = InsuranceTypeForm(request.POST, instance=insurance_type)
        if form.is_valid():
            form.save()
            messages.success(request, "Вид страхования обновлён.")
            return redirect("insurance:insurancetype-detail", pk=pk)
    else:
        form = InsuranceTypeForm(instance=insurance_type)
    return render(
        request,
        "insurance/insurancetype_form.html",
        {"form": form, "object": insurance_type},
    )


@employee_required
def insurancetype_delete(request, pk):
    insurance_type = get_object_or_404(models.InsuranceType, pk=pk)
    if request.method == "POST":
        insurance_type.delete()
        messages.success(request, "Вид страхования удалён.")
        return redirect("insurance:insurancetype-list")
    return render(
        request,
        "insurance/insurancetype_confirm_delete.html",
        {"object": insurance_type},
    )


# --- Agent ---


@employee_required
def agent_list(request):
    qs = models.Agent.objects.select_related("branch").order_by("last_name", "first_name")
    ctx = _page(request, qs, "agents")
    return render(request, "insurance/agent_list.html", ctx)


@employee_required
def agent_detail(request, pk):
    agent = get_object_or_404(
        models.Agent.objects.select_related("branch"), pk=pk
    )
    return render(request, "insurance/agent_detail.html", {"agent": agent})


@employee_required
def agent_create(request):
    if request.method == "POST":
        form = AgentForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Агент создан.")
            return redirect("insurance:agent-detail", pk=obj.pk)
    else:
        form = AgentForm()
    return render(request, "insurance/agent_form.html", {"form": form, "object": None})


@employee_required
def agent_update(request, pk):
    agent = get_object_or_404(models.Agent, pk=pk)
    if request.method == "POST":
        form = AgentForm(request.POST, instance=agent)
        if form.is_valid():
            form.save()
            messages.success(request, "Агент обновлён.")
            return redirect("insurance:agent-detail", pk=pk)
    else:
        form = AgentForm(instance=agent)
    return render(request, "insurance/agent_form.html", {"form": form, "object": agent})


@employee_required
def agent_delete(request, pk):
    agent = get_object_or_404(models.Agent, pk=pk)
    if request.method == "POST":
        agent.delete()
        messages.success(request, "Агент удалён.")
        return redirect("insurance:agent-list")
    return render(request, "insurance/agent_confirm_delete.html", {"object": agent})


# --- Client ---


@employee_required
def client_list(request):
    qs = models.Client.objects.order_by("full_name")
    ctx = _page(request, qs, "clients")
    return render(request, "insurance/client_list.html", ctx)


@employee_required
def client_detail(request, pk):
    client = get_object_or_404(
        models.Client.objects.select_related("user").prefetch_related(
            "contracts", "identity"
        ),
        pk=pk,
    )
    return render(request, "insurance/client_detail.html", {"client": client})


@employee_required
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Клиент создан.")
            return redirect("insurance:client-detail", pk=obj.pk)
    else:
        form = ClientForm()
    return render(request, "insurance/client_form.html", {"form": form, "object": None})


@employee_required
def client_update(request, pk):
    client = get_object_or_404(models.Client, pk=pk)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Клиент обновлён.")
            return redirect("insurance:client-detail", pk=pk)
    else:
        form = ClientForm(instance=client)
    return render(request, "insurance/client_form.html", {"form": form, "object": client})


@employee_required
def client_delete(request, pk):
    client = get_object_or_404(models.Client, pk=pk)
    if request.method == "POST":
        client.delete()
        messages.success(request, "Клиент удалён.")
        return redirect("insurance:client-list")
    return render(request, "insurance/client_confirm_delete.html", {"object": client})


# --- InsuredObject ---


@employee_required
def insuredobject_list(request):
    qs = models.InsuredObject.objects.order_by("-created_at")
    ctx = _page(request, qs, "insured_objects")
    return render(request, "insurance/insuredobject_list.html", ctx)


@employee_required
def insuredobject_detail(request, pk):
    insured_object = get_object_or_404(models.InsuredObject, pk=pk)
    return render(
        request,
        "insurance/insuredobject_detail.html",
        {"insured_object": insured_object},
    )


@employee_required
def insuredobject_create(request):
    if request.method == "POST":
        form = InsuredObjectForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Объект создан.")
            return redirect("insurance:insuredobject-detail", pk=obj.pk)
    else:
        form = InsuredObjectForm()
    return render(
        request, "insurance/insuredobject_form.html", {"form": form, "object": None}
    )


@employee_required
def insuredobject_update(request, pk):
    insured_object = get_object_or_404(models.InsuredObject, pk=pk)
    if request.method == "POST":
        form = InsuredObjectForm(request.POST, instance=insured_object)
        if form.is_valid():
            form.save()
            messages.success(request, "Объект обновлён.")
            return redirect("insurance:insuredobject-detail", pk=pk)
    else:
        form = InsuredObjectForm(instance=insured_object)
    return render(
        request,
        "insurance/insuredobject_form.html",
        {"form": form, "object": insured_object},
    )


@employee_required
def insuredobject_delete(request, pk):
    insured_object = get_object_or_404(models.InsuredObject, pk=pk)
    if request.method == "POST":
        insured_object.delete()
        messages.success(request, "Объект удалён.")
        return redirect("insurance:insuredobject-list")
    return render(
        request,
        "insurance/insuredobject_confirm_delete.html",
        {"object": insured_object},
    )


# --- Contract ---


@employee_required
def contract_list(request):
    qs = (
        models.Contract.objects.select_related(
            "branch", "agent", "client", "insurance_type"
        )
        .prefetch_related("insured_objects")
        .order_by("-signed_date", "-id")
    )
    ctx = _page(request, qs, "contracts")
    return render(request, "insurance/contract_list.html", ctx)


@contract_access_required
def contract_detail(request, pk):
    contract = get_object_or_404(
        models.Contract.objects.select_related(
            "branch", "agent", "client", "insurance_type"
        ).prefetch_related("insured_objects"),
        pk=pk,
    )
    return render(
        request,
        "insurance/contract_detail.html",
        {"contract": contract, "server_tz": settings.TIME_ZONE},
    )


@employee_required
def contract_create(request):
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, "Договор создан.")
            return redirect("insurance:contract-detail", pk=obj.pk)
    else:
        form = ContractForm()
    return render(request, "insurance/contract_form.html", {"form": form, "object": None})


@employee_required
def contract_update(request, pk):
    contract = get_object_or_404(models.Contract, pk=pk)
    if request.method == "POST":
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            form.save()
            messages.success(request, "Договор обновлён.")
            return redirect("insurance:contract-detail", pk=pk)
    else:
        form = ContractForm(instance=contract)
    return render(
        request, "insurance/contract_form.html", {"form": form, "object": contract}
    )


@employee_required
def contract_delete(request, pk):
    contract = get_object_or_404(models.Contract, pk=pk)
    if request.method == "POST":
        contract.delete()
        messages.success(request, "Договор удалён.")
        return redirect("insurance:contract-list")
    return render(
        request, "insurance/contract_confirm_delete.html", {"object": contract}
    )
