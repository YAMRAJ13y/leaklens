"""Compute trend statistics from a list of ransomware victims."""
from __future__ import annotations

from collections import Counter

from .models import Stats, Victim


def analyze(victims: list[Victim], source: str = "offline sample") -> Stats:
    groups = Counter(v.group for v in victims if v.group)
    sectors = Counter(v.sector for v in victims if v.sector)
    countries = Counter(v.country for v in victims if v.country)
    months = Counter(v.date[:7] for v in victims if v.date)

    dates = sorted(v.date[:10] for v in victims if v.date)
    period = f"{dates[0]} … {dates[-1]}" if dates else "n/a"

    return Stats(
        total=len(victims),
        distinct_groups=len(groups),
        period=period,
        by_group=groups.most_common(),
        by_sector=sectors.most_common(),
        by_country=countries.most_common(),
        by_month=sorted(months.items()),
        top_group=groups.most_common(1)[0] if groups else ("n/a", 0),
        busiest_month=max(months.items(), key=lambda kv: kv[1]) if months else ("n/a", 0),
        source=source,
    )
