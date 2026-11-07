#!/usr/bin/env python3
"""Fixture checks for the perfectUIs detector."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import detect


def rules_in(source: str, name: str = "Widget.tsx") -> set[str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        path.write_text(source, encoding="utf-8")
        return {item.rule for item in detect.scan_text(path, source, set(detect.RULE_INDEX))}


class DetectorTests(unittest.TestCase):
    def test_clean_control_is_quiet(self) -> None:
        source = """
        <button className="h-11 px-4" type="button">Export report</button>
        <label for="email">Email</label>
        <input id="email" />
        <img src="/a.png" alt="" />
        """
        self.assertEqual(rules_in(source), set())

    def test_contrast_pair_and_oklch(self) -> None:
        source = """
        .label { color: #9ca3af; background-color: #ffffff; font-size: 14px; }
        .ok { color: oklch(98% 0.01 250); background-color: oklch(20% 0.02 250); }
        """
        found = rules_in(source, "panel.css")
        self.assertIn("low-contrast-pair", found)
        self.assertNotIn("low-contrast-pair", rules_in(
            ".ok { color: oklch(98% 0.01 250); background: oklch(20% 0.02 250); }",
            "ok.css",
        ))

    def test_accessibility_and_tailwind(self) -> None:
        source = """
        <button className="size-4"><svg /></button>
        <div onClick={save}>Save</div>
        <img src="/hero.png" />
        <p className="text-gray-400 p-[13px]">Note</p>
        <span>🔥</span>
        """
        found = rules_in(source)
        self.assertTrue({
            "unlabeled-button",
            "undersized-target",
            "clickable-div",
            "missing-alt",
            "low-contrast-utility",
            "arbitrary-utility",
            "emoji-icon",
        } <= found)
        self.assertIn("unlabeled-field", rules_in('<input type="text" name="q" />', "Form.tsx"))
        self.assertIn("outline-removed", rules_in("button { outline: none; }", "button.css"))

    def test_motion_gradient_and_tokens(self) -> None:
        motion = ".hero { animation: rise 400ms ease; }\n@keyframes rise { from { opacity: 0; } }"
        self.assertIn("motion-without-reduced", rules_in(motion, "hero.css"))
        self.assertNotIn(
            "motion-without-reduced",
            rules_in(motion + "\n@media (prefers-reduced-motion: reduce) { .hero { animation: none; } }", "hero.css"),
        )
        self.assertIn(
            "gradient-text",
            rules_in(".title { background-clip: text; -webkit-text-fill-color: transparent; }", "type.css"),
        )
        tokens = ":root { --ink: #112233; }\n.body { color: var(--ink); }"
        self.assertNotIn("hardcoded-color", rules_in(tokens, "tokens.css"))
        self.assertIn("hardcoded-color", rules_in(".body { color: #112233; }", "card.css"))

    def test_partial_states_need_all_three_cues(self) -> None:
        bare = "export async function load() { const res = await fetch('/api/orders'); return res.json(); }\n"
        self.assertIn("partial-states", rules_in(bare, "Orders.tsx"))
        handled = bare + "if (isLoading) return <p>Loading orders</p>; if (isError) return <p>Could not load orders.</p>; if (rows.length === 0) return <p>No orders yet.</p>;"
        self.assertNotIn("partial-states", rules_in(handled, "Orders.tsx"))

    def test_scope_filters_rules(self) -> None:
        source = "<button></button>\n.box { width: 800px; }"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.css"
            path.write_text(source, encoding="utf-8")
            found = {item.rule for item in detect.scan_paths([path], set(detect.SCOPES["layout"]))}
        self.assertEqual(found, {"fixed-width"})

    def test_zoom_blocked_rule(self) -> None:
        blocked = '<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">'
        allowed = '<meta name="viewport" content="width=device-width, initial-scale=1">'
        self.assertIn("zoom-blocked", rules_in(blocked, "index.html"))
        self.assertNotIn("zoom-blocked", rules_in(allowed, "index.html"))

    def test_missing_lang_rule(self) -> None:
        missing = "<html><head><title>Test</title></head><body>Hello</body></html>"
        declared = '<html lang="en"><head><title>Test</title></head><body>Hello</body></html>'
        self.assertIn("missing-lang", rules_in(missing, "index.html"))
        self.assertNotIn("missing-lang", rules_in(declared, "index.html"))

    def test_positive_tabindex_rule(self) -> None:
        bad = '<button tabindex="1" type="button">Submit</button>'
        good = '<button tabindex="0" type="button">Submit</button><button tabIndex={-1}>Cancel</button>'
        self.assertIn("positive-tabindex", rules_in(bad, "Form.tsx"))
        self.assertNotIn("positive-tabindex", rules_in(good, "Form.tsx"))

    def test_viewport_unit_height_rule(self) -> None:
        bad_css = ".hero { height: 100vh; }"
        good_css = ".hero { height: 100dvh; }"
        self.assertIn("viewport-unit-height", rules_in(bad_css, "hero.css"))
        self.assertNotIn("viewport-unit-height", rules_in(good_css, "hero.css"))

    def test_root_font_size_rule(self) -> None:
        bad = "html { font-size: 12px; }"
        good = "html { font-size: 16px; } .card { font-size: 12px; }"
        self.assertIn("root-font-size", rules_in(bad, "global.css"))
        self.assertNotIn("root-font-size", rules_in(good, "global.css"))

    def test_placeholder_label_rule(self) -> None:
        bad = '<input type="text" placeholder="Search..." />'
        good = '<label>Search <input type="text" placeholder="Search..." /></label>'
        self.assertIn("placeholder-label", rules_in(bad, "Search.tsx"))
        self.assertNotIn("placeholder-label", rules_in(good, "Search.tsx"))

    def test_focus_not_obscured_rule(self) -> None:
        bad = "header { position: sticky; top: 0; background: white; }"
        good = "header { position: sticky; top: 0; }\nhtml { scroll-padding-top: 60px; }"
        self.assertIn("focus-not-obscured", rules_in(bad, "layout.css"))
        self.assertNotIn("focus-not-obscured", rules_in(good, "layout.css"))
        # Non-CSS files are not checked
        self.assertNotIn("focus-not-obscured", rules_in(bad, "Layout.tsx"))

    def test_missing_button_type_rule(self) -> None:
        bad = '<button onClick={save}>Save</button>'
        good_button = '<button type="button" onClick={save}>Save</button>'
        good_submit = '<button type="submit">Submit</button>'
        self.assertIn("missing-button-type", rules_in(bad, "Form.tsx"))
        self.assertNotIn("missing-button-type", rules_in(good_button, "Form.tsx"))
        self.assertNotIn("missing-button-type", rules_in(good_submit, "Form.tsx"))

    def test_aria_hidden_focusable_rule(self) -> None:
        bad_button = '<div aria-hidden="true"><button type="button">Close</button></div>'
        bad_link = '<div aria-hidden="true"><a href="/home">Home</a></div>'
        bad_jsx = '<div aria-hidden={true}><button type="button">x</button></div>'
        good_svg = '<svg aria-hidden="true"><path d="M0 0"/></svg>'
        good_text = '<div aria-hidden="true">decorative</div>'
        self.assertIn("aria-hidden-focusable", rules_in(bad_button, "Modal.tsx"))
        self.assertIn("aria-hidden-focusable", rules_in(bad_link, "Nav.tsx"))
        self.assertIn("aria-hidden-focusable", rules_in(bad_jsx, "Icon.tsx"))
        self.assertNotIn("aria-hidden-focusable", rules_in(good_svg, "Icon.tsx"))
        self.assertNotIn("aria-hidden-focusable", rules_in(good_text, "Widget.tsx"))

    def test_eyebrow_label_rule(self) -> None:
        bad = '<span className="uppercase tracking-widest text-xs">Category</span>'
        good = '<h2 className="text-xl font-bold">Category</h2>'
        self.assertIn("eyebrow-label", rules_in(bad, "Header.tsx"))
        self.assertNotIn("eyebrow-label", rules_in(good, "Header.tsx"))

    def test_hard_offset_shadow_rule(self) -> None:
        bad = ".card { box-shadow: 4px 4px 0 #000; }"
        good = ".card { box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); }"
        self.assertIn("hard-offset-shadow", rules_in(bad, "card.css"))
        self.assertNotIn("hard-offset-shadow", rules_in(good, "card.css"))

    def test_transition_all_rule(self) -> None:
        bad = ".btn { transition: all 150ms ease; }"
        good = ".btn { transition: color 150ms ease, background-color 150ms ease; }"
        self.assertIn("transition-all", rules_in(bad, "btn.css"))
        self.assertNotIn("transition-all", rules_in(good, "btn.css"))

    def test_tiny_text_rule(self) -> None:
        bad = ".note { font-size: 10px; }"
        good = ".note { font-size: 12px; }"
        self.assertIn("tiny-text", rules_in(bad, "note.css"))
        self.assertNotIn("tiny-text", rules_in(good, "note.css"))

    def test_monospace_body_rule(self) -> None:
        bad = "body { font-family: monospace; }"
        good = "body { font-family: sans-serif; } code { font-family: monospace; }"
        self.assertIn("monospace-body", rules_in(bad, "global.css"))
        self.assertNotIn("monospace-body", rules_in(good, "global.css"))

    def test_justified_text_rule(self) -> None:
        bad_css = ".prose { text-align: justify; }"
        good_css = ".prose { text-align: left; }"
        bad_tw = '<p className="text-justify">Body copy</p>'
        good_tw = '<p className="text-left">Body copy</p>'
        self.assertIn("justified-text", rules_in(bad_css, "article.css"))
        self.assertNotIn("justified-text", rules_in(good_css, "article.css"))
        self.assertIn("justified-text", rules_in(bad_tw, "Article.tsx"))
        self.assertNotIn("justified-text", rules_in(good_tw, "Article.tsx"))

    def test_extreme_negative_tracking_rule(self) -> None:
        bad_css = "h1 { letter-spacing: -0.05em; }"
        good_css = "h1 { letter-spacing: -0.02em; }"
        bad_tw = '<h1 className="tracking-[-0.05em]">Title</h1>'
        good_tw = '<h1 className="tracking-[-0.02em]">Title</h1>'
        self.assertIn("extreme-negative-tracking", rules_in(bad_css, "hero.css"))
        self.assertNotIn("extreme-negative-tracking", rules_in(good_css, "hero.css"))
        self.assertIn("extreme-negative-tracking", rules_in(bad_tw, "Hero.tsx"))
        self.assertNotIn("extreme-negative-tracking", rules_in(good_tw, "Hero.tsx"))


if __name__ == "__main__":
    unittest.main()
