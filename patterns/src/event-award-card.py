"""Player award card: photo with the subject uncropped, award name small, player name big, one real stat. Fictional player."""
from pathlib import Path

from PIL import ImageDraw

from lib import film, fit, font, photo, save_jpg, shade

W, H = 1080, 1350


def render(out: Path) -> Path:
    img = shade(film(fit(photo("player"), W, H, fx=0.5, fy=0.2)), "bottom", strength=230, start=0.4)
    d = ImageDraw.Draw(img)
    d.text((90, 960), "Best Setter", font=font("sans", 40), fill=(220, 214, 200))
    d.text((90, 1010), "Kavya Rao", font=font("sans-bold", 104), fill=(250, 248, 244))
    d.text((90, 1150), "Harbour FC  ·  41 assists across the league", font=font("sans", 36), fill=(220, 214, 200))
    return save_jpg(img, out / "event-award-card.jpg")
