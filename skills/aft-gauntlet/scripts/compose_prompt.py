#!/usr/bin/env python3
"""Compose a command-profiled AFT Gauntlet generator prompt with a project brief."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ASSET_PATH = Path(__file__).resolve().parents[1] / "assets" / "portable-generator.md"

HARNESS_DIRECTIVES = {
    "codex": """Generate an execution prompt whose first character is `/` and whose first line starts `/goal Complete` with a verifiable integrated terminal condition. Put no heading, preface, or code fence before the command. Goal mode is the continuation engine. Never name or describe the target agent product or harness, add target metadata, explain the adapter choice, or offer cross-harness fallbacks.

Require the lead to spawn native subagents immediately for the smallest independent research, implementation, test, and review workstreams. Keep shared architecture and integration with the lead and avoid conflicting parallel writes. Give every important builder output to a separate fresh-context critic. After each major wave, fan out strong critics across correctness and the project-relevant UX/visual, accessibility, performance, security, integration, and licensing dimensions. Require two independent critics for high-risk or highly subjective surfaces, wait for all requested results, synthesize evidence, fix the largest material gap, and run a separate integration critic. Keep the active session objective running until every terminal gate is evidenced or a real authority blocker requires user input.""",
    "claude-code": """Generate an execution prompt whose first character is `/` and whose first line starts `/loop Continue` with no time interval, so the loop self-paces. Put no heading, preface, or code fence before the command. Each iteration must read the live progress artifact, dispatch the highest-value independent work, collect fresh critic verdicts, repair the largest material gap, and stop only when the integrated terminal condition is evidenced or a real authority blocker requires user input. Never name or describe the target agent product or harness, add target metadata, explain the adapter choice, or offer cross-harness fallbacks.

Require the lead to spawn parallel subagents immediately for the smallest independent research, implementation, test, and review workstreams. Keep shared architecture and integration with the lead; use worktrees or disjoint ownership when parallel writers could conflict. Give critics isolated contexts containing the artifact location, requirements, selected bar, evidence contract, and scope, but no builder rationale. After each major wave, fan out strong critics across correctness and the project-relevant UX/visual, accessibility, performance, security, integration, and licensing dimensions. Require two independent critics for high-risk or highly subjective surfaces, collect all requested results, synthesize evidence, fix the largest material gap, and run a separate integration critic. Use an agent team only when it is already enabled and sustained peer coordination materially helps; ordinary subagents are the default.""",
}

ULTRACODE_DIRECTIVE = """Ultracode is explicitly enabled for this session. The completed execution prompt must state that Ultracode is on, but it still must not name the target agent product or harness. Require dynamic workflows for substantive parallel Gauntlet waves and ordinary subagents for narrow side tasks. Derive explicit workflow phases from real dependencies. Give every workflow agent a specific task, scope or file set, expected artifact, and evidence gate; never request an undifferentiated swarm. Separate builders from verifier/refuter agents, challenge findings adversarially before integration, and use a synthesis agent to rank evidence, deduplicate gaps, and select the next repair. Keep overlapping writes and shared architecture under one integration owner."""


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


def compose(
    template: str,
    brief: str,
    harness: str,
    platform: str,
    *,
    ultracode: bool = False,
) -> str:
    required = (
        "{{PROJECT_INPUT}}",
        "{{HARNESS_DIRECTIVES}}",
        "{{PLATFORM}}",
    )
    missing = [token for token in required if token not in template]
    if missing:
        raise ValueError(f"Generator template is missing placeholders: {', '.join(missing)}")
    if not brief:
        raise ValueError("The project brief is empty.")
    if harness not in HARNESS_DIRECTIVES:
        raise ValueError("Target harness is required and must be 'codex' or 'claude-code'.")
    if ultracode and harness != "claude-code":
        raise ValueError("--ultracode is valid only with --harness claude-code.")
    directives = HARNESS_DIRECTIVES[harness]
    if ultracode:
        directives = f"{directives}\n\n{ULTRACODE_DIRECTIVE}"
    return (
        template.replace("{{PROJECT_INPUT}}", brief)
        .replace("{{HARNESS_DIRECTIVES}}", directives)
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
        required=True,
        choices=tuple(HARNESS_DIRECTIVES),
        help="Required target command surface; never inferred from the current host",
    )
    parser.add_argument(
        "--platform",
        default="auto",
        choices=("auto", "website", "game", "ios-mobile", "pwa", "desktop", "hybrid"),
    )
    parser.add_argument(
        "--ultracode",
        action="store_true",
        help="Include the optional Ultracode-enabled workflow profile (claude-code only)",
    )
    parser.add_argument("--output", help="Write to this path instead of stdout")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        brief = read_brief(args.brief, args.text)
        template = ASSET_PATH.read_text(encoding="utf-8")
        result = compose(
            template,
            brief,
            args.harness,
            args.platform,
            ultracode=args.ultracode,
        )
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
