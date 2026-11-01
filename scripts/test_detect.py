#!/usr/bin/env python3
"""Fixture checks for the PrefectUIS detector."""

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


if __name__ == "__main__":
    unittest.main()
