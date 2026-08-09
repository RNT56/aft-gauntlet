#!/usr/bin/env python3
"""Validate the portable, dual-host AFT Gauntlet repository."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "aft-gauntlet"

REQUIRED = (
    ROOT / "LICENSE",
    ROOT / "VERSION",
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / "scripts" / "install_skill.py",
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
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
MIT_LICENSE = """MIT License

Copyright (c) 2026 RNT56

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the \"Software\"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def validate_required(errors: list[str]) -> None:
    for path in REQUIRED:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")


def validate_license(errors: list[str]) -> None:
    if (ROOT / "LICENSE").read_text(encoding="utf-8") != MIT_LICENSE:
        errors.append("LICENSE must contain the complete MIT license for 2026 RNT56")


def validate_skill(errors: list[str]) -> None:
    path = SKILL / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append("SKILL.md must start with YAML frontmatter")
        return

    fields = {
        line.split(":", 1)[0].strip()
        for line in match.group(1).splitlines()
        if ":" in line
    }
    if fields != {"name", "description"}:
        errors.append("SKILL.md frontmatter must contain only name and description")
    if "\nname: aft-gauntlet\n" not in text:
        errors.append("SKILL.md name must be aft-gauntlet")

    description = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    if not description or len(description.group(1).strip()) < 80:
        errors.append("SKILL.md needs an informative description")
    elif not all(name in description.group(1) for name in ("Codex", "Claude Code")):
        errors.append("SKILL.md description must advertise both Codex and Claude Code")

    if "python3 scripts/compose_prompt.py" in text:
        errors.append("SKILL.md must not assume the working directory is the skill root")


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"JSON root must be an object: {path.relative_to(ROOT)}")
        return {}
    return value


def validate_manifests(errors: list[str]) -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER_RE.fullmatch(version):
        errors.append("VERSION must contain strict semantic versioning")

    codex = load_json(ROOT / ".codex-plugin" / "plugin.json", errors)
    claude = load_json(ROOT / ".claude-plugin" / "plugin.json", errors)
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json", errors)

    for label, manifest in (("Codex", codex), ("Claude", claude)):
        if manifest.get("name") != "aft-gauntlet":
            errors.append(f"{label} plugin name must be aft-gauntlet")
        if manifest.get("version") != version:
            errors.append(f"{label} plugin version must match VERSION")
        if not manifest.get("description"):
            errors.append(f"{label} plugin needs a description")
        author = manifest.get("author")
        if not isinstance(author, dict) or not author.get("name"):
            errors.append(f"{label} plugin needs author.name")

    if codex.get("skills") != "./skills/":
        errors.append("Codex plugin must expose ./skills/")
    interface = codex.get("interface")
    if not isinstance(interface, dict):
        errors.append("Codex plugin needs interface metadata")
    else:
        required_interface = {
            "displayName",
            "shortDescription",
            "longDescription",
            "developerName",
            "category",
            "capabilities",
            "defaultPrompt",
        }
        missing = sorted(required_interface - interface.keys())
        if missing:
            errors.append(f"Codex plugin interface is missing: {', '.join(missing)}")

    if marketplace.get("name") != "aft-gauntlet":
        errors.append("Claude marketplace name must be aft-gauntlet")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        errors.append("Claude marketplace must contain exactly one plugin")
        return
    entry = plugins[0]
    if not isinstance(entry, dict) or entry.get("name") != "aft-gauntlet":
        errors.append("Claude marketplace plugin name must be aft-gauntlet")
        return
    if entry.get("version") != version:
        errors.append("Claude marketplace plugin version must match VERSION")
    source = entry.get("source")
    if source != {"source": "github", "repo": "RNT56/aft-gauntlet"}:
        errors.append("Claude marketplace must source RNT56/aft-gauntlet")


def validate_generator(errors: list[str]) -> None:
    path = SKILL / "assets" / "portable-generator.md"
    text = path.read_text(encoding="utf-8")
    for placeholder in (
        "{{PROJECT_INPUT}}",
        "{{HARNESS_DIRECTIVES}}",
        "{{PLATFORM}}",
    ):
        if text.count(placeholder) != 1:
            errors.append(f"portable generator must contain {placeholder} exactly once")

    composer = (SKILL / "scripts" / "compose_prompt.py").read_text(encoding="utf-8")
    if 'required=True' not in composer or '"codex"' not in composer or '"claude-code"' not in composer:
        errors.append("composer must require an explicit codex or claude-code harness")
    if '"auto", "codex"' in composer or '"other"' in composer:
        errors.append("composer must not accept inferred or generic harness targets")
    for forbidden in ("Target harness:", "Codex", "Claude Code"):
        if forbidden in text:
            errors.append(
                f"portable generator must not disclose the target harness: {forbidden}"
            )
    if "--ultracode" not in composer or "ULTRACODE_DIRECTIVE" not in composer:
        errors.append("composer must support the explicit optional Ultracode profile")
    brand_rules = (
        "missing brand, project name, or business identity as unknown",
        "Only when the original project input explicitly requests brand invention",
        "creative concepts, not facts about an existing business",
    )
    for phrase in brand_rules:
        if phrase not in text:
            errors.append(f"portable generator is missing brand authority rule: {phrase}")


def validate_readme(errors: list[str]) -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    required_phrases = (
        "~/.agents/skills/aft-gauntlet",
        "~/.claude/skills/aft-gauntlet",
        "$aft-gauntlet",
        "/aft-gauntlet",
        "claude --plugin-dir .",
        "Publication status",
        "Harness selection is mandatory",
        "--harness codex",
        "--harness claude-code",
        "--ultracode",
        "harness-silent",
        "MIT License",
        "invent a brand",
    )
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"README is missing cross-host guidance: {phrase}")


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
                errors.append(f"broken local link in {path.relative_to(ROOT)}: {raw}")


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
        validate_license(errors)
        validate_skill(errors)
        validate_manifests(errors)
        validate_generator(errors)
        validate_readme(errors)
        validate_local_links(errors)
        validate_no_placeholders(errors)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("Repository validation passed for Codex and Claude Code.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
