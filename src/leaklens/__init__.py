"""LeakLens - ransomware leak-site OSINT trend analysis.

Aggregates ransomware victim postings (group, sector, country, date) into
group/sector/country trend dashboards and a monthly timeline, with an optional
Claude-written weekly intel brief. Runs offline on a bundled synthetic snapshot;
``--live`` pulls the current feed from ransomware.live's free keyless API.

Public API:
    analyze(victims, source=...) -> Stats
    load_offline() / load_file(path) / fetch_live()
    to_dict(stats, brief=None) / to_markdown(stats, brief=None, top=10)
"""
from __future__ import annotations

from .analyze import analyze
from .feeds import fetch_live, load_file, load_offline
from .models import Stats, Victim
from .report import to_dict, to_markdown

__version__ = "0.1.0"

__all__ = [
    "analyze",
    "load_offline",
    "load_file",
    "fetch_live",
    "Stats",
    "Victim",
    "to_dict",
    "to_markdown",
    "__version__",
]
