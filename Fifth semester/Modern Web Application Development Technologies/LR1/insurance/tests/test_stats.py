import pytest

from insurance.stats import age_years, stats_triplet


def test_age_years():
    from datetime import date

    assert age_years(date(2000, 6, 15), date(2020, 6, 14)) == 19
    assert age_years(date(2000, 6, 15), date(2020, 6, 15)) == 20


def test_stats_triplet_empty():
    assert stats_triplet([]) == {"mean": None, "median": None, "mode": None}


def test_stats_triplet_simple():
    s = stats_triplet([1.0, 2.0, 3.0, 3.0])
    assert s["mean"] == pytest.approx(2.25)
    assert s["median"] == pytest.approx(2.5)
