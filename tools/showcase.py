"""Build public/showcase.jpg: a grid of real pattern previews, for the README and marketplace listings.
Run after re-rendering: python tools/showcase.py"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PREV = ROOT / "public" / "previews"
PICK = ["magazine-cover", "brutalist-statement", "retro-event-poster", "bar-chart-slide", "checklist-slide",
        "event-speaker-card", "story-countdown", "process-steps", "code-card-slide", "cafe-menu-board",
        "poetry-film-photo", "text-post-card"]
COLS, CW, CH, G = 6, 360, 450, 14


def main():
    rows = (len(PICK) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * CW + (COLS + 1) * G, rows * CH + (rows + 1) * G), (24, 24, 27))
    for i, slug in enumerate(PICK):
        with Image.open(PREV / f"{slug}.jpg") as im:
            im = im.convert("RGB")
            s = max(CW / im.width, CH / im.height)
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            x0, y0 = (im.width - CW) // 2, 0
            tile = im.crop((x0, y0, x0 + CW, y0 + CH))
        r, c = divmod(i, COLS)
        sheet.paste(tile, (G + c * (CW + G), G + r * (CH + G)))
    out = ROOT / "public" / "showcase.jpg"
    sheet.save(out, quality=84)
    print(out.relative_to(ROOT), sheet.size)


if __name__ == "__main__":
    main()
