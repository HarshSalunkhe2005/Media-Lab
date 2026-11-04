"""Shared drawing helpers for Media Lab. Pillow + ffmpeg only.

Fonts are bundled (SIL OFL, assets/fonts/), so output looks the same on Windows, macOS, Linux and CI.
Everything here is plain functions: no global state, no network.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

SKILL = Path(__file__).resolve().parents[2]
FONT_DIR = SKILL / "assets" / "fonts"

# kind -> bundled file. Old kinds (serif, sans, sans-bold, condensed) keep their meaning.
FONTS = {
    "serif": "eb-garamond-latin-400-normal.woff",
    "serif-italic": "eb-garamond-latin-400-italic.woff",
    "serif-bold": "eb-garamond-latin-700-normal.woff",
    "sans": "inter-latin-400-normal.woff",
    "sans-ext": "inter-latin-ext-400-normal.woff",  # currency and accented extras (₹, ₺, ł ...), no basic latin
    "sans-semibold": "inter-latin-600-normal.woff",
    "sans-bold": "inter-latin-800-normal.woff",
    "sans-black": "inter-latin-900-normal.woff",
    "condensed": "oswald-latin-700-normal.woff",
    "condensed-medium": "oswald-latin-500-normal.woff",
    "mono": "jetbrains-mono-latin-400-normal.woff",
    "mono-bold": "jetbrains-mono-latin-700-normal.woff",
    "display": "archivo-black-latin-400-normal.woff",
    "display-serif": "dm-serif-display-latin-400-normal.woff",
    "display-serif-italic": "dm-serif-display-latin-400-italic.woff",
}

_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font_path(kind: str) -> str:
    """A bundled kind name, or a path to any .ttf/.otf/.woff file."""
    if kind in FONTS:
        return str(FONT_DIR / FONTS[kind])
    if Path(kind).exists():
        return kind
    raise KeyError(f"unknown font {kind!r}; use one of {', '.join(FONTS)} or a font file path")


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    key = (kind, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(font_path(kind), size)
    return _cache[key]


def rgb(c) -> tuple[int, int, int]:
    """'#1a2b3c', '1a2b3c' or (r, g, b) -> (r, g, b)."""
    if isinstance(c, str):
        c = c.lstrip("#")
        return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
    return tuple(c)  # type: ignore[return-value]


def fit(img: Image.Image, w: int, h: int, fx: float = 0.5, fy: float = 0.5) -> Image.Image:
    """Cover-crop to w x h; fx/fy pick the focus (0 = left/top, 1 = right/bottom)."""
    return ImageOps.fit(img, (w, h), method=Image.LANCZOS, centering=(fx, fy))


def film(img: Image.Image, warmth: float = 1.0, grain: float = 0.06) -> Image.Image:
    """One muted film grade: lower saturation, softer contrast, slight warm cast, fine grain."""
    img = ImageEnhance.Contrast(ImageEnhance.Color(img).enhance(0.55)).enhance(0.92)
    r, g, b = img.split()
    r = r.point(lambda v: min(255, int(v * (1 + 0.03 * warmth) + 6 * warmth)))
    b = b.point(lambda v: int(v * (1 - 0.05 * warmth) + 4))
    img = Image.merge("RGB", (r, g, b))
    return Image.blend(img, Image.effect_noise(img.size, 30).convert("RGB"), grain)


def duotone(img: Image.Image, dark, light) -> Image.Image:
    """Map the photo's luminance between two colours (print-poster look)."""
    return ImageOps.colorize(ImageOps.grayscale(img), rgb(dark), rgb(light))


def halftone(img: Image.Image, cell: int = 10, ink=(20, 20, 20), paper_tone=(240, 235, 225)) -> Image.Image:
    """Dot halftone of the photo's luminance, for retro-print worlds."""
    g = ImageOps.grayscale(img)
    out = Image.new("RGB", img.size, rgb(paper_tone))
    d = ImageDraw.Draw(out)
    small = g.resize((max(1, img.width // cell), max(1, img.height // cell)), Image.BOX)
    for y in range(small.height):
        for x in range(small.width):
            r = (1 - small.getpixel((x, y)) / 255) * cell * 0.62
            if r > 0.4:
                cx, cy = x * cell + cell / 2, y * cell + cell / 2
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgb(ink))
    return out


def shade(img: Image.Image, where: str = "bottom", strength: int = 200, start: float = 0.45) -> Image.Image:
    """Darken only toward the text edge, with a smooth ramp; the rest of the photo is untouched."""
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    for y in range(h):
        t = (y - h * start) / (h * (1 - start)) if where == "bottom" else (h * (1 - start) - y) / (h * (1 - start))
        d.line((0, y, w, y), fill=int(max(0.0, min(1.0, t)) ** 1.4 * strength))
    return Image.composite(Image.new("RGB", (w, h), (8, 8, 9)), img, mask)


def blur(img: Image.Image, r: float = 24) -> Image.Image:
    return img.filter(ImageFilter.GaussianBlur(r))


def wrap(text: str, f: ImageFont.FreeTypeFont, width: int) -> list[str]:
    """Pixel-width wrap, then narrow until the line count would grow (balanced lines, no lonely last word).
    Explicit newlines in text are kept as line breaks."""
    if "\n" in text:
        return [ln for part in text.split("\n") for ln in (wrap(part, f, width) if part.strip() else [""])]

    def go(wd):
        lines, cur = [], ""
        for word in text.split():
            t = (cur + " " + word).strip()
            if f.getlength(t) > wd and cur:
                lines.append(cur)
                cur = word
            else:
                cur = t
        return lines + [cur]
    n, wd = len(go(width)), width
    while wd > 200 and len(go(wd - 10)) == n:
        wd -= 10
    return go(wd)


def fit_text(text: str, kind: str, width: int, max_lines: int, start: int, floor: int = 24):
    """Largest size (from start down) where text wraps into at most max_lines. Returns (font, lines)."""
    size = start
    while size > floor:
        f = font(kind, size)
        lines = wrap(text, f, width)
        if len(lines) <= max_lines and all(f.getlength(ln) <= width for ln in lines):
            return f, lines
        size -= 4
    f = font(kind, floor)
    return f, wrap(text, f, width)


def text_block(d: ImageDraw.ImageDraw, xy, lines, f, fill, leading=1.3, anchor="la"):
    """Draw lines from xy; returns the y below the last line."""
    x, y = xy
    lh = int(f.size * leading)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill, anchor=anchor)
        y += lh
    return y


def block_height(lines, f, leading=1.3) -> int:
    return int(f.size * leading) * len(lines)


def paper(w: int, h: int, tone=(240, 235, 225)) -> Image.Image:
    base = Image.new("RGB", (w, h), rgb(tone))
    return Image.blend(base, Image.effect_noise((w, h), 22).convert("RGB"), 0.05)


def rounded(img: Image.Image, r: int) -> Image.Image:
    """RGBA copy with rounded corners."""
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), r, fill=255)
    out = img.convert("RGBA")
    out.putalpha(m)
    return out


def circle(img: Image.Image, size: int) -> Image.Image:
    """Square-crop to a circle of the given diameter (avatars)."""
    img = fit(img, size, size)
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).ellipse((0, 0, size - 1, size - 1), fill=255)
    out = img.convert("RGBA")
    out.putalpha(m)
    return out


def ffmpeg(*args: str, cwd: Path | None = None) -> None:
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg not found on PATH (https://ffmpeg.org/download.html)")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], cwd=cwd, check=True)


def save(img: Image.Image, out: Path) -> Path:
    """Full-size export. PNG for flat graphics, high-quality JPEG for .jpg."""
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img = img.convert("RGB")
    if out.suffix.lower() in (".jpg", ".jpeg"):
        img.save(out, quality=92, subsampling=0)
    else:
        img.save(out)
    return out


def save_jpg(img: Image.Image, out: Path, preview_width: int = 540) -> Path:
    """Gallery preview: saved at preview_width (patterns render at full size first)."""
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    s = preview_width / img.width
    img.convert("RGB").resize((preview_width, round(img.height * s)), Image.LANCZOS).save(out, quality=86)
    return out


def contrast_ratio(a, b) -> float:
    """WCAG contrast ratio between two colours."""
    def lum(c):
        def ch(v):
            v /= 255
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        r, g, b_ = (ch(x) for x in rgb(c))
        return 0.2126 * r + 0.7152 * g + 0.0722 * b_
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
