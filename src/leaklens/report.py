"""Render LeakLens trend statistics to JSON and a markdown dashboard."""
from __future__ import annotations

from .models import Stats


def to_dict(stats: Stats, brief: str | None = None) -> dict:
    return {
        "source": stats.source,
        "period": stats.period,
        "total_victims": stats.total,
        "distinct_groups": stats.distinct_groups,
        "top_group": {"name": stats.top_group[0], "count": stats.top_group[1]},
        "busiest_month": {"month": stats.busiest_month[0], "count": stats.busiest_month[1]},
        "by_group": [{"name": n, "count": c} for n, c in stats.by_group],
        "by_sector": [{"name": n, "count": c} for n, c in stats.by_sector],
        "by_country": [{"name": n, "count": c} for n, c in stats.by_country],
        "by_month": [{"month": m, "count": c} for m, c in stats.by_month],
        "weekly_brief": brief,
    }


def _bar(count: int, max_count: int, width: int = 26) -> str:
    fill = round(width * count / max_count) if max_count else 0
    return "█" * fill


def _section(title: str, rows: list[tuple[str, int]], top: int) -> list[str]:
    out = [f"## {title}", "", "```"]
    rows = rows[:top]
    max_count = max((c for _, c in rows), default=0)
    label_w = max((len(str(n)) for n, _ in rows), default=4)
    for name, count in rows:
        out.append(f"{str(name):<{label_w}}  {_bar(count, max_count)} {count}")
    out += ["```", ""]
    return out


def to_markdown(stats: Stats, brief: str | None = None, top: int = 10) -> str:
    lines = [
        "# LeakLens — Ransomware Leak-Site Intel",
        "",
        f"**Source:** {stats.source}  ·  **Period:** {stats.period}  ",
        f"**Victims:** {stats.total}  ·  **Active groups:** {stats.distinct_groups}  ",
        f"**Most active group:** {stats.top_group[0]} ({stats.top_group[1]})  ·  "
        f"**Busiest month:** {stats.busiest_month[0]} ({stats.busiest_month[1]})",
        "",
    ]
    lines += _section("Top groups", stats.by_group, top)
    lines += _section("Top sectors", stats.by_sector, top)
    lines += _section("Top countries", stats.by_country, top)
    lines += _section("Monthly timeline", stats.by_month, 24)
    if brief:
        lines += ["## Weekly intel brief", "", f"> {brief}", ""]
    return "\n".join(lines)
