---
name: prefectuis
description: Use when improving an existing web or app frontend for accessibility, contrast, layout, typography, interaction states, or responsive behavior in a small verifiable pass.
argument-hint: "[target file or route (optional)]"
user-invocable: true
---

# PrefectUIS

PrefectUIS improves an existing frontend in small passes. Each run selects one or two defects, fixes them through a playbook, checks the result, and records what remains in `.prefectuis/backlog.md`.

## When to use

Use it for design debt on a real UI: low contrast, broken keyboards, weak hierarchy, missing states, overflow, or layouts that fail on small screens, tablets, or foldables.

Do not use it for backend-only work, for a product that has no interface yet, or for a rewrite of business logic. A new visual identity is out of scope; stay inside `DESIGN.md` and the incumbent UI.

## Six stages

```
[1 Setup] -> [2 Discover] -> [3 Review gate] -> [4 Fix] -> [5 Verify] -> [6 Record]
```

Resolve the detector from the directory that contains this `SKILL.md`. Do not assume one install path.

```bash
<skill-dir>/scripts/prefectuis detect --json <targets>
<skill-dir>/scripts/prefectuis detect --rules
```

Exit 0 means a clean scan. Exit 1 means findings. Exit 2 means the command was invalid. `python3` is required.

### 1. Setup

Search upward from the target file to the repository root for the nearest `PRODUCT.md` and `DESIGN.md`.

When both exist, they are the source of truth. Do not invent a second palette or a new audience.

When either is missing, stop before editing UI. Ask only what the files cannot answer: who it is for, what they are trying to finish, constraints that must not change, and which existing colors and type are intentional. Write only what was answered or directly observed. Mark anything else unconfirmed. If the user explicitly says to continue from the code, record observed tokens and unconfirmed product facts, then continue.

### 2. Discover

1. Read `.prefectuis/backlog.md` when it exists. Prefer open items that match the argument, then the highest open severity.
2. Choose targets in this order: the argument path, dirty UI files, then the app shell and primary screen.
3. Run `prefectuis detect` on those files. A finding is a candidate. Drop it when the surrounding code shows it is intentional or a false positive, and say why.
4. Read [reference/craft-floor.md](reference/craft-floor.md) for defects the scanner cannot see: hierarchy, rhythm, nested cards, hover-only disclosure, focus covered by sticky UI, and copy that does not name the action.
5. Order by P0, then P1, then P2. Take the top one or two issues. Two findings with the same root cause count as one fix.

### 3. Review gate

Show the plan and wait. Do not edit before a reply.

> ### PrefectUIS plan: `<file>`
> 1. **Issue** — `<what is wrong, with rule id if any>` → `<playbook>`
>    Acceptance: `<the observable check>`
> 2. **Issue** — same shape, or omit when the run is one issue.
>
> Reply "proceed", or correct the direction.

Apply corrections before editing. "Proceed" accepts the plan as written.

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

1. Re-run `prefectuis detect` on the files you changed. The targeted rule should be gone, and new findings should be fixed or called out as pre-existing.
2. Run the project's documented typecheck, test, or build for the change.
3. Review the diff against the craft floor.
4. When a dev server or browser is available, use the changed control: keyboard, pointer, a narrow viewport, and the empty or error state you touched. For layout and adapt work, also check a tablet width.

Report each check as passed, failed, or unavailable. A clean detector run does not prove hierarchy, copy, or motion quality.

### 6. Record

Update `DESIGN.md` when a token changed. Update `.prefectuis/backlog.md` using [reference/backlog-template.md](reference/backlog-template.md): check off the resolved items, append an execution-history entry with files, playbooks, and verification, and set the next one or two open items.

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

## References

- [reference/craft-floor.md](reference/craft-floor.md)
- [reference/playbooks.md](reference/playbooks.md)
- [reference/backlog-template.md](reference/backlog-template.md)
