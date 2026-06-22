"""LeakLens command-line interface.

    leaklens report [path] [--live] [--llm] [--json] [--top N]
    leaklens version
"""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .analyze import analyze
from .feeds import fetch_live, load_file, load_offline
from .llm import weekly_brief
from .report import to_dict, to_markdown


def _run_report(args) -> int:
    if args.path:
        victims = load_file(args.path)
        source = f"file: {args.path}"
    elif args.live:
        try:
            victims = fetch_live()
            source = "live: ransomware.live"
        except Exception as exc:
            print(f"warning: live fetch failed ({exc}); using offline sample.", file=sys.stderr)
            victims, snap = load_offline()
            source = f"offline sample {snap}"
    else:
        victims, snap = load_offline()
        source = f"offline sample {snap}"

    stats = analyze(victims, source=source)
    brief = weekly_brief(stats) if args.llm else None

    if args.json:
        print(json.dumps(to_dict(stats, brief), indent=2, ensure_ascii=False))
    else:
        print(to_markdown(stats, brief, top=args.top))
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    except Exception:
        pass

    parser = argparse.ArgumentParser(
        prog="leaklens",
        description="Ransomware leak-site OSINT — group/sector/country trend dashboards "
        "with an optional Claude weekly intel brief.",
    )
    sub = parser.add_subparsers(dest="cmd")

    rep = sub.add_parser("report", help="build a ransomware trend dashboard")
    rep.add_argument("path", nargs="?", help="victims file (.json/.csv); default: bundled sample")
    rep.add_argument("--live", action="store_true", help="fetch live data from ransomware.live")
    rep.add_argument("--llm", action="store_true", help="add a Claude weekly intel brief")
    rep.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    rep.add_argument("--top", type=int, default=10, help="rows per ranking (default 10)")

    sub.add_parser("version", help="print the version")

    args = parser.parse_args(argv)
    if args.cmd == "report":
        return _run_report(args)
    if args.cmd == "version":
        print(__version__)
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
