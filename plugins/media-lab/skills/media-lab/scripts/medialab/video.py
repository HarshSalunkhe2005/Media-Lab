"""Video builders: spec dict in, MP4 out. Pillow draws the frames or overlays, ffmpeg does the rest.

All output is H.264 + yuv420p + faststart (plays everywhere, uploads clean). 1080x1920 at 30 fps unless the
spec says otherwise; pass "preview": true for a 360 px wide, silent, small file (the gallery uses this).
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

from .core import ffmpeg, film, fit, fit_text, font, rgb, text_block, wrap
from .stills import M, background
from .themes import SIZES, cased

FPS = 30


def _enc(spec, extra_vf: str = "") -> list[str]:
    vf = extra_vf
    if spec.get("preview"):
        vf = (vf + "," if vf else "") + "scale=360:-2"
    args = (["-vf", vf] if vf else []) + ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                                          "-crf", "30" if spec.get("preview") else "20"]
    return args


def _size(spec):
    s = spec.get("size", "9:16")
    return SIZES[s] if isinstance(s, str) else tuple(s)


def _frames_to_mp4(frames_dir: Path, out: Path, spec, audio: str | None = None):
    args = ["-framerate", str(FPS), "-i", str(frames_dir / "%05d.png")]
    if audio and not spec.get("preview"):
        args += ["-i", audio, "-c:a", "aac", "-b:a", "160k", "-shortest"]
    else:
        args += ["-an"]
    ffmpeg(*args, *_enc(spec), str(out))
    return out


def kinetic(spec, t, out: Path):
    """Hook text that builds word by word on a plain or photo background, then holds.
    One word lands every `beat` seconds; the last line gets the accent."""
    w, h = _size(spec)
    bg = background(t, (w, h), spec.get("photo"), spec.get("focus", (0.5, 0.5)), "bottom", strength=230, start=0.2)
    words = cased(spec["text"], t).split()
    beat, hold = spec.get("beat", 0.32), spec.get("hold", 1.6)
    f, lines = fit_text(" ".join(words), t["head"], w - 2 * M, 6, 130)
    lh = int(f.size * 1.1)
    y0 = (h - lh * len(lines)) / 2
    on_photo = bool(spec.get("photo"))
    fg = (246, 244, 240) if on_photo else rgb(t["fg"])
    acc = rgb(t["accent"])
    hi = {x.lower().strip(".,!?") for x in spec.get("highlight", [])}
    pos, i = [], 0
    for li, ln in enumerate(lines):
        x = M
        for wd in ln.split():
            pos.append((wd, x, y0 + li * lh))
            x += f.getlength(wd + " ")
            i += 1
    total = int((len(pos) * beat + hold) * FPS)
    with tempfile.TemporaryDirectory() as tmp:
        for n in range(total):
            tsec = n / FPS
            img = bg.copy()
            d = ImageDraw.Draw(img)
            shown = min(len(pos), int(tsec / beat) + 1)
            for k, (wd, x, y) in enumerate(pos[:shown]):
                age = tsec - k * beat
                lift = max(0, 18 * (1 - age / 0.12)) if age < 0.12 else 0
                d.text((x, y + lift), wd, font=f, fill=acc if wd.lower().strip(".,!?") in hi else fg)
            img.save(Path(tmp) / f"{n:05d}.png")
        return _frames_to_mp4(Path(tmp), out, spec, spec.get("audio"))


def _sub(tmp: Path, name: str) -> Path:
    p = Path(tmp) / name
    p.mkdir(exist_ok=True)
    return p


def _clip(src: str, size, t, tmp: Path, name: str, dur: float) -> str:
    """A video path as-is, or a photo turned into a slow-push clip of dur seconds."""
    if src.endswith((".mp4", ".mov", ".webm", ".mkv")):
        return src
    return str(_slideshow({"size": size, "photos": [src]}, t, _sub(tmp, name), [dur]))


def _slideshow(spec, t, tmp: Path, durations: list[float]) -> Path:
    """Photos -> one silent clip with a slow push on each (no transitions: hard cuts read as edited)."""
    w, h = _size(spec)
    w, h = w - w % 2, h - h % 2
    parts = []
    for i, (p, dur) in enumerate(zip(spec["photos"], durations)):
        still = film(fit(Image.open(p).convert("RGB"), w, h)) if spec.get("grade", "film") == "film" else fit(Image.open(p).convert("RGB"), w, h)
        sp = tmp / f"s{i}.png"
        still.save(sp)
        n = max(1, int(dur * FPS))
        z = f"zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={w}x{h}:fps={FPS}"
        clip = tmp / f"c{i}.mp4"
        ffmpeg("-loop", "1", "-i", str(sp), "-vf", f"scale={w * 2}:{h * 2},{z}", "-t", f"{dur:.3f}",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", str(clip))
        parts.append(clip)
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{c.name}'\n" for c in parts))
    joined = tmp / "joined.mp4"
    ffmpeg("-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(joined), cwd=tmp)
    return joined


def beatcut(spec, t, out: Path):
    """Photos cut on the beat: each photo holds `beats_per_cut` beats at `bpm`. Pass audio to lay the track under."""
    beat = 60 / spec.get("bpm", 120)
    dur = beat * spec.get("beats_per_cut", 2)
    with tempfile.TemporaryDirectory() as tmp:
        clip = _slideshow(spec, t, Path(tmp), [dur] * len(spec["photos"]))
        args = ["-i", str(clip)]
        if spec.get("audio") and not spec.get("preview"):
            args += ["-i", spec["audio"], "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-shortest"]
        else:
            args += ["-an"]
        ffmpeg(*args, *_enc(spec), str(out))
    return out


def progress(spec, t, out: Path):
    """A thin progress bar along the top edge (inside the safe zone) over a slideshow or video.
    Tells viewers how long is left; useful for list and story Shorts over ~20 s."""
    w, h = _size(spec)
    acc = spec.get("bar", t["accent"]).lstrip("#")
    with tempfile.TemporaryDirectory() as tmp:
        if spec.get("video"):
            src = spec["video"]
        else:
            per = spec.get("seconds_per_photo", 2.5)
            src = str(_slideshow(spec, t, Path(tmp), [per] * len(spec["photos"])))
        dur = float(spec.get("duration") or _probe_duration(src))
        bar_y = spec.get("bar_y", 262)  # just below the top UI zone (formats/specs.md)
        vf = (f"drawbox=x=0:y={bar_y}:w=iw:h=10:color=black@0.35:t=fill,"
              f"drawbox=x=0:y={bar_y}:w='iw*t/{dur:.3f}':h=10:color=0x{acc}:t=fill")
        ffmpeg("-i", src, "-an", *_enc(spec, vf), str(out))
    return out


def splitscreen(spec, t, out: Path):
    """Two sources stacked (top: the thing, bottom: the reaction or the result). Each fills half of 9:16."""
    w, h = _size(spec)
    hh = h // 2
    dur = spec.get("duration", 4)
    with tempfile.TemporaryDirectory() as tmp:
        top = _clip(spec["top"], (w, hh), t, Path(tmp), "top", dur)
        bot = _clip(spec["bottom"], (w, hh), t, Path(tmp), "bottom", dur)
        fc = (f"[0:v]scale={w}:{hh}:force_original_aspect_ratio=increase,crop={w}:{hh}[a];"
              f"[1:v]scale={w}:{hh}:force_original_aspect_ratio=increase,crop={w}:{hh}[b];"
              f"[a][b]vstack=inputs=2,drawbox=y={hh - 4}:w=iw:h=8:color=black:t=fill")
        if spec.get("preview"):
            fc += ",scale=360:-2"
        ffmpeg("-i", top, "-i", bot, "-filter_complex", fc, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
               "-movflags", "+faststart", "-crf", "30" if spec.get("preview") else "20", "-t", str(dur), str(out))
    return out


def pip(spec, t, out: Path):
    """Picture-in-picture: main source full frame, a small rounded inset in the lower third (above captions)."""
    w, h = _size(spec)
    iw = int(w * spec.get("scale", 0.34))
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        dur = spec.get("duration", 4)
        ih = int(iw * 1.25)
        main = _clip(spec["main"], (w, h), t, tmp, "main", dur)
        ins_src = _clip(spec["inset"], (iw * 2, ih * 2), t, tmp, "inset", dur)
        mask = Image.new("L", (iw, ih), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, iw - 1, ih - 1), 28, fill=255)
        mask.save(tmp / "mask.png")
        x, y = w - iw - 60, int(h * 0.52)
        fc = (f"[1:v]scale={iw}:{ih}:force_original_aspect_ratio=increase,crop={iw}:{ih},format=rgba[ins];"
              f"[2:v]format=gray[m];[ins][m]alphamerge[r];[0:v]scale={w}:{h}[bg];[bg][r]overlay={x}:{y}:shortest=1")
        if spec.get("preview"):
            fc += ",scale=360:-2"
        ffmpeg("-i", main, "-i", ins_src, "-loop", "1", "-i", str(tmp / "mask.png"), "-filter_complex", fc, "-an",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-crf", "30" if spec.get("preview") else "20",
               "-t", str(spec.get("duration", 4)), str(out))
    return out


def countdown(spec, t, out: Path):
    """List Short: '3 ... 2 ... 1' with one item per beat, the number huge, the item under it."""
    w, h = _size(spec)
    items = spec["items"]
    per = spec.get("seconds_per_item", 2.2)
    photos = spec.get("photos") or [None] * len(items)
    fn = font(t["num"], 420)
    with tempfile.TemporaryDirectory() as tmp:
        n = 0
        for i, item in enumerate(items):
            rank = len(items) - i
            bg = background(t, (w, h), photos[i % len(photos)], where="bottom", strength=235, start=0.15)
            on_photo = bool(photos[i % len(photos)])
            fg = (246, 244, 240) if on_photo else rgb(t["fg"])
            f, lines = fit_text(cased(item, t), t["head"], w - 2 * M, 3, 96)
            for k in range(int(per * FPS)):
                img = bg.copy()
                d = ImageDraw.Draw(img)
                pop = 1 if k > 4 else 0.85 + 0.03 * k
                fz = font(t["num"], int(420 * pop))
                d.text((M - 10, 360), str(rank), font=fz, fill=rgb(t["accent"]))
                text_block(d, (M, 360 + fn.size * 1.05), lines, f, fg, 1.1)
                img.save(Path(tmp) / f"{n:05d}.png")
                n += 1
        return _frames_to_mp4(Path(tmp), out, spec)


def audiogram(spec, t, out: Path):
    """Podcast / voice clip: a still card (title, show, speaker) plus a live waveform from the audio.
    Burn captions separately with scripts/captions.py; the waveform sits above the caption zone."""
    w, h = _size(spec)
    card = background(t, (w, h), spec.get("photo"), spec.get("focus", (0.5, 0.3)), "bottom", strength=240, start=0.2)
    d = ImageDraw.Draw(card)
    on_photo = bool(spec.get("photo"))
    fg = (246, 244, 240) if on_photo else rgb(t["fg"])
    muted = (205, 200, 194) if on_photo else rgb(t["muted"])
    d.text((M, 300), cased(spec.get("show", ""), t, "body"), font=font(t["body"], 40), fill=rgb(t["accent"]), anchor="lt")
    f, lines = fit_text(spec["title"], t["head"], w - 2 * M, 4, 100)
    y = text_block(d, (M, 370), lines, f, fg, 1.12) + 30
    if spec.get("speaker"):
        d.text((M, y), spec["speaker"], font=font(t["body"], 40), fill=muted, anchor="lt")
    wave_y, wave_h = int(h * 0.62), 260
    acc = t["accent"].lstrip("#")
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp) / "card.png"
        card.save(cp)
        fc = (f"[1:a]aformat=channel_layouts=mono,showwaves=s={w - 2 * M}x{wave_h}:mode=cline:rate={FPS}:colors=0x{acc}:scale=cbrt,"
              f"format=rgba,colorkey=black:0.1:0.0[wv];[0:v][wv]overlay={M}:{wave_y}:shortest=1")
        if spec.get("preview"):
            fc += ",scale=360:-2"
        args = ["-loop", "1", "-framerate", str(FPS), "-i", str(cp), "-i", spec["audio"], "-filter_complex", fc,
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-crf", "30" if spec.get("preview") else "20"]
        if spec.get("preview"):
            args += ["-an"]
        else:
            args += ["-map", "1:a", "-c:a", "aac", "-b:a", "160k"]
        args += ["-t", str(spec.get("duration", _probe_duration(spec["audio"])))]
        ffmpeg(*args, str(out))
    return out


def _probe_duration(path: str) -> float:
    import subprocess
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


KINDS = {"kinetic": kinetic, "beatcut": beatcut, "progress": progress, "splitscreen": splitscreen, "pip": pip,
         "countdown": countdown, "audiogram": audiogram}
