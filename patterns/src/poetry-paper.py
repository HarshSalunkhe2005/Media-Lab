"""Poetry slide on warm paper: no photo, generous margins, one serif, a short stanza set with its own line breaks."""
from pathlib import Path

from PIL import ImageDraw

from lib import font, paper, save_jpg

W, H = 1080, 1350
STANZA = ["You left the radio", "on the wrong station,", "and I kept it there", "for a whole winter."]  # fictional


def render(out: Path) -> Path:
    img = paper(W, H)
    d = ImageDraw.Draw(img)
    f = font("serif", 56)
    y = 470
    for ln in STANZA:
        d.text((150, y), ln, font=f, fill=(38, 34, 30))
        y += 82
    d.text((150, y + 60), "from a notebook, page 12", font=font("serif", 30), fill=(120, 112, 100))
    d.text((W - 110, 100), "5/9", font=font("serif", 28), fill=(120, 112, 100), anchor="ra")
    return save_jpg(img, out / "poetry-paper.jpg")
