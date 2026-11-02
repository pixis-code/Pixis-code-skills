# Deck design

A sample deck shows the level of finish. It is not a theme, a palette, or a layout to repeat.

Pick colors from the content. Use a named theme only as a start (`professional`, `business`, `midnight`, `forest`, `blush`, `sage`, `sand`, `charcoal`). If the user names colors, `palette` or `colors` replaces that start. `palette` order is cover, secondary, eyebrow. A light cover switches the title to dark text. `plain` is only when the user wants unstyled Office slides.

One font for the whole deck. Set `fonts.font` when the user names a face. Set `sizes` when the user names a size (`title`, `heading`, `subtitle`, `body`, `kpi`, `table`, in points). A bullet can set its own `size`, `font`, and `color`. A table can set `font_size`. Leave table position and size unset.

Layout follows the content:

- Numbers → `kpis` cards
- Parallel groups → `cards` (set `tone` to `dark` only when that card should be filled)
- Four or more loose lines → cards
- Two or three short lines → bullets with a dot
- Comparisons → a wide table or a chart, placed so it does not cover the cards

Per-bullet `"color"` is kept. Per-slide `"background"` overrides the fill. Per-slide `"theme": "plain"` skips chrome on that slide.
