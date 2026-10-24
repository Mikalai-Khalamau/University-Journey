"""Statistics dashboard (Python stats + matplotlib chart)."""
from __future__ import annotations

import base64
import calendar
import logging

from django.conf import settings
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils import timezone

from . import models
from .access import employee_required
from .charts import contracts_by_type_png
from .stats import age_years, stats_triplet

log = logging.getLogger("insurance")


@employee_required
def stats_dashboard(request):
    now = timezone.now()
    contracts = list(
        models.Contract.objects.select_related("insurance_type", "client").values(
            "premium_amount",
            "commission_amount",
            "insurance_amount",
            "signed_date",
            "insurance_type__name",
            "client__birth_date",
        )
    )
    premiums = [float(c["premium_amount"]) for c in contracts]
    premium_stats = stats_triplet(premiums)
    total_premium = sum(premiums) if premiums else 0.0

    clients = list(models.Client.objects.values_list("birth_date", flat=True))
    ages = [age_years(bd) for bd in clients if bd]
    age_stats = stats_triplet([float(a) for a in ages])

    by_type = list(
        models.Contract.objects.values("insurance_type__name")
        .annotate(cnt=Count("id"), prem_sum=Sum("premium_amount"))
        .order_by("-cnt")
    )
    if by_type:
        most_popular_type = by_type[0]["insurance_type__name"]
        top_rev = max(by_type, key=lambda x: float(x["prem_sum"] or 0))
        most_profitable_type = top_rev["insurance_type__name"]
    else:
        most_popular_type = "—"
        most_profitable_type = "—"

    chart_b64 = base64.b64encode(contracts_by_type_png()).decode("ascii")

    ctx = {
        "now_utc": now,
        "calendar_text": calendar.TextCalendar().formatmonth(
            now.year, now.month, w=3, l=1
        ),
        "premium_stats": premium_stats,
        "total_premium": total_premium,
        "age_stats": age_stats,
        "by_type": by_type,
        "most_popular_type": most_popular_type,
        "most_profitable_type": most_profitable_type,
        "clients_alphabetical": list(
            models.Client.objects.order_by("full_name").values(
                "full_name", "phone", "birth_date"
            )[:50]
        ),
        "chart_png_base64": chart_b64,
        "server_tz": settings.TIME_ZONE,
    }
    return render(request, "insurance/stats_dashboard.html", ctx)
