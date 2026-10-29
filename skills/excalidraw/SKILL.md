---
name: excalidraw
description: "Draw hand-drawn style diagrams (architecture, flowcharts, sequence, concept maps) by writing Excalidraw JSON to a .excalidraw file that opens in excalidraw.com. Use when the user wants a diagram, flowchart, architecture sketch, or sequence diagram as an editable Excalidraw file. Not for Mermaid or SVG output, animated PR/diff diagrams (pr-lens), or charts of data (`data-visualization`)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Creative
    tags: [excalidraw, diagrams, flowcharts, architecture, visualization, json]
    related_skills: [pr-lens, codebase-documentation-generator, data-visualization]
---

# Excalidraw

Write Excalidraw element JSON, save it as a `.excalidraw` file, and the user can drag it onto [excalidraw.com](https://excalidraw.com) to view and edit. No account, API key, or rendering library is needed.

## Workflow

1. Write an array of element objects.
2. Wrap it in the envelope below and save to a `.excalidraw` file (any path, e.g. `~/diagrams/flow.excalidraw`).
3. Re-read the file to confirm it is valid JSON.
4. Optional, only if the user asks for a shareable link: run `scripts/upload.py` (see Sharing).

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "pixis",
  "elements": [ ...elements... ],
  "appState": { "viewBackgroundColor": "#ffffff" }
}
```

## Elements

Every element needs `type`, `id` (unique string), `x`, `y`, `width`, `height`. Defaults you can omit: `strokeColor` `#1e1e1e`, `backgroundColor` `transparent`, `fillStyle` `solid`, `strokeWidth` 2, `roughness` 1 (hand-drawn), `opacity` 100. The canvas is white.

- **Shapes:** `rectangle`, `ellipse`, `diamond`. Add `roundness: {"type": 3}` for rounded corners and `backgroundColor` (e.g. `#a5d8ff`) to fill.
- **Arrow:** `points` are `[dx, dy]` offsets from the element's `x`, `y`; `endArrowhead` is `null`, `"arrow"`, `"bar"`, `"dot"`, or `"triangle"`; `strokeStyle` is `solid`, `dashed`, or `dotted`.
- **Connected arrow:** add `startBinding` / `endBinding` like `{"elementId": "r1", "fixedPoint": [1, 0.5]}`. Fixed points: top `[0.5,0]`, bottom `[0.5,1]`, left `[0,0.5]`, right `[1,0.5]`. List the arrow in each shape's `boundElements` too.
- **Standalone text** (titles and notes only): `{"type":"text","id":"t1","x":150,"y":138,"text":"Hello","fontSize":20,"fontFamily":1,"strokeColor":"#1e1e1e","originalText":"Hello","autoResize":true}`. `x` is the left edge; to center at `cx` use `x = cx - (text.length * fontSize * 0.5) / 2`. Do not rely on `textAlign` or `width` for placement.

### Labels: container binding (required)

Never put `"label": {...}` on a shape or arrow. It is not part of the format, is silently ignored, and leaves blank shapes. Instead link both sides:

```json
{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 80,
  "roundness": { "type": 3 }, "backgroundColor": "#a5d8ff",
  "boundElements": [{ "id": "t_r1", "type": "text" }] },
{ "type": "text", "id": "t_r1", "x": 105, "y": 120, "width": 190, "height": 25,
  "text": "Hello", "fontSize": 20, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "r1", "originalText": "Hello", "autoResize": true }
```

The shape lists the text in `boundElements`, and the text points back with `containerId`. This works on rectangle, ellipse, diamond, and arrow. Text position and size are approximate; Excalidraw recalculates on load. Keep `originalText` equal to `text`, always set `fontFamily: 1`, and set `autoResize: true`.

### Order and size

- Array order is z-order (first = back). Emit progressively: background zone, shape, its bound text, its arrows and arrow labels, next shape. Put each bound text right after its shape. Draw decorations last.
- Font size: at least 16 for body and labels, 20 for titles, 14 only for rare secondary notes, never below 14.
- Labeled shapes at least 120x60; leave 20-30 px gaps; prefer fewer, larger elements.
- Keep arrow labels short or widen the arrow; check that text, boxes, and labels do not overlap.

## Colors

Use one palette consistently (full tables in `references/colors.md`):

| Use | Fill | Hex |
|---|---|---|
| Primary / input | Light blue | `#a5d8ff` |
| Success / output | Light green | `#b2f2bb` |
| Warning / external | Light orange | `#ffd8a8` |
| Processing / special | Light purple | `#d0bfff` |
| Error / critical | Light red | `#ffc9c9` |
| Notes / decisions | Light yellow | `#fff3bf` |
| Storage / data | Light teal | `#c3fae8` |

- Text on white must be `#757575` or darker (`#1e1e1e` is best); never light gray.
- No emoji in text; they do not render in the Excalidraw font.
- Dark diagrams: see `references/dark-mode.md`. Worked examples: `references/examples.md`.

## Sharing (optional)

`scripts/upload.py` uploads the diagram to excalidraw.com and prints a link. The data is encrypted on your machine and the key stays in the URL fragment, but it is still sent to an external server. Run it only when the user asks for a shareable link.

```bash
pip install cryptography
python scripts/upload.py ~/diagrams/flow.excalidraw
```

## Completion criteria

- The file parses as JSON, has `"type": "excalidraw"` and an `elements` array.
- Every label uses container binding on both sides (`boundElements` and `containerId`); no `label` property anywhere.
- All ids are unique; bound text follows its shape in the array.
- Font sizes, contrast, and spacing follow the rules above.
- The user was told where the file is and how to open it (drop it on excalidraw.com).
