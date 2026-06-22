"""Generate the bundled synthetic ransomware-victim snapshot (committed).

Deterministic (no randomness) so the dataset is reproducible. The data is
SYNTHETIC and for demo/tests only — use `leaklens report --live` for real data.

Run:  python scripts/build_sample.py
"""
from __future__ import annotations

import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "src" / "leaklens" / "data"
OUT.mkdir(parents=True, exist_ok=True)

# Weighted so one group clearly leads (mirrors real leak-site concentration).
WEIGHTED_GROUPS = (
    ["Qilin"] * 16 + ["Akira"] * 12 + ["RansomHub"] * 9 + ["Play"] * 7 + ["Cl0p"] * 6
    + ["Medusa"] * 5 + ["The Gentlemen"] * 5 + ["INC Ransom"] * 4 + ["BianLian"] * 3
    + ["LockBit"] * 3
)
SECTORS = [
    "Manufacturing", "Healthcare", "Technology", "Construction", "Education",
    "Finance", "Retail", "Legal", "Government", "Energy", "Transportation",
    "Professional Services",
]
COUNTRIES = ["US", "US", "US", "GB", "DE", "CA", "FR", "IN", "AU", "IT", "BR", "JP", "ES", "US", "GB"]
MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]

victims = []
for i, group in enumerate(WEIGHTED_GROUPS):
    sector = SECTORS[i % len(SECTORS)]
    country = COUNTRIES[i % len(COUNTRIES)]
    # Concentrate Qilin in 2026-05 to create a visible surge.
    if group == "Qilin" and i % 3 == 0:
        month = "2026-05"
    else:
        month = MONTHS[i % len(MONTHS)]
    day = (i % 27) + 1
    victims.append({
        "name": f"victim-{i:02d}",
        "group": group,
        "sector": sector,
        "country": country,
        "date": f"{month}-{day:02d}",
    })

payload = {
    "_note": "SYNTHETIC sample data for demo/tests — NOT real victims. Use `leaklens report --live`.",
    "snapshotDate": "2026-06-15",
    "victims": victims,
}
(OUT / "sample_victims.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(f"wrote {len(victims)} victims to {OUT / 'sample_victims.json'}")
