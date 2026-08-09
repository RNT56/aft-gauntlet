# Repository guidance

- Keep the universal Gauntlet mechanics in `references/kernel.md`; do not duplicate them across platform packs.
- Keep platform-specific evaluation and asset guidance in the matching flat reference file.
- Preserve lead-agent freedom. Add hard constraints and inspectable bars, not rigid implementation recipes.
- Verify current external sources before changing registries or generated prompts.
- Keep the generator package host-portable, but require an explicit `codex` or `claude-code` target. Every emitted prompt must be harness-silent and command-isolated: `/goal` for Codex, `/loop` for Claude Code, plus native subagent fan-out. Apply the Ultracode workflow profile only when explicitly enabled.
- Use `apply_patch` for edits.
- Run `python3 -m unittest discover -s tests -v` and `python3 scripts/validate_repo.py` before handing off changes.
