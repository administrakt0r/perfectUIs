# PrefectUIS Skill Improvement Guide & AI Prompt

This document contains a comprehensive, ready-to-copy-paste prompt to provide to an AI assistant (such as Antigravity, Claude, or ChatGPT) whenever you want to research upstream design updates, identify weaknesses in PrefectUIS, and upgrade the skill.

---

## 📋 Copy-Paste Prompt for AI Assistants

Copy and paste the prompt below into your AI coding assistant:

```markdown
You are an expert AI skill author and design systems engineer. 

I need you to audit, enhance, and upgrade the **PrefectUIS** repository (`prefectuis`), ensuring it incorporates the latest cutting-edge UI engineering standards, best practices, and automated detection techniques.

### Core Objectives:
1. **Research Upstream & Modern UI Innovations**:
   - Inspect the latest documentation, rules, and updates from modern design systems and reference systems such as https://impeccable.style/ (or local installations if present).
   - Check for new anti-patterns, updated accessibility rules (WCAG 2.2 / AAA additions), modern CSS capabilities (container queries, CSS `:has()`, view transitions, subgrid, modern color spaces like OKLCH), and responsive/touch guidelines.

2. **Audit PrefectUIS for Weaknesses & Gaps**:
   - Thoroughly examine all files in this repository:
     - `SKILL.md` (Workflow orchestration, 6-stage lifecycle, review gates)
     - `reference/craft-floor.md` (Quality floor, contrast, typography, prohibited anti-patterns)
     - `reference/playbooks.md` (Layout, typeset, colorize, harden, adapt, polish playbooks)
     - `reference/backlog-template.md` (Durable `.prefectuis/backlog.md` format)
     - `scripts/` (Detector scripts and CLI wrappers)
   - Identify any missing edge cases, weak rules, vague instructions, or gaps across frontend frameworks (e.g., React, Next.js, Vue, Svelte, Astro, Tailwind CSS, Vanilla CSS).

3. **Enhance and Upgrade**:
   - Improve the specialized playbooks with modern, high-impact techniques.
   - Tighten the Craft Floor with actionable, verifiable rules.
   - Refine the 6-stage execution lifecycle to ensure maximum reliability and seamless 1–2 issue incremental resolution.
   - Optimize `SKILL.md` for Skill Discovery Optimization (SDO) in line with standard agent skill specifications (clear "Use when..." description without leaking workflow summaries into frontmatter).

4. **Strict Isolation & Rebranding Invariant**:
   - All tools, artifacts, directories, and documentation MUST remain branded strictly as **`prefectuis`** (e.g., `.prefectuis/backlog.md`, `scripts/prefectuis`).
   - Do NOT include any upstream brand names (such as "impeccable") anywhere in the repository, files, comments, or documentation.

5. **Verification**:
   - Test any modified scripts, detectors, or templates.
   - Ensure markdown links and references remain intact and valid.
   - Summarize all upgrades made and highlight what was improved.
```

---

## 🔍 Specific Areas to Watch & Enhance

When running upgrades with the prompt above, consider focusing on these high-leverage domains:

1. **Framework-Specific Patterns**:
   - Tailwind CSS: Enforce token-based utilities over arbitrary square-bracket values (e.g. `p-[13px]`).
   - CSS Modules & Emotion/Styled-Components: Ensure clean scoped class naming and token injection.
2. **Modern Web Standards**:
   - Adoption of CSS `text-wrap: balance` and `text-wrap: pretty`.
   - Utilization of modern color spaces (`oklch()`) for perceptually uniform contrast.
   - Smooth CSS scroll-driven animations and View Transition API integration.
3. **Automated Detector Coverage**:
   - Adding custom regex/AST rules for detecting hardcoded colors, broken contrast combinations, unlabelled buttons, and unhandled loading/error states.
4. **Adaptive & Native Surface Rules**:
   - Extending `adapt` playbook rules for dual-screen foldables, tablets, and native web wrappers (Capacitor / Tauri / Electron).
