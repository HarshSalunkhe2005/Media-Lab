"""On-video hook title (first 2 s of a Short): result-first line, wrapped by hand, one box per line, upper safe zone."""
from pathlib import Path

from PIL import ImageDraw

from lib import film, fit, font, photo, save_jpg

W, H = 1080, 1920
LINES = ["THIS STREET SELLS", "212 KINDS OF", "NOODLES"]  # fictional claim for the demo


def render(out: Path) -> Path:
    img = film(fit(photo("street"), W, H, fx=0.5), warmth=0.2, grain=0.04)
    d = ImageDraw.Draw(img)
    f = font("sans-bold", 76)
    y = 330
    for ln in LINES:
        x0, y0, x1, y1 = d.textbbox((W // 2, y), ln, font=f, anchor="ma")
        d.rectangle((x0 - 22, y0 - 14, x1 + 22, y1 + 14), fill=(0, 0, 0))
        d.text((W // 2, y), ln, font=f, fill=(255, 255, 255), anchor="ma")
        y += 112
    return save_jpg(img, out / "hook-title-card.jpg", preview_width=405)
