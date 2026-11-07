# Changelog

## Unreleased

- Added automated weekly GitHub update check in `scripts/perfectuis` and `update` command.
- Updated `skill-improve.md` to guide cross-referencing upstream design skills (such as `https://github.com/pbakaus/impeccable`'s `skill/reference/`) to distill heuristics into simplified perfectUIs rules.
- Added WCAG 2.4.11 `focus-not-obscured` rule and guidance for sticky/fixed headers lacking `scroll-padding`.
- Added `missing-button-type` rule and guidance enforcing explicit `type="button"` or `type="submit"` on buttons.
- Added `aria-hidden-focusable` rule (P0) detecting focusable elements exposed inside `aria-hidden="true"` containers.
- Added `justified-text` rule and ban on `text-align: justify` producing uneven word rivers.
- Added `extreme-negative-tracking` rule enforcing the -0.04em heading tracking floor.
- Extended detector test suite to cover 100% of defined rules (31/31) with clean near-miss fixtures.
- Renamed prefectuis -> perfectUIs; added When-to-ask policy; added playbook examples; concrete verification.
