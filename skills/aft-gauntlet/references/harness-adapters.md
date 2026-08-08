# Harness Adapters

## General Rule

Inspect available capabilities first. Express intent portably and use native mechanisms only when they exist. The same prompt may be used in different environments.

## Codex

- Prefer `/plan` when the user wants to shape the objective before execution.
- Use `/goal` or the corresponding goal tool for a persistent objective when available.
- Use native subagent tools for independent, bounded workstreams.
- Goal mode supplies persistence; do not invent `/loop` in a Codex surface that does not expose it.
- Use the app's recurring task or monitor mechanism only when the user requested scheduled monitoring and the surface supports it.
- Current command reference: https://learn.chatgpt.com/docs/reference/slash-commands

## Claude Code

- Use its native goal mechanism when available.
- Use subagents with clean context for builders and critics.
- After initial fan-out, use `/loop <prompt>` or a project `.claude/loop.md` when supported and useful.
- A prompt-only `/loop` can choose the interval dynamically; a fixed interval is appropriate only when regular polling helps.
- Current scheduled-task reference: https://code.claude.com/docs/en/scheduled-tasks

## Other Agents

- Map goal persistence to the closest task, plan, run, thread, or workflow primitive.
- Map fan-out to child agents, parallel tasks, worktrees, or isolated sessions.
- Map continuation to a scheduler, monitor, recurring task, or inline Builder–Critic cycle.
- If no subagents exist, simulate separation with fresh contexts that do not receive builder rationale.
- If no loop exists, continue within the active task until the terminal condition is met.

## Portable Wording

Use language like:

> Inspect the capabilities of this harness. Register the objective with its native persistent goal mechanism when available. Fan out independent builders and fresh-context critics. After initial work begins, activate the native continuation or recurring-loop mechanism if one exists; otherwise run the cycle inline. Do not emit or pretend to execute unsupported commands.

## Safety

Persistence does not broaden authorization. Repeated loops may continue only previously authorized work. Do not purchase assets, publish, message users, charge accounts, alter production data, or create external resources unless explicitly authorized.
