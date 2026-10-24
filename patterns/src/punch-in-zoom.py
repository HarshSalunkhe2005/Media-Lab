"""Punch-in on emphasis: jump to 110% for two seconds, then back. Fixed pixel sizes so the crop always fits."""
import tempfile
from pathlib import Path

from lib import PHOTOS, ffmpeg

ZOOM = "scale=w='if(between(t,1.5,3),1188,1080)':h='if(between(t,1.5,3),2112,1920)':eval=frame,crop=1080:1920,scale=360:640"


def render(out: Path) -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        v = Path(tmp) / "v.mp4"
        ffmpeg("-loop", "1", "-i", str(PHOTOS / "desk.jpg"), "-t", "4.5",
               "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30", "-pix_fmt", "yuv420p", str(v))
        dst = out / "punch-in-zoom.mp4"
        ffmpeg("-i", str(v), "-vf", ZOOM, "-c:v", "libx264", "-crf", "30", "-an", "-movflags", "+faststart", str(dst))
    return dst
