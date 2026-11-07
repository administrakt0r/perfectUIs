# perfectUIs

This repository is the perfectUIs skill: incremental UI-quality instructions plus `scripts/perfectuis`. Artifacts stay branded `perfectuis` (`.perfectuis/backlog.md`, `scripts/perfectuis`). Do not add other design-tool brand names.

## Checks

- `python3 scripts/test_detect.py`
- `scripts/perfectuis detect --rules`
- `scripts/perfectuis detect --json <path>`
- `scripts/perfectuis update`

Detector findings are candidates. Do not weaken a test to hide a false positive; tighten the rule.

## Baseline

Skill upgrades follow `skill-improve.md`: extend existing rules, and do not re-add guidance that is already in the craft floor or detector. Inspect the relevant docs and detector before editing. Keep the change small and consistent with the six-stage flow in `SKILL.md`. Preserve the backlog format and detector JSON shape (`findings` with `rule`, `severity`, `playbook`, `file`, `line`, `message`) unless a change is intentional, and then update the tests and docs together. Do not invent commands or versions. Do not commit secrets. Report checks as passed, failed, or unavailable. Commit or publish only when the user asks.
