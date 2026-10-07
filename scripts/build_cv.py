"""Build the public CV: python3 scripts/build_cv.py (requires reportlab)."""

from html import escape, unescape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "files" / "Francis_Xiatian_Zhang_CV.pdf"
OUTPUT.parent.mkdir(exist_ok=True)
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
for name, filename in [
    ("CV", "DejaVuSans.ttf"),
    ("CV-Bold", "DejaVuSans-Bold.ttf"),
    ("CV-Italic", "DejaVuSans-Oblique.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
pdfmetrics.registerFontFamily("CV", normal="CV", bold="CV-Bold", italic="CV-Italic", boldItalic="CV-Bold")

NAVY = colors.HexColor("#203b58")
BLUE = colors.HexColor("#315f9c")
GREY = colors.HexColor("#596570")
BODY = colors.HexColor("#26323c")
styles = {
    "name": ParagraphStyle("name", fontName="CV-Bold", fontSize=23, leading=28, textColor=NAVY),
    "subtitle": ParagraphStyle("subtitle", fontName="CV", fontSize=11, leading=16, textColor=GREY),
    "body": ParagraphStyle("body", fontName="CV", fontSize=9.5, leading=13.4, textColor=BODY, spaceAfter=5),
    "small": ParagraphStyle("small", fontName="CV", fontSize=8.5, leading=12, textColor=GREY, spaceAfter=4),
    "section": ParagraphStyle("section", fontName="CV-Bold", fontSize=11.5, leading=16, textColor=NAVY, spaceBefore=12, spaceAfter=7, keepWithNext=True),
    "publication": ParagraphStyle("publication", fontName="CV", fontSize=9, leading=12.3, textColor=BODY, spaceAfter=7),
    "date": ParagraphStyle("date", fontName="CV", fontSize=8.5, leading=12.5, textColor=GREY, alignment=TA_LEFT),
}


def paragraph(text, style="body"):
    return Paragraph(text, styles[style])


def link(url, label):
    return f'<a href="{escape(url, quote=True)}" color="#315f9c">{escape(label)}</a>'


def section(title):
    return paragraph(title, "section")


def entry(date, title, detail=""):
    content = f"<b>{title}</b>" + (f"<br/>{detail}" if detail else "")
    table = Table([[paragraph(date, "date"), paragraph(content)]], colWidths=[91, 420])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(colors.HexColor("#d9e0e7"))
    canvas.line(42, 38, width - 42, 38)
    canvas.setFont("CV", 7.5)
    canvas.setFillColor(GREY)
    canvas.drawString(42, 25, "Francis Xiatian Zhang | Updated October 2026")
    canvas.drawRightString(width - 42, 25, f"{doc.page}")
    if doc.page > 1:
        canvas.drawString(42, A4[1] - 27, "Francis Xiatian Zhang | Curriculum Vitae")
    canvas.restoreState()


story = [
    paragraph("Francis Xiatian Zhang, PhD", "name"),
    paragraph("Robot Vision · Medical Robotics · Computer Vision", "subtitle"),
    Spacer(1, 8),
    paragraph(
        link("mailto:francis.zhang@ed.ac.uk", "francis.zhang@ed.ac.uk") + " · " +
        link("mailto:francis.xiatian.zhang@outlook.com", "francis.xiatian.zhang@outlook.com"), "small"
    ),
    paragraph(
        link("https://francisxzhang.github.io/", "Website") + " · " +
        link("https://github.com/FrancisXZhang", "GitHub") + " · " +
        link("https://scholar.google.com/citations?user=R04bvhAAAAAJ&hl=en", "Google Scholar") + " · " +
        link("https://www.linkedin.com/in/francis-xiatian-zhang/", "LinkedIn"), "small"
    ),
    section("Research Profile"),
    paragraph(
        "Research Associate at the University of Edinburgh working on robot vision for medical robotics. "
        "Research combines geometric modelling and deep learning for robotic bronchoscopy, with an emphasis "
        "on depth estimation, visual odometry, airway segmentation, and reliable visual navigation."
    ),
    section("Research and Teaching Experience"),
    entry("Nov 2024–present", "Research Associate · University of Edinburgh",
          "Develops visual navigation and perception systems for robotic bronchoscopy, including airway "
          "segmentation, geometric graph construction, and failure diagnosis. PI: Dr Mohsen Khadem."),
    entry("Oct–Nov 2023;<br/>Jul–Sep 2024", "Research Assistant · Durham University",
          "Contributed to the Edge Computing and Analytics 2.0 course, teaching model training, ONNX export, "
          "and deployment through Python APIs. PI: Dr Anish Jindal."),
    entry("Nov 2021–Jun 2024", "Demonstrator · Durham University",
          "Supported laboratory teaching in Computational Thinking, Data Science, Programming for Data "
          "Science, and Text Mining."),
    entry("Apr–Jul 2022", "Research Assistant · Northumbria University",
          "Developed multi-camera data collection and pose-based models for automatic assessment of CPR "
          "skills in nursing simulation. PI: Dr Merryn Constable."),
    section("Education"),
    entry("2025", "PhD · Durham University", "Geometric representations for clinical video analysis."),
    entry("", "MRes · King's College London"),
    entry("", "MSc · University of Southampton"),
    entry("", "Bachelor's degree · Beijing University of Chinese Medicine"),
    section("Awards"),
    entry("2026", "ICRA Best Paper Award in Medical Robotics",
          "Co-author of " + link("https://arxiv.org/abs/2607.05162",
          "Geometry-Aware Visual Odometry for Bronchoscopic Navigation via High-Gain Observer Fusion") + "."),
    entry("2020", "Dean's List Award for Outstanding Achievement", "University of Southampton."),
    PageBreak(),
    section("Selected Publications"),
    paragraph("Selected work in robotics, computer vision, and biomedical engineering. Full publication list: " +
              link("https://scholar.google.com/citations?user=R04bvhAAAAAJ&hl=en", "Google Scholar") + ".", "small"),
]

# Pull titles, authors, years, and verified links from the website to avoid duplicate metadata.
html = (ROOT / "index.html").read_text()
research = html.split('id="publications">', 1)[1].split('<!-- The Awards Section -->', 1)[0]
publications = re.findall(r'<li data-year="(\d+)" data-venue="([^"]+)"[^>]*>(.*?)</li>', research, re.S)
assert len(publications) == 13, "Review publication extraction after editing the website structure."
number = 0
for year, venue, content in publications:
    if venue in {"BMC Psychiatry", "Advances in Health Sciences Education"}:
        continue
    title = unescape(re.search(r"<strong>(.*?)</strong>", content, re.S).group(1))
    authors = unescape(re.sub(r"<[^>]+>", "", re.split(r"<br\s*/?>", content)[1])).strip()
    authors = escape(authors).replace("Francis Xiatian Zhang", "<b>Francis Xiatian Zhang</b>")
    links = re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', content, re.S)
    resources = " · ".join(link(unescape(url), unescape(label)) for url, label in links)
    number += 1
    item = (
        f"<b>{number}. {escape(title)}</b><br/>"
        f"{authors}<br/>"
        f'<font color="#596570">{escape(venue)} {year}</font> · {resources}'
    )
    if title.startswith("Geometry-Aware Visual Odometry"):
        item += '<br/><font color="#315f9c">Best Paper Award in Medical Robotics, ICRA 2026</font>'
    story.append(KeepTogether([paragraph(item, "publication")]))
assert number == 11

doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4,
    rightMargin=42, leftMargin=42, topMargin=43, bottomMargin=49,
    title="Francis Xiatian Zhang — Curriculum Vitae", author="Francis Xiatian Zhang",
    subject="Robot vision, medical robotics, and computer vision", pageCompression=1,
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
