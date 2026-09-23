# AFT Gauntlet

[![Validate](https://github.com/RNT56/aft-gauntlet/actions/workflows/validate.yml/badge.svg)](https://github.com/RNT56/aft-gauntlet/actions/workflows/validate.yml)
[![Version](https://img.shields.io/badge/version-1.3.0-blue)](VERSION)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](scripts)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-skill-D97757)](https://code.claude.com/docs/en/skills)
[![Codex](https://img.shields.io/badge/Codex-skill-412991)](https://learn.chatgpt.com/docs/build-skills)

![agent-skills](https://img.shields.io/badge/-agent--skills-informational) ![prompt-engineering](https://img.shields.io/badge/-prompt--engineering-informational) ![autonomous-agents](https://img.shields.io/badge/-autonomous--agents-informational) ![builder-critic](https://img.shields.io/badge/-builder--critic-informational) ![quality-gates](https://img.shields.io/badge/-quality--gates-informational)

AFT Gauntlet turns a project brief into one research-backed execution prompt for an autonomous coding agent. It keeps the universal Builder-Critic loop separate from platform-specific quality gates for websites and local businesses, games, iOS/mobile apps, PWAs, macOS/Windows desktop apps, and hybrid products.

The repository ships one standards-based skill that works natively in Codex and Claude Code, plus plugin manifests for both hosts and a deterministic prompt generator. Every generated prompt targets exactly one harness and uses only that harness's continuation and subagent model, while keeping the emitted execution prompt harness-silent.

## Requirements

- Codex or Claude Code with file, shell, and current web-research capabilities
- Python 3.10 or newer only when using the installer or deterministic prompt composer
- GitHub access to this repository while it remains private

The skill itself has no third-party Python dependencies.

## Install the native skill

From a clone of this repository, install the skill for both hosts:

```bash
python3 scripts/install_skill.py --host both --scope user
```

This copies the same skill to the current user locations:

- Codex: `~/.agents/skills/aft-gauntlet`
- Claude Code: `~/.claude/skills/aft-gauntlet`

Use `--mode symlink` to keep both installations linked to the clone. Existing installations are never overwritten silently. Add `--force` to move an existing target to a timestamped backup outside the discoverable `skills/` directory, under `.agents/skill-backups/` or `.claude/skill-backups/`.

For a repository-scoped installation:

```bash
python3 scripts/install_skill.py \
  --host both \
  --scope project \
  --project /path/to/project
```

Codex and Claude Code both support the same `SKILL.md` layout and supporting `references/`, `assets/`, and `scripts/` directories. See the official [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skill documentation](https://code.claude.com/docs/en/skills).

## Invoke it

In Codex:

```text
Use $aft-gauntlet to generate a Codex-targeted Gauntlet prompt for <project brief>.
```

In Claude Code:

```text
/aft-gauntlet Generate a Claude-Code-targeted Gauntlet prompt for <project brief>.
```

The skill generates the execution prompt; it does not build the requested product unless the user separately asks an agent to run that generated prompt.

### Required harness selection

Harness selection is mandatory. The user must say `codex` or `claude-code`; the skill never infers the target from the app in which it is running. If the target is missing, the skill asks one question and stops before research or generation.

- Codex output begins with `/goal` and relies on Codex Goal mode plus native parallel subagents. It contains no Claude Code loop command.
- Claude Code output begins with a self-paced `/loop` and relies on Claude Code subagents, using an agent team only when already enabled and genuinely helpful. It contains no Codex goal command.

The emitted execution prompt contains neither `Codex` nor `Claude Code`, no target-harness label, and no adapter explanation. Harness selection remains generator input only; the native first-line command carries the execution behavior.

Both variants require immediate fan-out, separate fresh-context critics, parallel specialist reviews after major waves, two critics for high-risk or subjective surfaces, and a final integration critic.

### Optional brand invention

A missing project, brand, or business name is treated as an unknown, not as permission to fabricate one. When the original brief explicitly asks to “invent a brand” or gives equivalent authority, the generated Gauntlet prompt may direct the execution team to develop and critically compare original naming, positioning, voice, narrative, and visual-identity concepts from the supplied context and current research.

Invented identities remain creative proposals. The prompt still forbids fabricated clients, staff, reviews, certifications, awards, performance claims, operational details, and legal text, and it cannot claim trademark, domain, or social-handle availability without authorized current checks.

### Optional Ultracode profile

When Ultracode is already enabled for the Claude Code session, add `--ultracode` to the deterministic composer or explicitly say so when invoking the skill. The output may state that Ultracode is on, but still does not name the harness. It requires dynamic workflows with dependency-aware phases, task-specific agent scopes, explicit artifacts and evidence gates, separate verifier/refuter agents, and one integration owner.

Enable the session setting before pasting the generated `/loop` prompt:

```text
/effort ultracode
```

The generator never claims Ultracode is enabled unless the user confirms it.

## Use it as a plugin

The repository root is a skills-only plugin for both hosts:

- Codex manifest: `.codex-plugin/plugin.json`
- Claude Code manifest: `.claude-plugin/plugin.json`
- Claude marketplace catalog: `.claude-plugin/marketplace.json`

Test the Claude Code plugin directly from the clone:

```bash
claude --plugin-dir .
```

Then invoke the namespaced skill:

```text
/aft-gauntlet:aft-gauntlet <project brief>
```

Users with repository access can also add its Claude marketplace and install it:

```text
/plugin marketplace add RNT56/aft-gauntlet
/plugin install aft-gauntlet@aft-gauntlet
```

The Codex manifest is ready for a local Codex marketplace or submission to the universal plugin directory. Until it is listed in a marketplace, the native-skill installer above is the direct local installation path.

## Portable generator

For an agent that does not load Agent Skills, compose a ready-to-paste generator prompt:

```bash
python3 skills/aft-gauntlet/scripts/compose_prompt.py \
  --brief my-project.md \
  --harness codex \
  --platform auto \
  --output generated/my-project-generator.md
```

For Claude Code, change the required selector to:

```bash
--harness claude-code
```

When that session already has Ultracode enabled:

```bash
--harness claude-code --ultracode
```

Use `--brief -` for stdin or `--text` for a short inline brief. The only harness choices are `codex` and `claude-code`; there is deliberately no `auto` or generic fallback. Platform choices are `auto`, `website`, `game`, `ios-mobile`, `pwa`, `desktop`, and `hybrid`.

The script performs deterministic assembly. The receiving agent must still inspect the target repository and perform live research before producing the final Gauntlet execution prompt.

## Package structure

```text
.
├── .codex-plugin/plugin.json
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── scripts/
│   ├── install_skill.py
│   └── validate_repo.py
├── skills/aft-gauntlet/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/
│   ├── references/
│   └── scripts/compose_prompt.py
└── tests/
```

Example briefs for every platform family live in `examples/`.

## Validate

Run the portable test suite and repository validator:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_repo.py
python3 -m py_compile \
  skills/aft-gauntlet/scripts/compose_prompt.py \
  scripts/install_skill.py \
  scripts/validate_repo.py
```

When the relevant development tools are installed, also run:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/aft-gauntlet
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
claude plugin validate --strict .claude-plugin/plugin.json
claude plugin validate --strict .claude-plugin/marketplace.json
```

GitHub Actions runs the portable checks across supported Python versions.

## License

AFT Gauntlet is distributed under the full [MIT License](LICENSE), copyright (c) 2026 RNT56.

## Publication status

The skill and both plugin manifests are complete for local use and MIT-licensed redistribution. Public availability still depends on making the source or release artifact accessible to intended users and completing any desired marketplace review.
