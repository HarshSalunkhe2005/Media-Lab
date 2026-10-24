"""Last carousel slide: one clear ask tied to the goal (save / send), photo continues the set's look."""
from pathlib import Path

from PIL import ImageDraw

from lib import film, fit, font, photo, save_jpg, shade, text_block, wrap

W, H = 1080, 1350


def render(out: Path) -> Path:
    img = shade(film(fit(photo("leaves"), W, H), grain=0.05), "bottom", strength=215, start=0.35)
    d = ImageDraw.Draw(img)
    f = font("sans-bold", 76)
    y = text_block(d, (90, 820), wrap("Save this for your next upload.", f, 880), f, (250, 248, 244), 1.12)
    fs = font("sans", 40)
    text_block(d, (90, y + 30), wrap("Send it to the friend who posts at 2 AM.", fs, 880), fs, (225, 222, 214), 1.3)
    return save_jpg(img, out / "cta-last-slide.jpg")
