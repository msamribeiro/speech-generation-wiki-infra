#!/usr/bin/env python3
"""Print Claude plan usage by making one tiny Haiku call and reading its rate_limit_event.

Exit code: 0 if every window is below --stop (default 0.85), 2 if any is at/above it, 1 on error.
Usage: python3 scripts/check_limits.py [--stop 0.85]
"""
import argparse, datetime, json, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("--stop", type=float, default=0.85)
args = ap.parse_args()

out = subprocess.run(
    ["claude", "-p", "Reply with the single word: ok", "--output-format", "stream-json",
     "--verbose", "--model", "haiku", "--tools", "", "--disable-slash-commands"],
    capture_output=True, text=True, timeout=120,
).stdout

info = None
for line in out.splitlines():
    try:
        d = json.loads(line)
    except json.JSONDecodeError:
        continue
    if d.get("type") == "rate_limit_event":
        info = d["rate_limit_info"]
if not info:
    print("no rate_limit_event in output", file=sys.stderr)
    sys.exit(1)

over = False
for name, w in info.get("unifiedWindows", {}).items():
    u = w.get("utilization", 0)
    reset = datetime.datetime.fromtimestamp(w["resetsAt"]).strftime("%a %d %b %H:%M")
    print(f"{name:10s} {u:4.0%} used  status={w.get('status')}  resets {reset}")
    over |= u >= args.stop
sys.exit(2 if over else 0)
