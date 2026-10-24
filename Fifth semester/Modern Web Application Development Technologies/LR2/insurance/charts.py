"""Charts built with matplotlib (lab: Python, not JavaScript)."""
from __future__ import annotations

import io

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from django.db.models import Count


def contracts_by_type_png() -> bytes:
    from . import models

    rows = list(
        models.Contract.objects.values("insurance_type__name")
        .annotate(cnt=Count("id"))
        .order_by("insurance_type__name")
    )
    if not rows:
        labels, values = ["нет данных"], [0]
    else:
        labels = [r["insurance_type__name"] for r in rows]
        values = [r["cnt"] for r in rows]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values, color="#2563eb")
    ax.set_title("Договоры по видам страхования")
    ax.set_ylabel("Количество")
    plt.xticks(rotation=25, ha="right")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100)
    plt.close(fig)
    buf.seek(0)
    return buf.read()
