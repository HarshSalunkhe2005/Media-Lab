"""Data-story slide: one earned giant number, one plain line saying what it means, source in small type."""
from pathlib import Path

from PIL import ImageDraw

from lib import font, paper, save_jpg, text_block, wrap

W, H = 1080, 1350
INK, ACCENT = (24, 24, 26), (196, 64, 38)


def render(out: Path) -> Path:
    img = paper(W, H, (246, 244, 240))
    d = ImageDraw.Draw(img)
    d.line((90, 160, W - 90, 160), fill=INK, width=3)
    d.text((90, 190), "Pebble Club fest, 2026", font=font("sans", 32), fill=INK)
    d.text((80, 360), "730", font=font("condensed", 330), fill=ACCENT)
    f = font("sans", 52)
    text_block(d, (90, 760), wrap("photos and clips from three days, sorted by when they were really taken.", f, 880), f, INK, 1.25)
    d.text((90, H - 120), "Source: club media folder count (fictional demo data)", font=font("sans", 26), fill=(110, 110, 110))
    return save_jpg(img, out / "data-story-number.jpg")
