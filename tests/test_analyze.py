"""Trend analytics over the bundled sample."""
from __future__ import annotations

from leaklens import analyze, load_offline


def test_offline_loads():
    victims, date = load_offline()
    assert len(victims) == 70
    assert date


def test_headline_stats():
    victims, _ = load_offline()
    stats = analyze(victims)
    assert stats.total == 70
    assert stats.distinct_groups == 10
    assert stats.top_group[0] == "Qilin"
    assert stats.busiest_month[0] == "2026-05"


def test_rankings_present_and_sorted():
    stats = analyze(load_offline()[0])
    assert stats.by_group and stats.by_sector and stats.by_country and stats.by_month
    counts = [c for _, c in stats.by_group]
    assert counts == sorted(counts, reverse=True)
