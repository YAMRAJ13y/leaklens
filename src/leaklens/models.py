"""Core data models for LeakLens."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Victim:
    """One ransomware leak-site victim posting."""

    group: str
    sector: str = ""
    country: str = ""
    date: str = ""  # ISO-8601 (YYYY-MM-DD or longer)
    name: str = ""


@dataclass
class Stats:
    total: int = 0
    distinct_groups: int = 0
    period: str = "n/a"
    by_group: list[tuple[str, int]] = field(default_factory=list)
    by_sector: list[tuple[str, int]] = field(default_factory=list)
    by_country: list[tuple[str, int]] = field(default_factory=list)
    by_month: list[tuple[str, int]] = field(default_factory=list)
    top_group: tuple[str, int] = ("n/a", 0)
    busiest_month: tuple[str, int] = ("n/a", 0)
    source: str = "offline sample"
