---
name: brutalist-skill
description: "Opt-in visual style: industrial brutalism with Swiss print or terminal-telemetry looks, rigid visible grids, huge uppercase type against tiny mono data, sharp corners, and a utilitarian palette with one red accent. Use only when the user names it (brutalist-skill) or asks for a brutalist, Swiss-industrial, or CRT-terminal interface for a landing page, dashboard, or site. Not a default for every UI task, not for soft or minimal styles (soft-skill, minimalist-skill), and not for token extraction (design-tokens)."
version: 1.0.0
author: Pixis
license: MIT
disable-model-invocation: true
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Creative
    tags: [ui, design, frontend, brutalism, swiss, terminal, style]
    related_skills: [soft-skill, minimalist-skill, css-coder, semantic-html, accessibility-frontend]
---

# Brutalist skill (industrial and telemetry UI)

Build interfaces that fuse mid-century Swiss typography, industrial manuals, and retro aerospace or military terminals: rigid modular grids, extreme type scale contrast, a purely utilitarian palette, and simulated analog wear (halftone, scanlines, dithering). The result projects raw function, mechanical precision, and dense data, and drops consumer-UI conventions on purpose.

## Choose one mode and commit

Pick ONE per project. Never alternate or mix modes, and never mix light and dark substrates.

- **Swiss industrial print (light):** newsprint or off-white paper, monolithic heavy sans type, grids drawn with visible lines, aggressive asymmetric negative space broken by oversized, viewport-bleeding numerals or letters, red as the alert accent.
- **Tactical telemetry and CRT terminal (dark only):** dense tabular data, monospace dominating, technical framing devices (ASCII brackets, crosshairs), and simulated hardware limits (phosphor glow, scanlines, low bit depth).

## Typography (the main structure; imagery is secondary)

- **Macro headers:** heavy neo-grotesque (Neue Haas Grotesk Black, Archivo Black, Inter Extra Bold/Black, Roboto Flex Heavy, Monument Extended). Massive fluid size such as `clamp(4rem, 10vw, 15rem)`; tracking `-0.03em` to `-0.06em` so letters form solid blocks; line-height `0.85` to `0.95`; always uppercase.
- **Micro data text:** monospace (JetBrains Mono, IBM Plex Mono, Space Mono, VT323, Courier Prime). Fixed small size (10 to 14px); tracking `0.05em` to `0.1em`; line-height `1.2` to `1.4`; always uppercase. Use it for all metadata, navigation, unit IDs, and coordinates.
- **Texture contrast (rare):** a high-contrast serif (Playfair Display, EB Garamond, Times New Roman), only when heavily degraded with a halftone or 1-bit dither so it clashes with the clean sans.
- Use `clamp()` only for macro type, so it scales aggressively while the structure holds.

## Color (no gradients, soft shadows, or translucency)

- **Swiss (light):** background `#F4F4F0` or `#EAE8E3`; text `#050505` to `#111111`.
- **Telemetry (dark):** background `#0A0A0A` or `#121212` (avoid pure `#000`); text `#EAEAEA`.
- **Accent (both):** `#E61919` or `#FF2A2A`, the only accent. Use it for strike-throughs, thick dividing lines, or critical data.
- **Terminal green `#4AF626` (dark mode, optional):** for one specific element such as a single status light or readout, never general text. If it has no clear purpose, leave it out.

## Layout

- **Blueprint grid:** strict CSS Grid. Elements anchor to tracks and intersections; nothing floats.
- **Visible compartments:** 1px or 2px solid borders mark zones, and full-width `<hr>` lines separate operational units.
- **Bimodal density:** swing between tightly packed monospace metadata and vast calculated empty space around giant type.
- **Geometry:** no `border-radius` at all. Every corner is exactly 90 degrees.

## Symbols and components

- **ASCII framing:** `[ DELIVERY SYSTEMS ]`, `< RE-IND >`, and directional `>>>`, `///`, `\\\\`.
- **Industrial marks:** `®`, `©`, `™` as structural graphic elements, not legal text.
- **Technical assets:** crosshairs (`+`) at grid intersections, barcode-like repeating lines, thick warning stripes, and fake spec strings (`REV 2.6`, `UNIT / D-01`) that suggest running machinery.

## Texture and wear

- **Halftone and 1-bit dither:** convert images or big serif type to dot patterns, via pre-processing or `mix-blend-mode: multiply` with SVG radial-dot patterns.
- **CRT scanlines (terminal mode):** `repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)` on the background.
- **Mechanical noise:** one global, low-opacity SVG noise filter on the root for unified grain in both modes.

## Build rules

1. **Grid determinism:** `display: grid; gap: 1px;` with contrasting parent and child backgrounds yields razor-thin dividing lines without border declarations.
2. **Semantic rigidity:** use precise tags (`<data>`, `<samp>`, `<kbd>`, `<output>`, `<dl>`) so the markup reflects the technical content.
3. **Type clamping:** `clamp()` for macro type only.
4. Keep scanlines and noise on fixed, non-interactive layers so they cost no performance and block no clicks.

## Completion criteria

- One mode and one substrate (light or dark) used throughout, with a single red accent.
- No gradients, soft shadows, translucency, or rounded corners anywhere.
- Huge uppercase macro headers against tiny uppercase mono data; visible borders or 1px grid lines.
- ASCII framing, industrial marks, and technical assets are present and purposeful.
- Texture effects (grain, and halftone or scanlines as appropriate) are applied without hurting readability.
- Semantic tags are used for the data elements.
