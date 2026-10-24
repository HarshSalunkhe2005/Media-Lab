"""Carousel cover: one promise in sentence case over a real photo, top-left in the calm area, '1/7' cue."""
from pathlib import Path

from PIL import ImageDraw

from lib import film, fit, font, photo, save_jpg, shade, text_block, wrap

W, H = 1080, 1350


def render(out: Path) -> Path:
    img = shade(film(fit(photo("desk"), W, H, fx=0.4), warmth=0.4, grain=0.04), "top", strength=190, start=0.5)
    d = ImageDraw.Draw(img)
    f = font("sans-bold", 84)
    lines = wrap("Five checks before you post any Reel", f, 820)
    text_block(d, (90, 120), lines, f, (250, 248, 244), 1.12)
    d.text((90, H - 110), "1/7  →", font=font("sans", 34), fill=(250, 248, 244))
    return save_jpg(img, out / "carousel-cover-promise.jpg")
