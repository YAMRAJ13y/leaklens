"""Dashboard serialization."""
from __future__ import annotations

import json

from leaklens import analyze, load_offline, to_dict, to_markdown


def test_to_dict_round_trips():
    stats = analyze(load_offline()[0])
    d = to_dict(stats)
    assert d["total_victims"] == 70
    assert d["top_group"]["name"] == "Qilin"
    assert d["by_group"][0]["count"] >= d["by_group"][-1]["count"]
    json.loads(json.dumps(d))


def test_to_markdown():
    stats = analyze(load_offline()[0])
    md = to_markdown(stats)
    assert "# LeakLens" in md
    assert "Top groups" in md
    assert "Qilin" in md
