---
name: minimalist-skill
description: "Opt-in visual style: refined editorial, document-like minimalist UI with a warm monochrome palette, strong serif/sans contrast, flat 1px-bordered bento grids, and quiet motion. Use only when the user names it (minimalist-skill) or asks for this Notion-like, ultra-flat editorial look for a landing page, product site, or UI. Not a default for every UI task, not for theme/token extraction (design-tokens), and not for accessibility or performance audits."
version: 1.0.0
author: Pixis
license: MIT
disable-model-invocation: true
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Creative
    tags: [ui, design, frontend, minimalism, editorial, style]
    related_skills: [soft-skill, css-coder, semantic-html, accessibility-frontend, design-tokens]
---

# Minimalist skill (utilitarian editorial UI)

Produce refined, document-style interfaces like top workspace tools: a high-contrast warm monochrome palette, expressive typography, generous whitespace, bento grids, and very flat components with a few muted pastel accents. Reject generic SaaS conventions.

Values below use plain CSS with Tailwind-style names where handy; apply the same rules in any framework.

## Banned

- Fonts: Inter, Roboto, Open Sans.
- Icon sets: thin-line Lucide, Feather, or stock Heroicons.
- Heavy shadows (`shadow-md/lg/xl`). Shadows must be near-invisible: ultra-diffuse, opacity under 0.05.
- Large saturated backgrounds (no bright blue, green, or red hero sections).
- Gradients, neon colors, and 3D glassmorphism (a subtle navbar blur is the only exception).
- `rounded-full` on large containers, cards, or primary buttons.
- Emojis anywhere (code, markup, copy, headings, alt text); use proper icons or clean SVG.
- Placeholder content: "John Doe", "Acme Corp", "Lorem Ipsum". Write realistic, contextual content.
- Copy clichés: Elevate, Seamless, Unleash, Next-Gen, Game-changer, Delve. Use plain, specific language.

## Typography

Rely on strong contrast between serif and sans.

- **Sans (body, UI, buttons):** `'SF Pro Display', 'Geist Sans', 'Helvetica Neue', 'Switzer', sans-serif`.
- **Serif (hero headings, quotes):** `'Lyon Text', 'Newsreader', 'Playfair Display', 'Instrument Serif', serif`, with tight tracking (`-0.02em` to `-0.04em`) and line-height about 1.1.
- **Mono (code, keystrokes, metadata):** `'Geist Mono', 'SF Mono', 'JetBrains Mono', monospace`.
- **Text color:** never pure black. Use `#111111` or `#2F3437`, line-height 1.6, and `#787774` for secondary text.

## Color (warm monochrome plus spot pastels)

Color is scarce and used only for meaning or subtle accents.

- Canvas: `#FFFFFF`, or warm off-white `#F7F6F3` / `#FBFBFA`. Cards: `#FFFFFF` or `#F9F9F8`.
- Borders and dividers: `#EAEAEA` or `rgba(0,0,0,0.06)`.
- Accents, only as desaturated pastels for tags, inline code, or icon backgrounds (background / text):
  - red `#FDEBEC` / `#9F2F2D`
  - blue `#E1F3FE` / `#1F6C9F`
  - green `#EDF3EC` / `#346538`
  - yellow `#FBF3DB` / `#956400`

## Components

- **Bento grids:** asymmetrical CSS Grid; cards with exactly `border: 1px solid #EAEAEA`; crisp radius of 8px or 12px at most; generous padding (24px to 40px).
- **Primary button:** solid `#111111` with white text, radius 4 to 6px, no shadow. Hover shifts to `#333333` or `scale(0.98)`.
- **Tags and status badges:** pill-shaped (`border-radius: 9999px`), tiny uppercase text with `0.05em` tracking, background from the pastel set.
- **FAQ accordions:** no container boxes; items separated only by `border-bottom: 1px solid #EAEAEA`; a sharp `+` and `-` toggle.
- **Keystrokes:** `<kbd>` styled as keys: `1px solid #EAEAEA`, radius 4px, background `#F7F6F3`, mono font.
- **Faux window chrome (when mocking software):** a minimal white top bar with three small light-gray circles.

## Icons and imagery

- **Icons:** Phosphor (bold or fill) or Radix UI Icons for a slightly thicker technical look; one consistent stroke width.
- **Illustrations:** monochrome, rough continuous-line ink sketches on white, with one offset geometric shape in a muted pastel.
- **Photography:** high quality, desaturated, warm tone, with a faint warm grain overlay (`opacity: 0.04`). No oversaturated stock photos. When real assets are missing, use placeholders like `https://picsum.photos/seed/{context}/1200/800`.
- **Backgrounds:** sections should not feel empty and flat. Add very low-opacity full-width imagery, soft warm radial light spots (`opacity: 0.03`), or minimal line patterns for depth.

## Motion (quiet, almost invisible)

- **Scroll entry:** fade in with `translateY(12px)` and `opacity: 0`, resolving over 600ms with `cubic-bezier(0.16, 1, 0.3, 1)`. Use `IntersectionObserver`, never a `scroll` listener.
- **Hover:** cards lift with a tiny shadow shift (`0 0 0` to `0 2px 8px rgba(0,0,0,0.04)` over 200ms). Buttons use `scale(0.98)` on `:active`.
- **Stagger:** lists and grids cascade (`animation-delay: calc(var(--index) * 80ms)`); never mount everything at once.
- **Ambient motion (optional):** one very slow radial blob (20s+, opacity 0.02 to 0.04) on a `position: fixed; pointer-events: none` layer, never on scrolling containers.
- **Performance:** animate only `transform` and `opacity`; no `top`, `left`, `width`, `height`; `will-change: transform` only on actively animating elements.
- **Reduced motion (mandatory):** gate scroll entry, staggers, and ambient motion behind `@media (prefers-reduced-motion: no-preference)`, and add a `reduce` block that shows content instantly at rest. Hover and `:active` feedback may stay.

## Workflow

1. Set macro whitespace first: very large vertical padding between sections (`py-24` to `py-32`).
2. Limit main text width to `max-w-4xl` or `max-w-5xl`.
3. Apply the type hierarchy and monochrome color variables immediately.
4. Make every card, divider, and border follow the `1px solid #EAEAEA` rule.
5. Add scroll-entry animation to all major content blocks.
6. Give every section depth (imagery, ambient gradient, or subtle texture); no empty flat backgrounds.
7. Deliver code that already reads as high-end, uncluttered, and editorial, with no manual cleanup needed.

## Completion criteria

- No banned font, icon set, shadow, gradient, pill-shaped large container, emoji, placeholder name, or cliché copy.
- Serif headings with tight tracking; off-black text; secondary text `#787774`.
- Cards, dividers, and borders all use the `#EAEAEA` 1px rule; radii at most 12px; buttons `#111111`.
- Color appears only as muted pastels for tags and accents.
- Scroll entry uses `IntersectionObserver`, only transform and opacity animate, and the reduced-motion block exists.
- Sections are spacious and have subtle depth.
