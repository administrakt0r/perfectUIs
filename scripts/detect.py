#!/usr/bin/env python3
"""perfectUIs source detector.

Regex and small CSS color checks for craft-floor defects. Findings are
candidates: confirm each one in context before editing.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

EXTENSIONS = {
    ".html",
    ".htm",
    ".css",
    ".scss",
    ".vue",
    ".svelte",
    ".astro",
    ".jsx",
    ".tsx",
    ".js",
    ".ts",
    ".mjs",
    ".cjs",
}

SKIP_DIRS = {
    "node_modules",
    "dist",
    "build",
    ".git",
    "coverage",
    ".next",
    ".nuxt",
    ".output",
    ".perfectuis",
    "vendor",
}

RULES = [
    ("gradient-text", "P1", "polish", "Gradient text (background clipped to the glyphs)."),
    ("eyebrow-label", "P2", "typeset", "Tiny uppercase tracked label, the usual eyebrow pattern."),
    ("hard-offset-shadow", "P2", "polish", "Zero-blur offset shadow."),
    ("emoji-icon", "P2", "polish", "Emoji used as an icon with no accompanying text."),
    ("hardcoded-color", "P2", "colorize", "Color literal outside a custom-property definition."),
    ("low-contrast-pair", "P1", "colorize", "Declared foreground/background pair under WCAG AA."),
    ("low-contrast-utility", "P2", "colorize", "Utility classes that usually fail 4.5:1 on a light surface."),
    ("arbitrary-utility", "P2", "layout", "Arbitrary bracket utility instead of a theme token."),
    ("fixed-width", "P1", "adapt", "Fixed width of 480px or more."),
    ("tiny-text", "P1", "typeset", "Font size below 12px."),
    ("unlabeled-button", "P0", "harden", "Button with no accessible name."),
    ("missing-alt", "P0", "harden", "Image missing an alt attribute."),
    ("unlabeled-field", "P1", "harden", "Field with no label, aria-label, or aria-labelledby."),
    ("clickable-div", "P0", "harden", "Click handler on a non-interactive element."),
    ("outline-removed", "P1", "polish", "Outline removed and no :focus-visible replacement in the file."),
    ("transition-all", "P2", "polish", "transition: all (or transition-all) animates layout properties."),
    ("undersized-target", "P1", "adapt", "Control sized under the 24px WCAG 2.2 minimum."),
    ("motion-without-reduced", "P1", "polish", "Authored motion with no prefers-reduced-motion alternative."),
    ("monospace-body", "P2", "typeset", "Monospace set on body or html."),
    ("partial-states", "P2", "harden", "Fetch-like code without loading, error, and empty cues."),
    ("zoom-blocked", "P1", "adapt", "Viewport meta blocks user zoom (user-scalable=no or maximum-scale=1)."),
    ("missing-lang", "P1", "harden", "<html> element missing a lang attribute."),
    ("positive-tabindex", "P2", "harden", "Positive tabindex disrupts natural focus order."),
    ("viewport-unit-height", "P2", "layout", "height: 100vh on mobile layout; suggest 100dvh."),
    ("root-font-size", "P1", "typeset", "Root font-size below 16px."),
    ("placeholder-label", "P1", "harden", "Placeholder used as the only label."),
]

RULE_INDEX = {rule_id: (severity, playbook, summary) for rule_id, severity, playbook, summary in RULES}

SCOPES = {
    "all": set(RULE_INDEX),
    "layout": {"arbitrary-utility", "fixed-width", "viewport-unit-height"},
    "type": {"eyebrow-label", "tiny-text", "monospace-body", "root-font-size"},
    "color": {"gradient-text", "hardcoded-color", "low-contrast-pair", "low-contrast-utility", "hard-offset-shadow"},
    "a11y": {
        "low-contrast-pair",
        "low-contrast-utility",
        "tiny-text",
        "unlabeled-button",
        "missing-alt",
        "unlabeled-field",
        "clickable-div",
        "outline-removed",
        "undersized-target",
        "partial-states",
        "zoom-blocked",
        "missing-lang",
        "positive-tabindex",
        "placeholder-label",
    },
    "motion": {"motion-without-reduced", "transition-all"},
}


def rel_luminance(r: float, g: float, b: float) -> float:
    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(fg: tuple[float, float, float], bg: tuple[float, float, float]) -> float:
    l1 = rel_luminance(*fg)
    l2 = rel_luminance(*bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def oklch_to_srgb(lightness: float, chroma: float, hue: float) -> tuple[float, float, float]:
    a = chroma * math.cos(math.radians(hue))
    b = chroma * math.sin(math.radians(hue))
    l_ = lightness + 0.3963377774 * a + 0.2158037573 * b
    m_ = lightness - 0.1055613458 * a - 0.0638541728 * b
    s_ = lightness - 0.0894841775 * a - 1.2914855480 * b
    l = l_ ** 3
    m = m_ ** 3
    s = s_ ** 3
    red = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    green = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    blue = -0.0041960362 * l - 0.7034186147 * m + 1.4578034394 * s

    def gamma(c: float) -> float:
        c = min(1.0, max(0.0, c))
        if c <= 0.0031308:
            return 12.92 * c
        return 1.055 * (c ** (1 / 2.4)) - 0.055

    return gamma(red), gamma(green), gamma(blue)


def parse_color(raw: str) -> tuple[float, float, float] | None:
    value = raw.strip().lower()
    named = {
        "white": (1.0, 1.0, 1.0),
        "black": (0.0, 0.0, 0.0),
    }
    if value in named:
        return named[value]
    hex_match = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6}|[0-9a-f]{8})", value)
    if hex_match:
        digits = hex_match.group(1)
        if len(digits) == 3:
            digits = "".join(ch * 2 for ch in digits)
        if len(digits) == 8 and int(digits[6:8], 16) < 255:
            return None
        return tuple(int(digits[i : i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]
    rgb_match = re.fullmatch(
        r"rgba?\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*([0-9.]+)(?:\s*,\s*([0-9.]+)\s*)?\)",
        value,
    )
    if rgb_match:
        if rgb_match.group(4) is not None and float(rgb_match.group(4)) < 1:
            return None
        return tuple(float(rgb_match.group(i)) / 255 for i in (1, 2, 3))  # type: ignore[return-value]
    oklch_match = re.fullmatch(
        r"oklch\(\s*([0-9.]+)(%?)\s+([0-9.]+)\s+([0-9.]+)(?:deg)?\s*\)",
        value,
    )
    if oklch_match:
        lightness = float(oklch_match.group(1))
        if oklch_match.group(2) == "%" or lightness > 1:
            lightness /= 100
        return oklch_to_srgb(lightness, float(oklch_match.group(3)), float(oklch_match.group(4)))
    return None


class Finding:
    def __init__(self, rule: str, path: str, line: int, message: str) -> None:
        severity, playbook, _summary = RULE_INDEX[rule]
        self.rule = rule
        self.severity = severity
        self.playbook = playbook
        self.path = path
        self.line = line
        self.message = message

    def as_dict(self) -> dict[str, object]:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "playbook": self.playbook,
            "file": self.path,
            "line": self.line,
            "message": self.message,
        }


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", lambda m: " " * (m.end() - m.start()), text, flags=re.S)
    text = re.sub(r"(^|[^:])//.*?$", lambda m: " " * (m.end() - m.start()), text, flags=re.M)
    return text


def iter_files(paths: list[Path]) -> list[Path]:
    found: list[Path] = []
    for raw in paths:
        if raw.is_file() and raw.suffix.lower() in EXTENSIONS:
            found.append(raw)
            continue
        if not raw.is_dir():
            continue
        for path in raw.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            found.append(path)
    return found


def add(findings: list[Finding], enabled: set[str], rule: str, path: str, line: int, message: str) -> None:
    if rule in enabled:
        findings.append(Finding(rule, path, line, message))


def scan_text(path: Path, text: str, enabled: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    display = str(path)
    source = strip_comments(text)
    suffix = path.suffix.lower()

    if "gradient-text" in enabled:
        for match in re.finditer(r'class(?:Name)?\s*=\s*["\']([^"\']+)["\']', source):
            classes = match.group(1)
            if "bg-clip-text" in classes and "text-transparent" in classes:
                add(findings, enabled, "gradient-text", display, line_of(source, match.start()), "bg-clip-text with text-transparent.")
        for match in re.finditer(r"background-clip\s*:\s*text|-webkit-background-clip\s*:\s*text", source):
            window = source[max(0, match.start() - 240) : match.end() + 240]
            if re.search(r"text-fill-color\s*:\s*transparent|-webkit-text-fill-color\s*:\s*transparent", window):
                add(
                    findings,
                    enabled,
                    "gradient-text",
                    display,
                    line_of(source, match.start()),
                    "background-clip: text with a transparent fill.",
                )

    if "eyebrow-label" in enabled:
        for match in re.finditer(r'class(?:Name)?\s*=\s*["\']([^"\']+)["\']', source):
            classes = match.group(1)
            if (
                re.search(r"(?:^|\s)uppercase(?:\s|$)", classes)
                and re.search(r"(?:^|\s)tracking-(?:widest|wider|\[)", classes)
                and re.search(r"(?:^|\s)text-(?:xs|\[(?:[0-9]|1[01])px\])(?:\s|$)", classes)
            ):
                add(findings, enabled, "eyebrow-label", display, line_of(source, match.start()), "Class list matches an eyebrow label.")

    if "hard-offset-shadow" in enabled:
        for match in re.finditer(
            r"box-shadow\s*:\s*-?\d+(?:px)?\s+-?\d+(?:px)?\s+0(?:px)?(?:\s+0(?:px)?)?(?:\s+[#(a-z])?",
            source,
        ):
            add(findings, enabled, "hard-offset-shadow", display, line_of(source, match.start()), match.group(0).strip())

    if "emoji-icon" in enabled:
        for match in re.finditer(r">([^<>]{1,12})<", source):
            chunk = match.group(1).strip()
            if not chunk or re.search(r"[A-Za-z0-9]", chunk):
                continue
            if re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", chunk):
                add(findings, enabled, "emoji-icon", display, line_of(source, match.start()), f"Text node is only an emoji: {chunk}")

    if "arbitrary-utility" in enabled:
        pattern = re.compile(
            r"(?:^|[\s\"'`])((?:[a-z0-9-]+:)*(?:p|px|py|pt|pb|pl|pr|m|mx|my|mt|mb|ml|mr|"
            r"gap|gap-x|gap-y|w|h|min-w|max-w|min-h|max-h|size|top|left|right|bottom|"
            r"inset|text|leading|tracking|rounded|basis)-\[(?!var\()[^\]]+\])"
        )
        for match in pattern.finditer(source):
            add(findings, enabled, "arbitrary-utility", display, line_of(source, match.start()), match.group(1))

    if "fixed-width" in enabled:
        for match in re.finditer(r"(?<![\w-])width\s*:\s*([0-9]+)px\b", source):
            if int(match.group(1)) >= 480:
                add(findings, enabled, "fixed-width", display, line_of(source, match.start()), match.group(0).strip())

    if "tiny-text" in enabled:
        for match in re.finditer(r"(?<![\w-])font-size\s*:\s*(1[01]|[0-9])px\b", source):
            add(findings, enabled, "tiny-text", display, line_of(source, match.start()), match.group(0).strip())
        for match in re.finditer(r"text-\[(?:[0-9]|1[01])px\]", source):
            add(findings, enabled, "tiny-text", display, line_of(source, match.start()), match.group(0))

    if "hardcoded-color" in enabled and suffix in {".css", ".scss", ".vue", ".svelte", ".astro", ".jsx", ".tsx", ".html", ".htm"}:
        for index, line in enumerate(source.splitlines(), start=1):
            if re.search(r"--[A-Za-z0-9_-]+\s*:", line):
                continue
            if "url(" in line:
                continue
            for match in re.finditer(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]+\)|oklch\([^)]+\)", line):
                token = match.group(0)
                if token.startswith("#") and len(token) not in {4, 7, 9}:
                    continue
                add(findings, enabled, "hardcoded-color", display, index, token)

    if "low-contrast-pair" in enabled:
        for match in re.finditer(r"\{[^{}]+\}", source):
            block = match.group(0)
            color = re.search(r"(?<![\w-])color\s*:\s*([^;]+)", block)
            background = re.search(r"background(?:-color)?\s*:\s*([^;]+)", block)
            if not color or not background:
                continue
            fg = parse_color(color.group(1).strip())
            bg = parse_color(background.group(1).strip())
            if fg is None or bg is None:
                continue
            ratio = contrast_ratio(fg, bg)
            large = bool(re.search(r"font-size\s*:\s*(\d+)px", block) and int(re.search(r"font-size\s*:\s*(\d+)px", block).group(1)) >= 24)
            minimum = 3.0 if large else 4.5
            if ratio + 1e-6 < minimum:
                add(
                    findings,
                    enabled,
                    "low-contrast-pair",
                    display,
                    line_of(source, match.start()),
                    f"{ratio:.2f}:1 is below {minimum:.1f}:1 ({color.group(1).strip()} on {background.group(1).strip()}).",
                )

    if "low-contrast-utility" in enabled:
        for match in re.finditer(r'class(?:Name)?\s*=\s*["\']([^"\']+)["\']', source):
            classes = match.group(1)
            if re.search(r"bg-(?:gray|slate|zinc|neutral|stone|black)-(?:[6-9]00|950)", classes):
                continue
            weak = re.search(r"(?:^|\s)text-(?:gray|slate|zinc|neutral|stone)-(?:300|400)(?:\s|$)", classes)
            if weak:
                add(
                    findings,
                    enabled,
                    "low-contrast-utility",
                    display,
                    line_of(source, match.start()),
                    f"{weak.group(0).strip()} is typically under 4.5:1 on white. Confirm the computed pair.",
                )

    if "unlabeled-button" in enabled:
        for match in re.finditer(r"<button\b([^>]*)>(.*?)</button>", source, flags=re.I | re.S):
            attrs, inner = match.group(1), match.group(2)
            if re.search(r"aria-label\s*=|aria-labelledby\s*=", attrs, re.I):
                continue
            if "{" in inner:
                continue
            visible = re.sub(r"<[^>]+>", "", inner)
            visible = re.sub(r"&[a-z]+;", "", visible).strip()
            if visible:
                continue
            add(findings, enabled, "unlabeled-button", display, line_of(source, match.start()), "Button has no text or aria-label.")

    if "missing-alt" in enabled:
        for match in re.finditer(r"<img\b([^>]*)>", source, flags=re.I):
            if not re.search(r"\balt\s*=", match.group(1), re.I):
                add(findings, enabled, "missing-alt", display, line_of(source, match.start()), "img has no alt attribute.")

    if "unlabeled-field" in enabled:
        for match in re.finditer(r"<(input|select|textarea)\b([^>]*)>", source, flags=re.I):
            attrs = match.group(2)
            if re.search(r"type\s*=\s*[\"']hidden[\"']", attrs, re.I):
                continue
            if re.search(r"aria-label\s*=|aria-labelledby\s*=|title\s*=", attrs, re.I):
                continue
            id_match = re.search(r"\bid\s*=\s*[\"']([^\"']+)[\"']", attrs)
            if id_match and re.search(r"\bfor\s*=\s*[\"']" + re.escape(id_match.group(1)) + r"[\"']", source):
                continue
            before = source[max(0, match.start() - 400) : match.start()]
            if re.search(r"<label\b[^>]*>[^<]*$", before, flags=re.I | re.S):
                continue
            add(findings, enabled, "unlabeled-field", display, line_of(source, match.start()), f"{match.group(1)} has no associated label.")

    if "clickable-div" in enabled:
        for match in re.finditer(r"<(div|span|li)\b[^>]*\b(?:onClick|@click|v-on:click)\s*=", source):
            add(findings, enabled, "clickable-div", display, line_of(source, match.start()), f"<{match.group(1)}> has a click handler.")

    if "outline-removed" in enabled and ":focus-visible" not in source and "focus-visible:" not in source:
        for match in re.finditer(r"(?<![\w-])outline\s*:\s*(?:none|0)\b|outline-none", source):
            add(findings, enabled, "outline-removed", display, line_of(source, match.start()), "Outline removed with no focus-visible rule in this file.")

    if "transition-all" in enabled:
        for match in re.finditer(r"(?<![\w-])transition\s*:\s*all\b|transition-all", source):
            add(findings, enabled, "transition-all", display, line_of(source, match.start()), match.group(0).strip())

    if "undersized-target" in enabled:
        for match in re.finditer(r"<(button|a)\b([^>]*)>", source, flags=re.I):
            classes = match.group(2)
            if re.search(r"(?:^|[\s\"'`])(?:size|w|h)-(?:[1-5]|\[(?:[0-9]|1[0-9]|2[0-3])px\])\b", classes):
                add(
                    findings,
                    enabled,
                    "undersized-target",
                    display,
                    line_of(source, match.start()),
                    "Control uses a utility under 24px. WCAG 2.2 target size minimum is 24px; primary touch targets should be 44px.",
                )

    if "motion-without-reduced" in enabled and "prefers-reduced-motion" not in source:
        match = re.search(r"view-transition|scroll-timeline|@keyframes|(?<![\w-])animation\s*:", source)
        if match:
            add(
                findings,
                enabled,
                "motion-without-reduced",
                display,
                line_of(source, match.start()),
                "Motion has no prefers-reduced-motion alternative in this file.",
            )

    if "monospace-body" in enabled:
        for match in re.finditer(r"(?:^|\n)\s*(?:body|html)\s*\{[^}]*font-family\s*:[^;}]*monospace", source, flags=re.I):
            add(findings, enabled, "monospace-body", display, line_of(source, match.start()), "body or html uses a monospace family.")

    if "partial-states" in enabled and suffix in {".jsx", ".tsx", ".vue", ".svelte"}:
        fetch_at = re.search(r"\buse(?:Query|SWR)\b|\bawait\s+fetch\s*\(|\bfetch\s*\(", source)
        if fetch_at:
            missing = []
            if not re.search(r"\b(isLoading|isPending|aria-busy|skeleton|Spinner)\b", source):
                missing.append("loading")
            if not re.search(r"\b(isError|setError|catch)\b|catch\s*\(", source):
                missing.append("error")
            if not re.search(r"\bempty\b|length\s*===\s*0|length\s*==\s*0|No results", source, flags=re.I):
                missing.append("empty")
            if missing:
                add(
                    findings,
                    enabled,
                    "partial-states",
                    display,
                    line_of(source, fetch_at.start()),
                    "Fetch-like code has no visible cue for: " + ", ".join(missing) + ". Confirm before adding UI.",
                )

    if "zoom-blocked" in enabled:
        for match in re.finditer(r"<meta\b([^>]*)>", source, flags=re.I):
            attrs = match.group(1)
            if re.search(r"\bname\s*=\s*[\"']viewport[\"']", attrs, re.I):
                content_match = re.search(r"\bcontent\s*=\s*[\"']([^\"']*)[\"']", attrs, re.I)
                if content_match:
                    content = content_match.group(1)
                    if re.search(r"user-scalable\s*=\s*(?:no|0)\b|maximum-scale\s*=\s*(?:1(?:\.0+)?|0(?:\.[0-9]+)?)\b", content, re.I):
                        add(findings, enabled, "zoom-blocked", display, line_of(source, match.start()), "Viewport meta blocks user zoom.")

    if "missing-lang" in enabled:
        for match in re.finditer(r"<html\b([^>]*)>", source, flags=re.I):
            attrs = match.group(1)
            if not re.search(r"\blang\s*=", attrs, re.I):
                add(findings, enabled, "missing-lang", display, line_of(source, match.start()), "<html> tag is missing a lang attribute.")

    if "positive-tabindex" in enabled:
        for match in re.finditer(r"\btabindex\s*=\s*[\"']?([1-9][0-9]*)[\"']?|\btabIndex\s*=\s*(?:[\"']?([1-9][0-9]*)[\"']?|\{\s*([1-9][0-9]*)\s*\})", source):
            add(findings, enabled, "positive-tabindex", display, line_of(source, match.start()), "Positive tabindex disrupts natural focus order.")

    if "viewport-unit-height" in enabled:
        for match in re.finditer(r"(?<![\w-])height\s*:\s*100vh\b", source):
            add(findings, enabled, "viewport-unit-height", display, line_of(source, match.start()), "height: 100vh causes mobile viewport overflow; suggest 100dvh.")
        for match in re.finditer(r"(?:^|[\s\"'`])(h-screen)(?:[\s\"'`]|$)", source):
            add(findings, enabled, "viewport-unit-height", display, line_of(source, match.start(1)), "h-screen uses 100vh; suggest h-dvh.")

    if "root-font-size" in enabled:
        for match in re.finditer(r"(?:^|\n)\s*(?:html|:root)\s*\{[^}]*(?<![\w-])font-size\s*:\s*([0-9]|1[0-5])px\b", source, flags=re.I):
            add(findings, enabled, "root-font-size", display, line_of(source, match.start()), "Root font-size is below 16px.")

    if "placeholder-label" in enabled:
        for match in re.finditer(r"<(input|textarea)\b([^>]*)>", source, flags=re.I):
            attrs = match.group(2)
            if not re.search(r"\bplaceholder\s*=", attrs, re.I):
                continue
            if re.search(r"type\s*=\s*[\"']hidden[\"']", attrs, re.I):
                continue
            if re.search(r"aria-label\s*=|aria-labelledby\s*=|title\s*=", attrs, re.I):
                continue
            id_match = re.search(r"\bid\s*=\s*[\"']([^\"']+)[\"']", attrs)
            if id_match and re.search(r"\bfor\s*=\s*[\"']" + re.escape(id_match.group(1)) + r"[\"']", source):
                continue
            before = source[max(0, match.start() - 400) : match.start()]
            if re.search(r"<label\b[^>]*>[^<]*$", before, flags=re.I | re.S):
                continue
            add(findings, enabled, "placeholder-label", display, line_of(source, match.start()), f"<{match.group(1)}> uses placeholder as its only label.")

    return findings


def scan_paths(paths: list[Path], enabled: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(paths):
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if len(data) > 1_000_000 or b"\0" in data[:1024]:
            continue
        findings.extend(scan_text(path, data.decode("utf-8", errors="replace"), enabled))
    severity_order = {"P0": 0, "P1": 1, "P2": 2}
    findings.sort(key=lambda item: (severity_order[item.severity], item.path, item.line, item.rule))
    return findings


def print_rules() -> None:
    for rule_id, severity, playbook, summary in RULES:
        print(f"{severity}  {rule_id}  playbook={playbook}  {summary}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="perfectuis detect", description="Scan frontend source for perfectUIs craft defects.")
    parser.add_argument("--json", action="store_true", help="Print findings as JSON.")
    parser.add_argument("--rules", action="store_true", help="List detector rules and exit.")
    parser.add_argument("--scope", default="all", choices=sorted(SCOPES), help="Limit rules to one domain.")
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args(argv)

    if args.rules:
        print_rules()
        return 0
    if not args.paths:
        parser.error("pass at least one file or directory")

    findings = scan_paths(args.paths, set(SCOPES[args.scope]))
    if args.json:
        json.dump({"findings": [item.as_dict() for item in findings]}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    elif not findings:
        print("No findings.")
    else:
        for item in findings:
            print(f"{item.severity} {item.rule} {item.path}:{item.line}  {item.message}  [{item.playbook}]")
        print(f"\n{len(findings)} finding(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
