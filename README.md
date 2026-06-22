# LeakLens 🔦

> Turn ransomware leak-site noise into trends. LeakLens aggregates victim postings into group/sector/country dashboards and a monthly timeline — with an optional Claude weekly intel brief.

[![CI](https://github.com/YAMRAJ13y/leaklens/actions/workflows/ci.yml/badge.svg)](https://github.com/YAMRAJ13y/leaklens/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![data: ransomware.live](https://img.shields.io/badge/data-ransomware.live-red.svg)](https://www.ransomware.live/)

Ransomware crews post their victims on leak sites daily. Individually it's noise; in
aggregate it's intelligence — who's most active, which sectors and countries are
being hit, and when a group surges. LeakLens does that aggregation and turns it into
a readable dashboard a CTI analyst can act on.

Runs **offline on a bundled snapshot with zero dependencies**; `--live` pulls the
current feed from **ransomware.live's free, keyless API**.

```bash
git clone https://github.com/YAMRAJ13y/leaklens && cd leaklens
python -m leaklens report          # offline sample
python -m leaklens report --live   # current data from ransomware.live
```

---

## ⚡ What it looks like

```
# LeakLens — Ransomware Leak-Site Intel
Source: offline sample 2026-06-15 · Period: 2026-01-01 … 2026-06-27
Victims: 70 · Active groups: 10
Most active group: Qilin (16) · Busiest month: 2026-05 (17)

## Top groups
Qilin      ██████████████████████████ 16
Akira      ████████████████████ 12
RansomHub  ███████████████ 9
Play       ███████████ 7
Cl0p       ██████████ 6

## Top countries
US  ██████████████████████████ 19
GB  ████████████ 9
DE  ███████ 5
```

`--json` emits the same data structured for pipelines; `--llm` adds a Claude-written
2–4 sentence weekly intel brief.

---

## 🎯 Why this matters

Ransomware hit an elevated "new normal" in 2025–2026 with heavy consolidation among
the top crews. Tracking *who* is surging and *which sectors* they favour is core CTI
work — and turning a raw feed into a trend story is exactly the analyst skill this
demonstrates. It rounds out the portfolio's threat-intel side alongside
[IOCForge](https://github.com/YAMRAJ13y/iocforge) (indicator enrichment).

---

## 🔧 Usage

```bash
python -m leaklens report                  # bundled offline snapshot, markdown
python -m leaklens report --live           # live ransomware.live feed (keyless)
python -m leaklens report --json --top 15  # structured output, more rows
python -m leaklens report victims.csv      # your own export (.json or .csv)
```

Input records use `group`, `sector` (or `activity`), `country`, and `date` (other
ransomware.live field names like `attackdate` / `victim` are auto-mapped). The
optional brief needs `pip install -e ".[llm]"` + `ANTHROPIC_API_KEY`.

---

## ✅ Testing & CI

```bash
ruff check .   # lint
pytest -q      # analytics correctness, field mapping, dashboard serialization
```

GitHub Actions runs lint + tests on Python 3.10–3.13 and smoke-tests the dashboard — all offline, no secrets. Regenerate the sample with `python scripts/build_sample.py`.

---

## 🚧 Roadmap

- [ ] Anomaly alerts when a group's weekly count spikes vs its trailing average
- [ ] Sector risk-scoring for a chosen industry
- [ ] Map group → MITRE ATT&CK TTPs
- [ ] Scheduled refresh + a hosted static dashboard
- [ ] Cross-reference victims with [IOCForge](https://github.com/YAMRAJ13y/iocforge) for linked infrastructure

---

## ⚠️ Disclaimer & ethics

LeakLens consumes **already-public, pre-structured** leak-site metadata (group,
sector, country, date) for defensive trend analysis — it does not scrape, host, or
republish stolen victim data. The bundled `data/sample_victims.json` is **synthetic**;
use `--live` for real data and respect ransomware.live's terms.

---

## 📄 License

[MIT](LICENSE) © 2026 Yamraj ([@YAMRAJ13y](https://github.com/YAMRAJ13y))
