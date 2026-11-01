# PrefectUIS

PrefectUIS is an automated UI review and polish skill for AI coding assistants. It scans your frontend, picks the one or two most critical design or accessibility issues, fixes them with targeted techniques, verifies that the build still passes, and logs what it did in `.prefectuis/backlog.md`.

Instead of making dozens of edits across your app at once, it works in small, verifiable steps.

---

## Quick Install Prompts

Paste one of these prompts into your AI coding assistant to install PrefectUIS immediately.

### Prompt for Claude Code, Antigravity, Cursor, or Codex

```text
Please install the PrefectUIS skill into your personal skills directory from GitHub:
git clone https://github.com/administrakt0r/prefectuis.git <skills-dir>/prefectuis

For reference:
- Antigravity: ~/.gemini/config/skills/prefectuis
- Claude Code: ~/.claude/skills/prefectuis
- Codex / Universal: ~/.agents/skills/prefectuis

After cloning, ensure scripts/prefectuis has executable permissions (chmod +x scripts/prefectuis).
Confirm when the skill is installed and ready to invoke as /prefectuis.
```

---

## Command-Line Installation

If you prefer to install it yourself from the terminal, pick the command matching your tool:

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

## Running the Detector via CLI / NPX

You can run the built-in anti-pattern detector on any directory or file without invoking an agent:

```bash
# Direct execution using the bundled launcher
~/.gemini/config/skills/prefectuis/scripts/prefectuis detect src/

# Scan and print structured JSON output
~/.gemini/config/skills/prefectuis/scripts/prefectuis detect --json src/components/

# Scan a running local web page
~/.gemini/config/skills/prefectuis/scripts/prefectuis detect http://localhost:3000
```

---

## How It Works

Every time you invoke `/prefectuis`, it runs through six stages:

1. **Setup Check**: Looks for `PRODUCT.md` and `DESIGN.md`. If this is a new project without them, it conducts a short interview and extracts your color and typography tokens first.
2. **Issue Discovery**: Checks `.prefectuis/backlog.md` for open tasks. If none exist, it runs the detector on dirty Git files or your main layout, then selects the top one or two items by severity.
3. **Review Gate**: Shows you the chosen items and the proposed plan. It waits for you to reply "proceed" or provide custom guidance before touching code.
4. **Targeted Playbook Fix**: Maps the issue to the appropriate playbook (`layout`, `typeset`, `colorize`, `harden`, `adapt`, or `polish`) and applies the fix while respecting the Craft Floor.
5. **Verification**: Re-runs the detector on touched files, runs your project build or typecheck, and reviews the Git diff to make sure nothing broke.
6. **Document and Close**: Marks items complete in `.prefectuis/backlog.md`, records what changed in execution history, and lists the next recommended items for your next run.

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

- **layout**: Spacing rhythm, grid alignment, 8px spatial scale, and grouping related items together.
- **typeset**: Line lengths bounded to 65–75 characters, heading hierarchies, `text-wrap: balance`, and tabular numbers.
- **colorize**: Fixing WCAG AA contrast failures (minimum 4.5:1 for body text), tokenizing colors, and dark mode readability.
- **harden**: Adding empty states, loading indicators, error recovery text, and preventing text overflow on long strings.
- **adapt**: Responsive breakpoints, fluid widths, and minimum 44x44px touch targets on mobile.
- **polish**: Consistent corner radii, custom text selection colors (`::selection`), themed focus rings (`:focus-visible`), and styled scrollbars.

---

## The Craft Floor

Every code edit must pass these baseline rules:

- **Contrast**: Body text must have at least a 4.5:1 ratio against its background. Large text must meet 3:1.
- **Spacing**: Headings must have noticeably more margin above them than below them.
- **Typography**: Paragraphs must not run wider than 75 characters per line. Headings must avoid single trailing words.
- **States**: Interactive elements must support hover, focus-visible, active, disabled, loading, empty, and error states.
- **Browser defaults**: Text selection, custom scrollbars, and focus rings must match your palette rather than standard browser blue.

### Banned Patterns
- No gradient text.
- No floating uppercase category labels (eyebrows) above headings.
- No repetitive three-card grids used as default page structures.
- No nested cards.
- No raw emojis acting as icons; use SVGs with consistent stroke weights.
- No monospace fonts outside actual code, timestamps, or technical data.

---

## The Progress Journal

Progress is recorded in `.prefectuis/backlog.md`. A typical entry looks like this:

```markdown
# PrefectUIS Quality Journal

> Context: PRODUCT.md | DESIGN.md
> Last Run: 2026-11-02 00:15 | Open Items: 3 | Completed: 2

## Next Recommended Focus
1. src/components/Sidebar.tsx: Low contrast text on inactive tabs (colorize)
2. src/pages/Settings.tsx: Fixed width breaks on screens under 768px (adapt)

## Active UI Backlog
- [ ] [P1] Low contrast text on inactive tabs - src/components/Sidebar.tsx
- [ ] [P1] Fixed width breaks on mobile - src/pages/Settings.tsx
- [ ] [P2] Missing empty state when list is clear - src/components/TodoList.tsx

## Execution History
### Run #1 - 2026-11-02 00:15
- Target: src/components/Header.tsx
- Issues Resolved:
  1. Raised button contrast ratio from 3.2:1 to 5.2:1.
  2. Added visible focus ring with 2px offset.
- Playbooks Used: colorize, polish
- Verification: Detector reported 0 findings; npm run build passed.
```

When you invoke `/prefectuis` again, it reads this file, picks up where it stopped, and continues.
