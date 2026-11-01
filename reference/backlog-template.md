# PrefectUIS Backlog Specification

The file `.prefectuis/backlog.md` is the durable source of truth for UI quality and iterative progress across a codebase. Every invocation of PrefectUIS reads this file at startup and updates it upon completion.

---

## File Structure Template

```markdown
# PrefectUIS Quality Journal

> Context: [PRODUCT.md](../PRODUCT.md) | [DESIGN.md](../DESIGN.md)  
> Last Run: <YYYY-MM-DD HH:mm> | Open Items: <Count> | Completed: <Count>

---

## 🎯 Next Recommended Focus

The next run of PrefectUIS will automatically tackle:
1. **[Target File / Component]**: <Short description of issue 1> (`playbook-name`)
2. **[Target File / Component]**: <Short description of issue 2> (`playbook-name`)

---

## 📋 Active UI Backlog

### High Priority (P0 / P1)
- [ ] **[P1] Contrast failure on primary button hover** — `src/components/Button.tsx` (WCAG AA 3.8:1 < 4.5:1) · *playbook: `colorize`*
- [ ] **[P1] Layout overflow on mobile viewport** — `src/pages/Dashboard.tsx` (Fixed 800px table breaks small screens) · *playbook: `adapt`*

### Medium / Polish Priority (P2)
- [ ] **[P2] Missing empty state for transaction list** — `src/components/TransactionList.tsx` · *playbook: `harden`*
- [ ] **[P2] Line length exceeds 90ch in guide content** — `src/pages/Docs.tsx` · *playbook: `typeset`*

---

## 📜 Execution History

### Run #1 — <YYYY-MM-DD HH:mm>
- **Target**: `src/components/Header.tsx`
- **Issues Resolved**:
  1. Fixed low-contrast navigation links (increased ratio from 3.2:1 to 5.1:1).
  2. Aligned navigation items to standard 16px spatial grid and added `:focus-visible` styling.
- **Playbooks Used**: `colorize`, `layout`, `polish`
- **Verification**:
  - PrefectUIS Detector: 0 findings (down from 2).
  - Project Build: Passed.
  - Craft Floor Diff Check: Verified clean semantic markup, custom focus ring, zero gradient text.
- **Diff Summary**: Updated `Header.module.css` with semantic tokens and focus styles.
```
