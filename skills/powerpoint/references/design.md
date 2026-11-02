# Deck design

`pptx_create.py` themes (default **business**):

| Theme | Title slide | Content slides |
|-------|-------------|----------------|
| `business` | Navy `#0E1F38`, gold top/bottom bars, teal eyebrow, page `NN / NN` | Navy header band `#16274D`, gold rule, KPI cards with colored left rails |
| `professional` | Navy background, white title | Light background, navy titles, accent bar, styled tables |
| `midnight` | Indigo | Violet accent |
| `forest` | Deep green | Green accent |
| `plain` | Stock Office look — only when requested | |

Per-bullet `"color": "CC0000"` is preserved. Per-slide `"background"` overrides the theme fill. Per-slide `"theme": "plain"` skips chrome on that slide.

Do not hand-build a full theme with dozens of absolute-positioned shapes when the built-in theme already covers hierarchy. Do use `shapes` for a few KPI cards and `charts` when the data is numeric.
