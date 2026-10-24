"""Thumbnail built on one number: huge numeral, a small context word, real photo behind, readable at 160 px."""
from pathlib import Path

from PIL import ImageDraw, ImageEnhance

from lib import fit, font, photo, save_jpg

W, H = 1280, 720


def render(out: Path) -> Path:
    img = ImageEnhance.Brightness(fit(photo("desk"), W, H, fx=0.5, fy=0.4)).enhance(0.55)
    d = ImageDraw.Draw(img)
    d.text((70, 40), "212", font=font("condensed", 420), fill=(255, 255, 255))
    d.text((80, 520), "duplicates", font=font("sans-bold", 80), fill=(255, 214, 64))
    return save_jpg(img, out / "thumb-big-number.jpg", preview_width=640)
