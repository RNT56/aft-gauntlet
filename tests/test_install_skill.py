from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "install_skill.py"
SPEC = importlib.util.spec_from_file_location("install_skill", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class InstallSkillTests(unittest.TestCase):
    def test_user_targets_for_both_hosts(self) -> None:
        home = Path("/tmp/example-home")
        targets = MODULE.target_paths("both", "user", home=home, project=None)
        self.assertEqual(
            targets,
            [
                home / ".agents" / "skills" / "aft-gauntlet",
                home / ".claude" / "skills" / "aft-gauntlet",
            ],
        )

    def test_project_scope_requires_project(self) -> None:
        with self.assertRaisesRegex(ValueError, "--project"):
            MODULE.target_paths(
                "codex", "project", home=Path("/tmp/example-home"), project=None
            )

    def test_copy_install_and_safe_force_backup(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("first", encoding="utf-8")
            target = root / "target" / "aft-gauntlet"

            result = MODULE.install_one(
                source,
                target,
                mode="copy",
                force=False,
                dry_run=False,
                stamp="20260809T000000Z",
            )
            self.assertEqual(result.action, "copy")
            self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "first")

            with self.assertRaises(FileExistsError):
                MODULE.install_one(
                    source,
                    target,
                    mode="copy",
                    force=False,
                    dry_run=False,
                    stamp="20260809T000000Z",
                )

            (source / "SKILL.md").write_text("second", encoding="utf-8")
            replaced = MODULE.install_one(
                source,
                target,
                mode="copy",
                force=True,
                dry_run=False,
                stamp="20260809T000000Z",
            )
            self.assertIsNotNone(replaced.backup)
            assert replaced.backup is not None
            self.assertEqual(replaced.backup.parent, root / "skill-backups")
            self.assertFalse(any(target.parent.glob("aft-gauntlet.backup-*")))
            self.assertEqual(
                (replaced.backup / "SKILL.md").read_text(encoding="utf-8"), "first"
            )
            self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "second")

    def test_symlink_install_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("skill", encoding="utf-8")
            target = root / "target" / "aft-gauntlet"

            MODULE.install_one(
                source,
                target,
                mode="symlink",
                force=False,
                dry_run=False,
                stamp="20260809T000000Z",
            )
            result = MODULE.install_one(
                source,
                target,
                mode="symlink",
                force=False,
                dry_run=False,
                stamp="20260809T000000Z",
            )
            self.assertEqual(result.action, "already-linked")

    def test_failed_replacement_restores_backup(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("new", encoding="utf-8")
            target = root / "target" / "aft-gauntlet"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("original", encoding="utf-8")

            def partial_failure(_source: Path, destination: Path, **_kwargs: object) -> None:
                destination.mkdir()
                (destination / "partial").write_text("partial", encoding="utf-8")
                raise OSError("simulated copy failure")

            with mock.patch.object(MODULE.shutil, "copytree", side_effect=partial_failure):
                with self.assertRaisesRegex(OSError, "simulated"):
                    MODULE.install_one(
                        source,
                        target,
                        mode="copy",
                        force=True,
                        dry_run=False,
                        stamp="20260809T000000Z",
                    )

            self.assertEqual(
                (target / "SKILL.md").read_text(encoding="utf-8"), "original"
            )
            self.assertFalse((target / "partial").exists())


if __name__ == "__main__":
    unittest.main()
