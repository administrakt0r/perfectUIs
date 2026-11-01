# PrefectUIS Craft Floor

The Craft Floor defines the non-negotiable standards for visual polish, interaction quality, and UX rigor. Every UI refinement made under PrefectUIS must satisfy these requirements.

---

## 1. Non-Negotiable Quality Requirements

### Contrast & Legibility
- **Body & placeholder text**: Must meet WCAG AA standard of ≥ 4.5:1 against its background.
- **Large text (≥ 18pt or 14pt bold)**: Must meet ≥ 3.0:1.
- **Colored surfaces**: Secondary text must be a tinted shade of the background hue or foreground; never plain washed-out gray on colored backgrounds.

### Depth & Elevation
- Shadows must have a realistic directional offset and a soft blur.
- Do not use zero-offset colored halos as pseudo-shadows.

### Spacing & Rhythm
- Spacing must follow an intentional scale (e.g. 4px / 8px / 16px / 24px / 32px / 48px).
- Group related items tightly; separate distinct groups generously.
- Headings must have noticeably more space above them than below them to maintain section anchoring.
- Honor optical alignment over strict mathematical bounding box alignment when visual weight is unbalanced.

### Typography
- **Body measure**: Keep text line length within 65–75 characters per line (`ch`) for comfortable reading.
- **Headings**: Use `text-wrap: balance` for clean line wrapping without trailing single words (widows).
- **Scale**: Maintain clear typographic hierarchy with distinct weight, size, and line-height steps between levels.
- **Tracking**: Avoid unnatural letter spacing; keep body tracking at standard zero, small caps or uppercase slightly tracked out (+0.05em), display headings tight.

### States & Resilience
- Every interactive control must provide distinct, polished states:
  - Default / Rest
  - Hover
  - Focus (`:focus-visible` with high-contrast ring)
  - Active / Pressed
  - Disabled (with proper `aria-disabled` or disabled styling)
  - Loading / Pending
  - Empty (informative empty state with clear call-to-action)
  - Error (clear problem description and actionable recovery)

### Polished Browser Surfaces
- The unstyled default browser controls reflect an incomplete UI. Ensure:
  - Custom themed text selection (`::selection`) using palette accent colors.
  - Styled scrollbars where visible.
  - Accessible, themed focus rings that do not rely on browser default blue halos.
  - Tabular numerals (`font-variant-numeric: tabular-nums`) for numeric data and timers.

### Content & Microcopy
- Buttons and action elements must name their specific action (e.g., "Export report" instead of "Submit").
- Error messages must explain what happened and how to resolve it.

---

## 2. Prohibited Anti-Patterns (Refusals)

Avoid these category cliches and AI-slop patterns unless explicitly mandated by the user:

1. **No Gradient Text**: Gradient text harms legibility. Visual weight and emphasis must come from font weight, size, or contrast.
2. **No Eyebrows / Kickers**: Do not put tiny uppercase category labels floating above headings. Headings should carry their own authority.
3. **No Card Spam**: Avoid defaulting to identical 3-column card grids (icon + heading + paragraph). Use semantic layouts, list structures, tables, or asymmetric compositions.
4. **No Nested Cards**: Never put a card inside another card.
5. **No Fake Emoji Icons**: Do not use raw Unicode emojis in place of an icon system. Use coherent SVG icons with consistent stroke weights.
6. **No Monospace as Costume**: Only use monospace typography for real code snippets, technical metrics, or tabular data.
7. **No Zero-Blur Hard Shadows**: Do not add `box-shadow: 4px 4px 0` block shadows unless the design system is intentionally neobrutalist.
