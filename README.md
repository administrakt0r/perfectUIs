# PrefectUIS

> **The autonomous, disciplined UI engineering and polish workflow for AI coding agents.**

PrefectUIS orchestrates end-to-end frontend craftsmanship into a unified, repeatable cycle. Instead of overwhelming diffs or vague design advice, PrefectUIS evaluates any frontend codebase, targets the **1 or 2 highest-priority visual or structural issues**, dispatches specialized craft playbooks, verifies results through automated scans and builds, and tracks continuous progress in a persistent journal (`.prefectuis/backlog.md`).

---

## 🌟 Key Principles

1. **Focused Increments (1–2 Issues)**: Avoids massive, risky PRs. Every run tackles 1 or 2 high-impact items with surgical precision.
2. **Context-Grounded**: Honors product facts (`PRODUCT.md`) and design system tokens (`DESIGN.md`). If context is missing, it runs a discovery interview before touching UI code.
3. **Specialized Playbook Dispatch**: Maps each issue to its targeted technique (`layout`, `typeset`, `colorize`, `harden`, `adapt`, `polish`).
4. **Relentless Craft Floor**: Enforces non-negotiable quality criteria (WCAG AA contrast, optical spacing, balanced text wrap, styled scrollbars/focus rings) and bans AI-slop cliches (no gradient text, no eyebrows, no card spam).
5. **Multi-Stage Verification**: Validates changes using an automated anti-pattern detector, project typechecks/builds, and strict diff checks before closing any issue.
6. **Persistent State & Memory**: Keeps track of completed fixes, open backlog items, and future recommendations in `.prefectuis/backlog.md` so you can resume anytime without context loss.

---

## 🔄 The 6-Stage Execution Lifecycle

```
[Stage 1: Setup Gate] ──> [Stage 2: Discovery & Backlog] ──> [Stage 3: Review Gate]
                                                                     │
[Stage 6: Document & Close] <── [Stage 5: Verification] <── [Stage 4: Playbook Fix]
```

| Stage | Name | Action |
|---|---|---|
| **1** | **Setup Gate** | Ensures `PRODUCT.md` and `DESIGN.md` exist. Pauses for initial discovery interview on fresh codebases. |
| **2** | **Discovery & Backlog** | Checks `.prefectuis/backlog.md`, scans dirty Git files or entrypoints with the detector, and selects top 1–2 issues. |
| **3** | **Direction & Review Gate** | Presents the proposed 1–2 fixes to the user. Waits for a quick `"proceed"` or custom guidance. |
| **4** | **Playbook Execution** | Dispatches fixes to targeted playbooks while enforcing the strict Craft Floor. |
| **5** | **Multi-Stage Verification** | Runs detector scan on modified files + project build/typecheck + diff review. |
| **6** | **Document & Close** | Updates design tokens, marks items resolved in `.prefectuis/backlog.md`, logs execution history, and queues the next focus. |

---

## 🛠️ Specialized Playbooks

PrefectUIS maps discovered UI issues into 6 specialized playbooks:

- **`layout`**: Grid alignment, spatial scale standardization (8px increments), Gestalt proximity grouping, balanced section spacing.
- **`typeset`**: Line measure constraint (65–75ch), heading scale, `text-wrap: balance`, tabular numerals (`font-variant-numeric: tabular-nums`).
- **`colorize`**: WCAG AA contrast elevation (≥4.5:1 body, ≥3.0:1 large text), semantic token mapping, dark-mode harmony.
- **`harden`**: Empty states, skeleton loading states, error recovery paths, text overflow wrapping (`break-word`), form validation.
- **`adapt`**: Fluid responsive breakpoints, touch target compliance (≥44x44px), mobile layout stacking.
- **`polish`**: Border radii harmonization, subtle interaction transitions, themed `::selection`, custom `:focus-visible` rings, styled scrollbars.

---

## 🛡️ Craft Floor (Non-Negotiable Standards)

Every modification made by PrefectUIS must satisfy the rules in [`reference/craft-floor.md`](reference/craft-floor.md):

- **Contrast**: Body text ≥ 4.5:1; large text ≥ 3.0:1.
- **Spacing**: Strict hierarchy with 2x–3x more space above headings than below.
- **Typography**: Measure bounded at 65–75ch; no widows in headings.
- **States**: Complete coverage for default, hover, focus-visible, active, disabled, loading, empty, and error.
- **Browser Surfaces**: Must theme text selection, custom scrollbars, and focus rings.

### Prohibited Patterns (Refusals)
- ❌ **No Gradient Text**: Visual weight must come from weight, size, or contrast.
- ❌ **No Eyebrows / Kickers**: No floating uppercase category labels above headings.
- ❌ **No Card Spam**: Avoid repetitive 3-column card containers; use semantic lists, tables, or asymmetric layouts.
- ❌ **No Nested Cards**: Cards inside cards are prohibited.
- ❌ **No Fake Emoji Icons**: Raw emojis in place of an icon system are prohibited.
- ❌ **No Monospace as Costume**: Only for code, measurements, or tabular data.

---

## 📂 Repository Structure

```
prefectuis/
├── SKILL.md                          # Main invocable skill entrypoint
├── README.md                         # Project documentation
├── skill-improve.md                  # Prompt for upgrading & enhancing the skill
├── reference/
│   ├── craft-floor.md                # Quality standards & anti-pattern bans
│   ├── playbooks.md                  # Execution guides for all 6 playbooks
│   └── backlog-template.md           # Specification for .prefectuis/backlog.md
└── scripts/
    ├── prefectuis                    # Launcher script
    └── bin/linux-x64/prefectuis      # Standalone detector binary (Linux x64)
```

---

## 🚀 Installation

To install PrefectUIS into your AI coding assistant:

### Google Antigravity
Clone or copy the directory into your skills folder:
```bash
git clone https://github.com/administrakt0r/prefectuis.git ~/.gemini/config/skills/prefectuis
```

### Claude Code
```bash
git clone https://github.com/administrakt0r/prefectuis.git ~/.claude/skills/prefectuis
```

### Codex / Gemini CLI
```bash
git clone https://github.com/administrakt0r/prefectuis.git ~/.agents/skills/prefectuis
```

---

## 💻 Usage

On any codebase, invoke:
```text
/prefectuis
```
Or target a specific file/route:
```text
/prefectuis src/components/Navigation.tsx
/prefectuis pages/index.html
```

PrefectUIS will scan the target, report the top 1–2 issues, ask for a quick nod, execute the fix, verify everything, and log progress in `.prefectuis/backlog.md`.
