# PrefectUIS

PrefectUIS is a UI review skill for coding agents. It proposes the one or two most important design or accessibility issues, waits for you to accept the plan, fixes those issues, checks the result, and records the rest in `.prefectuis/backlog.md`.

It works in small, verifiable steps.

---

## Quick Install Prompts

Paste one of these prompts into your AI coding assistant to install PrefectUIS immediately.

### Prompt for Claude Code, Antigravity, Cursor, or Codex

```text
Please install the PrefectUIS skill into your personal skills directory from GitHub:
git clone https://github.com/administrakt0r/prefectuis.git <skills-dir>/prefectuis

For reference:
- Cursor: ~/.cursor/skills/prefectuis
- Antigravity: ~/.gemini/config/skills/prefectuis
- Claude Code: ~/.claude/skills/prefectuis
- Codex / Universal: ~/.agents/skills/prefectuis

After cloning, ensure scripts/prefectuis is executable (chmod +x scripts/prefectuis). The detector needs python3.
Confirm when the skill is installed and ready to invoke as /prefectuis.
```

---

## Command-Line Installation

If you prefer to install it yourself from the terminal, pick the command matching your tool:

### Cursor
```bash
git clone https://github.com/administrakt0r/prefectuis.git ~/.cursor/skills/prefectuis
chmod +x ~/.cursor/skills/prefectuis/scripts/prefectuis
```

### Google Antigravity
```bash
git clone https://github.com/administrakt0r/prefectuis.git ~/.gemini/config/skills/prefectuis
chmod +x ~/.gemini/config/skills/prefectuis/scripts/prefectuis
```

### Claude Code
```bash
git clone https://github.com/administrakt0r/prefectuis.git ~/.claude/skills/prefectuis
chmod +x ~/.claude/skills/prefectuis/scripts/prefectuis
```

### Codex or Generic Agent Runtimes
```bash
git clone https://github.com/administrakt0r/prefectuis.git ~/.agents/skills/prefectuis
chmod +x ~/.agents/skills/prefectuis/scripts/prefectuis
```

---

## Running the detector

The launcher is `scripts/prefectuis` inside the skill directory. It needs `python3`. Point it at files or directories (HTML, CSS, and component source). It does not scan a live URL.

```bash
# From the skill directory
scripts/prefectuis detect src/
scripts/prefectuis detect --json src/components/
scripts/prefectuis detect --scope color src/components/Button.tsx
scripts/prefectuis detect --rules
```

Exit 0 means no findings. Exit 1 means the JSON or text report contains candidates to confirm.

---

## How It Works

Every time you invoke `/prefectuis`, it runs through six stages:

1. **Setup**: Finds the nearest `PRODUCT.md` and `DESIGN.md`. If either is missing, it asks a short set of questions and writes only what you answered or what is already in the code.
2. **Discovery**: Reads `.prefectuis/backlog.md`, runs the detector, and checks the craft floor for issues the scanner cannot see. It keeps the top one or two items.
3. **Review gate**: Shows the plan, including how you can tell each fix worked. It waits until you reply "proceed" or change the direction.
4. **Playbook fix**: Applies `layout`, `typeset`, `colorize`, `harden`, `adapt`, or `polish` without restyling unrelated screens.
5. **Verification**: Re-runs the detector, runs the project's check, reviews the diff, and exercises the control in a browser when one is available. Each check is reported as passed, failed, or unavailable.
6. **Record**: Marks the items done in `.prefectuis/backlog.md` and names the next one or two.

---

## How to Use It

### Run on the current project
In your AI chat, type:
```text
/prefectuis
```

The assistant will scan your project, show you the top one or two issues it found, and ask for your confirmation before making edits.

### Run on a specific file or route
```text
/prefectuis src/components/Navbar.tsx
/prefectuis pages/pricing.html
```

---

## The Six Playbooks

PrefectUIS categorizes fixes into six distinct playbooks:

- **layout**: Spacing on the product scale, grouping, container queries, and flex or grid overflow.
- **typeset**: 45–75 character measure, `text-wrap: balance` on headings, `text-wrap: pretty` on body, and tabular numbers.
- **colorize**: WCAG AA contrast (4.5:1 body, 3:1 large text and controls), `oklch()` ramps, and tokens instead of raw hex.
- **harden**: Labels, empty, loading, and error states, and long or translated strings.
- **adapt**: Phone, tablet, and foldable structure, 24px minimum targets (44px for primary touch), and web shells such as Capacitor, Tauri, and Electron.
- **polish**: Radii, `::selection`, `:focus-visible`, and motion that respects `prefers-reduced-motion`.

---

## The Craft Floor

Every code edit must pass these baseline rules:

- **Contrast**: Body and placeholder text at least 4.5:1. Large text, icons, and focus rings at least 3:1. Status is not color alone.
- **Spacing**: Headings have more space above than below, on a consistent scale.
- **Typography**: Prose stays within 45–75 characters. Headings use balanced wrapping; body copy uses `text-wrap: pretty`.
- **Targets**: At least 24×24 CSS px, and 44×44 px for primary touch controls. Focus stays visible and is not covered by sticky bars.
- **States**: Hover, focus-visible, active, disabled, loading, empty, and error, including recovery text.
- **Browser surfaces**: Selection, scrollbars, and focus rings use the product palette.

### Banned patterns
- No gradient text.
- No uppercase eyebrow labels above headings.
- No nested cards, and no default page made only of identical icon cards.
- No emoji used as the icon system.
- No monospace for ordinary copy.
- No zero-blur decorative shadows unless the design system is neobrutalist.

---

## The Progress Journal

Progress is recorded in `.prefectuis/backlog.md`. A typical entry looks like this:

```markdown
# PrefectUIS Quality Journal

> Context: [PRODUCT.md](../PRODUCT.md) | [DESIGN.md](../DESIGN.md)
> Last Run: 2026-11-02 00:15 | Open: 3 | Done: 2

## Next recommended focus

1. **src/components/Sidebar.tsx**: Inactive tab text is under 4.5:1 (`colorize`, `low-contrast-pair`)
2. **src/pages/Settings.tsx**: Fixed width breaks under 768px (`adapt`, `fixed-width`)

## Active backlog

### P0 / P1
- [ ] **[P1] Inactive tab text is under 4.5:1** — `src/components/Sidebar.tsx` · rule `low-contrast-pair` · `colorize`
- [ ] **[P1] Settings layout is a fixed width** — `src/pages/Settings.tsx` · rule `fixed-width` · `adapt`

### P2
- [ ] **[P2] Cleared list has no empty state** — `src/components/TodoList.tsx` · rule `partial-states` · `harden`

## Execution history

### Run 1 — 2026-11-02 00:15
- **Targets**: `src/components/Header.tsx`
- **Resolved**:
  1. Button contrast 3.2:1 to 5.2:1 (`low-contrast-pair`, `colorize`).
  2. Visible focus ring (`outline-removed`, `polish`).
- **Verification**:
  - Detector: passed (0 findings on touched files).
  - Project check: passed (`npm run build`).
  - Rendered: unavailable (no dev server).
  - Craft floor: passed.
```

The field list and severity rules live in `reference/backlog-template.md`. The next invocation reads this file and continues from the open items.

Maintainers upgrading the skill itself should use `skill-improve.md`.
