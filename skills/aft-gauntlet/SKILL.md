---
name: aft-gauntlet
description: Generate or refine research-backed Gauntlet Loop prompts for autonomous agents building websites, games, iOS/mobile apps, PWAs, macOS/Windows desktop apps, and hybrid products. Use when Codex must turn a sparse or detailed project brief into one executable prompt with live comparison research, asset and component sources, integrations, independent builder/critic loops, harness-aware goal persistence, evidence gates, and platform-specific quality criteria.
---

# AFT Gauntlet

Generate one ready-to-paste Gauntlet execution prompt. Do not build the requested project unless the user explicitly asks to run the generated prompt.

## Workflow

1. Inspect the conversation, supplied files, repository, and project brief. Preserve explicit requirements and distinguish facts, assumptions, and unknowns.
2. Read [kernel.md](references/kernel.md), [harness-adapters.md](references/harness-adapters.md), and [research-sources.md](references/research-sources.md).
3. Read only the relevant platform packs:
   - Websites, SaaS, commerce, or local businesses: [websites.md](references/websites.md)
   - Games on any runtime: [games.md](references/games.md)
   - Native or cross-platform mobile, especially iOS: [ios-mobile.md](references/ios-mobile.md)
   - Installable/offline web apps: [pwa.md](references/pwa.md) plus `websites.md`
   - macOS, Windows, Electron, Tauri, or native desktop: [desktop.md](references/desktop.md)
   - Hybrid products: read every applicable pack and require separate platform gates plus a cross-platform integration critic.
4. If the brief includes external services, read [integrations.md](references/integrations.md).
5. Research current competitors, exemplary products, components, assets, and official integration documentation. Open the actual pages; do not rely on snippets or stale memory.
6. Use [portable-generator.md](assets/portable-generator.md) as the output contract and quality checklist, not as text to repeat wholesale.
7. Return one complete prompt only. Keep it outcome-led and give the lead agent freedom to choose architecture, decomposition, and implementation.

## Research Rules

- Find concrete, inspectable bars in three layers when relevant: direct market competitors, best-in-class experience references, and feature-level product references.
- Link exact relevant pages, flows, components, templates, assets, or official docs. Do not use catalog homepages when a useful deep link exists.
- Include only sources material to this project. Require a resource scout to evaluate them; never turn the output into a component checklist.
- Verify current availability and licensing. Mark paid, subscription, attribution, editorial-only, or unknown terms.
- Research official documentation for APIs and integrations. Specify consent, credentials, failure states, privacy, security, and fallbacks.
- Never fabricate business claims, users, staff, reviews, metrics, awards, prices, availability, legal text, or credentials.

## Prompt Rules

- Start with the goal, quality bar, and hard constraints—not a prescribed implementation plan.
- Require immediate fan-out when subagents are available. The lead agent chooses the smallest independently judgeable workstreams.
- Assign each important surface to a builder and a separate fresh-context critic. The builder never grades itself.
- Make critics inspect the real artifact: pixels, recordings, playable builds, installed apps, tests, traces, benchmarks, or packaged binaries.
- Prefer blind A/B comparisons. A failed critic returns the largest meaningful gap, which is fixed and judged again.
- Do not set a fixed iteration count. Require integration/smoothing passes after major waves and a live progress artifact.
- Adapt goal and loop instructions to the detected harness. Never emit unsupported slash commands as if universal.
- Define evidence-based exit gates. Compilation, one approval, or completion of a component list is never sufficient.
- Keep a normal generated prompt around 800–1,600 words. Expand only when project complexity truly requires it.
- Ask at most three questions, only when the answer cannot be researched or safely inferred and would materially change the result.

## Website Composition Rule

For visual websites, treat full-page spatial and background composition as a judged artifact. Reject default stacks of interchangeable rectangular sections unless the selected art direction intentionally demands them. Derive layers, transitions, texture, rhythm, and motion from the brand, subject, place, or product; judge full-page desktop and mobile renders.

## Output Contract

Return only the generated Gauntlet prompt. Do not add an introduction, research notes, alternative versions, or next steps.

When a reusable standalone prompt file is requested, run:

```bash
python3 scripts/compose_prompt.py --brief <brief.md> --harness auto --platform auto --output <gauntlet-prompt.md>
```

Then replace or enrich the script-produced research placeholders with verified live sources before delivery.
