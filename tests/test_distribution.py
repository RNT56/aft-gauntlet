from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def test_full_mit_license(self) -> None:
        expected = """MIT License

Copyright (c) 2026 RNT56

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        self.assertEqual((ROOT / "LICENSE").read_text(encoding="utf-8"), expected)

    def test_plugin_versions_and_names_match(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        paths = (
            ROOT / ".codex-plugin" / "plugin.json",
            ROOT / ".claude-plugin" / "plugin.json",
        )
        for path in paths:
            manifest = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["name"], "aft-gauntlet")
            self.assertEqual(manifest["version"], version)

    def test_claude_marketplace_points_to_repository(self) -> None:
        marketplace = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        [plugin] = marketplace["plugins"]
        self.assertEqual(
            plugin["source"],
            {"source": "github", "repo": "RNT56/aft-gauntlet"},
        )

    def test_shared_skill_contains_supporting_resources(self) -> None:
        skill = ROOT / "skills" / "aft-gauntlet"
        self.assertTrue((skill / "SKILL.md").is_file())
        self.assertTrue((skill / "agents" / "openai.yaml").is_file())
        self.assertGreaterEqual(len(list((skill / "references").glob("*.md"))), 9)
        self.assertTrue((skill / "scripts" / "compose_prompt.py").is_file())

    def test_skill_requires_explicit_harness_selection(self) -> None:
        text = (ROOT / "skills" / "aft-gauntlet" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Do not infer it from the current app", text)
        self.assertIn(
            "Which target harness should the Gauntlet prompt use: Codex or Claude Code?",
            text,
        )
        self.assertIn("Then stop; do not research or generate a prompt yet", text)

    def test_brand_invention_requires_explicit_original_authority(self) -> None:
        skill = (ROOT / "skills" / "aft-gauntlet" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        generator = (
            ROOT / "skills" / "aft-gauntlet" / "assets" / "portable-generator.md"
        ).read_text(encoding="utf-8")
        website = (
            ROOT / "skills" / "aft-gauntlet" / "references" / "websites.md"
        ).read_text(encoding="utf-8")
        brief_template = (
            ROOT / "skills" / "aft-gauntlet" / "assets" / "project-brief-template.md"
        ).read_text(encoding="utf-8")

        self.assertIn("original user input explicitly asks", skill)
        self.assertIn("not as permission to invent", skill)
        self.assertIn("original project input explicitly requests brand invention", generator)
        self.assertIn("If and only if the original user input", website)
        self.assertIn("omission means no", brief_template)


if __name__ == "__main__":
    unittest.main()
