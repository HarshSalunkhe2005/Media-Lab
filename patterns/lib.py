"""Shared helpers for pattern renderers. Thin layer over the skill's medialab package (Pillow + ffmpeg only).

Every pattern in patterns/src/<slug>.py exposes render(out_dir: Path) -> Path. Older patterns draw by hand with
these helpers; newer ones are a spec passed to medialab.make.build, the same thing the CLI runs, so every such
pattern is also a working `medialab make` example.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHOTOS = ROOT / "assets" / "photos"
SCRIPTS = ROOT.parent / "plugins" / "media-lab" / "skills" / "media-lab" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from medialab.core import (blur, circle, contrast_ratio, ffmpeg, film, fit, fit_text, font, font_path,  # noqa: E402,F401
                           paper, rgb, save, save_jpg, shade, text_block, wrap)
from medialab.make import build  # noqa: E402


def photo(name: str):
    from PIL import Image
    return Image.open(PHOTOS / f"{name}.jpg").convert("RGB")


def ph(name: str) -> str:
    """Path to a bundled CC0 photo, for specs."""
    return str(PHOTOS / f"{name}.jpg")


def from_spec(slug: str, spec: dict, out: Path) -> Path:
    """Render a spec as this pattern's gallery preview (.jpg for stills, small .mp4 for video)."""
    from medialab import video
    ext = "mp4" if spec["kind"] in video.KINDS else "jpg"
    return build(spec, out / f"{slug}.{ext}", preview=True)[0]
