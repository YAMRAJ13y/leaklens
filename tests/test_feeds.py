"""File loading (JSON / CSV) and field normalization."""
from __future__ import annotations

import json

from leaklens.feeds import load_file


def test_load_json_normalizes_fields(tmp_path):
    p = tmp_path / "v.json"
    p.write_text(
        json.dumps([{"group": "Qilin", "activity": "Tech", "country": "us", "attackdate": "2026-06-01T00:00:00"}]),
        encoding="utf-8",
    )
    victims = load_file(str(p))
    assert len(victims) == 1
    assert victims[0].group == "Qilin"
    assert victims[0].sector == "Tech"  # mapped from 'activity'
    assert victims[0].country == "US"  # upper-cased
    assert victims[0].date == "2026-06-01"  # truncated to date


def test_load_csv(tmp_path):
    p = tmp_path / "v.csv"
    p.write_text("group,sector,country,date\nAkira,Healthcare,GB,2026-05-02\n", encoding="utf-8")
    victims = load_file(str(p))
    assert victims[0].group == "Akira"
    assert victims[0].sector == "Healthcare"
