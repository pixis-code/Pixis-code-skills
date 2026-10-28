---
name: css-coder
description: "Write, review, refactor, or clean up CSS and stylesheets: messy or inconsistent styles, specificity and !important problems, custom properties/design tokens, layout (flex/grid), responsive design, focus styles, reduced motion, dark mode, and CSS performance. Use for ANY task that edits or audits .css files or component styling, including projects that also use Tailwind. Favors native CSS and web standards. See references/patterns.md."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [Frontend, CSS, Accessibility, Performance, Web]
    category: frontend
    related_skills: [accessibility-frontend, performance-frontend, core-web-vitals]
---

# CSS Coder

Guidance for CSS that prioritizes web standards, accessibility, performance, and maintainability.

## Core Principles

1. **Web standards first** — native CSS over libraries/frameworks. No Tailwind, no CSS-in-JS unless explicitly requested.
2. **Accessibility is a requirement** — styles must support, never hinder, assistive tech, and must respect user preferences (motion, color scheme, contrast).
3. **Performance matters** — minimize repaints, avoid layout thrashing, keep selectors efficient.
4. **Readable over clever** — future maintainers (including you) should understand it at a glance.
5. **Explicit over implicit** — no magic numbers; put shared values in custom properties.

## Workflow

1. Check `references/patterns.md` before writing anything — it holds the established patterns/snippets.
2. When unsure, validate against MDN or the CSS spec rather than guessing.
3. Suggesting an alternative beyond the skill's own patterns is fine, as long as it still fits the core principles above.

## Writing Guidelines

**Selectors** — prefer classes over element/ID selectors; keep specificity low and predictable; avoid nesting past 2–3 levels.

**Custom properties** — `--`-prefixed for colors, spacing, typography, and anything repeated; defined at `:root` or the right scope; named by purpose (`--color-primary`, `--spacing-md`, `--font-size-body`), not appearance.

**Logical properties** — always prefer logical (`margin-inline`, `padding-block`, `inset-inline-start`, `block-size`) over physical (`margin-left`, `padding-top`, `left`, `height`) — they carry internationalization and writing-mode support for free. Fall back to physical only where no logical equivalent exists yet.

**Units** — `rem` for typography/spacing (respects user font-size prefs); `em` for component-relative sizing; viewport units (`vw`, `vh`, `dvh`) with fallbacks where needed; avoid `px` for font sizes (fine for borders/shadows/fine detail).

**Colors** — modern space-separated syntax for `rgb()`/`hsl()`/`oklch()`; reach for `oklch()` when you want vibrant or wide-gamut colors; use relative color syntax to derive hover states or transparent variants from existing variables (syntax examples in `references/patterns.md`).

**Layout** — Grid for two-dimensional layouts or when you need vertical flow without extra declarations; Flexbox for one-dimensional alignment (note it defaults to `row`); no floats for layout (legacy only).

**Media queries** — modern range syntax (`@media (width < 48rem)`, `@media (width >= 48rem)`); Shared First over mobile-first — shared styles live outside any query, viewport-specific styles get bounded queries; keep breakpoints to a minimum, add only when there's a clear need (details in `references/patterns.md`).

**Accessibility** — never use `display: none`/`visibility: hidden` to hide content that should stay available to screen readers (use the techniques in the references instead); respect `prefers-reduced-motion`, `prefers-color-scheme`, `prefers-contrast`; keep contrast at WCAG AA minimum, AAA preferred; never strip `:focus` styles without a replacement.

**Performance** — stick to `transform`/`opacity` in animations (avoid expensive properties); use `will-change` sparingly; minimize `*` selectors; prefer `@layer` to manage cascade on larger codebases.

## References

`references/patterns.md` has the visually-hidden utility, user-preference media queries (motion/color-scheme/contrast), modern color syntax and relative colors, Shared First responsive examples, and any project-specific conventions. It grows as patterns are added — if something's missing, propose one that fits the core principles.
