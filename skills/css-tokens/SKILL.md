---
name: css-tokens
description: "Scaffold a foundational CSS design-token file (custom properties) for typography, spacing, colors, borders, z-index, and transitions. Use when a project needs a base token system set up from scratch."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [Frontend, CSS, Design Tokens, Scaffolding, Web]
    category: frontend
    related_skills: [css-coder, design-tokens]
---

# CSS Design Tokens

## Purpose

Scaffolds a complete `tokens.css` of CSS custom properties — a consistent design foundation for a web project that doesn't have one yet. Use it for requests like "add design tokens," "set up CSS tokens/variables," or "create a tokens file."

**Don't use it when:** the project already has a token system (modify that instead); the user wants a framework-specific system (Tailwind config, CSS-in-JS tokens); or they only want a subset of tokens (offer to extract just those categories).

## What It Provides

The full token set lives in `references/tokens.css`:

- **Typography** — font families, weights, a modular size scale (xs–4xl)
- **Spacing** — 4px-based scale from 4px to 96px, named by pixel value (`--size-16` = 1rem)
- **Colors** — `oklch()` for perceptually uniform color, with light/dark variants for surfaces, text, brand, interactive states, and semantic states (success/error/warning/info); dark mode is first-class via `prefers-color-scheme: dark`, not bolted on
- **Borders** — radius values derived from the spacing scale (sm–full)
- **Z-index** — named stacking layers (dropdown, modal, toast, etc.)
- **Transitions** — fast/base/slow timing values

Tokens are semantically named by purpose or scale, not appearance (`--color-primary` not `--color-teal`; `--size-16` not `--spacing-small`), and the system is interconnected — radii reference the spacing scale, typography follows a modular scale, z-index uses named layers instead of arbitrary numbers. Reference any token as `var(--token-name)`.

`oklch()` support: Chrome/Edge 111+, Safari 15.4+, Firefox 113+. For older browsers, use a PostCSS fallback plugin or treat this as progressive enhancement.

## How to Use This Skill

1. **Find the CSS directory** — check for `css/`, `styles/`, `assets/css/`, `stylesheets/`, `src/css/`, `src/styles/` at root, `src/`, and `public/`.
2. **Confirm before writing** — found one: "I found a CSS directory at [path]. Add the design tokens there as `tokens.css`? Say so if you want a different location or filename." Found none: ask directly for the directory path (create it if needed) and the filename (e.g. `tokens.css`, `design-tokens.css`).
3. **Write the file** — copy `references/tokens.css` from this skill directory verbatim to the confirmed location.
4. **Tell the user how to wire it in**: `✓ Design tokens written to [full-path]`, then show both an `@import url('path/to/tokens.css');` (CSS) and `<link rel="stylesheet" href="path/to/tokens.css" />` (HTML) option, and a couple of usage examples, e.g. `background-color: var(--color-primary)`, `padding: var(--size-24)`, `border-radius: var(--radius-lg)`.

## Customization

The tokens are a starting point, not a fixed spec — swap in brand colors, adjust the spacing scale, add project-specific tokens, extend into shadows/animations/grid systems as needed. What's worth keeping even after customizing is the *structure*: semantic naming, scale consistency, system thinking (new tokens should still reference the base scales rather than introducing one-off values). Projects can also build on top — component tokens that reference the base ones, semantic aliases like `--button-bg: var(--color-primary)`.

This is a scaffolding skill: it sets up the initial file, not ongoing maintenance of it.

## Important

- Don't assume directory structure or filename — always confirm with the user first.
- Create directories only once the user has confirmed.
- Use the exact content of `references/tokens.css`; don't invent or drop tokens.
