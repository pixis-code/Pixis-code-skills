# Excalidraw examples

Wrap an elements array in the `.excalidraw` envelope from SKILL.md before saving. All labels use container binding (`containerId` + `boundElements`); a `label` property is ignored and leaves blank shapes.

## 1. Two connected boxes

```json
[
  { "type": "text", "id": "title", "x": 280, "y": 30, "text": "Simple Flow", "fontSize": 28, "fontFamily": 1, "strokeColor": "#1e1e1e", "originalText": "Simple Flow", "autoResize": true },
  { "type": "rectangle", "id": "b1", "x": 100, "y": 100, "width": 200, "height": 100, "roundness": { "type": 3 }, "backgroundColor": "#a5d8ff", "fillStyle": "solid", "boundElements": [{ "id": "t_b1", "type": "text" }, { "id": "a1", "type": "arrow" }] },
  { "type": "text", "id": "t_b1", "x": 105, "y": 130, "width": 190, "height": 25, "text": "Start", "fontSize": 20, "fontFamily": 1, "strokeColor": "#1e1e1e", "textAlign": "center", "verticalAlign": "middle", "containerId": "b1", "originalText": "Start", "autoResize": true },
  { "type": "rectangle", "id": "b2", "x": 450, "y": 100, "width": 200, "height": 100, "roundness": { "type": 3 }, "backgroundColor": "#b2f2bb", "fillStyle": "solid", "boundElements": [{ "id": "t_b2", "type": "text" }, { "id": "a1", "type": "arrow" }] },
  { "type": "text", "id": "t_b2", "x": 455, "y": 130, "width": 190, "height": 25, "text": "End", "fontSize": 20, "fontFamily": 1, "strokeColor": "#1e1e1e", "textAlign": "center", "verticalAlign": "middle", "containerId": "b2", "originalText": "End", "autoResize": true },
  { "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 150, "height": 0, "points": [[0,0],[150,0]], "endArrowhead": "arrow", "startBinding": { "elementId": "b1", "fixedPoint": [1, 0.5] }, "endBinding": { "elementId": "b2", "fixedPoint": [0, 0.5] } }
]
```

## 2. Sequence diagram (two actors, one round trip)

Actor boxes at the top, dashed vertical lifelines (arrows with `endArrowhead: null`), and horizontal message arrows with bound labels. Solid arrow = request, dashed = response.

```json
[
  { "type": "text", "id": "title", "x": 150, "y": 15, "text": "Request Flow", "fontSize": 24, "fontFamily": 1, "strokeColor": "#1e1e1e", "originalText": "Request Flow", "autoResize": true },

  { "type": "rectangle", "id": "aHead", "x": 60, "y": 60, "width": 120, "height": 40, "backgroundColor": "#d0bfff", "fillStyle": "solid", "roundness": { "type": 3 }, "strokeColor": "#8b5cf6", "boundElements": [{ "id": "t_aHead", "type": "text" }] },
  { "type": "text", "id": "t_aHead", "x": 65, "y": 70, "width": 110, "height": 20, "text": "Agent", "fontSize": 16, "fontFamily": 1, "strokeColor": "#1e1e1e", "textAlign": "center", "verticalAlign": "middle", "containerId": "aHead", "originalText": "Agent", "autoResize": true },
  { "type": "arrow", "id": "aLine", "x": 120, "y": 100, "width": 0, "height": 260, "points": [[0,0],[0,260]], "strokeColor": "#757575", "strokeWidth": 1, "strokeStyle": "dashed", "endArrowhead": null },

  { "type": "rectangle", "id": "sHead", "x": 340, "y": 60, "width": 120, "height": 40, "backgroundColor": "#ffd8a8", "fillStyle": "solid", "roundness": { "type": 3 }, "strokeColor": "#f59e0b", "boundElements": [{ "id": "t_sHead", "type": "text" }] },
  { "type": "text", "id": "t_sHead", "x": 345, "y": 70, "width": 110, "height": 20, "text": "Server", "fontSize": 16, "fontFamily": 1, "strokeColor": "#1e1e1e", "textAlign": "center", "verticalAlign": "middle", "containerId": "sHead", "originalText": "Server", "autoResize": true },
  { "type": "arrow", "id": "sLine", "x": 400, "y": 100, "width": 0, "height": 260, "points": [[0,0],[0,260]], "strokeColor": "#757575", "strokeWidth": 1, "strokeStyle": "dashed", "endArrowhead": null },

  { "type": "arrow", "id": "m1", "x": 120, "y": 160, "width": 280, "height": 0, "points": [[0,0],[280,0]], "strokeWidth": 2, "endArrowhead": "arrow", "boundElements": [{ "id": "t_m1", "type": "text" }] },
  { "type": "text", "id": "t_m1", "x": 230, "y": 135, "width": 60, "height": 20, "text": "request", "fontSize": 16, "fontFamily": 1, "strokeColor": "#1e1e1e", "textAlign": "center", "verticalAlign": "middle", "containerId": "m1", "originalText": "request", "autoResize": true },

  { "type": "arrow", "id": "m2", "x": 400, "y": 240, "width": -280, "height": 0, "points": [[0,0],[-280,0]], "strokeWidth": 2, "strokeStyle": "dashed", "endArrowhead": "arrow", "boundElements": [{ "id": "t_m2", "type": "text" }] },
  { "type": "text", "id": "t_m2", "x": 230, "y": 215, "width": 60, "height": 20, "text": "result", "fontSize": 16, "fontFamily": 1, "strokeColor": "#1e1e1e", "textAlign": "center", "verticalAlign": "middle", "containerId": "m2", "originalText": "result", "autoResize": true }
]
```

## Common mistakes

- Using `"label"` instead of container binding: the shape renders blank.
- Linking only one side: the shape needs `boundElements` and the text needs `containerId`.
- Omitting `originalText`, `autoResize: true`, or `fontFamily: 1` on text.
- Overlapping elements from close y-coordinates, or arrow labels longer than the arrow.
- Titles not centered over the diagram.
- Decorations drawn early instead of last in the array.
