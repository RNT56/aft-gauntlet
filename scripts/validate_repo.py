#!/usr/bin/env python3
"""Validate the portable AFT Gauntlet repository without third-party packages."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "aft-gauntlet"

REQUIRED = (
    SKILL / "SKILL.md",
    SKILL / "agents" / "openai.yaml",
    SKILL / "assets" / "portable-generator.md",
    SKILL / "assets" / "project-brief-template.md",
    SKILL / "scripts" / "compose_prompt.py",
    SKILL / "references" / "kernel.md",
    SKILL / "references" / "harness-adapters.md",
    SKILL / "references" / "research-sources.md",
    SKILL / "references" / "integrations.md",
    SKILL / "references" / "websites.md",
    SKILL / "references" / "games.md",
    SKILL / "references" / "ios-mobile.md",
    SKILL / "references" / "pwa.md",
    SKILL / "references" / "desktop.md",
)

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def validate_required(errors: list[str]) -> None:
    for path in REQUIRED:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")


def validate_skill(errors: list[str]) -> None:
    path = SKILL / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
    if "\nname: aft-gauntlet\n" not in text:
        errors.append("SKILL.md name must be aft-gauntlet")
    description = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    if not description or len(description.group(1).strip()) < 40:
        errors.append("SKILL.md needs an informative description")


def validate_generator(errors: list[str]) -> None:
    path = SKILL / "assets" / "portable-generator.md"
    text = path.read_text(encoding="utf-8")
    for placeholder in ("{{PROJECT_INPUT}}", "{{TARGET_HARNESS}}", "{{PLATFORM}}"):
        if text.count(placeholder) != 1:
            errors.append(f"portable generator must contain {placeholder} exactly once")


def validate_local_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = raw.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(
                    f"broken local link in {path.relative_to(ROOT)}: {raw}"
                )


def validate_no_placeholders(errors: list[str]) -> None:
    allowed = {
        SKILL / "assets" / "portable-generator.md",
        SKILL / "assets" / "project-brief-template.md",
    }
    for path in ROOT.rglob("*.md"):
        if path in allowed or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if "[TODO" in text or "TODO:" in text:
            errors.append(f"unresolved TODO in {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    if not errors:
        validate_skill(errors)
        validate_generator(errors)
        validate_local_links(errors)
        validate_no_placeholders(errors)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
