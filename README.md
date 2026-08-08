# AFT Gauntlet

A modular generator for research-backed Gauntlet Loop prompts. It supports websites and local businesses, games, iOS/mobile apps, PWAs, macOS/Windows desktop apps, and hybrid products.

The package keeps the universal Builder–Critic loop separate from platform-specific quality gates. A generated prompt gives the lead agent a concrete destination, real comparison bars, relevant assets and integrations, and evidence requirements while leaving architecture and decomposition to the agent.

## Use with Codex

Install or link `skills/aft-gauntlet` into your Codex skills directory, then ask:

```text
Use $aft-gauntlet to generate a Gauntlet prompt for <project brief>.
```

The skill reads only the relevant platform packs. It uses Codex's native goal and subagent capabilities when the generated prompt is executed and does not assume `/loop` exists on every Codex surface.

## Use with Claude Code or another agent

Copy the contents of [`skills/aft-gauntlet/assets/portable-generator.md`](skills/aft-gauntlet/assets/portable-generator.md), replace the input placeholders, and send it to the agent. The generated execution prompt detects native goal, subagent, and continuation capabilities. Claude Code may use `/loop` when the installed version supports it.

You can also compose a ready-to-paste generator prompt:

```bash
python3 skills/aft-gauntlet/scripts/compose_prompt.py \
  --brief my-project.md \
  --harness auto \
  --platform auto \
  --output generated/my-project-generator.md
```

Use `--brief -` for stdin or `--text` for a short inline brief. Platform choices are `auto`, `website`, `game`, `ios-mobile`, `pwa`, `desktop`, and `hybrid`.

The script performs deterministic prompt assembly. The receiving agent still performs live research before producing the final Gauntlet execution prompt.

Example briefs for each platform family live in [`examples/`](examples/). They are suitable for smoke-testing the generator or as starting points for new projects.

## Package structure

```text
skills/aft-gauntlet/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── portable-generator.md
│   └── project-brief-template.md
├── references/
│   ├── kernel.md
│   ├── harness-adapters.md
│   ├── research-sources.md
│   ├── integrations.md
│   ├── websites.md
│   ├── games.md
│   ├── ios-mobile.md
│   ├── pwa.md
│   └── desktop.md
└── scripts/compose_prompt.py
```

## Validation

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_repo.py
python3 /path/to/skill-creator/scripts/quick_validate.py skills/aft-gauntlet
```

GitHub Actions runs the portable tests and repository validator on pushes and pull requests.
