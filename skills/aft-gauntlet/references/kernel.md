# Universal Gauntlet Kernel

## Purpose

Preserve the Gauntlet Loop while allowing the lead agent to exercise judgment. Specify the destination, inspectable bar, constraints, ingredient pool, and evidence—not the route.

## Required Mechanics

1. **Persistent objective:** Register the concrete outcome with the harness-native goal/task mechanism when available.
2. **Lead-owned decomposition:** The lead agent splits the artifact into the smallest parts that can be independently improved and judged.
3. **Specialist builders:** Assign bounded work to agents suited to each problem.
4. **Independent critics:** Use separate agents with fresh context. Do not provide builder rationale or self-evaluation.
5. **Real artifact inspection:** Critics inspect the running, rendered, recorded, installed, packaged, measured, or tested artifact.
6. **Concrete comparison:** Compare against an actual reference, product, test suite, benchmark, or measurable target. Use blind A/B judgment when possible.
7. **Largest-gap repair:** If ours loses, identify the single highest-impact gap, return it to a builder, fix it, and judge again.
8. **Unbounded improvement:** Do not choose an arbitrary round count. Continue until the evidence clears the bar, the user stops, or a real authority blocker occurs.
9. **Smoothing pass:** After major waves, use a fresh integration agent to resolve inconsistency without redesigning successful work.
10. **Live receipts:** Maintain a progress artifact showing references, outputs, verdicts, open gaps, tests, metrics, and unresolved assumptions.

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

A surface passes only when a fresh critic finds no material gap and it still succeeds inside the integrated artifact. Use a second independent critic for high-risk or highly subjective surfaces.

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
