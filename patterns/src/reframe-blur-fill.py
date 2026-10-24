"""Landscape footage into 9:16 with a blurred, darkened copy behind it. Use when the panels look too empty."""
import importlib.util
import tempfile
from pathlib import Path

from lib import ffmpeg

_spec = importlib.util.spec_from_file_location("panels", Path(__file__).with_name("reframe-dark-panels.py"))
panels = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(panels)

BLUR = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24:2,eq=brightness=-0.08[bg];"
        "[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,scale=360:640")


def render(out: Path) -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        src = panels.landscape_clip(Path(tmp))
        dst = out / "reframe-blur-fill.mp4"
        ffmpeg("-i", str(src), "-filter_complex", BLUR, "-c:v", "libx264", "-crf", "30", "-an", "-movflags", "+faststart", str(dst))
    return dst
