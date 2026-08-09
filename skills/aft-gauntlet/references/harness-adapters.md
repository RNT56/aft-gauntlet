# Harness Adapters

## Selection Invariant

The user must explicitly select `codex` or `claude-code` before generation. Never infer the target from the host running this skill. Generate one command-isolated prompt, not a portable prompt that asks the executing agent to discover its harness.

## Output Non-Disclosure Invariant

Harness selection is generator input, never execution-prompt content. The completed prompt must not contain `Codex`, `Claude Code`, `target harness`, adapter rationale, compatibility notes, or instructions to identify or fall back to another harness. Do not add a target label or harness metadata. The first-line native command already selects the execution behavior.

## Codex Adapter

The completed execution prompt's first character must be `/`, beginning a `/goal` command whose condition names a verifiable integrated end state. Put no title, preface, or code fence before it. Use Goal mode as the continuation engine across turns.

Required execution language:

- Tell the lead to spawn parallel native subagents immediately for independent research, implementation, test, and review workstreams without naming the host product.
- Keep shared architecture and integration with the lead. Parallelize writes only when ownership boundaries avoid conflicts.
- Pair every important builder output with a different, fresh-context critic. Give critics the artifact, requirements, selected reference or threshold, and required evidence; withhold builder rationale.
- Fan out strong critics after major waves. At minimum cover correctness and the relevant UX/visual, accessibility, performance, security, integration, and licensing risks. Give high-risk and subjective surfaces two independent critics.
- Require the lead to wait for requested critics, synthesize their evidence, repair the largest material gap, and send the rebuilt artifact to a new critic.
- Keep the `/goal` active until the integrated terminal gates are evidenced or a real authority blocker requires user input.

Forbidden in the emitted prompt:

- `/loop`, `/proactive`, `.claude/loop.md`, agent-team configuration from another command surface, either harness product name, or instructions to discover/fallback to another harness.

Current references:

- Goal mode: https://learn.chatgpt.com/use-cases/follow-goals
- Slash commands: https://learn.chatgpt.com/docs/reference/slash-commands
- Subagents: https://learn.chatgpt.com/docs/agent-configuration/subagents

## Claude Code Adapter

The completed execution prompt's first character must be `/`, beginning a self-paced `/loop <prompt>` command. Put no title, preface, or code fence before it. Do not include an interval: each loop iteration should read the live progress artifact, dispatch the highest-value independent work, collect fresh critic verdicts, repair the largest material gap, and stop only at the stated terminal condition or a real authority blocker.

Required execution language:

- Tell the lead to spawn parallel subagents immediately for independent research, implementation, test, and review workstreams without naming the host product.
- Use isolated subagent contexts for critics. The lead must pass the artifact location, requirements, selected bar, evidence contract, and scope—but not builder rationale.
- Keep shared architecture and integration with the lead. Use worktrees or disjoint file ownership when parallel writers could conflict.
- Fan out strong critics after major waves. At minimum cover correctness and the relevant UX/visual, accessibility, performance, security, integration, and licensing risks. Give high-risk and subjective surfaces two independent critics.
- Require the lead to collect all requested critic results, synthesize evidence, repair the largest material gap, and send the rebuilt artifact to a new critic.
- Use an agent team only when that capability is already enabled and sustained peer coordination materially helps; ordinary subagents remain the default.

### Optional Ultracode Profile

Apply this profile only when the user explicitly states that Ultracode is enabled. The emitted prompt may name `Ultracode`, but still must not name the harness product.

- State that Ultracode is on for the session; do not instruct the executing agent to enable it from inside the `/loop` prompt.
- Require dynamic workflows for substantive, parallel Gauntlet waves. Use ordinary subagents for narrow side tasks that do not justify a workflow.
- Define workflow phases from actual dependencies. Give every agent a specific task, scope or file set, expected artifact, and evidence gate. Avoid an undifferentiated “spawn many agents” request.
- Separate builders from verifier/refuter agents. Use adversarial reviewers to challenge findings before integration and a synthesis agent to rank evidence, deduplicate gaps, and identify the next repair.
- Keep shared architecture and overlapping writes under one integration owner. Use isolated copies or disjoint ownership for parallel edits.
- Do not claim Ultracode is on when the user has not confirmed it.

Current Ultracode and workflow reference: https://code.claude.com/docs/en/workflows

Forbidden in the emitted prompt:

- `/goal`, commands or configuration from another command surface, either harness product name, or instructions to discover/fallback to another harness.

Current references:

- Loop command: https://code.claude.com/docs/en/commands
- Subagents and parallel agents: https://code.claude.com/docs/en/agents
- Custom subagents: https://code.claude.com/docs/en/sub-agents
- Agent teams: https://code.claude.com/docs/en/agent-teams

## Safety

Persistence does not broaden authorization. Repeated loops may continue only previously authorized work. Do not purchase assets, publish, message users, charge accounts, alter production data, or create external resources unless explicitly authorized.
