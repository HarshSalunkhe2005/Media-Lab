"""Faceless Short from a script with zero assets: edge-tts voice, word-highlight captions, hook title. Runs scripts/make_short.py."""
import subprocess
import sys
import tempfile
from pathlib import Path

from lib import SCRIPTS, ffmpeg

SCRIPT = """This app sorted 600 event photos in one night.
Pebble Club shot a three day fest on five different phones.
Half the dates were wrong, because messaging apps strip the camera time."""  # fictional club


def render(out: Path) -> Path:
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "script.txt").write_text(SCRIPT, encoding="utf-8")
        subprocess.run([sys.executable, str(SCRIPTS / "make_short.py"), str(t / "script.txt"), str(t / "job")], check=True)
        dst = out / "short-word-captions.mp4"
        ffmpeg("-i", str(t / "job" / "short.mp4"), "-t", "8", "-vf", "scale=360:640", "-c:v", "libx264", "-crf", "30",
               "-preset", "slow", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", str(dst))
    return dst
