# PrefectUIS Craft Floor

Every UI edit meets this floor. A pinned product or `DESIGN.md` decision overrides a default. It does not override a line marked **Ban**.

The detector (`scripts/prefectuis detect --rules`) catches mechanical candidates. Hierarchy, copy, and whether a state actually helps still need a human look.

## Contrast and color

- Body text, placeholders, and disabled-looking text that still has to be read: **4.5:1** against the immediate background.
- Large text (24px, or 19px bold and above): **3:1**.
- Icons, input borders, and focus rings that show a control: **3:1** against the adjacent surface.
- Status is never color alone. Pair it with text, icon, or position.
- On a colored surface, secondary text comes from that surface hue or the foreground. Washed gray on a colored fill fails the floor.
- New web palettes use `oklch()` so lightness can change without a hue surprise. Keep high chroma away from near-white and near-black.
- Dark theme is designed as its own set of surfaces. Do not invert the light theme.
- Alpha stacks are a last resort for text. Prefer an explicit color when contrast depends on whatever sits behind the layer.
- WCAG AAA (7:1 body text, stricter focus appearance) applies only when the product asks for it.

## Type

- Ordinary body text is at least `1rem` (16px), unless a documented dense role or platform setting says otherwise.
- Reading measure is **45–75ch**. Long prose sits nearer **65–75ch**.
- Headings and short centered lines use `text-wrap: balance`. Body copy uses `text-wrap: pretty`. Both are progressive enhancements.
- Break a heading by hand only between phrases, and check that break at every width.
- Line-height follows the face, the measure, and the theme. Light text on dark needs slightly more leading, a touch more tracking, and sometimes one step more weight.
- Role steps are obvious in size or weight. Repeated roles stay identical.
- Tabular numerals for columns of numbers, prices, and timers.
- Monospace is for code, identifiers, and measurement. **Ban:** monospace as a costume for ordinary UI copy.

## Space and structure

- Use the project spacing scale. A 4-based scale (4, 8, 12, 16, 24, 32, 48, 64) is the default when `DESIGN.md` has none.
- Related items sit closer than separate groups. A heading has more space above it than below it.
- Prefer `gap` on the parent over one-off margins on every child.
- Flex and grid children that hold text get `min-width: 0` so long strings can shrink.
- Alignment may be optical when a glyph or icon is visibly heavier than its box.
- Container queries (`@container`) when the same component sits in different parents. Viewport queries when the page itself changes.
- `subgrid` when nested tracks must share the parent columns.
- `:has()` when parent state can be expressed without an extra script class.

**Ban:** a card nested inside a card.

**Ban:** a kicker or eyebrow (tiny uppercase category label) above a heading. The heading carries the label's job.

Defaults to reject unless `DESIGN.md` already chose them: identical icon-plus-heading-plus-text cards as the page structure, a hero metric with a big number and three supporting stats, decorative section numbers, a modal for a task that does not need interruption, and a thick colored side border on cards, rows, or alerts.

## Targets, focus, and input

- WCAG 2.2 target size minimum is **24×24 CSS px**, or spacing that keeps a 24px circle around the target clear of the next target. Primary touch controls are **44×44 px**.
- Every control has visible `:focus-visible`. Do not remove `outline` without a replacement. Focus contrast is at least 3:1, and sticky headers or footers must not cover the focused item (WCAG 2.2 Focus Not Obscured).
- Anything draggable also works with a single click or keyboard action (WCAG 2.2 Dragging Movements).
- Hover does not hide the only copy, action, or status.
- Hit order matches visual order and DOM order.
- Buttons and links name the action ("Export report", not "Submit" or "Click here"). Icon-only controls have an accessible name.
- Inputs have a visible `<label>` (or `aria-label` / `aria-labelledby` when a visible label would be wrong), errors use `aria-describedby`, and errors say what happened and how to recover.

## States

Interactive UI shows the states the task can actually reach: default, hover, focus-visible, active, disabled, loading, empty, error, and success when success is not obvious. Loading reserves the layout it will occupy. Empty states say what is missing and what to do next.

Text survives long strings, a missing string, and about 30% expansion for translation. Use `overflow-wrap: break-word` for unbreakable tokens. Do not rely on a single-line ellipsis for primary content.

## Motion and browser chrome

- One deliberate motion, eased out, starting from a visible default. Prefer opacity, transform, and a small amount of filter or clip when they stay smooth.
- `prefers-reduced-motion: reduce` shows the end state and keeps any cue required to understand the change.
- View transitions and scroll-driven animations are optional wayfinding. They are not required to operate the page, and they get the same reduced-motion path.
- Do not set `transition: all`.
- Theme `::selection`, the caret, scrollbars, focus, underline offset, and tabular numerals from the product palette.
- Shadows have an offset and a soft blur. **Ban:** `box-shadow` with zero blur as decoration, unless `DESIGN.md` is explicitly neobrutalist.
- **Ban:** gradient text. Emphasis comes from weight, size, or contrast.
- **Ban:** emoji or other Unicode glyphs as the icon system. Use one SVG or icon set with a consistent stroke.
- Glass blur is a material for a specific layer, not a default card fill.

## Frameworks

- **Tailwind:** spacing, color, type, and radius come from the theme. Arbitrary values such as `p-[13px]` or `text-[#333]` are a defect when a token exists or the value is off the scale. A one-off that repeats becomes a token.
- **CSS Modules, Vue scoped CSS, styled-components, Emotion:** put color and space in custom properties or the theme object. Do not repeat hex in component styles. Class names describe the role.
- **React, Next.js, Vue, Svelte, Astro:** use `button` and `a` for actions and navigation. Do not put click handlers on `div` or `span`. Images have `alt` (`alt=""` only when the image is decorative).

## Detector limits

`detect` can flag gradient text, eyebrow-like class clusters, hard shadows, emoji-only text nodes, color literals, simple contrast pairs (hex, rgb, oklch), weak gray utilities, arbitrary utilities, wide fixed widths, sub-12px type, unlabeled buttons, missing `alt`, unlabeled fields, clickable non-controls, removed outlines, `transition: all`, sub-24px target utilities, motion without `prefers-reduced-motion`, monospace on `body`/`html`, and fetch-like components missing loading, error, or empty cues.

It cannot compute styles across imported tokens, CSS-in-JS theme functions, or the rendered cascade. Confirm contrast and target size in the browser when the source check is incomplete.
