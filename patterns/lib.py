"""Shared helpers for pattern renderers. Pillow + ffmpeg only.

Every pattern in patterns/src/<slug>.py exposes render(out_dir: Path) -> Path and uses these helpers.
"""
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
PHOTOS = ROOT / "assets" / "photos"
SCRIPTS = ROOT.parent / "plugins" / "media-lab" / "skills" / "media-lab" / "scripts"

# System fonts (not redistributed). Windows paths first, then common Linux/macOS fallbacks.
FONTS = {
    "serif": ["C:/Windows/Fonts/GARA.TTF", "/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Regular.ttf",
              "/Library/Fonts/Georgia.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
    "serif-bold": ["C:/Windows/Fonts/GARABD.TTF", "C:/Windows/Fonts/georgiab.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
    "sans": ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    "sans-bold": ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "condensed": ["C:/Windows/Fonts/bahnschrift.ttf", "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"],
}


def font_path(kind: str) -> str:
    for p in FONTS[kind]:
        if Path(p).exists():
            return p
    raise FileNotFoundError(f"no font found for {kind}; edit FONTS in patterns/lib.py")


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(font_path(kind), size)


def photo(name: str) -> Image.Image:
    return Image.open(PHOTOS / f"{name}.jpg").convert("RGB")


def fit(img: Image.Image, w: int, h: int, fx: float = 0.5, fy: float = 0.5) -> Image.Image:
    return ImageOps.fit(img, (w, h), method=Image.LANCZOS, centering=(fx, fy))


def film(img: Image.Image, warmth: float = 1.0, grain: float = 0.06) -> Image.Image:
    """One muted film grade: lower saturation, softer contrast, slight warm cast, fine grain."""
    img = ImageEnhance.Contrast(ImageEnhance.Color(img).enhance(0.55)).enhance(0.92)
    r, g, b = img.split()
    r = r.point(lambda v: min(255, int(v * (1 + 0.03 * warmth) + 6 * warmth)))
    b = b.point(lambda v: int(v * (1 - 0.05 * warmth) + 4))
    img = Image.merge("RGB", (r, g, b))
    return Image.blend(img, Image.effect_noise(img.size, 30).convert("RGB"), grain)


def shade(img: Image.Image, where: str = "bottom", strength: int = 200, start: float = 0.45) -> Image.Image:
    """Darken only toward the text edge, with a smooth ramp; the rest of the photo is untouched."""
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    for y in range(h):
        t = (y - h * start) / (h * (1 - start)) if where == "bottom" else (h * (1 - start) - y) / (h * (1 - start))
        d.line((0, y, w, y), fill=int(max(0.0, min(1.0, t)) ** 1.4 * strength))
    return Image.composite(Image.new("RGB", (w, h), (8, 8, 9)), img, mask)


def wrap(text: str, f: ImageFont.FreeTypeFont, width: int) -> list[str]:
    """Pixel-width wrap, then narrow until the line count would grow (balanced lines, no lonely last word)."""
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


def text_block(d: ImageDraw.ImageDraw, xy, lines, f, fill, leading=1.3, anchor="la"):
    x, y = xy
    lh = int(f.size * leading)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill, anchor=anchor)
        y += lh
    return y


def paper(w: int, h: int, tone=(240, 235, 225)) -> Image.Image:
    base = Image.new("RGB", (w, h), tone)
    return Image.blend(base, Image.effect_noise((w, h), 22).convert("RGB"), 0.05)


def ffmpeg(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], cwd=cwd, check=True)


def save_jpg(img: Image.Image, out: Path, preview_width: int = 540) -> Path:
    """Patterns render at full size; the gallery preview is saved at preview_width."""
    out.parent.mkdir(parents=True, exist_ok=True)
    s = preview_width / img.width
    img.resize((preview_width, round(img.height * s)), Image.LANCZOS).save(out, quality=86)
    return out
