"""LinkedIn document: a carousel spec rendered to slides plus one multi-page PDF (upload the PDF as a document).
The preview fans out the first three pages; the PDF itself is written next to it in a temp folder and checked."""
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

from lib import build, ph, save_jpg

SPEC = {
    "kind": "carousel", "theme": "data-story", "size": "linkedin", "pdf": True, "handle": "Tidewater Research (fictional)",
    "slides": [
        {"kind": "cover", "kicker": "Reader panel, winter", "title": "What 212 readers told us about carousels", "photo": ph("desk"), "focus": [0.5, 0.4]},
        {"kind": "number", "value": "64%", "caption": "made it past slide 1. Slide 2 is where most of the set is decided.", "source": "Tidewater panel, n=212 (fictional data)"},
        {"kind": "bars", "title": "Where they stopped", "data": [["Slide 1", 100], ["Slide 2", 64], ["Slide 5", 38], ["Last", 29]], "highlight": "Slide 2", "fmt": "{}%"},
        {"kind": "cta", "ask": "Get the full report as a PDF", "why": "Link in the first comment"},
    ],
}


def render(out: Path) -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        paths = build(SPEC, Path(tmp) / "doc")
        pdf = [p for p in paths if p.suffix == ".pdf"][0]
        assert pdf.read_bytes()[:5] == b"%PDF-", "PDF export failed"
        pages = [Image.open(p).convert("RGB") for p in paths[:3]]
    W, H = 1600, 1200
    sheet = Image.new("RGB", (W, H), (226, 229, 234))
    s = 0.62
    for i, pg in enumerate(reversed(pages)):
        pg = pg.resize((int(pg.width * s), int(pg.height * s)), Image.LANCZOS)
        x = 120 + (2 - i) * 400
        y = 180 - (2 - i) * 30
        ImageDraw.Draw(sheet).rectangle((x + 14, y + 18, x + pg.width + 14, y + pg.height + 18), fill=(190, 194, 202))
        sheet.paste(pg, (x, y))
    return save_jpg(sheet, out / "linkedin-document.jpg", preview_width=640)
