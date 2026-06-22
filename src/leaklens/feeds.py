"""Load ransomware-victim data.

Offline by default (bundled synthetic snapshot). ``--live`` pulls the current
recent-victims feed from ransomware.live's free, keyless v2 API.
"""
from __future__ import annotations

import csv
import json
from importlib import resources

from .models import Victim

LIVE_URL = "https://api.ransomware.live/v2/recentvictims"
_UA = {"User-Agent": "LeakLens/1.0 (+ransomware-trend-analysis)"}


def _norm_date(value) -> str:
    return str(value or "")[:10]


def _record_to_victim(d: dict) -> Victim:
    return Victim(
        group=str(d.get("group") or d.get("group_name") or "").strip(),
        sector=str(d.get("sector") or d.get("activity") or "").strip(),
        country=str(d.get("country") or "").strip().upper(),
        date=_norm_date(
            d.get("date") or d.get("attackdate") or d.get("discovered") or d.get("published")
        ),
        name=str(d.get("name") or d.get("victim") or d.get("post_title") or "").strip(),
    )


def load_offline() -> tuple[list[Victim], str]:
    path = resources.files("leaklens").joinpath("data/sample_victims.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    return [_record_to_victim(v) for v in data["victims"]], data.get("snapshotDate", "")


def load_file(path: str) -> list[Victim]:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if path.lower().endswith(".csv"):
        return [_record_to_victim(d) for d in csv.DictReader(text.splitlines())]
    data = json.loads(text)
    records = data["victims"] if isinstance(data, dict) and "victims" in data else data
    return [_record_to_victim(d) for d in records]


def fetch_live() -> list[Victim]:
    import urllib.request

    req = urllib.request.Request(LIVE_URL, headers=_UA)
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 - fixed https feed
        data = json.loads(resp.read().decode("utf-8"))
    records = data if isinstance(data, list) else data.get("data", data.get("victims", []))
    return [_record_to_victim(d) for d in records]
