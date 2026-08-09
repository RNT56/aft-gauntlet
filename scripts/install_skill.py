#!/usr/bin/env python3
"""Install the shared AFT Gauntlet skill for Codex, Claude Code, or both."""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_SOURCE = ROOT / "skills" / "aft-gauntlet"
SKILL_NAME = "aft-gauntlet"


@dataclass(frozen=True)
class InstallResult:
    target: Path
    action: str
    backup: Path | None = None


def target_paths(
    host: str,
    scope: str,
    *,
    home: Path,
    project: Path | None,
) -> list[Path]:
    if scope == "project" and project is None:
        raise ValueError("--project is required when --scope project is used.")

    if scope == "user":
        base = home
    else:
        assert project is not None
        base = project.resolve()
    roots = {
        "codex": base / ".agents" / "skills",
        "claude-code": base / ".claude" / "skills",
    }
    selected = ("codex", "claude-code") if host == "both" else (host,)
    return [roots[item] / SKILL_NAME for item in selected]


def next_backup_path(target: Path, stamp: str) -> Path:
    backup_root = target.parent.parent / "skill-backups"
    candidate = backup_root / f"{target.name}-{stamp}"
    suffix = 2
    while candidate.exists() or candidate.is_symlink():
        candidate = backup_root / f"{target.name}-{stamp}-{suffix}"
        suffix += 1
    return candidate


def is_current_symlink(source: Path, target: Path) -> bool:
    return target.is_symlink() and target.resolve() == source.resolve()


def install_one(
    source: Path,
    target: Path,
    *,
    mode: str,
    force: bool,
    dry_run: bool,
    stamp: str,
) -> InstallResult:
    if is_current_symlink(source, target):
        return InstallResult(target, "already-linked")

    exists = target.exists() or target.is_symlink()
    backup: Path | None = None
    if exists and not force:
        raise FileExistsError(
            f"Target already exists: {target}. Re-run with --force to back it up first."
        )
    if exists:
        backup = next_backup_path(target, stamp)

    if dry_run:
        return InstallResult(target, f"would-{mode}", backup)

    target.parent.mkdir(parents=True, exist_ok=True)
    if backup is not None:
        backup.parent.mkdir(parents=True, exist_ok=True)
        target.rename(backup)

    try:
        if mode == "symlink":
            target.symlink_to(source.resolve(), target_is_directory=True)
        else:
            shutil.copytree(
                source,
                target,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
            )
    except Exception:
        if target.is_symlink():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
        if backup is not None:
            backup.rename(target)
        raise

    return InstallResult(target, mode, backup)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install AFT Gauntlet as a native Codex and/or Claude Code skill."
    )
    parser.add_argument(
        "--host",
        choices=("codex", "claude-code", "both"),
        default="both",
    )
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project", type=Path, help="Project root for project scope")
    parser.add_argument("--mode", choices=("copy", "symlink"), default="copy")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Move an existing target to a non-discoverable timestamped backup before installing",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not (SKILL_SOURCE / "SKILL.md").is_file():
        print(f"error: missing skill source: {SKILL_SOURCE}", file=sys.stderr)
        return 2

    try:
        targets = target_paths(
            args.host,
            args.scope,
            home=Path.home(),
            project=args.project,
        )
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        results = [
            install_one(
                SKILL_SOURCE,
                target,
                mode=args.mode,
                force=args.force,
                dry_run=args.dry_run,
                stamp=stamp,
            )
            for target in targets
        ]
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    for result in results:
        print(f"{result.action}: {result.target}")
        if result.backup is not None:
            verb = "would back up" if args.dry_run else "backed up"
            print(f"  {verb}: {result.backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
