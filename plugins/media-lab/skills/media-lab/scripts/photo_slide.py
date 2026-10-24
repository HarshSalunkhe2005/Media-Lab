"""Real photo -> 4:5 slide with text in its negative space. Darkens only the text area, no glows or ornaments.

Usage: python photo_slide.py photo.jpg "Text, in sentence case." out.png [--where top|bottom] [--font path.ttf] [--focus 0.5]
--focus: horizontal centre of the crop (0 = left edge, 1 = right edge) so the subject stays in frame.
Needs: pip install pillow
"""
import argparse
import textwrap

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1350


def crop_45(im: Image.Image, focus: float) -> Image.Image:
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - W) * min(max(focus, 0), 1))
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("text")
    ap.add_argument("out")
    ap.add_argument("--where", choices=["top", "bottom"], default="bottom")
    ap.add_argument("--font", default="C:/Windows/Fonts/georgia.ttf")
    ap.add_argument("--size", type=int, default=54)
    ap.add_argument("--focus", type=float, default=0.5)
    a = ap.parse_args()

    im = crop_45(Image.open(a.photo).convert("RGB"), a.focus)
    font = ImageFont.truetype(a.font, a.size)
    width = 30
    lines = textwrap.wrap(a.text, width)
    while len(lines) > 1 and len(lines[-1].split()) == 1 and width > 18:  # no single-word last line
        width -= 2
        lines = textwrap.wrap(a.text, width)
    lh = round(a.size * 1.35)
    block = lh * len(lines)
    pad = 90
    y0 = pad if a.where == "top" else H - pad - block

    # darken a soft band behind the text only: a vertical gradient, strongest under the text
    band = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(band)
    top, bot = max(y0 - 160, 0), min(y0 + block + 160, H)
    for y in range(top, bot):
        edge = min(y - top, bot - y) / 160
        d.line([(0, y), (W, y)], fill=round(120 * min(edge, 1)))
    band = band.filter(ImageFilter.GaussianBlur(30))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, band)

    draw = ImageDraw.Draw(im)
    for i, line in enumerate(lines):
        draw.text((pad, y0 + i * lh), line, font=font, fill=(245, 242, 236))
    im.save(a.out, quality=92)
    print(f"wrote {a.out} ({W}x{H}, {len(lines)} lines, text {a.where})")


if __name__ == "__main__":
    main()
