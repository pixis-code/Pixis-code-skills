#!/usr/bin/env python3
"""Create a styled PDF from a JSON spec using reportlab platypus.

Default theme is ``professional`` (accent color, hierarchy, spaced layout).
Use ``"theme": "plain"`` only when the user asks for minimal/B&W output.

Spec format (UTF-8 JSON):
{
  "title": "Q2 Business Review",
  "author": "Analytics",
  "subtitle": "Confidential — internal use",
  "theme": "professional",   // professional | plain | midnight | forest
  "accent": "#1F4E79",       // optional hex override
  "page_size": "A4",         // or letter
  "page_numbers": true,
  "margin_pt": 54,
  "elements": [
    {"type": "heading", "text": "Executive summary", "level": 1},
    {"type": "paragraph", "text": "Body with <b>bold</b> and <i>italic</i>."},
    {"type": "bullet_list", "items": ["First point", "Second point"]},
    {"type": "numbered_list", "items": ["Step one", "Step two"]},
    {"type": "callout", "text": "Key metric: revenue +45.8% YoY.", "style": "info"},
    {"type": "spacer", "height": 12},
    {"type": "hrule"},
    {"type": "table", "rows": [["Region", "Units"], ["North", "1250"]], "header": true},
    {"type": "image", "path": "chart.png", "width": 400},
    {"type": "pagebreak"}
  ]
}
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


THEMES: dict[str, dict[str, Any]] = {
    "professional": {
        "accent": "#1F4E79",
        "accent_soft": "#D6E3F0",
        "text": "#1A1A1A",
        "muted": "#5A5A5A",
        "table_header_bg": "#1F4E79",
        "table_header_fg": "#FFFFFF",
        "table_alt_bg": "#F2F6FA",
        "callout_info_bg": "#E8F1FB",
        "callout_warn_bg": "#FFF4E5",
        "callout_success_bg": "#E7F6ED",
        "rule": "#1F4E79",
    },
    "midnight": {
        "accent": "#312E81",
        "accent_soft": "#E0E7FF",
        "text": "#111827",
        "muted": "#4B5563",
        "table_header_bg": "#312E81",
        "table_header_fg": "#FFFFFF",
        "table_alt_bg": "#EEF2FF",
        "callout_info_bg": "#EEF2FF",
        "callout_warn_bg": "#FEF3C7",
        "callout_success_bg": "#D1FAE5",
        "rule": "#312E81",
    },
    "forest": {
        "accent": "#14532D",
        "accent_soft": "#DCFCE7",
        "text": "#14532D",
        "muted": "#3F6212",
        "table_header_bg": "#166534",
        "table_header_fg": "#FFFFFF",
        "table_alt_bg": "#F0FDF4",
        "callout_info_bg": "#ECFDF5",
        "callout_warn_bg": "#FEF9C3",
        "callout_success_bg": "#DCFCE7",
        "rule": "#166534",
    },
    "business": {
        "accent": "#0E1F38",
        "accent_soft": "#E8EEF6",
        "text": "#1A2332",
        "muted": "#5B6770",
        "table_header_bg": "#16274D",
        "table_header_fg": "#FFFFFF",
        "table_alt_bg": "#F4F7FB",
        "callout_info_bg": "#E7F6F4",
        "callout_warn_bg": "#FFF4E5",
        "callout_success_bg": "#E7F6ED",
        "rule": "#E89B3C",
        "gold": "#E89B3C",
        "eyebrow": "#159E93",
        "header": "#16274D",
        "cover": "#0E1F38",
    },
    "plain": {
        "accent": "#000000",
        "accent_soft": "#EEEEEE",
        "text": "#000000",
        "muted": "#333333",
        "table_header_bg": "#DDDDDD",
        "table_header_fg": "#000000",
        "table_alt_bg": "#F7F7F7",
        "callout_info_bg": "#F0F0F0",
        "callout_warn_bg": "#F0F0F0",
        "callout_success_bg": "#F0F0F0",
        "rule": "#999999",
    },
}


def _reconfigure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def _hex_to_color(value: str, colors_mod):
    raw = value.strip().lstrip("#")
    if len(raw) == 3:
        raw = "".join(ch * 2 for ch in raw)
    if len(raw) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", raw):
        raise ValueError(f"invalid hex color: {value!r}")
    r = int(raw[0:2], 16) / 255.0
    g = int(raw[2:4], 16) / 255.0
    b = int(raw[4:6], 16) / 255.0
    return colors_mod.Color(r, g, b)


def _resolve_theme(spec: dict[str, Any], colors_mod) -> dict[str, Any]:
    name = str(spec.get("theme", "professional")).lower()
    if name not in THEMES:
        print(f"Warning: unknown theme {name!r}, using professional", file=sys.stderr)
        name = "professional"
    base = dict(THEMES[name])
    if spec.get("accent"):
        accent = str(spec["accent"])
        base["accent"] = accent
        base["table_header_bg"] = accent
        base["rule"] = accent
    resolved: dict[str, Any] = {}
    for key, val in base.items():
        if isinstance(val, str):
            hexv = val if val.startswith("#") else f"#{val}"
            resolved[key] = _hex_to_color(hexv, colors_mod)
        else:
            resolved[key] = val
    resolved["_name"] = name
    return resolved


def _build_styles(theme: dict[str, Any], getSampleStyleSheet, ParagraphStyle):
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "PixisTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=theme["accent"],
            spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "PixisSubtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=14,
            textColor=theme["muted"],
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "PixisH1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=theme["accent"],
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "PixisH2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=theme["accent"],
            spaceBefore=12,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "PixisH3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=theme["text"],
            spaceBefore=10,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "PixisBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=theme["text"],
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "PixisBullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=theme["text"],
            leftIndent=14,
            bulletIndent=0,
            spaceAfter=3,
        ),
        "callout": ParagraphStyle(
            "PixisCallout",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=theme["text"],
        ),
        "table_cell": ParagraphStyle(
            "PixisTableCell",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=11,
            textColor=theme["text"],
        ),
        "table_header": ParagraphStyle(
            "PixisTableHeader",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=11,
            textColor=theme["table_header_fg"],
        ),
    }
    return styles


def _as_paragraphs(rows: list[list[Any]], styles, header: bool, paragraph_cls) -> list[list[Any]]:
    """Wrap table cells in Paragraphs so text wraps cleanly."""
    out = []
    for r_i, row in enumerate(rows):
        style = styles["table_header"] if header and r_i == 0 else styles["table_cell"]
        out.append([paragraph_cls(str(cell), style) for cell in row])
    return out


def build_pdf(spec: dict, out_path: str) -> int:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.pagesizes import A4, letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            HRFlowable,
            Image,
            KeepTogether,
            ListFlowable,
            ListItem,
            PageBreak,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except ImportError:
        print(
            "Missing dependency: install with 'python3 -m pip install reportlab'",
            file=sys.stderr,
        )
        return 2

    theme = _resolve_theme(spec, colors)
    styles = _build_styles(theme, getSampleStyleSheet, ParagraphStyle)
    if theme.get("_name") == "business":
        styles["title"].textColor = colors.white
        styles["title"].fontSize = 32
        styles["title"].leading = 38
        styles["title"].alignment = TA_LEFT
        styles["subtitle"].textColor = colors.Color(0.725, 0.796, 0.918)
        styles["subtitle"].alignment = TA_LEFT
    page_choice = str(spec.get("page_size", "widescreen" if theme.get("_name") == "business" else "A4")).lower()
    if page_choice == "letter":
        page_size = letter
    elif page_choice == "widescreen":
        page_size = (13.333 * inch, 7.5 * inch)
    else:
        page_size = A4
    margin = float(spec.get("margin_pt", 54))
    top_margin = 96 if theme.get("_name") == "business" else margin

    story: list[Any] = []

    # Document title block when title is set and first element isn't already that heading
    if spec.get("title"):
        if theme.get("_name") == "business":
            story.append(Spacer(1, 70))
            brand = str(spec.get("brand") or spec.get("eyebrow") or "").strip()
            if brand:
                eyebrow = ParagraphStyle(
                    "PixisEyebrow",
                    parent=styles["subtitle"],
                    textColor=colors.Color(0.082, 0.620, 0.576),
                    fontName="Helvetica-Bold",
                    fontSize=11,
                    leading=14,
                    alignment=TA_LEFT,
                )
                story.append(Paragraph(brand.upper(), eyebrow))
        story.append(Paragraph(str(spec["title"]), styles["title"]))
        if spec.get("subtitle"):
            story.append(Paragraph(str(spec["subtitle"]), styles["subtitle"]))
        else:
            story.append(Spacer(1, 10))
        story.append(
            HRFlowable(
                width="28%" if theme.get("_name") == "business" else "100%",
                thickness=3 if theme.get("_name") == "business" else 2,
                color=theme.get("rule") or theme["accent"],
                hAlign="LEFT" if theme.get("_name") == "business" else "CENTER",
                spaceBefore=2,
                spaceAfter=14,
            )
        )
        if theme.get("_name") == "business":
            story.append(PageBreak())

    for el in spec.get("elements", []):
        etype = el.get("type")
        if etype == "heading":
            level = min(max(int(el.get("level", 1)), 1), 3)
            key = {1: "h1", 2: "h2", 3: "h3"}[level]
            story.append(Paragraph(el.get("text", ""), styles[key]))
        elif etype == "paragraph":
            story.append(Paragraph(el.get("text", ""), styles["body"]))
        elif etype in {"bullet_list", "bullets", "list"}:
            items = el.get("items") or el.get("text") or []
            if isinstance(items, str):
                items = [items]
            flow_items = [
                ListItem(Paragraph(str(item), styles["bullet"]), leftIndent=10, bulletColor=theme["accent"])
                for item in items
            ]
            story.append(
                ListFlowable(
                    flow_items,
                    bulletType="bullet",
                    leftIndent=18,
                    bulletFontName="Helvetica",
                    bulletFontSize=10,
                    spaceBefore=2,
                    spaceAfter=8,
                )
            )
        elif etype in {"numbered_list", "numbered"}:
            items = el.get("items") or []
            flow_items = [
                ListItem(Paragraph(str(item), styles["bullet"]), leftIndent=10, bulletColor=theme["accent"])
                for item in items
            ]
            story.append(
                ListFlowable(
                    flow_items,
                    bulletType="1",
                    leftIndent=18,
                    spaceBefore=2,
                    spaceAfter=8,
                )
            )
        elif etype == "callout":
            text = el.get("text", "")
            kind = str(el.get("style", "info")).lower()
            bg_key = {
                "info": "callout_info_bg",
                "warn": "callout_warn_bg",
                "warning": "callout_warn_bg",
                "success": "callout_success_bg",
            }.get(kind, "callout_info_bg")
            inner = Paragraph(text, styles["callout"])
            box = Table([[inner]], colWidths=["*"])
            box.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), theme[bg_key]),
                        ("BOX", (0, 0), (-1, -1), 1.2, theme["accent"]),
                        ("LEFTPADDING", (0, 0), (-1, -1), 10),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ]
                )
            )
            story.append(KeepTogether([box, Spacer(1, 10)]))
        elif etype == "spacer":
            story.append(Spacer(1, float(el.get("height", 12))))
        elif etype in {"hrule", "rule", "divider"}:
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=float(el.get("thickness", 1)),
                    color=theme["rule"],
                    spaceBefore=6,
                    spaceAfter=10,
                )
            )
        elif etype == "table":
            rows = el.get("rows", [])
            if not rows:
                continue
            header = bool(el.get("header", True))
            wrapped = _as_paragraphs(rows, styles, header, Paragraph)
            table = Table(wrapped, repeatRows=1 if header else 0, hAlign="LEFT")
            style_cmds = [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.Color(0.75, 0.78, 0.82)),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
            if header:
                style_cmds += [
                    ("BACKGROUND", (0, 0), (-1, 0), theme["table_header_bg"]),
                    ("TEXTCOLOR", (0, 0), (-1, 0), theme["table_header_fg"]),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ]
                start = 1
            else:
                start = 0
            # zebra rows
            for i in range(start, len(wrapped)):
                if (i - start) % 2 == 1:
                    style_cmds.append(("BACKGROUND", (0, i), (-1, i), theme["table_alt_bg"]))
            table.setStyle(TableStyle(style_cmds))
            story.append(table)
            story.append(Spacer(1, 12))
        elif etype == "image":
            kwargs = {}
            if el.get("width"):
                kwargs["width"] = float(el["width"])
            if el.get("height"):
                kwargs["height"] = float(el["height"])
            img = Image(el["path"], **kwargs)
            if "width" in kwargs and "height" not in kwargs:
                ratio = img.imageHeight / float(img.imageWidth or 1)
                img.drawWidth = kwargs["width"]
                img.drawHeight = kwargs["width"] * ratio
            story.append(img)
            story.append(Spacer(1, 10))
        elif etype == "pagebreak":
            story.append(PageBreak())
        else:
            print(f"Warning: unknown element type {etype!r}, skipped", file=sys.stderr)

    def draw_chrome(canvas, doc):
        canvas.saveState()
        if theme.get("_name") == "business" and doc.page == 1 and spec.get("title"):
            canvas.setFillColor(theme["cover"])
            canvas.rect(0, 0, page_size[0], page_size[1], fill=1, stroke=0)
            canvas.setFillColor(theme["rule"])
            canvas.rect(0, page_size[1] - 8, page_size[0], 8, fill=1, stroke=0)
            canvas.rect(0, 0, page_size[0], 8, fill=1, stroke=0)
            canvas.setFillColor(colors.Color(0.725, 0.796, 0.918))
            canvas.setFont("Helvetica", 9)
            footer = str(spec.get("footer") or "")
            if footer:
                canvas.drawString(36, 22, footer)
            canvas.drawRightString(page_size[0] - 36, 22, "01")
        elif theme.get("_name") == "business":
            canvas.setFillColor(theme["header"])
            canvas.rect(0, page_size[1] - 78, page_size[0], 78, fill=1, stroke=0)
            canvas.setFillColor(theme["rule"])
            canvas.rect(0, page_size[1] - 84, page_size[0], 6, fill=1, stroke=0)
            brand = str(spec.get("brand") or spec.get("eyebrow") or "")
            report = str(spec.get("report") or "")
            running = " · ".join(part for part in (brand, report) if part)
            if running:
                canvas.setFillColor(colors.Color(0.725, 0.796, 0.918))
                canvas.setFont("Helvetica", 8)
                canvas.drawString(36, page_size[1] - 22, running.upper())
        elif theme.get("_name") != "plain":
            canvas.setStrokeColor(theme["accent"])
            canvas.setLineWidth(2)
            canvas.line(margin, page_size[1] - 24, page_size[0] - margin, page_size[1] - 24)
        if spec.get("page_numbers", True) and not (theme.get("_name") == "business" and doc.page == 1 and spec.get("title")):
            canvas.setFillColor(theme["muted"])
            canvas.setFont("Helvetica", 9)
            title = str(spec.get("title") or "").strip()
            label = f"{title}  ·  Page {doc.page}" if title else f"Page {doc.page}"
            canvas.drawCentredString(page_size[0] / 2.0, 0.45 * inch, label)
        canvas.restoreState()

    doc = SimpleDocTemplate(
        out_path,
        pagesize=page_size,
        title=spec.get("title", ""),
        author=spec.get("author", ""),
        leftMargin=margin,
        rightMargin=margin,
        topMargin=top_margin if theme.get("_name") == "business" else margin + 12,
        bottomMargin=margin,
    )
    doc.build(story, onFirstPage=draw_chrome, onLaterPages=draw_chrome)
    print(
        json.dumps(
            {
                "output": out_path,
                "elements": len(spec.get("elements", [])),
                "theme": theme.get("_name", "professional"),
            }
        )
    )
    return 0


def main() -> int:
    _reconfigure_stdio()
    parser = argparse.ArgumentParser(description="Create a styled PDF from a JSON spec (reportlab).")
    parser.add_argument("spec", help="Path to UTF-8 JSON spec file")
    parser.add_argument("-o", "--output", required=True, help="Output PDF path")
    args = parser.parse_args()
    with open(args.spec, encoding="utf-8") as fh:
        spec = json.load(fh)
    return build_pdf(spec, args.output)


if __name__ == "__main__":
    sys.exit(main())
