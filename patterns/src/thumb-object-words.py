"""YouTube thumbnail: one real object, three words that add what the title does not say, clear of the bottom-right badge."""
from pathlib import Path

from PIL import ImageDraw

from lib import fit, font, photo, save_jpg

W, H = 1280, 720


def render(out: Path) -> Path:
    img = fit(photo("coffee"), W, H, fx=0.5, fy=0.75)
    d = ImageDraw.Draw(img)
    f = font("sans-bold", 118)
    d.text((70, 120), "COLD", font=f, fill=(250, 248, 244), stroke_width=4, stroke_fill=(0, 0, 0))
    d.text((70, 250), "BY 9 AM?", font=f, fill=(255, 214, 64), stroke_width=4, stroke_fill=(0, 0, 0))
    return save_jpg(img, out / "thumb-object-words.jpg", preview_width=640)
