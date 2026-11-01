# Improving PrefectUIS

Open this repository and paste the prompt below as the whole task. Do not add a second agenda in chat. The prompt is written so the next run closes gaps and leaves the current rules in place.

## Prompt

```markdown
Upgrade the PrefectUIS skill in this repository. It is an incremental UI-quality workflow: a review gate, one or two issues per run, six stages, six playbooks (layout, typeset, colorize, harden, adapt, polish), a craft floor, and a dependency-free Python detector.

Read these before editing, and treat them as the current contract: SKILL.md, reference/craft-floor.md, reference/playbooks.md, reference/backlog-template.md, README.md, AGENTS.md, scripts/prefectuis, scripts/detect.py, scripts/test_detect.py.

## Goal

Close real gaps between this skill and current, widely shipped UI practice. Prefer a smaller, stricter skill. Do not rewrite prose that is already correct, and do not add a technique because it is new.

## Research

Check WCAG 2.2 level AA. Treat AAA as optional unless a product explicitly asks for it. For any CSS or platform behavior you want the skill to require, confirm it in current MDN or the relevant platform docs. You may read design references already installed on this machine. Rewrite every idea in PrefectUIS language.

Do not copy another tool's names, commands, directory names, or sentences into any file here. Do not add product or tool brand names other than PrefectUIS.

## Keep

- The prefectuis name on the skill, the launcher (`scripts/prefectuis`), and the journal (`.prefectuis/backlog.md`).
- The six stages, including the review gate that waits for "proceed" before editing.
- A limit of one or two issues per run. Two findings with the same cause count as one fix.
- The detector on python3, with no package install and no downloaded binary.
- JSON findings as objects with `rule`, `severity`, `playbook`, `file`, `line`, and `message`.
- A `SKILL.md` description that starts with "Use when" and does not list the stages or playbooks.
- WCAG AA as the default floor. Do not raise body text to 7:1.
- Motion, view transitions, and scroll-driven animation as optional. They need a `prefers-reduced-motion` path and must not be required to operate the page.

## Edit

- If a rule already exists, tighten its wording or its false-positive boundary. Do not add a second paragraph that repeats it.
- Put a technique in a playbook only when it fixes a defect that playbook already owns.
- When a user-facing rule changes, update the craft floor, the playbook, `SKILL.md` if the workflow changes, the README summary, and the backlog template together.
- Every new detector rule needs a fixture that reports it and a near-miss fixture that stays clean. Extend `scripts/test_detect.py`. Do not weaken a test to go green.
- A detector hit is a candidate. Document limits the scanner still cannot see.
- Do not commit, push, or publish.

## Verify

- `python3 scripts/test_detect.py` from the repository root.
- `scripts/prefectuis detect --rules` lists every rule the tests cover.
- Relative links in `SKILL.md` and `reference/` resolve to files in this repo. Example links inside the backlog template point at a target project's `PRODUCT.md` and `DESIGN.md`; leave those.
- Search the repo for stray design-tool brand names and remove any you added.

## Report

Lead with what changed and why. Mark each check passed, failed, or unavailable. Name any gap you left open and the reason.
```

## What a good run leaves alone

The craft floor already covers AA contrast, OKLCH for new ramps, `text-wrap: balance` and `pretty`, 24px minimum targets and 44px primary touch targets, container queries, `:has()`, subgrid, foldables, and Capacitor, Tauri, and Electron. The detector already flags the rules printed by `detect --rules`. Extend those. Do not re-add them.
