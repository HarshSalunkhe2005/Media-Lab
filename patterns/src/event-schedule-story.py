"""Daily schedule story (9:16): plain table of fixtures inside the safe zone, from a data list. Fictional teams."""
from pathlib import Path

from PIL import ImageDraw

from lib import film, fit, font, photo, save_jpg

W, H = 1080, 1920
FIXTURES = [("4:30", "Ridgeway", "Northfield"), ("4:50", "Harbour FC", "Kestrel"), ("5:10", "Lowmoor", "Ridgeway"),
            ("5:30", "Northfield", "Harbour FC"), ("5:50", "Kestrel", "Lowmoor")]


def render(out: Path) -> Path:
    img = film(fit(photo("courtaerial"), W, H, fx=0.5), warmth=0.2).point(lambda v: int(v * 0.35))
    d = ImageDraw.Draw(img)
    d.text((90, 300), "Day 2", font=font("condensed", 120), fill=(250, 248, 244))
    d.text((90, 440), "Saturday · Court A", font=font("sans", 40), fill=(210, 206, 198))
    fs, fb = font("sans", 44), font("sans-bold", 44)
    y = 600
    for t, a, b in FIXTURES:
        d.line((90, y - 24, W - 90, y - 24), fill=(90, 90, 92), width=2)
        d.text((90, y), t, font=fs, fill=(210, 206, 198))
        d.text((240, y), a, font=fb, fill=(250, 248, 244))
        d.text((640, y), "vs", font=fs, fill=(150, 150, 150), anchor="ma")
        d.text((W - 90, y), b, font=fb, fill=(250, 248, 244), anchor="ra")
        y += 120
    d.text((90, 1440), "Standings after every match: link in bio", font=font("sans", 34), fill=(200, 196, 188))
    return save_jpg(img, out / "event-schedule-story.jpg", preview_width=405)
