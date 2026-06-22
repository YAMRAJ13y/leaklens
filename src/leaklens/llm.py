"""Optional Claude-written weekly ransomware intel brief.

Runs only when ``anthropic`` is installed and ``ANTHROPIC_API_KEY`` is set; the
dashboard works fully offline without it.
"""
from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Stats

_SYSTEM = (
    "You are a CTI analyst. Given aggregated ransomware leak-site statistics, write a "
    "2-4 sentence weekly intelligence brief: the most active group(s), notable sector/"
    "country concentration, and any shift worth flagging. Be specific with numbers; no "
    "preamble, no markdown, no bullet points."
)


def weekly_brief(stats: Stats, model: str | None = None) -> str | None:
    try:
        from anthropic import Anthropic
    except Exception:
        return None
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None

    top_groups = ", ".join(f"{n} ({c})" for n, c in stats.by_group[:5])
    top_sectors = ", ".join(f"{n} ({c})" for n, c in stats.by_sector[:5])
    top_countries = ", ".join(f"{n} ({c})" for n, c in stats.by_country[:5])
    timeline = ", ".join(f"{m}:{c}" for m, c in stats.by_month)
    prompt = (
        f"Period: {stats.period}. {stats.total} victims across {stats.distinct_groups} groups.\n"
        f"Top groups: {top_groups}\nTop sectors: {top_sectors}\nTop countries: {top_countries}\n"
        f"Monthly: {timeline}\n(If this is labelled sample data, frame it as a demonstration.)"
    )
    try:
        client = Anthropic()
        msg = client.messages.create(
            model=model or os.environ.get("LEAKLENS_MODEL", "claude-haiku-4-5"),
            max_tokens=256,
            system=_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in msg.content if getattr(b, "type", None) == "text").strip()
        return text or None
    except Exception:
        return None
