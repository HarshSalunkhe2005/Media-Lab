"""Poetry slide: real CC0 photo, one film grade, plain Garamond in the photo's darkest edge, slide counter."""
from pathlib import Path

from PIL import ImageDraw

from lib import film, fit, font, photo, save_jpg, shade, text_block, wrap

W, H = 1080, 1350
LINES = "The kettle still clicks off at seven. Nobody comes to the window now."  # fictional


def render(out: Path) -> Path:
    img = shade(film(fit(photo("coffee"), W, H, fx=0.5)), "bottom")
    d = ImageDraw.Draw(img)
    f = font("serif", 50)
    lines = wrap(LINES, f, 860)
    y0 = H - 140 - int(f.size * 1.32) * len(lines)
    text_block(d, (110, y0), lines, f, (244, 240, 232), 1.32)
    d.text((W - 110, 100), "3/9", font=font("serif", 28), fill=(220, 214, 204), anchor="ra")
    return save_jpg(img, out / "poetry-film-photo.jpg")
