"""Create the English, four-page printable programme from the website data."""

import importlib.util
from collections import defaultdict
from datetime import date
from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/IJTCS-FAW-2026-Programme.pdf"
URL = "https://ijtcs-faw2026.github.io/IJTCS-FAW2026/"
NAVY = colors.HexColor("#22324D")
BLUE = colors.HexColor("#315F86")
PALE = colors.HexColor("#E9EEF4")
GREY = colors.HexColor("#586575")
LINE = colors.HexColor("#D6DEE7")


def load_source():
    spec = importlib.util.spec_from_file_location("conference_pages", ROOT / "scripts/build-conference-pages.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.load_data()


def register_fonts():
    candidates = [
        (Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/arialbd.ttf")),
        (Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
         Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")),
    ]
    for normal, bold in candidates:
        if normal.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont("Programme", str(normal)))
            pdfmetrics.registerFont(TTFont("ProgrammeBold", str(bold)))
            pdfmetrics.registerFontFamily("Programme", normal="Programme", bold="ProgrammeBold")
            return "Programme", "ProgrammeBold"
    return "Helvetica", "Helvetica-Bold"


def text(value):
    value = re.sub(r"\$([^$]+)\$", r"\1", str(value))
    value = value.replace(r"\\(k\\)", "k").replace(r"\(k\)", "k")
    value = value.translate(str.maketrans({c: "-" for c in "\u2010\u2011\u2012\u2013\u2014\u2212"}))
    return escape(value).replace("l_p", "<i>l</i><sub>p</sub>")


def styles(normal, bold, size):
    return {
        "paper": ParagraphStyle("Paper", fontName=normal, fontSize=size,
                                leading=size + 1.7, textColor=NAVY, alignment=TA_LEFT),
        "author": ParagraphStyle("Author", fontName=normal, fontSize=7.4,
                                 leading=8.6, textColor=GREY),
        "session": ParagraphStyle("Session", fontName=bold, fontSize=9.2,
                                  leading=10.8, textColor=NAVY),
        "event": ParagraphStyle("Event", fontName=bold, fontSize=9.1,
                                leading=10.8, textColor=NAVY),
        "note": ParagraphStyle("Note", fontName=normal, fontSize=7.6,
                               leading=8.8, textColor=GREY),
        "time": ParagraphStyle("Time", fontName=normal, fontSize=8,
                               leading=9.7, textColor=GREY),
    }


def make_rows(events, slots, papers, module, style, talk_minutes):
    rows = []
    for event in events:
        time = f'{event["start"]}-{event["end"]}'
        if event["type"] == "Session":
            sid = event["session"]
            rows.append((time, [(f'{sid} | {text(event["title"])}', "session")], "session"))
            for slot in sorted(slots[sid], key=lambda s: s["order"]):
                start = module.minutes(event["start"]) + (slot["order"] - 1) * talk_minutes
                talk_time = f"{module.clock(start)}-{module.clock(start + talk_minutes)}"
                if slot["status"] != "accepted":
                    raise ValueError("Remove withdrawn slots before generating the printable programme")
                paper = papers[slot["paper_number"]]
                title = f'<b>#{paper["number"]}</b> {text(paper["title"])}'
                rows.append((talk_time, [(title, "paper"), (text(paper["authors"]), "author")], "paper"))
        else:
            content = [(text(event["title"]), "event")]
            if event["type"] in ("Keynote", "Tutorial"):
                content.append(("Speaker and title: TBA", "note"))
            elif event["type"] == "Forum":
                content.append(("Speakers and details: TBA", "note"))
            elif event["type"] == "Poster":
                content.append(("Poster lineup and display details: TBA", "note"))
            rows.append((time, content, "event"))
    return rows


def layout_rows(rows, width, style):
    time_width = 67
    body_width = width - time_width - 14
    result = []
    for time, content, kind in rows:
        paragraphs = []
        for value, category in content:
            para = Paragraph(value, style[category])
            _, height = para.wrap(body_width, 1000)
            paragraphs.append((para, height))
        time_para = Paragraph(time, style["time"])
        _, time_height = time_para.wrap(time_width - 6, 1000)
        gap = 2 if len(paragraphs) > 1 else 0
        content_height = sum(height for _, height in paragraphs) + gap * (len(paragraphs) - 1)
        height = max(time_height, content_height) + (9 if kind == "session" else 7)
        result.append((time_para, time_height, paragraphs, height, gap, kind))
    return result, sum(row[3] for row in result)


def draw_rows(pdf, rows, x, top, width):
    y = top
    for time_para, time_height, paragraphs, height, gap, kind in rows:
        if kind == "session":
            pdf.setFillColor(PALE)
            pdf.rect(x, y - height, width, height, fill=1, stroke=0)
            pdf.setFillColor(BLUE)
            pdf.rect(x, y - height, 2, height, fill=1, stroke=0)
        time_para.drawOn(pdf, x + 6, y - 4 - time_height)
        content_y = y - 4
        for para, para_height in paragraphs:
            para.drawOn(pdf, x + 74, content_y - para_height)
            content_y -= para_height + gap
        pdf.setStrokeColor(LINE)
        pdf.setLineWidth(0.3)
        pdf.line(x, y - height, x + width, y - height)
        y -= height


def main():
    module, (data, paper_rows, sessions, slot_rows, events) = load_source()
    updated = date.fromisoformat(data["updated"])
    updated_label = f"{updated:%b} {updated.day}, {updated.year}"
    talk_minutes = data["talk_minutes"]
    normal, bold = register_fonts()
    by_number = {p["number"]: p for p in paper_rows}
    slots = defaultdict(list)
    days = defaultdict(list)
    for slot in slot_rows:
        slots[slot["session"]].append(slot)
    for event in events:
        days[event["date"]].append(event)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=landscape(A4), invariant=1)
    pdf.setTitle("IJTCS-FAW 2026 - Conference Programme")
    pdf.setAuthor("IJTCS-FAW 2026 Organizing Committee")
    pdf.setSubject("English programme, Nov 7-10, 2026; all times Beijing time (UTC+8)")
    width, height = landscape(A4)
    margin, gutter = 28, 20
    body_top, body_bottom = height - 123, 37
    days_sorted = sorted(days)
    for page, day in enumerate(days_sorted, 1):
        pdf.setFillColor(NAVY)
        pdf.setFont(bold, 20)
        pdf.drawString(margin, height - 32, "IJTCS-FAW 2026")
        pdf.setFont(normal, 10)
        pdf.drawString(margin, height - 48, "Conference Programme | English Edition")
        for index, filename in enumerate(["ccf-emblem.png", "ruc-emblem.png"]):
            asset = ImageReader(str(ROOT / "assets/img" / filename))
            iw, ih = asset.getSize()
            x, y = width - margin - 84 + index * 46, height - 49
            if filename == "ruc-emblem.png":
                # Clip the source asset's wide white margins in the PDF only.
                crop_left, crop_top, crop_right, crop_bottom = 348, 34, 577, 267
                scale = 36 / max(crop_right - crop_left, crop_bottom - crop_top)
                pdf.saveState()
                clip = pdf.beginPath()
                clip.rect(x, y, 36, 36)
                pdf.clipPath(clip, stroke=0, fill=0)
                pdf.drawImage(asset, x - crop_left * scale,
                              y - (ih - crop_bottom) * scale,
                              width=iw * scale, height=ih * scale, mask="auto")
                pdf.restoreState()
            else:
                scale = min(36 / iw, 36 / ih)
                pdf.drawImage(asset, x, y, width=iw * scale, height=ih * scale, mask="auto")
        pdf.setStrokeColor(BLUE)
        pdf.setLineWidth(1.2)
        pdf.line(margin, height - 58, width - margin, height - 58)
        pdf.setFont(bold, 14)
        label = date.fromisoformat(day).strftime("%b %d, %Y | %A").replace(" 0", " ")
        pdf.drawString(margin, height - 78, label)
        pdf.setFont(normal, 8.2)
        pdf.setFillColor(GREY)
        pdf.drawString(margin, height - 92, "Culture Building, Renmin University of China | Beijing, China")
        pdf.drawRightString(width - margin, height - 92, f"All times: Beijing time (UTC+8) | Paper slots: {talk_minutes} min incl. Q&A")
        morning = [e for e in days[day] if module.minutes(e["start"]) < 13 * 60]
        afternoon = [e for e in days[day] if module.minutes(e["start"]) >= 13 * 60]
        panels = [("MORNING", morning)] + ([("AFTERNOON", afternoon)] if afternoon else [])
        panel_width = (width - 2 * margin - gutter) / 2 if afternoon else width - 2 * margin
        for panel, (heading, entries) in enumerate(panels):
            x = margin + panel * (panel_width + gutter)
            for size in (9.2, 9.0, 8.8, 8.6):
                style = styles(normal, bold, size)
                rows, used_height = layout_rows(make_rows(entries, slots, by_number, module, style, talk_minutes), panel_width, style)
                if used_height <= body_top - body_bottom:
                    break
            else:
                raise ValueError(f"Programme column overflows: {day} {heading} ({used_height:.1f} pt)")
            pdf.setFillColor(BLUE)
            pdf.setFont(bold, 8.8)
            pdf.drawString(x + 6, body_top + 9, heading)
            draw_rows(pdf, rows, x, body_top, panel_width)
            print(f"{day} {heading}: {used_height:.1f}/{body_top-body_bottom:.1f} pt; title font {size}")
        pdf.setFillColor(GREY)
        pdf.setFont(normal, 7.2)
        pdf.drawString(margin, 20, f"Updated {updated_label} | Keynote/tutorial speakers and titles, and session chairs: TBA.")
        pdf.drawRightString(width - margin, 20, f"{page} / {len(days_sorted)}")
        pdf.drawString(margin, 10, URL)
        pdf.linkURL(URL, (margin, 8, margin + 230, 17), relative=0)
        pdf.showPage()
    pdf.save()
    print(OUTPUT)


if __name__ == "__main__":
    main()
