"""Pre-publish checks for an image or video against a platform spec (formats/specs.md).

Measures what a script can measure honestly: canvas, aspect, duration, codec, pixel format, faststart,
loudness and true peak, black or silent openings, detail inside the platform UI zones, and how much
contrast survives at feed size. It does not judge taste: run playbook/critique.md and taste.md for that.

Each check returns PASS, WARN or FAIL with the measured value and the fix.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

# canvas, max seconds (None = still), UI zones as (x0, y0, x1, y1) fractions of the frame
PLATFORMS = {
    "shorts": dict(canvas=(1080, 1920), max_s=180, zones=[(0, 0, 1, 0.13, "top bar"), (0, 0.78, 1, 1, "title + buttons"), (0.89, 0.35, 1, 0.78, "action column")]),
    "reels": dict(canvas=(1080, 1920), max_s=180, zones=[(0, 0, 1, 0.13, "top bar"), (0, 0.78, 1, 1, "caption + audio"), (0.89, 0.4, 1, 0.78, "action column")]),
    "tiktok": dict(canvas=(1080, 1920), max_s=600, zones=[(0, 0, 1, 0.13, "top tabs"), (0, 0.76, 1, 1, "caption + sound"), (0.87, 0.35, 1, 0.76, "action column")]),
    "story": dict(canvas=(1080, 1920), max_s=60, zones=[(0, 0, 1, 0.13, "profile bar"), (0, 0.84, 1, 1, "reply bar")]),
    "ig-feed": dict(canvas=(1080, 1350), max_s=None, zones=[]),
    "carousel": dict(canvas=(1080, 1350), max_s=None, zones=[]),
    "linkedin": dict(canvas=(1080, 1350), max_s=None, zones=[]),
    "x": dict(canvas=(1200, 675), max_s=None, zones=[]),
    "yt-thumb": dict(canvas=(1280, 720), max_s=None, max_mb=2, zones=[(0.82, 0.84, 1, 1, "duration badge")]),
    "youtube": dict(canvas=(1920, 1080), max_s=None, zones=[]),
}
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}


@dataclass
class Result:
    check: str
    status: str  # PASS | WARN | FAIL
    value: str
    fix: str = ""


def _ratio(w, h):
    return round(w / h, 3)


def canvas(w, h, spec) -> Result:
    cw, ch = spec["canvas"]
    if (w, h) == (cw, ch):
        return Result("canvas", "PASS", f"{w}x{h}")
    if _ratio(w, h) == _ratio(cw, ch):
        st = "WARN" if w < cw else "PASS"
        return Result("canvas", st, f"{w}x{h} (right aspect)", f"export at {cw}x{ch}" if st == "WARN" else "")
    return Result("canvas", "FAIL", f"{w}x{h} ({w / h:.2f}:1)", f"expected {cw}x{ch}; reframe (recipes/ffmpeg.md) instead of letting the app crop")


def ui_zones(img: Image.Image, spec) -> list[Result]:
    """Edge density inside each UI zone vs the rest of the frame: text there gets covered."""
    if not spec["zones"]:
        return []
    g = ImageOps.grayscale(img).resize((270, round(270 * img.height / img.width)))
    edges = g.filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 60 else 0)
    W, H = edges.size

    def density(box):
        x0, y0, x1, y1 = (round(box[0] * W), round(box[1] * H), round(box[2] * W), round(box[3] * H))
        crop = edges.crop((x0, y0, max(x0 + 1, x1), max(y0 + 1, y1)))
        return sum(crop.histogram()[255:]) / max(1, crop.width * crop.height)

    body = density((0.08, 0.2, 0.86, 0.72))
    out = []
    for x0, y0, x1, y1, name in spec["zones"]:
        dz = density((x0, y0, x1, y1))
        busy = dz > max(0.08, body * 1.2)
        out.append(Result(f"ui zone: {name}", "WARN" if busy else "PASS", f"edge density {dz:.2f} (body {body:.2f})",
                          "move text or key detail out of this zone (formats/specs.md safe zones)" if busy else ""))
    return out


def feed_contrast(img: Image.Image) -> Result:
    """Luminance spread at 160 px wide: low spread means the post turns to mush in a feed or as a thumbnail."""
    small = ImageOps.grayscale(img).resize((160, max(1, round(160 * img.height / img.width))), Image.LANCZOS)
    px = sorted(small.getdata())
    n = len(px)
    spread = px[int(n * 0.95)] - px[int(n * 0.05)]
    st = "PASS" if spread >= 110 else "WARN" if spread >= 70 else "FAIL"
    return Result("contrast at 160 px", st, f"5-95% luma spread {spread}",
                  "" if st == "PASS" else "darken behind the text or raise text weight/size (formats/thumbnail.md)")


def file_size(path: Path, spec) -> Result | None:
    if "max_mb" not in spec:
        return None
    mb = path.stat().st_size / 1e6
    return Result("file size", "PASS" if mb <= spec["max_mb"] else "FAIL", f"{mb:.2f} MB",
                  "" if mb <= spec["max_mb"] else f"must be under {spec['max_mb']} MB: save as JPEG quality 85")


def _probe(path: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def _ff_filter(path: Path, af: str | None = None, vf: str | None = None, seconds: float | None = None) -> str:
    args = ["ffmpeg", "-hide_banner", "-nostats"]
    if seconds:
        args += ["-t", str(seconds)]
    args += ["-i", str(path)]
    args += ["-af", af, "-vn"] if af else ["-vf", vf, "-an"]
    args += ["-f", "null", "-"]
    return subprocess.run(args, capture_output=True, text=True).stderr


def check_video(path: Path, spec) -> list[Result]:
    info = _probe(path)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    if not v:
        return [Result("video stream", "FAIL", "none", "file has no video stream")]
    out = [canvas(int(v["width"]), int(v["height"]), spec)]
    dur = float(info["format"].get("duration", 0))
    if spec["max_s"]:
        out.append(Result("duration", "PASS" if dur <= spec["max_s"] else "FAIL", f"{dur:.1f} s",
                          "" if dur <= spec["max_s"] else f"platform max is {spec['max_s']} s"))
    out.append(Result("codec", "PASS" if v["codec_name"] == "h264" else "WARN", v["codec_name"],
                      "" if v["codec_name"] == "h264" else "re-encode with -c:v libx264 for the cleanest upload"))
    out.append(Result("pixel format", "PASS" if v.get("pix_fmt") == "yuv420p" else "FAIL", v.get("pix_fmt", "?"),
                      "" if v.get("pix_fmt") == "yuv420p" else "add -pix_fmt yuv420p (other formats show black or green on phones)"))
    num, den = (int(x) for x in v.get("avg_frame_rate", "0/1").split("/"))
    fps = num / den if den else 0
    out.append(Result("frame rate", "PASS" if 23.9 <= fps <= 60.1 else "WARN", f"{fps:.2f} fps",
                      "" if 23.9 <= fps <= 60.1 else "use 30 or 60 fps"))
    head = path.read_bytes()[:1 << 20]
    moov, mdat = head.find(b"moov"), head.find(b"mdat")
    fast = moov != -1 and (mdat == -1 or moov < mdat)
    if path.suffix.lower() in (".mp4", ".m4v", ".mov"):
        out.append(Result("faststart", "PASS" if fast else "WARN", "moov first" if fast else "moov at end",
                          "" if fast else "add -movflags +faststart"))
    black = re.findall(r"black_start:([\d.]+)", _ff_filter(path, vf="blackdetect=d=0.3:pic_th=0.95", seconds=2))
    opens_black = any(float(b) < 0.1 for b in black)
    out.append(Result("first frame", "FAIL" if opens_black else "PASS", "black opening" if opens_black else "picture from frame 1",
                      "cut the black lead-in: the first frame is the hook and often the cover" if opens_black else ""))
    if a:
        log = _ff_filter(path, af="ebur128=peak=true")
        i = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)
        tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)
        if i:
            lufs = float(i[-1])
            st = "PASS" if -16 <= lufs <= -12 else "WARN"
            out.append(Result("loudness", st, f"{lufs:.1f} LUFS", "" if st == "PASS" else "normalise to -14 LUFS: recipes/ffmpeg.md (loudnorm)"))
        if tp:
            peak = float(tp[-1])
            out.append(Result("true peak", "PASS" if peak <= -1 else "WARN", f"{peak:.1f} dBTP", "" if peak <= -1 else "limit to -1 dBTP"))
        sil = re.findall(r"silence_start: ([\d.]+)", _ff_filter(path, af="silencedetect=n=-45dB:d=0.8", seconds=3))
        quiet = any(float(s) < 0.2 for s in sil)
        out.append(Result("audio opening", "WARN" if quiet else "PASS", "silent first 0.8 s+" if quiet else "sound from the start",
                          "start on a word or a sound; silence reads as a dead open" if quiet else ""))
    else:
        out.append(Result("audio", "WARN", "no audio stream", "fine for a silent loop; most Shorts and Reels need sound"))
    # sample frame at 1 s for zones and contrast
    tmp = path.with_suffix(".check.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(min(1.0, dur / 2)), "-i", str(path), "-frames:v", "1", str(tmp)], check=True)
    try:
        img = Image.open(tmp).convert("RGB")
        out += ui_zones(img, spec)
        out.append(feed_contrast(img))
    finally:
        tmp.unlink(missing_ok=True)
    return out


def check_image(path: Path, spec) -> list[Result]:
    img = Image.open(path).convert("RGB")
    out = [canvas(img.width, img.height, spec)]
    fs = file_size(path, spec)
    if fs:
        out.append(fs)
    out += ui_zones(img, spec)
    out.append(feed_contrast(img))
    return out


def check(path: str | Path, platform: str) -> list[Result]:
    path = Path(path)
    if platform not in PLATFORMS:
        raise KeyError(f"unknown platform {platform!r}; one of {', '.join(PLATFORMS)}")
    spec = PLATFORMS[platform]
    if path.suffix.lower() in VIDEO_EXT:
        if not shutil.which("ffprobe"):
            raise RuntimeError("ffprobe (part of ffmpeg) is needed to check video")
        return check_video(path, spec)
    return check_image(path, spec)


def report(path, platform, results: list[Result], as_json=False) -> str:
    if as_json:
        return json.dumps({"file": str(path), "platform": platform, "results": [asdict(r) for r in results]}, indent=2)
    lines = [f"{path}  ->  {platform}", ""]
    for r in results:
        lines.append(f"  {r.status:4s}  {r.check:24s} {r.value}")
        if r.fix:
            lines.append(f"        {'':24s} fix: {r.fix}")
    fails = sum(r.status == "FAIL" for r in results)
    warns = sum(r.status == "WARN" for r in results)
    lines += ["", f"  {fails} fail, {warns} warn. " + ("Ship after a human watch-through." if not fails else "Fix the FAILs first.")]
    return "\n".join(lines)
