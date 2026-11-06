---
name: perfectuis
description: Use when the user asks to polish, audit, fix, or "perfect" an existing web or app UI - contrast, accessibility, spacing, typography, focus/keyboard, loading/empty/error states, or responsive/tablet/foldable layout - in small, verifiable passes tracked in .perfectuis/backlog.md. Triggers - "polish this UI", "fix contrast", "a11y audit", "make this responsive", "UI looks off", "/perfectuis". Do NOT use for backend-only work, brand-new interfaces, visual rebrands, or business-logic rewrites.
argument-hint: "[target file or route (optional)]"
user-invocable: true
---

# perfectUIs

perfectUIs improves an existing frontend in small passes. Each run selects one or two defects, fixes them through a playbook, checks the result, and records what remains in `.perfectuis/backlog.md`.

## When to use

Use it for design debt on a real UI: low contrast, broken keyboards, weak hierarchy, missing states, overflow, or layouts that fail on small screens, tablets, or foldables.

Do not use it for backend-only work, for a product that has no interface yet, or for a rewrite of business logic. A new visual identity is out of scope; stay inside `DESIGN.md` and the incumbent UI.

## Six stages

```
[1 Setup] -> [2 Discover] -> [3 Review gate] -> [4 Fix] -> [5 Verify] -> [6 Record]
```

Resolve the detector from the directory that contains this `SKILL.md`. Do not assume one install path.

```bash
<skill-dir>/scripts/perfectuis detect --json <targets>
<skill-dir>/scripts/perfectuis detect --rules
```

Exit 0 means a clean scan. Exit 1 means findings. Exit 2 means the command was invalid. `python3` is required.

### 1. Setup

Search upward from the target file to the repository root for the nearest `PRODUCT.md` and `DESIGN.md`.

When both exist, they are the source of truth. Do not invent a second palette or a new audience.

When either is missing, stop before editing UI. Ask only what the files cannot answer: who it is for, what they are trying to finish, constraints that must not change, and which existing colors and type are intentional. Write only what was answered or directly observed. Mark anything else unconfirmed. If the user explicitly says to continue from the code, record observed tokens and unconfirmed product facts, then continue.

### 2. Discover

1. If `.perfectuis/backlog.md` is missing but `.prefectuis/backlog.md` exists, move the directory to `.perfectuis/` (git mv if tracked, else mv), update the heading to perfectUIs, and note the migration in the run history. Read `.perfectuis/backlog.md` when it exists. Prefer open items that match the argument, then the highest open severity.
2. Choose targets in this order: the argument path, dirty UI files, then the app shell and primary screen.
3. Run `perfectuis detect` on those files. A finding is a candidate. Drop it when the surrounding code shows it is intentional or a false positive, and say why.
4. Read [reference/craft-floor.md](reference/craft-floor.md) for defects the scanner cannot see: hierarchy, rhythm, nested cards, hover-only disclosure, focus covered by sticky UI, and copy that does not name the action.
5. Order by P0, then P1, then P2. Take the top one or two issues. Two findings with the same root cause count as one fix.
   - P0: blocks a task for some users (no keyboard access, unreadable text, unreachable content)
   - P1: degrades the task (contrast < 4.5:1, layout breaks at 320/768px, missing error state)
   - P2: polish (radius drift, motion, selection color)

### 3. Review gate

Show the plan and wait. Do not edit before a reply.

> ### perfectUIs plan: `<file>`
> 1. **Issue** — `<what is wrong, with rule id if any>` → `<playbook>`
>    Acceptance: `<the observable check>`
> 2. **Issue** — same shape, or omit when the run is one issue.
>
> Reply "proceed", or correct the direction.

Apply corrections before editing. "Proceed" accepts the plan as written.

## When to ask

Ask only when the answer changes the outcome, and never nag otherwise.

ASK (crucial), then wait:
1. `PRODUCT.md` or `DESIGN.md` is missing (existing Setup behavior, unchanged).
2. The fix needs an identity decision: new palette, new typeface, layout redesign, or new component pattern.
3. The fix needs a copy change beyond naming an action, or touches business logic, routing, or data.
4. The target file has uncommitted changes (ask: edit anyway / skip / pick another file).
5. Verification still fails after one fix attempt (report it; ask: keep, adjust, or revert).
6. The argument is ambiguous (two files or routes match equally).

DO NOT ASK (decide, then state the assumption in the plan's one-line note):
- which of two equally valid spacing-scale steps to use
- token names, class ordering, formatting
- whether to run the detector or the project check
- anything already answered by `PRODUCT.md`, `DESIGN.md`, or `.perfectuis/backlog.md`

FORMAT:
- At most ONE question batch per run, max 3 questions, each with a recommended default. Example:
    "Two things I need before editing:
     1. DESIGN.md has no focus color. Use the existing `--accent` (#2F6FEB, 4.6:1 on white)? [default: yes]
     2. `Settings.tsx` has uncommitted changes. Edit it anyway, or skip it? [default: skip]"
- Put the questions inside or directly before the Review-gate plan so the user answers once.
- Never revert or overwrite a user's uncommitted work. Reverting is limited to this run's own edits to files that were clean when the run started, and only after the user chose "revert" in rule 5.

### 4. Fix

Map each issue to one playbook in [reference/playbooks.md](reference/playbooks.md):

| Domain | Playbook |
|---|---|
| Spacing, alignment, hierarchy | `layout` |
| Type, measure, wrapping | `typeset` |
| Contrast, tokens, themes | `colorize` |
| States, labels, overflow, i18n | `harden` |
| Viewports, targets, input, shells | `adapt` |
| Radii, focus, motion, browser surfaces | `polish` |

Edit only the files those issues require, including a shared token they must use. Leave neighboring screens alone. Follow the craft floor while editing.

### 5. Verify

Do this before claiming a fix:

1. Re-run `perfectuis detect` on the files you changed. The targeted rule should be gone, and new findings should be fixed or called out as pre-existing.
2. Run the project's documented typecheck, test, or build for the change.
3. Review the diff against the craft floor.
4. If the project already has a dev server and a browser tool (check package.json scripts and available tools; install nothing), capture the changed screen at 320, 768 and 1280 px and record per width: horizontal scroll (yes/no), focus ring visible on the changed control (yes/no), and the empty/error state if touched. Report as `Rendered: passed | failed | unavailable (<reason>)`. Never claim a render check you did not run. If any check fails, fix once. If it still fails, report it as failed and ask the user whether to keep, adjust, or revert; do not revert on your own.

Report each check as passed, failed, or unavailable. A clean detector run does not prove hierarchy, copy, or motion quality.

### 6. Record

Update `DESIGN.md` when a token changed. Update `.perfectuis/backlog.md` using [reference/backlog-template.md](reference/backlog-template.md): check off the resolved items, append an execution-history entry with files, playbooks, and verification, and set the next one or two open items.

Then tell the user what changed, how it was checked, and what the next run should pick up.

## Rationalizations

| Excuse | What to do |
|---|---|
| "The change is tiny, so skip the review gate." | Show the plan and wait. |
| "I am already in the file, so I will fix the whole page." | Stop at the one or two issues in the plan. |
| "The context files are missing, but the audience is obvious." | Ask, then write only what was answered or observed. |
| "The detector is clean, so the screen is done." | Still judge hierarchy, states, and the rendered control. |
| "The build failed, but the CSS looks right." | Fix the build or report it as failed. |
| "I will update the backlog next time." | Update it before the run ends. |
| "It is a judgment call, so I will just ask the user." | Ask only for the crucial cases in "When to ask"; otherwise decide and state the assumption. |
| "The user is busy, so I will skip the question and guess." | If a crucial case applies, ask. A wrong guess costs more than one question. |

## References

- [reference/craft-floor.md](reference/craft-floor.md)
- [reference/playbooks.md](reference/playbooks.md)
- [reference/backlog-template.md](reference/backlog-template.md)
