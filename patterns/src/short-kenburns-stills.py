"""Short from real stills: one CC0 photo per beat with a slow Ken Burns push, voice and captions on top. Runs make_short.py --images."""
import subprocess
import sys
import tempfile
from pathlib import Path

from lib import PHOTOS, SCRIPTS, ffmpeg

SCRIPT = """Rain on the window, and the tea goes cold.
The street outside is still awake at midnight.
And the leaves on the step say it is October."""  # fictional


def render(out: Path) -> Path:
    imgs = [str(PHOTOS / f"{n}.jpg") for n in ("rain", "street", "leaves")]
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "script.txt").write_text(SCRIPT, encoding="utf-8")
        subprocess.run([sys.executable, str(SCRIPTS / "make_short.py"), str(t / "script.txt"), str(t / "job"),
                        "--voice", "en-GB-SoniaNeural", "--images", *imgs], check=True)
        dst = out / "short-kenburns-stills.mp4"
        ffmpeg("-i", str(t / "job" / "short.mp4"), "-t", "9", "-vf", "scale=360:640", "-c:v", "libx264", "-crf", "30",
               "-preset", "slow", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", str(dst))
    return dst
