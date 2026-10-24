"""List carousel middle slide: number, short headline, two lines of support, same layout every slide."""
from pathlib import Path

from PIL import ImageDraw

from lib import font, paper, save_jpg, text_block, wrap

W, H = 1080, 1350
INK = (28, 28, 30)


def render(out: Path) -> Path:
    img = paper(W, H, (236, 240, 236))
    d = ImageDraw.Draw(img)
    d.text((90, 140), "02", font=font("condensed", 150), fill=(46, 104, 82))
    fh = font("sans-bold", 72)
    y = text_block(d, (90, 380), wrap("Say the hook out loud", fh, 860), fh, INK, 1.12)
    fb = font("sans", 44)
    text_block(d, (90, y + 40), wrap("If it takes longer than two seconds to say, it is too long. Cut words until it does not.", fb, 860), fb, (70, 70, 72), 1.35)
    d.text((W - 90, H - 110), "@pebbleclub", font=font("sans", 30), fill=(110, 110, 110), anchor="ra")
    return save_jpg(img, out / "list-point-slide.jpg")
