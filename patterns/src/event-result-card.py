"""Match result card (4:5): real court photo, score as the hero, both teams, one moment, next fixture. Fictional teams."""
from pathlib import Path

from PIL import ImageDraw

from lib import film, fit, font, photo, save_jpg, shade

W, H = 1080, 1350
WHITE, DIM = (250, 248, 244), (205, 202, 196)


def render(out: Path) -> Path:
    img = shade(film(fit(photo("courtaerial"), W, H, fx=0.5), warmth=0.3), "bottom", strength=225, start=0.3)
    d = ImageDraw.Draw(img)
    d.text((90, 110), "FINAL  ·  DAY 3", font=font("sans-bold", 34), fill=WHITE)
    d.text((90, 690), "Ridgeway", font=font("sans-bold", 64), fill=WHITE)
    d.text((W - 90, 690), "Northfield", font=font("sans-bold", 64), fill=DIM, anchor="ra")
    d.text((W // 2, 800), "3 – 2", font=font("condensed", 230), fill=WHITE, anchor="ma")
    d.text((90, 1110), "Saved two match points in set five.", font=font("sans", 40), fill=WHITE)
    d.text((90, 1170), "Next: semi-final, Sunday 5:45 PM", font=font("sans", 34), fill=DIM)
    return save_jpg(img, out / "event-result-card.jpg")
