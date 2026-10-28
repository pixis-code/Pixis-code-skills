---
name: soft-skill
description: "Opt-in visual style: a calm, polished, premium UI look with soft contrast, generous whitespace, nested 'double-bezel' cards, pill buttons, and spring-like motion. Use only when the user names it (soft-skill) or asks for this soft, high-end agency look for a landing page, site, or UI component. Not a default for every UI task, not for token/theme extraction (design-tokens), and not for accessibility or performance audits."
version: 1.0.0
author: Pixis
license: MIT
disable-model-invocation: true
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Creative
    tags: [ui, design, frontend, motion, premium, style]
    related_skills: [css-coder, semantic-html, accessibility-frontend, performance-frontend, design-tokens]
---

# Soft skill (high-end visual style)

Build agency-grade interfaces: depth you can almost feel, generous spacing, careful micro-interactions, and fluid motion. The goal is an Apple/Linear-tier feel, not a template with nice fonts. Never repeat the same layout and aesthetic twice in a row; combine archetypes freely within the rules below.

Class names below are Tailwind-style examples. Apply the same ideas in plain CSS or any framework.

## Hard no-list (if any appear, the design fails)

- **Fonts:** Inter, Roboto, Arial, Open Sans, Helvetica. Prefer Geist, Clash Display, PP Editorial New, or Plus Jakarta Sans (assume available).
- **Icons:** thick-stroke Lucide, FontAwesome, Material. Use ultra-light line icons (Phosphor Light, Remix Line).
- **Borders and shadows:** plain 1px gray borders; harsh dark drop shadows (`shadow-md`, `rgba(0,0,0,0.3)`).
- **Layouts:** a navbar glued edge-to-edge to the top; symmetrical Bootstrap-style 3-column grids without large whitespace gaps.
- **Motion:** `linear` or `ease-in-out`, or instant state changes with no interpolation.

## Pick one of each before coding

**Vibe and texture**
1. *Ethereal glass* (SaaS, AI, tech): near-black `#050505`, soft radial mesh gradients (faint purple or emerald glows), very dark cards with heavy `backdrop-blur-2xl` and white/10 hairlines, wide geometric grotesk type.
2. *Editorial luxury* (lifestyle, real estate, agency): warm cream `#FDFBF7`, muted sage or deep espresso, large high-contrast variable serif headings, a faint film-grain overlay (about 3% opacity).
3. *Soft structuralism* (consumer, health, portfolio): silver-grey or pure white, very large bold grotesk type, airy floating components with extremely soft, diffused ambient shadows.

**Layout**
1. *Asymmetrical bento:* a masonry-like grid of unequal cards (e.g. an 8-column two-row card beside stacked 4-column cards). On mobile: single column, `gap-6`, all spans reset to 1.
2. *Z-axis cascade:* cards stacked with slight overlaps, depth, and small rotations (about -2 or 3 degrees). On mobile (below 768px): remove rotations and negative-margin overlaps, since overlap causes touch-target conflicts.
3. *Editorial split:* huge type on the left half, interactive scrollable pills or staggered cards on the right. On mobile: full-width stack, type first, horizontal scroll kept if needed.

**Mobile rule for every asymmetric layout:** below `md` (768px) fall back to full width with `px-4 py-8`. Use `min-h-[100dvh]` instead of `h-screen` to avoid iOS Safari viewport jumps.

## Component craft

- **Double-bezel cards.** Never lay a premium card, image, or container flat on the background; nest it like a glass plate in a tray.
  - *Outer shell:* faint background (`bg-black/5` or `bg-white/5`), hairline ring (`ring-1 ring-black/5` or `border border-white/10`), small padding (`p-1.5` to `p-2`), large radius (`rounded-[2rem]`).
  - *Inner core:* its own background, an inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`), and a smaller concentric radius (`rounded-[calc(2rem-0.375rem)]`).
- **Pill buttons with island icons.** Primary buttons are fully rounded (`rounded-full`, about `px-6 py-3`). A trailing arrow never sits bare next to the text: place it in its own circle (`w-8 h-8 rounded-full bg-black/5 dark:bg-white/10`) flush against the button's right inner padding.
- **Spacing.** Double normal padding: sections at `py-24` to `py-40`. Put a tiny pill eyebrow tag (`rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em]`) above major H1/H2s.

## Motion

Nothing uses default transitions. Simulate mass and springs with custom curves, e.g. `duration-700 ease-[cubic-bezier(0.32,0.72,0,1)]`.

- **Floating glass nav pill** detached from the top (`mt-6 mx-auto w-max rounded-full`). The hamburger lines rotate and translate into a clean X (not just vanish). The menu opens as a full-screen heavy-glass overlay (`backdrop-blur-3xl`, `bg-black/80` or `bg-white/80`), and its links fade and slide up in a staggered sequence (`translate-y-12 opacity-0` to rest, `delay-100/150/200`).
- **Button physics.** Use `group`; on press scale down slightly (`active:scale-[0.98]`); on hover the inner icon circle moves diagonally (`group-hover:translate-x-1 group-hover:-translate-y-[1px]`) and grows a little (`scale-105`) instead of just changing color.
- **Scroll entry.** Elements never appear statically: a gentle heavy fade-up (`translate-y-16 blur-md opacity-0` to rest over 800ms or more). Use `IntersectionObserver` or Framer Motion `whileInView`; never a `scroll` event listener (reflows hurt mobile).

## Performance guardrails

- Animate only `transform` and `opacity`, never `top`, `left`, `width`, or `height`. Use `will-change: transform` sparingly, only on elements actively animating.
- Use `backdrop-blur` only on fixed or sticky elements (nav, overlays), never on scrolling containers or large content areas.
- Put grain or noise on a fixed, `pointer-events-none` layer, never on a scrolling container.
- Keep z-index systematic (sticky nav, modals, overlays, tooltips); no arbitrary `z-50` or `z-[9999]`.

## Workflow

1. Silently choose a vibe and a layout from the lists above to suit the prompt.
2. Scaffold: background texture, macro whitespace, very large type.
3. Build the DOM with double-bezel cards, inputs, and feature grids (generous squircle radii like `rounded-[2rem]`).
4. Add the custom-curve transitions, staggered nav reveal, and button hover physics.
5. Output complete, polished code with no generic fallbacks.

## Completion criteria

- None of the no-list items appear.
- One vibe and one layout were chosen and applied consistently.
- Major cards use the double-bezel structure; CTAs use the island-icon pattern where an arrow exists.
- Sections have at least `py-24` padding; all transitions use custom curves; entry animations exist.
- Layout collapses to a single column with `w-full` and `px-4` below 768px.
- Animations touch only transform and opacity; blur is limited to fixed or sticky elements.
- The result reads as an expensive agency build, not a template.
