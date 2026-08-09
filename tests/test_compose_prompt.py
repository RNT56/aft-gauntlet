from __future__ import annotations

import importlib.util
import subprocess
import sys
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
        template = "D={{HARNESS_DIRECTIVES}} P={{PLATFORM}} B={{PROJECT_INPUT}}"
        result = MODULE.compose(template, "Build a racing game", "codex", "game")
        folded = result.casefold()
        self.assertIn("/goal", result)
        self.assertIn("P=game B=Build a racing game\n", result)
        self.assertNotIn("codex", folded)
        self.assertNotIn("claude code", folded)

    def test_rejects_empty_brief(self) -> None:
        template = "{{HARNESS_DIRECTIVES}} {{PLATFORM}} {{PROJECT_INPUT}}"
        with self.assertRaisesRegex(ValueError, "empty"):
            MODULE.compose(template, "", "codex", "auto")

    def test_rejects_incomplete_template(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing placeholders"):
            MODULE.compose("{{PROJECT_INPUT}}", "Brief", "codex", "auto")

    def test_rejects_missing_or_generic_harness(self) -> None:
        template = "{{HARNESS_DIRECTIVES}} {{PLATFORM}} {{PROJECT_INPUT}}"
        for harness in ("", "auto", "other", "claude"):
            with self.subTest(harness=harness):
                with self.assertRaisesRegex(ValueError, "required"):
                    MODULE.compose(template, "Brief", harness, "auto")

    def test_cli_requires_harness(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--text", "Build a game"],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--harness", result.stderr)

    def test_ultracode_profile_is_explicit_and_task_specific(self) -> None:
        template = "{{HARNESS_DIRECTIVES}} {{PLATFORM}} {{PROJECT_INPUT}}"
        result = MODULE.compose(
            template,
            "Build a complex migration",
            "claude-code",
            "auto",
            ultracode=True,
        )
        self.assertIn("Ultracode is explicitly enabled", result)
        self.assertIn("specific task, scope or file set", result)
        self.assertIn("verifier/refuter agents", result)
        self.assertNotIn("codex", result.casefold())
        self.assertNotIn("claude code", result.casefold())

    def test_ultracode_rejected_for_other_profile(self) -> None:
        template = "{{HARNESS_DIRECTIVES}} {{PLATFORM}} {{PROJECT_INPUT}}"
        with self.assertRaisesRegex(ValueError, "only"):
            MODULE.compose(
                template,
                "Build a game",
                "codex",
                "auto",
                ultracode=True,
            )

    def test_all_examples_compose_for_codex_and_claude_code(self) -> None:
        template = (
            ROOT
            / "skills"
            / "aft-gauntlet"
            / "assets"
            / "portable-generator.md"
        ).read_text(encoding="utf-8")
        examples = sorted((ROOT / "examples").glob("*.md"))
        self.assertGreaterEqual(len(examples), 5)

        for example in examples:
            brief = example.read_text(encoding="utf-8")
            for harness in ("codex", "claude-code"):
                with self.subTest(example=example.name, harness=harness):
                    result = MODULE.compose(template, brief, harness, "auto")
                    self.assertIn(brief, result)
                    self.assertNotIn("{{PROJECT_INPUT}}", result)
                    self.assertNotIn("{{HARNESS_DIRECTIVES}}", result)
                    self.assertNotIn("{{PLATFORM}}", result)
                    self.assertNotIn("Target harness", result)
                    self.assertNotIn("codex", result.casefold())
                    self.assertNotIn("claude code", result.casefold())
                    if harness == "codex":
                        self.assertIn("first line starts `/goal Complete`", result)
                        self.assertIn("native subagents immediately", result)
                        self.assertNotIn("/loop", result)
                        self.assertNotIn("Ultracode", result)
                    else:
                        self.assertIn("first line starts `/loop Continue`", result)
                        self.assertIn("spawn parallel subagents immediately", result)
                        self.assertNotIn("/goal", result)
                        self.assertNotIn("Ultracode", result)


if __name__ == "__main__":
    unittest.main()
