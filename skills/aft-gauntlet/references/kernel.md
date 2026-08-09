# Universal Gauntlet Kernel

## Purpose

Preserve the Gauntlet Loop while allowing the lead agent to exercise judgment. Specify the destination, inspectable bar, constraints, ingredient pool, and evidence—not the route.

## Required Mechanics

1. **Native continuation:** Use the selected harness adapter's required session command from the first line; do not offer cross-harness fallbacks.
2. **Lead-owned decomposition:** The lead agent splits the artifact into the smallest parts that can be independently improved and judged, retaining shared architecture and integration.
3. **Immediate parallel fan-out:** Spawn native subagents for independent research, building, testing, and review workstreams. Avoid conflicting concurrent writes.
4. **Specialist builders:** Assign bounded work to agents suited to each problem.
5. **Independent critics:** Use separate agents with fresh context and strong reasoning. Do not provide builder rationale or self-evaluation.
6. **Real artifact inspection:** Critics inspect the running, rendered, recorded, installed, packaged, measured, or tested artifact.
7. **Concrete comparison:** Compare against an actual reference, product, test suite, benchmark, or measurable target. Use blind A/B judgment when possible.
8. **Largest-gap repair:** If ours loses, identify the single highest-impact gap, return it to a builder, fix it, and judge again with a new critic.
9. **Unbounded improvement:** Do not choose an arbitrary round count. Continue until the evidence clears the bar, the user stops, or a real authority blocker occurs.
10. **Smoothing pass:** After major waves, use a fresh integration agent to resolve inconsistency without redesigning successful work.
11. **Live receipts:** Maintain a progress artifact showing references, outputs, verdicts, open gaps, tests, metrics, and unresolved assumptions.

## Quality-Bar Model

Use several narrow bars instead of one vague aspiration:

- **Market truth:** Real competitors reveal expected offers, language, trust, and workflows.
- **Experience quality:** Best-in-class products reveal visual, interaction, usability, and storytelling quality.
- **Feature quality:** A strong real product or technical reference supplies a bar for each unusual feature.
- **Engineering quality:** Tests, budgets, profiles, failure recovery, security, and accessibility establish nonvisual bars.

Tell each critic which dimensions the reference judges. Never ask a critic merely whether work is “good.”

## Critic Contract

Each verdict should contain:

- Winner: ours or reference/threshold
- Confidence
- Evidence from the actual artifact
- Largest meaningful gap
- A testable acceptance condition for the next round

A surface passes only when a fresh critic finds no material gap and it still succeeds inside the integrated artifact. Use a second independent critic for high-risk or highly subjective surfaces. After every major wave, fan out reviewers across correctness and the project-relevant visual/UX, accessibility, performance, security, integration, and licensing dimensions; then run a separate integration critic.

## Progress Artifact

Select an appropriate format: HTML dashboard, Markdown ledger, screenshots directory, build report, test dashboard, or playable capture gallery. Include:

- Active workstreams and owners
- Current artifact and comparison references
- Latest critic verdicts
- Selected/rejected assets and components
- Open risks and assumptions
- Functional, accessibility, performance, security, and licensing status
- Items requiring user or owner confirmation

## Exit Conditions

Do not pass because the project compiles, a hero looks polished, planned pieces exist, tests are shallowly green, or one critic approves. Complete only when:

- Required functionality is verified in the real artifact.
- Relevant quality bars are cleared with evidence.
- Integration and platform-specific gates pass.
- No material critic gap remains.
- Unverified assumptions and launch blockers are disclosed.
- No required work remains.

## Prompt Shape

Generated prompts should normally contain, in compact prose:

1. Goal and project truth
2. Non-negotiable user constraints
3. Research-backed references with exact links and judging dimensions
4. Curated asset/component/integration candidates with exact links
5. Harness-aware goal, fan-out, critic, and continuation rules
6. Credibility, licensing, safety, and progress requirements
7. Project-specific gates and terminal condition

Avoid detailed page outlines, schemas, subagent rosters, or animation timelines unless the user explicitly requires them.
