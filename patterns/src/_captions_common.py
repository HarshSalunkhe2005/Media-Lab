"""Shared by the caption-style patterns: burn an ASS file onto one photo frame and save it as the preview."""
import sys
import tempfile
from pathlib import Path

from lib import PHOTOS, SCRIPTS, ffmpeg

sys.path.insert(0, str(SCRIPTS))
from captions import build  # noqa: E402

WORDS = [{"word": w, "start": i * 0.3, "end": i * 0.3 + 0.3} for i, w in enumerate("half the dates were wrong".split())]


def burn(ass_text: str, out: Path, photo: str = "street", at: float = 0.45) -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "c.ass").write_text(ass_text, encoding="utf-8")
        ffmpeg("-loop", "1", "-i", str(PHOTOS / f"{photo}.jpg"), "-t", "2",
               "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=brightness=-0.12,subtitles=c.ass",
               "-pix_fmt", "yuv420p", "v.mp4", cwd=t)
        ffmpeg("-ss", str(at), "-i", "v.mp4", "-frames:v", "1", "-vf", "scale=405:-1", str(out.resolve()), cwd=t)
    return out


def default_ass(**kw) -> str:
    args = dict(font="Arial", size=84, chunk=3, y=1320, color="&H00FFFFFF", highlight="&H0000E5FF", upper=True)
    args.update(kw)
    return build(WORDS, args["font"], args["size"], args["chunk"], args["y"], args["color"], args["highlight"], args["upper"])
