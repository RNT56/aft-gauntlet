from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "aft-gauntlet" / "scripts" / "compose_prompt.py"
SPEC = importlib.util.spec_from_file_location("compose_prompt", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ComposePromptTests(unittest.TestCase):
    def test_replaces_all_placeholders(self) -> None:
        template = "H={{TARGET_HARNESS}} P={{PLATFORM}} B={{PROJECT_INPUT}}"
        result = MODULE.compose(template, "Build a racing game", "codex", "game")
        self.assertEqual(result, "H=codex P=game B=Build a racing game\n")

    def test_rejects_empty_brief(self) -> None:
        template = "{{TARGET_HARNESS}} {{PLATFORM}} {{PROJECT_INPUT}}"
        with self.assertRaisesRegex(ValueError, "empty"):
            MODULE.compose(template, "", "auto", "auto")

    def test_rejects_incomplete_template(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing placeholders"):
            MODULE.compose("{{PROJECT_INPUT}}", "Brief", "auto", "auto")


if __name__ == "__main__":
    unittest.main()
