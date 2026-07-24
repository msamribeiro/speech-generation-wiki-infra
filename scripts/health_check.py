#!/usr/bin/env python3
"""
Pipeline Health Suite — entry point.

Runs one or more check modules against the pipeline outputs and reports
issues with severity (error / warning). Exits 0 if all modules pass
(no errors), 1 if any module has at least one error.

Usage:
    python scripts/health_check.py                          # run all available modules
    python scripts/health_check.py --module ingest          # run one module
    python scripts/health_check.py --module agents          # validate Claude/Codex parity
    python scripts/health_check.py --module ingest --id 2501.12345  # single paper
    python scripts/health_check.py --module integrate --concept flow-matching --phase 2
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from checks._base import CheckArgs, ModuleResult
from checks import agents as _agents
from checks import ingest as _ingest
from checks import integrate as _integrate
from checks import render as _render

AVAILABLE_MODULES = {
    "agents": _agents,
    "ingest": _ingest,
    "integrate": _integrate,
    "render": _render,
}


def _print_result(result: ModuleResult, verbose: bool) -> None:
    status = "PASS" if result.passed else "FAIL"
    s = result.stats
    extra = ", ".join(f"{k}={v}" for k, v in s.items() if k not in ("errors", "warnings"))
    summary = f"{s.get('errors', 0)} errors, {s.get('warnings', 0)} warnings"
    if extra:
        summary += f" | {extra}"
    print(f"[{result.module:<10}] {status}  ({summary})")
    if verbose or not result.passed:
        for issue in result.issues:
            pid = issue.paper_id or "—"
            print(f"  {issue.severity:<7}  {issue.module}  {pid:<30}  {issue.check}  {issue.message}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pipeline Health Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--module",
        default=",".join(AVAILABLE_MODULES),
        help=f"Comma-separated modules to run (default: all). Available: {', '.join(AVAILABLE_MODULES)}",
    )
    parser.add_argument(
        "--id",
        dest="paper_id",
        default=None,
        help="Scope checks to a single paper ID (supported by: ingest)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print all issues, including warnings, even on passing modules",
    )
    parser.add_argument(
        "--wiki-dir",
        dest="wiki_dir",
        default=None,
        help="Override wiki root directory (default: wiki/ submodule). Useful for pointing at a standalone content repo.",
    )
    parser.add_argument(
        "--concept",
        dest="concept",
        default=None,
        help="Scope checks to a single concept (supported by: integrate, render)",
    )
    parser.add_argument(
        "--phase",
        dest="phase",
        type=int,
        choices=[1, 2],
        default=None,
        help="Force Phase 1 or Phase 2 checks (integrate only); default auto-detects per YAML",
    )
    args = parser.parse_args()

    module_names = [m.strip() for m in args.module.split(",") if m.strip()]
    unknown = [m for m in module_names if m not in AVAILABLE_MODULES]
    if unknown:
        parser.error(f"Unknown module(s): {', '.join(unknown)}. Available: {', '.join(AVAILABLE_MODULES)}")

    wiki_dir = Path(args.wiki_dir) if args.wiki_dir else None
    check_args = CheckArgs(paper_id=args.paper_id, wiki_dir=wiki_dir, concept=args.concept, phase=args.phase)

    all_passed = True
    for name in module_names:
        result = AVAILABLE_MODULES[name].run(check_args)
        _print_result(result, verbose=args.verbose)
        if not result.passed:
            all_passed = False

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
