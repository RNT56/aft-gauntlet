#!/usr/bin/env python3
"""Compose the portable AFT Gauntlet generator prompt with a project brief."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ASSET_PATH = Path(__file__).resolve().parents[1] / "assets" / "portable-generator.md"


def read_brief(path: str | None, text: str | None) -> str:
    if path and text:
        raise ValueError("Use either --brief or --text, not both.")
    if text:
        return text.strip()
    if path == "-":
        return sys.stdin.read().strip()
    if path:
        return Path(path).expanduser().read_text(encoding="utf-8").strip()
    raise ValueError("Provide --brief <path>, --brief -, or --text <brief>.")


def compose(template: str, brief: str, harness: str, platform: str) -> str:
    required = ("{{PROJECT_INPUT}}", "{{TARGET_HARNESS}}", "{{PLATFORM}}")
    missing = [token for token in required if token not in template]
    if missing:
        raise ValueError(f"Generator template is missing placeholders: {', '.join(missing)}")
    if not brief:
        raise ValueError("The project brief is empty.")
    return (
        template.replace("{{PROJECT_INPUT}}", brief)
        .replace("{{TARGET_HARNESS}}", harness)
        .replace("{{PLATFORM}}", platform)
        .rstrip()
        + "\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a ready-to-paste AFT Gauntlet generator prompt."
    )
    parser.add_argument("--brief", help="Markdown/text brief path, or - for stdin")
    parser.add_argument("--text", help="Inline project brief")
    parser.add_argument(
        "--harness",
        default="auto",
        choices=("auto", "codex", "claude-code", "other"),
    )
    parser.add_argument(
        "--platform",
        default="auto",
        choices=("auto", "website", "game", "ios-mobile", "pwa", "desktop", "hybrid"),
    )
    parser.add_argument("--output", help="Write to this path instead of stdout")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        brief = read_brief(args.brief, args.text)
        template = ASSET_PATH.read_text(encoding="utf-8")
        result = compose(template, brief, args.harness, args.platform)
        if args.output:
            output = Path(args.output).expanduser()
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(result, encoding="utf-8")
        else:
            sys.stdout.write(result)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
