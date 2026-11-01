---
name: prefectuis
description: Use when auditing, polishing, or systematically resolving UI design flaws, accessibility gaps, or visual inconsistency on any frontend codebase in focused, verifiable 1-2 issue increments.
argument-hint: "[target file or route (optional)]"
user-invocable: true
---

# PrefectUIS

## Overview

PrefectUIS is an autonomous, disciplined UI engineering workflow. It evaluates frontend code, selects the 1–2 highest-priority visual or structural issues, executes targeted craft fixes, verifies them against strict quality standards, and tracks cumulative progress in a persistent backlog.

---

## When to Use

**Use when:**
- A user wants to improve, polish, or fix UI quality on a web or application frontend without getting overwhelmed.
- A codebase has design debt: low contrast, broken responsive behavior, messy spacing, unstyled browser surfaces, or missing edge-case states.
- You need a structured, repeatable cycle that tackles 1–2 discrete UI improvements per invocation and remembers what is done versus what remains.

**When NOT to use:**
- Backend-only code, database migrations, or non-visual APIs.
- Greenfield projects before any UI scaffold or markup exists (use project setup tools first).
- Major product pivot requiring complete architectural rewriting of the business logic.

---

## The 6-Stage Execution Lifecycle

Every invocation of `prefectuis` executes this exact 6-stage cycle:

```
[Stage 1: Setup Gate] ──> [Stage 2: Discovery & Backlog] ──> [Stage 3: Review Gate]
                                                                     │
[Stage 6: Document & Close] <── [Stage 5: Verification] <── [Stage 4: Playbook Fix]
```

### Stage 1: Setup Gate (Context Authority)
1. Check for `PRODUCT.md` and `DESIGN.md` in the project root.
2. **If missing**:
   - Pause immediately before touching any UI code.
   - Run the discovery interview to establish `PRODUCT.md` (target audience, product mechanism, durable constraints).
   - Extract design tokens from existing styles to establish `DESIGN.md` (colors, typography, radii, spacing).
   - Only proceed to Stage 2 once both context files exist.
3. **If present**: Load both documents as the binding visual and strategic source of truth.

### Stage 2: Scope & Backlog Discovery
1. Check if `.prefectuis/backlog.md` exists:
   - If active open items exist, read the top open items.
2. Inspect target scope:
   - If an explicit target was passed as an argument (e.g. `/prefectuis src/components/Card.tsx`), prioritize that file.
   - If no target was passed, prioritize dirty/modified Git files.
   - If Git working tree is clean, inspect core UI entrypoints (app shell, main landing page, dashboard navigation).
3. Run the automated detector over the target files:
   ```bash
   ~/.gemini/config/skills/prefectuis/scripts/prefectuis detect --json <target-files>
   ```
4. Merge detector findings with visual inspection against `reference/craft-floor.md`.
5. Triage all findings by severity (P0: broken/inaccessible, P1: contrast/layout breaks, P2: polish/consistency).
6. Select the **top 1 or 2 issues** to resolve in this run.

### Stage 3: Direction & Review Gate
Present the proposed plan to the user in chat using this concise format:

> ### PrefectUIS Plan: Target `<resolved-file>`
> 1. **Issue 1**: <concise summary of problem> → *Playbook: `<playbook-name>`*
> 2. **Issue 2**: <concise summary of problem> → *Playbook: `<playbook-name>`*
> 
> *Reply "proceed" to apply these fixes, or provide custom direction (e.g., "use darker borders", "prefer flexbox").*

**Rule**: Wait for user response before editing code. If the user provides specific stylistic guidance, adapt the plan accordingly.

### Stage 4: Specialized Playbook Execution
Execute the fixes for the selected 1–2 issues. Map each issue to its specialized playbook from `reference/playbooks.md`:

| Problem Domain | Playbook | Key Actions |
|---|---|---|
| Spacing, alignment, rhythm, visual hierarchy | `layout` | Standardize spatial grid (8px scale), proximity grouping, balanced heading spacing |
| Typography, line measure, font hierarchy | `typeset` | Limit measure to 65–75ch, `text-wrap: balance`, tabular numerals |
| Contrast failure, color harmony, dark mode | `colorize` | Elevate contrast to ≥4.5:1, bind to `DESIGN.md` tokens, tint neutrals |
| Missing states (empty, loading, error), overflow | `harden` | Add resilient states, `overflow-wrap: break-word`, accessible form labels |
| Mobile breaks, touch targets, rigid widths | `adapt` | Fluid widths, ≥44x44px touch targets, mobile viewport layout stacking |
| Micro-details, radii, browser surfaces | `polish` | Custom `::selection`, `:focus-visible` rings, styled scrollbars, uniform radii |

**Enforce Craft Floor**: Consult `reference/craft-floor.md` before writing code. Absolute bans:
- NO gradient text
- NO category eyebrows/kickers above headings
- NO cards-as-default or nested cards
- NO raw Unicode emojis in place of real SVG icons
- NO monospace styling for non-code content

### Stage 5: Multi-Stage Verification
Before claiming an issue is resolved or updating the backlog:
1. **Automated Detector Pass**:
   Run the PrefectUIS detector on all modified files:
   ```bash
   ~/.gemini/config/skills/prefectuis/scripts/prefectuis detect --json <modified-files>
   ```
   Confirm that targeted anti-patterns are eliminated and no new warnings were introduced.
2. **Project Build & Typecheck**:
   Run project verification commands (e.g. `npm run build`, `npm run typecheck`, or equivalent). Do not leave broken builds.
3. **Craft Floor Diff Check**:
   Review `git diff` against `reference/craft-floor.md`: verify clean token usage, accessible states, and absence of prohibited patterns.

### Stage 6: Documentation & Backlog Close
1. If new design tokens were created, update `DESIGN.md`.
2. Update `.prefectuis/backlog.md`:
   - Mark the resolved 1–2 items as completed `[x]`.
   - Append an entry to `## Execution History` with timestamp, files touched, playbooks used, diff summary, and verification results.
   - Update `## 🎯 Next Recommended Focus` with the next 1–2 pending items for the following invocation.
3. Present the completion report to the user:
   - Summary of changes made.
   - Verification results (detector output + build status).
   - What was logged in `.prefectuis/backlog.md`.
   - The recommended focus for the next run.

---

## Red Flags & Rationalizations

| Excuse / Rationalization | Reality | Correct Action |
|---|---|---|
| "This issue is small, I can skip the review gate." | Unconfirmed edits risk user dissatisfaction and rework. | Always show the 1–2 items and get user confirmation. |
| "I'll fix 5 or 6 issues while I'm in this file." | Batching too many fixes causes large, risky diffs and muddies review. | Limit strictly to the top 1–2 issues per run. |
| "PRODUCT.md is missing, but I can guess the design direction." | Designing without product truth produces generic, misaligned results. | Conduct the setup gate interview before touching UI code. |
| "The build failed, but the visual CSS looks correct." | A broken build is broken code, regardless of aesthetics. | Fix all compiler/type errors before finishing the stage. |
| "I can skip updating the backlog file this time." | Skipping backlog updates breaks persistence across invocations. | Always update `.prefectuis/backlog.md` before completing the run. |

---

## Supporting References

- **Craft Standards & Refusals**: [reference/craft-floor.md](reference/craft-floor.md)
- **Specialized Playbooks**: [reference/playbooks.md](reference/playbooks.md)
- **Backlog Format Specification**: [reference/backlog-template.md](reference/backlog-template.md)
