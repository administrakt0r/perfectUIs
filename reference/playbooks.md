# perfectUIs playbooks

Fix the selected issue inside the current visual system. Read [craft-floor.md](craft-floor.md) before editing. A playbook does not authorize a new identity.

Run the matching detector scope while assessing, then again after the edit:

```bash
<skill-dir>/scripts/perfectuis detect --json --scope <layout|type|color|a11y|motion|all> <targets>
```

## layout

**Use for** uneven rhythm, weak grouping, arbitrary spacing, overflow from nested flex or grid, and hierarchy that does not match the task.

1. Name the primary path, what must sit together, and what must separate. Look at narrow, tablet, and wide widths before moving boxes.
2. Map spacing onto the `DESIGN.md` scale. Replace one-off margins and Tailwind bracket spacing (`p-[13px]`) with scale steps or a token.
3. Group with proximity first. Add a container only when the group needs its own boundary. Headings keep more space above than below.
4. Use `gap` for sibling rhythm. Give flex and grid children `min-width: 0` when text or tables overflow.
5. When a component's layout depends on its parent rather than the viewport, switch that component to a container query. Use `subgrid` when nested rows must line up with the parent tracks. Use `:has()` for parent state that is already in the DOM.
6. In Tailwind, theme keys only. In CSS Modules, Emotion, or styled-components, read spacing from custom properties, not raw pixel literals copied into each file.

**Example:**
```tsx
// Before: arbitrary off-scale values
<div className="p-[13px] mt-[7px]">
// After: mapped to the 4-based spacing scale
<div className="p-3 mt-2">
```

**Verify:** squinting still shows primary, then secondary, then groups. Keyboard order matches the visual order. Long and empty content do not collapse the structure. Detector scope `layout` has no unexplained hits.

## typeset

**Use for** flat hierarchy, unreadable measure, bad wrapping, and type that ignores the face or the theme.

1. Keep the families `DESIGN.md` already chose. Add a face only when an existing role cannot do the job.
2. Set body at 16px or larger. Keep prose between 45ch and 75ch, nearer 65–75ch for long reading. Widen leading as the measure grows. Align text to the start edge; avoid `text-align: justify`. Negative tracking on headings stops at -0.04em.
3. Set `text-wrap: balance` on headings and short centered text. Set `text-wrap: pretty` on body copy. Do not insert a hard break that lands mid-line on a phone.
4. Make adjacent roles differ in size or weight, not only in color. Use `font-variant-numeric: tabular-nums` for figures that should not jitter.
5. Load only the weights you use, with a metric-compatible fallback so text does not jump.
6. Tailwind `text-[13px]` and `leading-[1.07]` become theme roles. Do not set `font-family: monospace` on body copy.

**Example:**
```css
/* Before: default un-balanced wrapping and unbounded line length */
h1 { text-wrap: wrap; }
/* After: balanced heading and readable measure on body copy */
h1 { text-wrap: balance; }
p { text-wrap: pretty; max-inline-size: 68ch; }
```

**Verify:** heading, body, label, and metadata are distinct without reading them. 200% zoom and a longer translation still fit. Scope `type` is clean or each remaining hit is an intentional break.

## colorize

**Use for** contrast failures, raw color literals, theme leaks, and status shown only by hue.

1. List the roles already in `DESIGN.md`: canvas, elevated surface, primary text, secondary text, action, focus, border, and status. Edit roles, not one-off swatches.
2. For a new ramp, use `oklch()`. Change lightness first. Drop chroma as colors approach white or black. Tint neutrals from the brand hue only when that hue is already part of the system.
3. Meet 4.5:1 for body and placeholder text, 3:1 for large text and for non-text controls. Check hover, disabled, text on images, and both themes.
4. Pair status color with a word or icon. Build the dark theme as its own elevation steps.
5. Replace hex in components with tokens. Tailwind `text-[#112233]` and `bg-gray-400` on white are typical failures. CSS Modules and Emotion should reference the same custom properties as the stylesheet.
6. Leave alpha-composited text alone until you have replaced it with an explicit color you can measure.

**Example:**
```css
/* Before: fails WCAG AA (2.85:1 contrast against #ffffff) */
color: #999; background: #fff;
/* After: tokenized secondary text at 7.00:1 contrast against #ffffff */
color: var(--text-secondary); /* --text-secondary: #595959 */
```

**Verify:** the primary action is the strongest color, and it is not also used as decoration. Scope `color` reports no unexplained pair. Where the detector cannot see imported tokens, measure the computed colors.

## harden

**Use for** missing loading, empty, or error UI, unlabeled controls, overflow, and copy that assumes perfect data.

1. For each async region, render loading (stable footprint, `aria-busy` when helpful), empty (what is missing and the next action), error (cause and recovery), and the success path.
2. Give every input a visible label wired with `for`/`id`, or `aria-labelledby` when the visible label is elsewhere. Tie the error to the field with `aria-describedby`.
3. Icon-only buttons need an accessible name. Images need `alt`, empty when decorative. Replace `div` click handlers with `button` or `a`.
4. Every `<button>` has an explicit `type` attribute. Use `type="button"` for actions that do not submit a form; `type="submit"` for the primary form submit. Without it the browser defaults to `submit`, which submits the nearest ancestor form on Enter or click.
5. Never set `aria-hidden="true"` on an element that contains a focusable child (`<a>`, `<button>`, `<input>`, etc.). Assistive technology hides the content from the accessibility tree while keyboard focus can still reach it. Use `aria-hidden` only on decorative elements such as SVG icons.
6. Constrain user text with `min-width: 0`, `overflow-wrap: break-word`, and a line clamp only for secondary preview text. Keep the full value available.
7. Plan for strings about 30% longer, RTL, and large numbers. Format dates, numbers, and currency for the locale instead of hard-coding separators.
8. Do not treat a spinner as the empty state, or a toast as the only error.

**Example:**
```tsx
// Before: icon-only button without accessible name and no type
<button><svg/></button>
// After: accessible name, icon hidden from screen readers, explicit type
<button type="button" aria-label="Export report"><svg aria-hidden="true"/></button>
```

**Verify:** keyboard users can complete and recover the task. Scope `a11y` is clean or each `partial-states` hit is disproved. Extreme strings do not overlap the next control.

## adapt

**Use for** layouts that only work at one width, targets that are too small, hover-only interaction, and shells that ignore the device.

Adaptation changes the structure for the context. It does not scale the desktop frame down.

1. **Phone:** one column, primary actions in reach, 44px touch targets, no horizontal page scroll, type at least 16px so inputs do not zoom unexpectedly on iOS.
2. **Tablet:** a real intermediate layout, often two panes. Do not stretch a phone column across the width, and do not keep a three-column desktop grid.
3. **Foldable and dual-screen:** allow a hinge or fold to split list and detail. Test folded, unfolded, and a phone-width window on a large screen. Do not lock orientation to hide a bug.
4. **Desktop and large monitors:** use the width for the task, with a max measure so lines do not run to the edges of a 4K display. Keep hover as an extra, not the only path.
5. **Capacitor, Tauri, Electron, and other web shells:** respect safe-area insets, window resizing, and the system title bar. Do not trap keyboard focus. Do not assume a browser chrome or a phone viewport. Tauri and Electron still follow this web floor for HTML UI.
6. Replace `width: 800px` and `w-[500px]` with `max-width: 100%`, a scale token, or `clamp()`. Page regions reflow at 200% zoom and at 320px wide.
7. WCAG 2.2 requires at least 24×24 CSS px, or a 24px spacing circle that does not overlap the next target. Primary touch controls are 44×44. Dragging needs a click or keyboard alternative.
8. When a header or navigation bar uses `position: sticky` or `position: fixed`, add `scroll-padding-top` (or the matching side) to the scroll container so keyboard focus is never hidden beneath it (WCAG 2.4.11). Confirm in the browser: tab through the page and check that the focused element is fully visible.

**Example:**
```css
/* Before: fixed width overflows viewports under 800px */
.panel { width: 800px; }
/* After: responsive width bounded by maximum measure */
.panel { width: min(100%, 50rem); }
```

**Verify:** 320px, about 768px, and a wide window. Focus is not hidden under a sticky bar. Scope `layout` and scope `a11y` (target-size findings) are resolved.

## polish

**Use for** the last inconsistencies on a path that already works: radii, focus, selection, motion, and token drift. Polish does not redesign the screen.

1. Classify each drift. A missing token is added once. A one-off implementation should use the shared component. A local defect is fixed in place. A conceptual mismatch is reported, not quietly redesigned.
2. Radii, borders, and shadows come from `DESIGN.md`. Shadows keep an offset and a blur. Declare elevation once: choose either a clean border or a soft shadow, never both stacked on the same container.
3. Transition specific properties (`color`, `background-color`, `transform`) for about 150ms. Never `transition: all`.
4. `::selection`, caret, scrollbar, and `:focus-visible` use the product palette. The focus ring stays visible on the surfaces behind it.
5. If you add a view transition or a scroll-driven animation, it must be skippable: under `prefers-reduced-motion: reduce`, show the end state immediately. Motion is not the only sign that something changed.
6. Remove dead classes, unused style, and debug attributes left by the edit. Do not sweep unrelated files.

**Example:**
```css
/* Before: animates all properties; destroys keyboard focus indicator */
.btn { transition: all .3s; outline: none; }
/* After: transitions specific properties; visible focus ring */
.btn { transition: color .15s, background-color .15s; }
.btn:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
```

**Verify:** mouse, keyboard, and a narrow viewport on the same path. Scope `motion` is clean. The diff contains no new banned pattern from the craft floor.
