# PrefectUIS backlog

`.prefectuis/backlog.md` is the durable journal for a codebase. Read it at the start of a run and update it before the run ends. Copy this structure when the file does not exist yet.

```markdown
# PrefectUIS Quality Journal

> Context: [PRODUCT.md](../PRODUCT.md) | [DESIGN.md](../DESIGN.md)
> Last Run: <YYYY-MM-DD HH:mm> | Open: <count> | Done: <count>

## Next recommended focus

1. **<file>**: <issue> (`<playbook>`, `<rule-id or manual>`)
2. **<file>**: <issue> (`<playbook>`, `<rule-id or manual>`)

## Active backlog

### P0 / P1
- [ ] **[P1] Primary button text is 3.8:1** — `src/components/Button.tsx` · rule `low-contrast-pair` · `colorize`
- [ ] **[P1] Orders table is 800px wide** — `src/pages/Orders.tsx` · rule `fixed-width` · `adapt`

### P2
- [ ] **[P2] Order list has no empty state** — `src/components/OrderList.tsx` · rule `partial-states` · `harden`

## Execution history

### Run 1 — <YYYY-MM-DD HH:mm>
- **Targets**: `src/components/Header.tsx`
- **Resolved**:
  1. Nav link contrast 3.2:1 to 5.1:1 (`low-contrast-pair`, `colorize`).
  2. Focus ring was the browser default (`outline-removed`, `polish`).
- **Verification**:
  - Detector: passed (0 findings on touched files; was 2).
  - Project check: passed (`npm run typecheck`).
  - Rendered: passed at desktop and 390px, keyboard through the nav. Tablet width unavailable.
  - Craft floor: passed (tokens, no gradient text, focus ring from the palette).
- **Diff**: `Header.module.css` now uses `--ink` and a 2px focus ring.
```

Rules for entries:

- Severity is P0 (blocked or unlabeled control), P1 (WCAG AA, broken layout, missing recovery), or P2 (polish and consistency).
- Include the detector rule id when the scanner reported it. Use `manual` when the craft floor caught it and the detector did not.
- Verification lines say passed, failed, or unavailable. Do not write "passed" for a check that did not run.
- The next-focus list is the following run's default pair, still subject to the review gate.
