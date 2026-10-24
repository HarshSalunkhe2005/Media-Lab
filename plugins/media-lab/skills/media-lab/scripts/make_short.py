"""End-to-end Short with free tools: script -> edge-tts voice (word timings) -> 9:16 visuals -> burned captions.

Usage:
  python make_short.py script.txt out_dir [--voice en-US-GuyNeural] [--images a.jpg b.jpg ...]
script.txt: one beat per line; line 1 is the hook (also shown as on-screen title for the first 2 s).
No --images: each beat gets a dark gradient card, so it runs with zero assets.
Needs: pip install edge-tts ; ffmpeg on PATH ; internet for edge-tts (free Microsoft voices, no key).
Outputs in out_dir: voice.mp3, words.json, captions.ass, short.mp4
"""
import argparse
import asyncio
import json
import subprocess
import sys
import textwrap
from pathlib import Path

import edge_tts

sys.path.insert(0, str(Path(__file__).parent))
from captions import build  # noqa: E402

W, H, FPS = 1080, 1920, 30


async def tts(text: str, voice: str, mp3: Path) -> list[dict]:
    words = []
    com = edge_tts.Communicate(text, voice, rate="+8%", boundary="WordBoundary")
    with open(mp3, "wb") as f:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                s = chunk["offset"] / 1e7
                words.append({"word": chunk["text"], "start": s, "end": s + chunk["duration"] / 1e7})
    return words


def run(args: list[str], cwd: Path) -> None:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], cwd=cwd, check=True)


def beat_times(beats: list[str], words: list[dict], total: float) -> list[float]:
    """Start time of each beat, found by counting words."""
    starts, i = [], 0
    for b in beats:
        starts.append(words[min(i, len(words) - 1)]["start"] if words else 0)
        i += len(b.split())
    starts[0] = 0.0
    return starts + [total]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out")
    ap.add_argument("--voice", default="en-US-GuyNeural")
    ap.add_argument("--images", nargs="*", default=[])
    ap.add_argument("--font", default=r"C\:/Windows/Fonts/arialbd.ttf", help="font file for the hook title (escape the drive colon)")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    beats = [l.strip() for l in Path(a.script).read_text(encoding="utf-8").splitlines() if l.strip()]
    words = asyncio.run(tts(" ".join(beats), a.voice, out / "voice.mp3"))
    (out / "words.json").write_text(json.dumps(words, indent=1), encoding="utf-8")
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                  str(out / "voice.mp3")], capture_output=True, text=True).stdout) + 0.4
    times = beat_times(beats, words, total)

    parts = []
    for n, b in enumerate(beats):
        dur = max(times[n + 1] - times[n], 0.5)
        seg = f"seg{n:02d}.mp4"
        if n < len(a.images):
            img = Path(a.images[n]).resolve().as_posix()
            vf = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
                  f"zoompan=z='min(zoom+0.0010,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(dur*FPS)}:s={W}x{H}:fps={FPS}")
            run(["-loop", "1", "-i", img, "-t", f"{dur:.3f}", "-vf", vf, "-pix_fmt", "yuv420p", seg], out)
        else:
            hue = (n * 47) % 360
            src = f"gradients=s={W}x{H}:c0=0x101014:c1=0x2a2a40:x0=0:y0=0:x1={W}:y1={H}:d={dur:.3f}:r={FPS}"
            run(["-f", "lavfi", "-i", src, "-vf", f"hue=h={hue}", "-pix_fmt", "yuv420p", seg], out)
        parts.append(seg)
    (out / "list.txt").write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
    run(["-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "visual.mp4"], out)

    (out / "captions.ass").write_text(build(words, "Arial", 84, 3, 1320, "&H00FFFFFF", "&H0000E5FF"), encoding="utf-8")
    # hook title for the first 2.2 s: wrapped to fit the safe zone, real font file (no fontconfig on Windows)
    # one drawtext per line: multi-line textfile draws a box glyph at each line break in ffmpeg 8 on Windows
    lines = textwrap.wrap(beats[0].upper(), 20)
    for i, line in enumerate(lines):
        (out / f"hook{i}.txt").write_text(line, encoding="utf-8")
    title = ",".join(
        f"drawtext=textfile=hook{i}.txt:fontfile='{a.font}':fontcolor=white:fontsize=72:box=1:boxcolor=black@0.6:"
        f"boxborderw=18:x=(w-text_w)/2:y={330 + i * 100}:enable='lt(t,2.2)'" for i in range(len(lines)))
    run(["-i", "visual.mp4", "-i", "voice.mp3", "-filter_complex",
         f"[0:v]subtitles=captions.ass,{title}[v];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac",
         "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", "short.mp4"], out)
    for p in parts:
        (out / p).unlink()
    print(f"wrote {out / 'short.mp4'} ({total:.1f}s, {len(words)} words, {len(beats)} beats)")


if __name__ == "__main__":
    main()
