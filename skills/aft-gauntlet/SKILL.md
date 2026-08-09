---
name: aft-gauntlet
description: Generate or refine research-backed Gauntlet Loop prompts explicitly targeted to Codex or Claude Code for websites, games, iOS/mobile apps, PWAs, macOS/Windows desktop apps, and hybrid products. Use when a project brief must become one executable prompt with native session commands, live comparison research, asset and component sources, integrations, parallel builders, strong fresh-context critics, evidence gates, and platform-specific quality criteria.
---

# AFT Gauntlet

Generate one ready-to-paste Gauntlet execution prompt. Do not build the requested project unless the user explicitly asks to run the generated prompt.

## Workflow

1. Require the user to name exactly one target harness: `codex` or `claude-code`. Do not infer it from the current app, shell, repository, or invocation syntax. If it is missing or ambiguous, ask only: “Which target harness should the Gauntlet prompt use: Codex or Claude Code?” Then stop; do not research or generate a prompt yet.
2. Inspect the conversation, supplied files, repository, and project brief. Preserve explicit requirements and distinguish facts, assumptions, and unknowns.
3. Read [kernel.md](references/kernel.md), [harness-adapters.md](references/harness-adapters.md), and [research-sources.md](references/research-sources.md). Select exactly one adapter and obey its required command form, optional capability profile, and output non-disclosure rules.
4. Read only the relevant platform packs:
   - Websites, SaaS, commerce, or local businesses: [websites.md](references/websites.md)
   - Games on any runtime: [games.md](references/games.md)
   - Native or cross-platform mobile, especially iOS: [ios-mobile.md](references/ios-mobile.md)
   - Installable/offline web apps: [pwa.md](references/pwa.md) plus `websites.md`
   - macOS, Windows, Electron, Tauri, or native desktop: [desktop.md](references/desktop.md)
   - Hybrid products: read every applicable pack and require separate platform gates plus a cross-platform integration critic.
5. If the brief includes external services, read [integrations.md](references/integrations.md).
6. Research current competitors, exemplary products, components, assets, and official integration documentation. Open the actual pages; do not rely on snippets or stale memory.
7. Use [portable-generator.md](assets/portable-generator.md) as the output contract and quality checklist, not as text to repeat wholesale.
8. Return one complete, harness-specific prompt only. Keep it outcome-led and give the lead agent freedom to choose architecture, decomposition, and implementation.

## Research Rules

- Find concrete, inspectable bars in three layers when relevant: direct market competitors, best-in-class experience references, and feature-level product references.
- Link exact relevant pages, flows, components, templates, assets, or official docs. Do not use catalog homepages when a useful deep link exists.
- Include only sources material to this project. Require a resource scout to evaluate them; never turn the output into a component checklist.
- Verify current availability and licensing. Mark paid, subscription, attribution, editorial-only, or unknown terms.
- Research official documentation for APIs and integrations. Specify consent, credentials, failure states, privacy, security, and fallbacks.
- Never fabricate business claims, users, staff, reviews, metrics, awards, prices, availability, legal text, or credentials.
- Treat an absent brand, name, or business identity as unknown, not as permission to invent it. Only when the original user input explicitly asks to invent or create a brand, name, or business concept may the generated prompt authorize original naming, positioning, narrative, voice, and visual identity grounded in the supplied data and current research.
- Keep invented brand elements clearly framed as creative proposals. Do not turn them into claims about an existing business or assert trademark, domain, social-handle, or legal availability without authorized current checks.

## Prompt Rules

- Start with the goal, quality bar, and hard constraints—not a prescribed implementation plan.
- Require immediate native subagent fan-out into the smallest independent workstreams that can proceed without file conflicts. The lead owns shared architecture and integration.
- Assign each important surface to a builder and a separate fresh-context critic. Critics receive the artifact, requirements, bar, and evidence—not builder rationale. The builder never grades itself.
- Require strong review fan-out after each major wave. Use the strongest suitable reasoning available for critics; cover correctness plus the relevant visual/UX, accessibility, performance, security, integration, and licensing risks. High-risk or subjective surfaces need two independent critics.
- Make critics inspect the real artifact: pixels, recordings, playable builds, installed apps, tests, traces, benchmarks, or packaged binaries.
- Prefer blind A/B comparisons. A failed critic returns the largest meaningful gap, which is fixed and judged again.
- Do not set a fixed iteration count. Require integration/smoothing passes after major waves and a live progress artifact.
- Make the prompt command-isolated for the user-selected harness. Its first character must be `/`; place no heading, preface, or code fence before the native command. A Codex-targeted prompt begins with and relies on `/goal`; it must not contain `/loop` or Claude-specific paths. A Claude-Code-targeted prompt begins with and relies on `/loop` without a fixed interval; it must not contain `/goal` or Codex-specific commands.
- Keep the emitted prompt harness-silent. Never write `Codex`, `Claude Code`, a target-harness label, adapter rationale, compatibility note, or instruction to detect/fallback to another harness. The native command is sufficient.
- If and only if the user explicitly says Ultracode is enabled for a Claude-Code-targeted prompt, state that Ultracode is on and require task-specific dynamic workflows. Give every workflow agent a bounded task, scope or files, expected artifact, and evidence gate; use separate verifier/refuter agents. Do not claim Ultracode is enabled otherwise.
- Define evidence-based exit gates. Compilation, one approval, or completion of a component list is never sufficient.
- Keep a normal generated prompt around 800–1,600 words. Expand only when project complexity truly requires it.
- Ask at most three questions, only when the answer cannot be researched or safely inferred and would materially change the result.

## Website Composition Rule

For visual websites, treat full-page spatial and background composition as a judged artifact. Reject default stacks of interchangeable rectangular sections unless the selected art direction intentionally demands them. Derive layers, transitions, texture, rhythm, and motion from the brand, subject, place, or product; judge full-page desktop and mobile renders.

## Output Contract

Return only the generated Gauntlet prompt. Do not add an introduction, research notes, alternative versions, or next steps.

When a reusable standalone prompt file is requested, run one of these explicit forms:

```bash
python3 <skill-directory>/scripts/compose_prompt.py --brief <brief.md> --harness codex --platform auto --output <gauntlet-prompt.md>
python3 <skill-directory>/scripts/compose_prompt.py --brief <brief.md> --harness claude-code --platform auto --output <gauntlet-prompt.md>
python3 <skill-directory>/scripts/compose_prompt.py --brief <brief.md> --harness claude-code --ultracode --platform auto --output <gauntlet-prompt.md>
```

Resolve `<skill-directory>` as the directory containing this `SKILL.md`; do not assume the agent's working directory is the skill directory. Then replace or enrich the script-produced research placeholders with verified live sources before delivery.
