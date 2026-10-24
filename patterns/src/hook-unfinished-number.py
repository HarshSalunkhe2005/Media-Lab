"""Unfinished-number hook: a countdown promise on screen, a small number badge, minimal outlined text."""
from pathlib import Path

from PIL import ImageDraw

from lib import film, fit, font, photo, save_jpg

W, H = 1080, 1920
LINES = ["ffmpeg flags I use daily.", "The last one saved", "a whole edit."]


def render(out: Path) -> Path:
    img = film(fit(photo("desk"), W, H, fx=0.45), warmth=0.3)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((90, 300, 250, 460), 24, fill=(255, 214, 64))
    d.text((170, 380), "4", font=font("condensed", 130), fill=(20, 20, 20), anchor="mm")
    f = font("sans-bold", 70)
    for i, ln in enumerate(LINES):
        d.text((90, 520 + i * 92), ln, font=f, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    return save_jpg(img, out / "hook-unfinished-number.jpg", preview_width=405)
