# Excalidraw dark mode

Make the **first element** a huge dark rectangle so it covers any viewport:

```json
{ "type": "rectangle", "id": "darkbg", "x": -4000, "y": -3000, "width": 10000, "height": 7500,
  "backgroundColor": "#1e1e2e", "fillStyle": "solid", "strokeColor": "transparent", "strokeWidth": 0 }
```

## Text on dark

| Color | Hex | Use |
|---|---|---|
| Light | `#e5e5e5` | Primary text, titles |
| Muted | `#a0a0a0` | Secondary text, notes |
| Never | `#555` or darker | Invisible on dark |

Set `"strokeColor": "#e5e5e5"` explicitly on every text element, standalone or bound. The default `#1e1e1e` disappears.

## Fills on dark

| Color | Hex | For |
|---|---|---|
| Dark blue | `#1e3a5f` | Primary nodes |
| Dark green | `#1a4d2e` | Success, output |
| Dark purple | `#2d1b69` | Processing, special |
| Dark orange | `#5c3d1a` | Warning, pending |
| Dark red | `#5c1a1a` | Error, critical |
| Dark teal | `#1a4d4d` | Storage, data |

## Strokes and arrows on dark

Use the standard bright accents from `colors.md` (blue `#4a9eed`, amber `#f59e0b`, green `#22c55e`, red `#ef4444`, purple `#8b5cf6`). Use `#555555` for subtle borders.

## Example: labeled rectangle

Container binding as usual (never a `label` property), with light text:

```json
[
  { "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 80,
    "backgroundColor": "#1e3a5f", "fillStyle": "solid", "strokeColor": "#4a9eed", "strokeWidth": 2,
    "roundness": { "type": 3 }, "boundElements": [{ "id": "t_r1", "type": "text" }] },
  { "type": "text", "id": "t_r1", "x": 105, "y": 120, "width": 190, "height": 25,
    "text": "Dark Node", "fontSize": 20, "fontFamily": 1, "strokeColor": "#e5e5e5",
    "textAlign": "center", "verticalAlign": "middle",
    "containerId": "r1", "originalText": "Dark Node", "autoResize": true }
]
```
