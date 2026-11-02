#!/usr/bin/env python3
"""Create a .pptx presentation from a JSON deck spec.

Spec format (all positions/sizes in inches, colors as RRGGBB hex):
{
  "slide_size": "16:9",              // or "4:3" (default "16:9")
  "slides": [
    {"layout": "title", "title": "My Deck", "subtitle": "Q3 review"},
    {"layout": "title_content", "title": "Agenda",
     "bullets": ["Top item",
                 {"text": "Sub item", "level": 1, "bold": true,
                  "size": 18, "color": "CC0000", "font": "Arial",
                  "italic": false,
                  "link": "https://example.com/agenda"}],
     "background": "1F2937",           // solid slide background (hex)
     "footer": "Confidential",         // footer placeholder text
     "slide_number": true,             // enable slide-number placeholder
     "notes": "Speaker notes for this slide"},
    {"layout": "blank", "title": "Widgets",
     "images":  [{"path": "logo.png", "left": 1, "top": 1, "width": 3}],
     "tables":  [{"header": true, "font_size": 15,
                  "rows": [["H1", "H2"], ["a", "b"]]}],
     "shapes":  [{"type": "rounded_rectangle", "left": 8, "top": 1,
                  "width": 3, "height": 1, "fill": "4472C4",
                  "text": "Callout", "text_color": "FFFFFF"}],
     "charts":  [{"type": "bar", "left": 1, "top": 3, "width": 6,
                  "height": 3.5, "title": "Sales",
                  "categories": ["Q1", "Q2"],
                  "series": {"North": [10, 20], "South": [7, 13]}}]}
  ]
}
Layouts: title, title_content, section, two_content, title_only, blank
Chart types: bar, bar_h, line, pie   Shape types: rectangle,
rounded_rectangle, oval, diamond, right_arrow, chevron
"""
import argparse
import copy
import json
import re
import sys

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from lxml import etree

LAYOUTS = {"title": 0, "title_content": 1, "section": 2,
           "two_content": 3, "title_only": 5, "blank": 6}

# Default visual system. "plain" keeps the stock Office look.
THEMES = {
    "professional": {
        "bg": "F4F7FB",
        "title_bg": "1F4E79",
        "title_fg": "FFFFFF",
        "subtitle_fg": "D6E3F0",
        "heading": "1F4E79",
        "body": "1A1A1A",
        "accent": "1F4E79",
        "muted": "5B6770",
        "card": "FFFFFF",
        "table_header": "1F4E79",
        "table_header_fg": "FFFFFF",
        "table_alt": "E8F1FB",
    },
    "midnight": {
        "bg": "F5F3FF",
        "title_bg": "312E81",
        "title_fg": "FFFFFF",
        "subtitle_fg": "E0E7FF",
        "heading": "312E81",
        "body": "1F2937",
        "accent": "4F46E5",
        "muted": "6B7280",
        "card": "FFFFFF",
        "table_header": "312E81",
        "table_header_fg": "FFFFFF",
        "table_alt": "EEF2FF",
    },
    "forest": {
        "bg": "F0FDF4",
        "title_bg": "14532D",
        "title_fg": "FFFFFF",
        "subtitle_fg": "DCFCE7",
        "heading": "14532D",
        "body": "14532D",
        "accent": "166534",
        "muted": "3F6212",
        "card": "FFFFFF",
        "table_header": "166534",
        "table_header_fg": "FFFFFF",
        "table_alt": "DCFCE7",
    },
    "business": {
        "bg": "FFFFFF",
        "title_bg": "0E1F38",
        "header_bg": "16274D",
        "title_fg": "FFFFFF",
        "subtitle_fg": "B9CBEA",
        "eyebrow": "159E93",
        "gold": "E89B3C",
        "heading": "0E1F38",
        "body": "1A2332",
        "accent": "159E93",
        "muted": "5B6770",
        "card": "FFFFFF",
        "table_header": "16274D",
        "table_header_fg": "FFFFFF",
        "table_alt": "F4F7FB",
    },
    "blush": {
        "bg": "FBF7F8",
        "title_bg": "F8EEF0",
        "header_bg": "F3DDE3",
        "title_fg": "6B3044",
        "subtitle_fg": "8A5A68",
        "eyebrow": "A84B63",
        "gold": "C48A7A",
        "heading": "6B3044",
        "body": "3F2A32",
        "accent": "C45C74",
        "muted": "8A6A72",
        "card": "FFFFFF",
        "table_header": "6B3044",
        "table_header_fg": "FFFFFF",
        "table_alt": "FBF3F5",
    },
    "sage": {
        "bg": "F7F8F4",
        "title_bg": "E7EFE6",
        "header_bg": "D5E3D4",
        "title_fg": "1F3D32",
        "subtitle_fg": "4E6B5C",
        "eyebrow": "2F6F56",
        "gold": "C4A574",
        "heading": "1F3D32",
        "body": "24332C",
        "accent": "3E7A62",
        "muted": "5E7268",
        "card": "FFFFFF",
        "table_header": "1F3D32",
        "table_header_fg": "FFFFFF",
        "table_alt": "F3F7F2",
    },
    "sand": {
        "bg": "FBF8F3",
        "title_bg": "F6F0E6",
        "header_bg": "EBE1D2",
        "title_fg": "3E3428",
        "subtitle_fg": "6E6254",
        "eyebrow": "A15C38",
        "gold": "C4843E",
        "heading": "3E3428",
        "body": "2C261F",
        "accent": "A15C38",
        "muted": "7A6E60",
        "card": "FFFFFF",
        "table_header": "3E3428",
        "table_header_fg": "FFFFFF",
        "table_alt": "F8F3EA",
    },
    "charcoal": {
        "bg": "F6F6F5",
        "title_bg": "2A2A28",
        "header_bg": "3A3A37",
        "title_fg": "F7F4EE",
        "subtitle_fg": "D9D3C7",
        "eyebrow": "E07A5F",
        "gold": "E07A5F",
        "heading": "2A2A28",
        "body": "2A2A28",
        "accent": "E07A5F",
        "muted": "6B675F",
        "card": "FFFFFF",
        "table_header": "2A2A28",
        "table_header_fg": "FFFFFF",
        "table_alt": "F3F2EF",
    },
    "plain": {},
}

# Serif display + sans body. The pair changes by theme so decks are not identical.
THEME_FONTS = {
    "business": ("Georgia", "Calibri"),
    "professional": ("Cambria", "Calibri"),
    "midnight": ("Georgia", "Trebuchet MS"),
    "forest": ("Constantia", "Candara"),
    "blush": ("Palatino Linotype", "Calibri"),
    "sage": ("Constantia", "Calibri"),
    "sand": ("Georgia", "Candara"),
    "charcoal": ("Georgia", "Arial"),
}
for _theme_name, (_title_font, _body_font) in THEME_FONTS.items():
    if THEMES.get(_theme_name):
        THEMES[_theme_name]["title_font"] = _title_font
        THEMES[_theme_name]["body_font"] = _body_font

NAMED_COLORS = {
    "navy": "0E1F38",
    "gold": "E89B3C",
    "teal": "159E93",
    "blue": "1D4ED8",
    "red": "B91C1C",
    "green": "166534",
    "orange": "C2410C",
    "purple": "6D28D9",
    "black": "111827",
    "white": "FFFFFF",
    "gray": "4B5563",
    "grey": "4B5563",
    "pink": "BE185D",
    "yellow": "CA8A04",
    "indigo": "312E81",
}
CHART_TYPES = {"bar": XL_CHART_TYPE.COLUMN_CLUSTERED,
               "bar_h": XL_CHART_TYPE.BAR_CLUSTERED,
               "line": XL_CHART_TYPE.LINE_MARKERS,
               "pie": XL_CHART_TYPE.PIE}
SHAPE_TYPES = {"rectangle": MSO_SHAPE.RECTANGLE,
               "rounded_rectangle": MSO_SHAPE.ROUNDED_RECTANGLE,
               "oval": MSO_SHAPE.OVAL, "diamond": MSO_SHAPE.DIAMOND,
               "right_arrow": MSO_SHAPE.RIGHT_ARROW,
               "chevron": MSO_SHAPE.CHEVRON}


def style_run(run, spec):
    """Apply font styling from a bullet/text spec dict to a run."""
    font = run.font
    if spec.get("size"):
        font.size = Pt(spec["size"])
    if spec.get("bold") is not None:
        font.bold = spec["bold"]
    if spec.get("italic") is not None:
        font.italic = spec["italic"]
    if spec.get("font"):
        font.name = spec["font"]
    if spec.get("color"):
        font.color.rgb = RGBColor.from_string(spec["color"])
    if spec.get("link"):
        run.hyperlink.address = spec["link"]


def _enable_bullet(paragraph, level):
    """A bare text box has no bullet marker until the paragraph asks for one."""
    p_pr = paragraph._p.get_or_add_pPr()
    for child in list(p_pr):
        if child.tag in {qn("a:buNone"), qn("a:buFont"), qn("a:buChar"), qn("a:buAutoNum")}:
            p_pr.remove(child)
    bu_font = etree.SubElement(p_pr, qn("a:buFont"))
    bu_font.set("typeface", "Arial")
    bu_char = etree.SubElement(p_pr, qn("a:buChar"))
    bu_char.set("char", "•")
    p_pr.set("marL", str(int(Inches(0.28 + 0.28 * level))))
    p_pr.set("indent", str(int(Inches(-0.2))))


def add_bullets(text_frame, bullets):
    text_frame.clear()
    for i, item in enumerate(bullets):
        if isinstance(item, str):
            item = {"text": item}
        para = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
        level = int(item.get("level", 0))
        para.level = level
        para.space_after = Pt(8)
        run = para.add_run()
        run.text = item.get("text", "")
        style_run(run, item)
        _enable_bullet(para, level)


def copy_layout_placeholder(slide, ph_idx):
    """Copy a layout placeholder (footer=11, slide number=12) onto the
    slide so it actually renders; returns the shape or None if the layout
    does not provide it."""
    for ph in slide.slide_layout.placeholders:
        if ph.placeholder_format.idx == ph_idx:
            slide.shapes._spTree.append(copy.deepcopy(ph._element))
            for shape in slide.placeholders:
                if shape.placeholder_format.idx == ph_idx:
                    return shape
    return None


def _paint_runs(shape, color_hex, size=None, bold=None, name="Calibri"):
    if shape is None or not getattr(shape, "text_frame", None):
        return
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            if size:
                run.font.size = Pt(size)
            if bold is not None:
                run.font.bold = bold
            if name and not run.font.name:
                run.font.name = name
            # Do not override an explicit per-run color already set.
            try:
                existing = run.font.color.rgb
            except Exception:
                existing = None
            if existing is None:
                run.font.color.rgb = RGBColor.from_string(color_hex)


def _set_bg(slide, hex_color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(hex_color)


def apply_theme(prs, slide, spec, theme):
    """Apply deck theme chrome unless the slide opts out or theme is plain."""
    if not theme or spec.get("theme") == "plain":
        return
    layout = spec.get("layout", "title_content")
    if spec.get("background"):
        pass  # caller already painted an explicit background
    elif layout == "title":
        _set_bg(slide, theme["title_bg"])
    elif layout == "section":
        _set_bg(slide, theme["accent"])
    else:
        _set_bg(slide, theme["bg"])

    if layout in {"title", "section"}:
        title_color = theme["title_fg"]
        sub_color = theme["subtitle_fg"]
        title_size = 40 if layout == "title" else 32
    else:
        title_color = theme["heading"]
        sub_color = theme["muted"]
        title_size = 28
        # left accent bar
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0),
            Inches(0.12), prs.slide_height)
        bar.fill.solid()
        bar.fill.fore_color.rgb = RGBColor.from_string(theme["accent"])
        bar.line.fill.background()

    if slide.shapes.title is not None and spec.get("title"):
        _paint_runs(slide.shapes.title, title_color, size=title_size, bold=True, name=_fonts(theme)[0])

    for ph in slide.placeholders:
        idx = ph.placeholder_format.idx
        if idx == 1 and spec.get("subtitle"):
            _paint_runs(ph, sub_color, size=18, bold=False)
        elif idx not in (0, 1) and spec.get("bullets") and layout not in {"title", "section"}:
            # color only runs that were not given an explicit color
            for para in ph.text_frame.paragraphs:
                for run in para.runs:
                    explicit = False
                    # bullets with a color key were styled already
                    if run.font.color is not None:
                        try:
                            _ = run.font.color.rgb
                            explicit = _ is not None
                        except Exception:
                            explicit = False
                    if not explicit:
                        run.font.color.rgb = RGBColor.from_string(theme["body"])
                        if run.font.size is None:
                            run.font.size = Pt(20)
                        if not run.font.name:
                            run.font.name = _fonts(theme)[1]


def _textbox(slide, left, top, width, height, text, size, color, bold=False, font="Calibri"):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    frame = box.text_frame
    frame.word_wrap = True
    paragraph = frame.paragraphs[0]
    run = paragraph.add_run()
    run.text = "" if text is None else str(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = font
    run.font.color.rgb = RGBColor.from_string(color)
    return box


def _content_width(prs):
    # 16:9 is 13.333in; 4:3 is 10in. Leave side margins.
    return max(8.0, prs.slide_width.inches - 1.15)


def _rect(slide, left, top, width, height, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(color)
    shape.line.fill.background()
    return shape


def _paint_bullets(box, theme):
    for paragraph in box.text_frame.paragraphs:
        paragraph.space_after = Pt(10)
        for run in paragraph.runs:
            if run.font.size is None:
                run.font.size = Pt(_size(theme, "body", 16))
            if not run.font.name:
                run.font.name = _fonts(theme)[1]
            try:
                explicit = run.font.color.rgb
            except Exception:
                explicit = None
            if explicit is None:
                run.font.color.rgb = RGBColor.from_string(theme["body"])


def _color_token(value):
    """Return RRGGBB for a hex string or color name, or None."""
    if not isinstance(value, str):
        return None
    raw = value.strip().lower()
    if raw in NAMED_COLORS:
        return NAMED_COLORS[raw]
    hexv = raw.lstrip("#")
    if len(hexv) == 3 and all(ch in "0123456789abcdef" for ch in hexv):
        hexv = "".join(ch * 2 for ch in hexv)
    if len(hexv) == 6 and all(ch in "0123456789abcdef" for ch in hexv):
        return hexv.upper()
    print(f"Warning: ignoring color {value!r}", file=sys.stderr)
    return None


def _distinct(values):
    out = []
    for value in values:
        if value and value not in out:
            out.append(value)
    return out


def _is_light(hex_rgb):
    red = int(hex_rgb[0:2], 16)
    green = int(hex_rgb[2:4], 16)
    blue = int(hex_rgb[4:6], 16)
    return (0.299 * red + 0.587 * green + 0.114 * blue) > 160


def _pick_color(spec, colors, keys, top_level=()):
    for key in keys:
        token = _color_token(colors.get(key)) if isinstance(colors.get(key), str) else None
        if token:
            return token
    for key in top_level:
        token = _color_token(spec.get(key)) if isinstance(spec.get(key), str) else None
        if token:
            return token
    return None


def _apply_color_request(theme, spec):
    """Copy a theme and replace chrome colors when the spec names them.

    ``palette`` is an ordered list (cover, secondary, eyebrow, ...).
    ``colors`` or top-level ``accent`` / ``gold`` override a single role.
    A light cover switches title text to dark so the words stay readable.
    """
    if not theme:
        return None
    theme = dict(theme)
    fonts = spec.get("fonts") if isinstance(spec.get("fonts"), dict) else {}
    if fonts.get("font"):
        theme["title_font"] = str(fonts["font"])
        theme["body_font"] = str(fonts["font"])
    else:
        if fonts.get("title"):
            theme["title_font"] = str(fonts["title"])
        if fonts.get("body"):
            theme["body_font"] = str(fonts["body"])
    sizes = spec.get("sizes") if isinstance(spec.get("sizes"), dict) else {}
    # Points on a 13.333×7.5in slide. Matches a 96/72/44/32/24 px scale at 144 dpi.
    defaults = {"title": 48, "heading": 36, "subtitle": 22, "body": 16, "kpi": 36, "table": 16}
    for key, fallback in defaults.items():
        raw = sizes.get(key, theme.get(f"size_{key}", fallback))
        try:
            theme[f"size_{key}"] = max(12, int(raw))
        except (TypeError, ValueError):
            theme[f"size_{key}"] = fallback
    colors = spec.get("colors") if isinstance(spec.get("colors"), dict) else {}
    palette = []
    raw_palette = spec.get("palette") if isinstance(spec.get("palette"), list) else colors.get("palette")
    if isinstance(raw_palette, list):
        for item in raw_palette:
            token = _color_token(item)
            if token:
                palette.append(token)
    accent = _pick_color(spec, colors, ("accent", "primary"), ("accent", "primary")) or (palette[0] if palette else None)
    gold = _pick_color(spec, colors, ("gold", "secondary"), ("gold", "secondary")) or (palette[1] if len(palette) > 1 else None)
    eyebrow = _pick_color(spec, colors, ("eyebrow",)) or (palette[2] if len(palette) > 2 else None)
    cover = _pick_color(spec, colors, ("cover", "title_bg")) or (palette[0] if palette else None)
    header = _pick_color(spec, colors, ("header", "header_bg"))
    if not any((accent, gold, eyebrow, cover, header, palette)):
        if not theme.get("kpi_stripes"):
            theme["kpi_stripes"] = _distinct([
                theme.get("accent"), theme.get("eyebrow"), theme.get("heading"), theme.get("gold"),
            ]) or ["1F4E79"]
        return theme
    if accent:
        theme["accent"] = accent
        theme["heading"] = accent
        theme["title_bg"] = cover or accent
        theme["header_bg"] = header or accent
        theme["table_header"] = header or accent
        if gold is None:
            theme["gold"] = accent
    if gold:
        theme["gold"] = gold
    if eyebrow:
        theme["eyebrow"] = eyebrow
    if cover and not accent:
        theme["title_bg"] = cover
    if header and not accent:
        theme["header_bg"] = header
        theme["table_header"] = header
    theme["kpi_stripes"] = palette or _distinct([
        theme.get("accent"), theme.get("eyebrow"), theme.get("gold"), theme.get("heading"),
    ])
    if theme.get("title_bg") and _is_light(theme["title_bg"]):
        theme["title_fg"] = "1A1A1A"
        theme["subtitle_fg"] = "334155"
    return theme


def _fonts(theme):
    if not theme:
        return "Georgia", "Calibri"
    title = theme.get("title_font") or "Georgia"
    body = theme.get("body_font") or "Calibri"
    return title, body


def _size(theme, key, fallback):
    try:
        value = int((theme or {}).get(f"size_{key}", fallback))
    except (TypeError, ValueError):
        value = fallback
    return max(12, value)


_METRIC_VALUE = r"[$€£]?\s*[+\-]?\d[\d,]*(?:\.\d+)?\s*%?\s*[KkMmBb]?"


def _metric_kpi(item):
    """Turn a short numeric line into a card. Prose bullets stay lines."""
    if isinstance(item, dict) and item.get("level"):
        return None
    text = item.get("text", "") if isinstance(item, dict) else str(item)
    text = " ".join(str(text).split())
    if not text or len(text) > 72:
        return None
    lead = re.match(
        rf"^(?P<value>{_METRIC_VALUE})(?:\s*[|:—–\-]\s*|\s+)(?P<label>\S.*)$",
        text,
    )
    if lead and len(lead.group("value").strip()) <= 14:
        return {"value": lead.group("value").strip(), "label": lead.group("label").strip()}
    tail = re.match(
        rf"^(?P<label>[A-Za-z][^:]{{1,40}}):\s*(?P<value>{_METRIC_VALUE})$",
        text,
    )
    if tail:
        return {"value": tail.group("value").strip(), "label": tail.group("label").strip()}
    return None


def _lift_metric_bullets(spec):
    kpis = [dict(item) for item in (spec.get("kpis") or [])]
    kept = []
    for item in spec.get("bullets") or []:
        kpi = _metric_kpi(item) if len(kpis) < 4 else None
        if kpi:
            kpis.append(kpi)
        else:
            kept.append(item)
    return kpis, kept


def _draw_kpis(slide, kpis, theme, left, top, width):
    count = min(len(kpis), 4)
    gap = 0.18
    card_w = (width - gap * (count - 1)) / count
    stripes = theme.get("kpi_stripes") or [theme.get("accent") or "1F4E79"]
    for index, kpi in enumerate(kpis[:4]):
        x = left + index * (card_w + gap)
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(top),
            Inches(card_w), Inches(1.15))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor.from_string(theme["card"])
        card.line.color.rgb = RGBColor.from_string("E6EAF0")
        stripe = _color_token(kpi.get("color")) if isinstance(kpi.get("color"), str) else None
        stripe = stripe or stripes[index % len(stripes)]
        _rect(slide, Inches(x), Inches(top + 0.18), Inches(0.06), Inches(0.78), stripe)
        frame = card.text_frame
        frame.word_wrap = True
        frame.margin_left = Inches(0.2)
        value = frame.paragraphs[0]
        value_run = value.add_run()
        value_run.text = str(kpi.get("value", ""))
        title_font, body_font = _fonts(theme)
        value_run.font.size = Pt(_size(theme, "kpi", 26))
        value_run.font.bold = True
        value_run.font.color.rgb = RGBColor.from_string(theme["heading"])
        value_run.font.name = title_font
        label = frame.add_paragraph()
        label_run = label.add_run()
        label_run.text = str(kpi.get("label", ""))
        label_run.font.size = Pt(12)
        label_run.font.color.rgb = RGBColor.from_string(theme["muted"])
        label_run.font.name = body_font


def _point_from_bullet(item):
    text = item.get("text", "") if isinstance(item, dict) else str(item)
    text = " ".join(str(text).split())
    point = {"title": "", "body": text}
    if isinstance(item, dict) and item.get("color"):
        point["color"] = item["color"]
    for sep in (" — ", " – ", " - "):
        if sep in text:
            title, body = text.split(sep, 1)
            point["title"] = title.strip()
            point["body"] = body.strip()
            break
    return point


def _draw_point_grid(slide, cards, theme, left, top, width, bottom=6.55):
    """Group related lines into cards. A tone is used only when the spec sets one."""
    points = []
    for card in cards:
        if isinstance(card, str):
            points.append(_point_from_bullet(card))
            continue
        items = card.get("items") or ([card["body"]] if card.get("body") else [])
        points.append({
            "title": str(card.get("title") or ""),
            "body": "\n".join(str(item) for item in items),
            "tone": card.get("tone"),
            "color": card.get("color"),
        })
    if not points:
        return top
    count = len(points)
    cols = 1 if count == 1 else (3 if count == 3 else 2)
    rows_n = (count + cols - 1) // cols
    gap = 0.18
    card_w = (width - gap * (cols - 1)) / cols
    title_font, body_font = _fonts(theme)
    accent = theme.get("accent") or theme["heading"]
    rails = theme.get("kpi_stripes") or [accent]

    def _line_count(text):
        if not text:
            return 0
        per_line = max(18, int(card_w * 10))
        return sum(max(1, (len(line) + per_line - 1) // per_line) for line in str(text).split("\n"))

    row_heights = []
    for row in range(rows_n):
        heights = []
        for col in range(cols):
            index = row * cols + col
            if index >= count:
                break
            point = points[index]
            lines = (1 if point.get("title") else 0) + _line_count(point.get("body"))
            heights.append(min(3.2, max(1.15, 0.36 * lines + 0.5)))
        row_heights.append(max(heights) if heights else 1.15)
    y_cursor = top
    for row in range(rows_n):
        card_h = row_heights[row]
        if y_cursor + card_h > bottom:
            break
        for col in range(cols):
            index = row * cols + col
            if index >= count:
                break
            point = points[index]
            x = left + col * (card_w + gap)
            dark = point.get("tone") == "dark"
            shape = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y_cursor),
                Inches(card_w), Inches(card_h))
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor.from_string(theme["heading"] if dark else "FFFFFF")
            shape.line.color.rgb = RGBColor.from_string(theme["heading"] if dark else "E6E0D8")
            if not dark:
                _rect(
                    slide, Inches(x), Inches(y_cursor + 0.18), Inches(0.06),
                    Inches(max(0.4, card_h - 0.36)), rails[index % len(rails)],
                )
            frame = shape.text_frame
            frame.word_wrap = True
            frame.margin_left = Inches(0.22)
            frame.margin_right = Inches(0.18)
            body_pr = frame._txBody.find(qn("a:bodyPr"))
            if body_pr is not None:
                body_pr.set("anchor", "ctr")
            title = point.get("title") or ""
            body = point.get("body") or ""
            title_color = "FFFFFF" if dark else (point.get("color") or accent)
            body_color = "F4F1EC" if dark else theme["body"]
            paragraph = frame.paragraphs[0]
            paragraph.alignment = PP_ALIGN.CENTER
            if title:
                run = paragraph.add_run()
                run.text = title
                run.font.size = Pt(_size(theme, "body", 16))
                run.font.bold = True
                run.font.name = title_font
                run.font.color.rgb = RGBColor.from_string(str(title_color).lstrip("#"))
            if body:
                for line_index, line in enumerate(str(body).split("\n")):
                    paragraph = frame.add_paragraph() if (title or line_index) else paragraph
                    paragraph.alignment = PP_ALIGN.CENTER
                    run = paragraph.add_run()
                    run.text = line
                    run.font.size = Pt(_size(theme, "body", 16))
                    run.font.name = body_font
                    run.font.color.rgb = RGBColor.from_string(body_color)
        y_cursor += card_h + gap
    return y_cursor + 0.08


def _draw_designed(prs, slide, spec, theme, meta):
    """Widescreen report chrome: navy cover or header band, gold rule, KPI cards."""
    layout = spec.get("layout", "title_content")
    width = _content_width(prs)
    title_font, body_font = _fonts(theme)
    gold = theme.get("gold") or theme["accent"]
    eyebrow = spec.get("eyebrow") or meta.get("brand") or ""
    page_label = f"{meta['index']:02d} / {meta['total']:02d}"
    if layout == "title":
        _set_bg(slide, theme["title_bg"])
        _rect(slide, 0, 0, prs.slide_width, Inches(0.1), gold)
        _rect(slide, 0, prs.slide_height - Inches(0.1), prs.slide_width, Inches(0.1), gold)
        if eyebrow:
            _textbox(slide, 0.7, 1.7, width, 0.35, eyebrow.upper(), 13, theme.get("eyebrow", gold), bold=True, font=body_font)
        if spec.get("title"):
            _textbox(slide, 0.7, 2.15, width, 1.5, spec["title"], _size(theme, "title", 36), theme["title_fg"], bold=True, font=title_font)
        _rect(slide, Inches(0.7), Inches(3.85), Inches(1.15), Inches(0.055), gold)
        if spec.get("subtitle"):
            _textbox(slide, 0.7, 4.05, width, 0.7, spec["subtitle"], _size(theme, "subtitle", 16), theme["subtitle_fg"], font=body_font)
        footer = meta.get("footer") or ""
        if footer:
            _textbox(slide, 0.7, 6.85, 8, 0.3, footer, 12, theme["subtitle_fg"], font=body_font)
        _textbox(slide, width - 0.4, 6.85, 1.6, 0.3, page_label, 12, theme["subtitle_fg"], font=body_font)
        return None
    if layout == "section":
        _set_bg(slide, theme["title_bg"])
        _rect(slide, 0, 0, prs.slide_width, Inches(0.1), gold)
        if spec.get("title"):
            _textbox(slide, 0.7, 2.9, width, 1.2, spec["title"], 34, theme["title_fg"], bold=True, font=title_font)
        if spec.get("subtitle"):
            _textbox(slide, 0.7, 4.2, width, 0.6, spec["subtitle"], 16, theme["subtitle_fg"], font=body_font)
        return None

    _set_bg(slide, theme["bg"])
    header = theme.get("header_bg") or theme["title_bg"]
    _rect(slide, 0, 0, prs.slide_width, Inches(1.2), header)
    _rect(slide, 0, Inches(1.2), prs.slide_width, Inches(0.055), gold)
    running = " · ".join(part for part in (eyebrow, meta.get("report")) if part)
    if running:
        _textbox(slide, 0.45, 0.12, width - 1.5, 0.28, running.upper(), 12, theme["subtitle_fg"], bold=True, font=body_font)
    if spec.get("title"):
        _textbox(slide, 0.45, 0.4, width - 1.6, 0.65, spec["title"], _size(theme, "heading", 28), theme["title_fg"], bold=True, font=title_font)
    _textbox(slide, width - 0.3, 0.42, 1.5, 0.4, page_label, 12, theme["subtitle_fg"], font=body_font)
    y = 1.45
    if spec.get("subtitle"):
        _textbox(slide, 0.5, y, width, 0.32, spec["subtitle"], _size(theme, "subtitle", 16), theme["muted"], font=body_font)
        y = 1.85
    kpis, bullets = _lift_metric_bullets(spec)
    cards = spec.get("cards") or []
    if kpis:
        _draw_kpis(slide, kpis, theme, 0.5, y, width)
        y += 1.5
    if cards:
        y = _draw_point_grid(slide, cards, theme, 0.5, y, width)
    elif bullets and len(bullets) >= 4 and not kpis:
        y = _draw_point_grid(slide, [_point_from_bullet(item) for item in bullets], theme, 0.5, y, width)
    elif bullets:
        box = slide.shapes.add_textbox(
            Inches(0.5), Inches(y), Inches(width), Inches(max(1.2, 6.7 - y)))
        add_bullets(box.text_frame, bullets)
        _paint_bullets(box, theme)
        y = 6.7
    footer = meta.get("footer") or ""
    if footer:
        _textbox(slide, 0.45, 6.95, 8, 0.28, footer, 12, theme["muted"], font=body_font)
        _textbox(slide, width - 0.2, 6.95, 1.4, 0.28, f"{meta['index']:02d}", 12, theme["muted"], font=body_font)
    return y


def style_table(table, theme, header=True, font_size=None):
    if not theme:
        return
    for r, row in enumerate(table.rows):
        for cell in row.cells:
            fill = cell.fill
            fill.solid()
            if header and r == 0:
                fill.fore_color.rgb = RGBColor.from_string(theme["table_header"])
                color = theme["table_header_fg"]
                bold = True
            else:
                fill.fore_color.rgb = RGBColor.from_string(
                    theme["table_alt"] if r % 2 == 0 else theme["card"])
                color = theme["body"]
                bold = False
            for para in cell.text_frame.paragraphs:
                for run in para.runs:
                    run.font.color.rgb = RGBColor.from_string(color)
                    run.font.bold = bold
                    run.font.size = Pt(font_size or _size(theme, "table", 15))
                    run.font.name = _fonts(theme)[1]


def build_slide(prs, spec, theme=None, meta=None):
    layout_name = spec.get("layout", "title_content")
    # Explicit chrome still uses Office placeholders (footer, slide number, custom background).
    uses_placeholders = bool(spec.get("background") or spec.get("footer") or spec.get("slide_number"))
    designed = (
        theme
        and not uses_placeholders
        and layout_name in {"title", "section", "title_content", "title_only"}
    )
    layout_idx = 6 if designed else LAYOUTS.get(layout_name, 1)
    slide = prs.slides.add_slide(prs.slide_layouts[layout_idx])

    if spec.get("background"):
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor.from_string(spec["background"])
    if spec.get("slide_number"):
        copy_layout_placeholder(slide, 12)
    if spec.get("footer"):
        shape = copy_layout_placeholder(slide, 11)
        if shape is not None:
            shape.text_frame.text = spec["footer"]

    content_bottom = None
    if designed:
        content_bottom = _draw_designed(prs, slide, spec, theme, meta or {"index": 1, "total": 1})
    else:
        if spec.get("title") is not None and slide.shapes.title is not None:
            slide.shapes.title.text = spec["title"]
        if spec.get("subtitle") is not None:
            for ph in slide.placeholders:
                if ph.placeholder_format.idx == 1:
                    ph.text = spec["subtitle"]
                    break
        if spec.get("bullets"):
            body = next((ph for ph in slide.placeholders
                         if ph.placeholder_format.idx != 0), None)
            if body is None:
                body = slide.shapes.add_textbox(Inches(0.5), Inches(1.5),
                                                Inches(9), Inches(5))
            add_bullets(body.text_frame, spec["bullets"])

    for img in spec.get("images", []):
        kwargs = {}
        if img.get("width"):
            kwargs["width"] = Inches(img["width"])
        if img.get("height"):
            kwargs["height"] = Inches(img["height"])
        slide.shapes.add_picture(img["path"], Inches(img.get("left", 1)),
                                 Inches(img.get("top", 1)), **kwargs)

    for tbl in spec.get("tables", []):
        rows = tbl["rows"]
        full_w = _content_width(prs)
        left = float(tbl["left"]) if "left" in tbl else 0.55
        top = float(tbl["top"]) if "top" in tbl else (content_bottom or 2.05)
        width = float(tbl["width"]) if "width" in tbl else full_w
        height = float(tbl["height"]) if "height" in tbl else min(4.5, max(2.3, 0.52 * len(rows) + 0.3))
        if designed and width <= 6.5:
            left, width = 0.55, full_w
        if designed and height <= 2.2:
            height = min(4.5, max(2.4, 0.52 * len(rows) + 0.35))
        if content_bottom and top < content_bottom - 0.05:
            top = content_bottom
        room = 6.85 - top
        height = min(height, max(1.6, room))
        shape = slide.shapes.add_table(
            len(rows), len(rows[0]), Inches(left),
            Inches(top), Inches(width), Inches(height))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                shape.table.cell(r, c).text = str(val)
        if theme and not tbl.get("plain"):
            style_table(shape.table, theme, header=tbl.get("header", True), font_size=tbl.get("font_size"))

    for shp in spec.get("shapes", []):
        shape = slide.shapes.add_shape(
            SHAPE_TYPES.get(shp.get("type", "rectangle"), MSO_SHAPE.RECTANGLE),
            Inches(shp.get("left", 1)), Inches(shp.get("top", 1)),
            Inches(shp.get("width", 2)), Inches(shp.get("height", 1)))
        if shp.get("fill"):
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor.from_string(shp["fill"])
        if shp.get("text"):
            shape.text_frame.text = shp["text"]
            if shp.get("text_color"):
                run = shape.text_frame.paragraphs[0].runs[0]
                run.font.color.rgb = RGBColor.from_string(shp["text_color"])

    for cht in spec.get("charts", []):
        data = CategoryChartData()
        data.categories = cht["categories"]
        for name, values in cht["series"].items():
            data.add_series(name, values)
        top = float(cht.get("top", 2))
        height = float(cht.get("height", 4))
        if content_bottom and top < content_bottom - 0.05:
            top = content_bottom
            height = min(height, max(1.8, 7.05 - top))
        frame = slide.shapes.add_chart(
            CHART_TYPES.get(cht.get("type", "bar"),
                            XL_CHART_TYPE.COLUMN_CLUSTERED),
            Inches(cht.get("left", 1)), Inches(top),
            Inches(cht.get("width", 6)), Inches(height), data)
        if cht.get("title"):
            frame.chart.has_title = True
            frame.chart.chart_title.text_frame.text = cht["title"]

    if spec.get("notes"):
        slide.notes_slide.notes_text_frame.text = spec["notes"]
    if theme and not designed:
        apply_theme(prs, slide, spec, theme)
    return slide


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(
        description="Create a .pptx deck from a JSON spec.",
        epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("spec", help="path to JSON deck spec")
    parser.add_argument("output", help="output .pptx path")
    args = parser.parse_args(argv)

    with open(args.spec, encoding="utf-8") as fh:
        spec = json.load(fh)

    prs = Presentation()
    if spec.get("slide_size", "16:9") == "16:9":
        prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    else:
        prs.slide_width, prs.slide_height = Inches(10), Inches(7.5)

    theme_name = str(spec.get("theme", "professional")).lower()
    if theme_name not in THEMES:
        print(f"Warning: unknown theme {theme_name!r}, using professional", file=sys.stderr)
        theme_name = "professional"
    base_theme = THEMES[theme_name]
    theme = _apply_color_request(dict(base_theme), spec) if base_theme else None

    slides = spec.get("slides", [])
    meta_base = {
        "brand": spec.get("brand") or spec.get("eyebrow") or "",
        "footer": spec.get("footer") or "",
        "report": spec.get("report") or "",
        "total": len(slides) or 1,
    }
    for index, slide_spec in enumerate(slides, start=1):
        # per-slide "theme": "plain" skips chrome for that slide
        slide_theme = None if slide_spec.get("theme") == "plain" else _apply_color_request(
            dict(theme) if theme else None, slide_spec)
        meta = dict(meta_base, index=index)
        build_slide(prs, slide_spec, slide_theme, meta)

    prs.save(args.output)
    print(json.dumps({"ok": True, "output": args.output,
                      "slides": len(prs.slides._sldIdLst),
                      "theme": theme_name}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
