# Deck design

Choose the theme for the topic and say which one you chose. `business` is for finance and board decks, not the default for every subject.

| Topic | Theme | Cover |
|-------|--------|--------|
| Finance, enterprise, board | `business` | Navy `#0E1F38`, gold `#E89B3C`, teal eyebrow |
| Beauty, wellness, lifestyle | `blush` or `sage` | Blush `#F8EEF0` / sage `#E7EFE6`, dark type |
| Tech, startups | `midnight` | Indigo `#312E81`, violet rule |
| Sustainability, health | `forest` | Deep green `#14532D`, brass rule |
| Hospitality, food, travel | `sand` | Warm paper `#F6F0E6`, terracotta rule |
| Fashion, architecture | `charcoal` | Charcoal `#2A2A28`, terracotta `#E07A5F` |
| Neutral / short | `professional` | Navy `#1F4E79` |
| Unstyled, only when asked | `plain` | Stock Office |

Titles and body use different fonts (Georgia/Calibri, Cambria/Calibri, Palatino/Calibri, and so on by theme). Numbers belong in `kpis` cards. A bullet that starts with a figure is drawn as a card instead of a line.

User colors replace the theme palette. Set `palette` (cover, secondary, eyebrow) or `colors.accent` / `colors.gold` / `colors.eyebrow`. Hex and names (`red`, `navy`, `gold`, `teal`) both work. A light cover switches the title to dark text. Per-bullet `"color": "CC0000"` is preserved. Per-slide `"background"` overrides the theme fill. Per-slide `"theme": "plain"` skips chrome on that slide.

Do not hand-build a full theme with dozens of absolute-positioned shapes when the built-in theme already covers hierarchy. Do use `shapes` for a few KPI cards and `charts` when the data is numeric.
