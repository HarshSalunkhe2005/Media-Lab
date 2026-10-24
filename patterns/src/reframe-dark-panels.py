"""Landscape footage into 9:16 with dark panels (reads less 'edited' than blur). Footage here is a slow pan over a CC0 photo."""
import tempfile
from pathlib import Path

from lib import PHOTOS, ffmpeg

PAN = "scale=2400:-2,crop=1920:1080:x='(iw-1920)*t/5':y='(ih-1080)/2'"


def landscape_clip(tmp: Path) -> Path:
    src = tmp / "landscape.mp4"
    ffmpeg("-loop", "1", "-i", str(PHOTOS / "street.jpg"), "-t", "5", "-vf", PAN + ",fps=30", "-pix_fmt", "yuv420p", str(src))
    return src


def render(out: Path) -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        src = landscape_clip(Path(tmp))
        dst = out / "reframe-dark-panels.mp4"
        ffmpeg("-i", str(src), "-vf", "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x0d0d0f,scale=360:640",
               "-c:v", "libx264", "-crf", "30", "-an", "-movflags", "+faststart", str(dst))
    return dst
