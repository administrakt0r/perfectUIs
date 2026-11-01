# PrefectUIS Specialized Playbooks

When an issue is selected from the backlog or diagnostic scan, PrefectUIS routes the resolution through the appropriate specialized playbook while upholding the Craft Floor.

---

## 1. Playbook: Layout & Hierarchy (`layout`)

**Use for**: Inconsistent spacing, cluttered interfaces, weak visual rhythm, misaligned grids, weak visual grouping.

### Execution Steps
1. **Analyze Spacing Rhythm**: Identify hard-coded margins, arbitrary paddings, and uneven gaps.
2. **Apply Spatial Scale**: Standardize onto an intentional scale (4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px).
3. **Proximity & Grouping**:
   - Enforce Gestalt law of proximity: elements within a logical component should be spaced closer together than the boundary between separate components.
   - Headings must possess 2x to 3x more top margin than bottom margin.
4. **Alignment**: Establish consistent vertical and horizontal baseline axes. Replace nested ad-hoc divs with CSS Flexbox (`gap`) or CSS Grid.

---

## 2. Playbook: Typography & Readability (`typeset`)

**Use for**: Poor contrast, illegible fonts, unreadable line lengths, messy heading scales, missing typographic hierarchy.

### Execution Steps
1. **Line Measure**: Restrict paragraph width to 65–75 characters (`max-width: 65ch`–`75ch`).
2. **Hierarchy & Scale**: Establish clear size/weight distinctions:
   - Page Title / H1: Boldest weight, balanced line wrap (`text-wrap: balance`).
   - Section Headings (H2/H3): Proportional line-height (1.2–1.3), clear visual step-down.
   - Body copy: Line-height 1.5–1.6 for comfortable reading.
   - Small / Caption: Minimum 12px / 0.75rem with increased contrast to preserve legibility.
3. **Tabular Numerals**: Apply `font-variant-numeric: tabular-nums` to financial data, timestamps, countdowns, and table columns.

---

## 3. Playbook: Color & Contrast (`colorize`)

**Use for**: WCAG AA contrast failures, washed out monochromatic UIs, harsh uncoordinated colors, dark mode contrast breaks.

### Execution Steps
1. **Audit Contrast Ratios**: Check foreground text against immediate background using the PrefectUIS detector.
2. **Elevate Contrast**: Adjust lightness/chroma until contrast reaches ≥ 4.5:1 for body text (or ≥ 3.0:1 for large text).
3. **Semantic Hierarchy**:
   - Primary: Action items and key focal points.
   - Neutral Surface & Text: Subtle tinted grays (derived from primary hue) rather than dead #000/#fff.
   - Status: Distinct, accessible semantic colors (success, warning, error, info).
4. **Tokenization**: Ensure colors map cleanly to `DESIGN.md` tokens rather than one-off hex values.

---

## 4. Playbook: Hardening & States (`harden`)

**Use for**: Missing loading/empty/error states, text overflow clipping, unhandled long strings, fragile input controls.

### Execution Steps
1. **State Completeness**:
   - Empty State: When data is null/empty, render a purposeful illustration/icon, clear explanation, and primary action.
   - Loading State: Provide smooth skeleton loaders or spinners that preserve the layout footprint without causing layout shift.
   - Error State: Render friendly, actionable feedback when an action fails.
2. **Overflow Resilience**:
   - Add `overflow-wrap: break-word` and `hyphens: auto` where user-generated text could blow out boundaries.
   - Ensure containers adapt to 2x or 3x text expansion (e.g. localization).
3. **Form & Validation**: Ensure explicit labels (`<label for="...">`), visible error messages tied to inputs with `aria-describedby`, and disabled states with `aria-disabled`.

---

## 5. Playbook: Responsive & Adaptation (`adapt`)

**Use for**: Mobile layout breaks, small touch targets, horizontal scrolling on small viewports, rigid fixed widths.

### Execution Steps
1. **Touch Targets**: Ensure all interactive controls have minimum hit targets of 44x44px on touch viewports (WCAG 2.5.8 requires at least 24x24 CSS px with surrounding clearance).
2. **Fluid Typography & Containers**: Replace hardcoded pixel widths (`width: 500px`) with fluid max-widths (`max-width: 100%`, `clamp()`).
3. **Stacking Behavior**: Transition multi-column grid layouts to single-column or scroll-snap lists on viewport widths < 768px.
4. **Safe Area Insets**: Accommodate notch/bottom home indicator (`env(safe-area-inset-bottom)`).

---

## 6. Playbook: Micro-Detail Polish (`polish`)

**Use for**: Final pass before shipping, inconsistent corner radii, misaligned borders, jumpy transitions, neglected browser surfaces.

### Execution Steps
1. **Radii & Borders**: Consolidate border radii to match `DESIGN.md` (`rounded.sm`, `rounded.md`, `rounded.lg`).
2. **Interactive Transitions**: Apply smooth, subtle transitions (e.g. `transition: color 150ms ease, background-color 150ms ease`). Avoid transition on `all`.
3. **Browser Surface Styling**:
   - `::selection`: Set background to tinted brand color and foreground to high-contrast text.
   - `:focus-visible`: Implement clean 2px offset focus ring.
4. **Code Cleanliness**: Remove dead styles, redundant inline properties, and debug logs.
