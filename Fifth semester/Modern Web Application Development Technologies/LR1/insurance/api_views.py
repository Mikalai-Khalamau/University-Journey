"""JSON endpoints and HTML pages backed by external APIs."""
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from . import models
from .services.branch_weather import weather_for_branch
from .services.nager_holidays import public_holidays

log = logging.getLogger("insurance.api")


class BranchWeatherJsonView(LoginRequiredMixin, View):
    """Nominatim + Open-Meteo for branch city (two external services)."""

    def get(self, request, pk, *args, **kwargs):
        branch = get_object_or_404(models.Branch, pk=pk)
        try:
            payload = weather_for_branch(branch)
        except Exception as exc:
            log.exception("branch_weather failed: %s", exc)
            return JsonResponse(
                {"ok": False, "error": "upstream_error"},
                status=502,
            )
        status = 200 if payload.get("ok") else 404
        log.info("branch_weather api branch_id=%s ok=%s", pk, payload.get("ok"))
        return JsonResponse(payload, status=status)


class PublicHolidaysJsonView(LoginRequiredMixin, View):
    """Nager.Date public holidays (second external API)."""

    def get(self, request, year, *args, **kwargs):
        country = (request.GET.get("country") or "BY").upper()[:2]
        try:
            items = public_holidays(int(year), country)
        except ValueError:
            return JsonResponse({"error": "invalid_year"}, status=400)
        except Exception as exc:
            log.exception("holidays failed: %s", exc)
            return JsonResponse({"error": "upstream_error"}, status=502)
        slim = [
            {"date": h.get("date"), "name": h.get("name"), "localName": h.get("localName")}
            for h in items[:64]
        ]
        return JsonResponse(
            {"year": int(year), "country": country, "count": len(slim), "holidays": slim}
        )


@login_required
def holidays_page(request, year: int):
    """Human-readable holidays list (Nager.Date API) — for lab demo."""
    country = (request.GET.get("country") or "BY").upper()[:2]
    error = None
    try:
        items = public_holidays(int(year), country)
    except ValueError:
        items = []
        error = "Неверный год."
    except Exception as exc:
        log.exception("holidays page failed: %s", exc)
        items = []
        error = "Сервис праздников недоступен. Проверьте интернет."
    rows = [
        {
            "date": h.get("date", ""),
            "name": h.get("localName") or h.get("name") or "—",
        }
        for h in items
    ]
    return render(
        request,
        "insurance/holidays.html",
        {
            "year": year,
            "country": country,
            "holidays": rows,
            "error": error,
            "json_url_name": "insurance:api-holidays",
        },
    )
