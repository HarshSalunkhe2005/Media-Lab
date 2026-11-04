"""build(spec, out): the one entry point. A spec is a dict (JSON or YAML file).

    {"kind": "thumbnail", "theme": "explainer", "words": "Stop doing this", "highlight": "stop", "photo": "me.jpg"}
    {"kind": "carousel", "theme": "data-story", "pdf": true, "slides": [{"kind": "cover", ...}, {"kind": "point", ...}]}

Relative photo/audio/video paths resolve against `base` (the spec file's folder).
"""
from __future__ import annotations

import json
from pathlib import Path

from . import brand as brandkit
from . import stills, video
from .themes import theme

MEDIA_KEYS = ("photo", "photos", "audio", "video", "top", "bottom", "main", "inset")


def load(path: str | Path) -> dict:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in (".yml", ".yaml"):
        try:
            import yaml
        except ImportError as e:
            raise SystemExit("YAML specs need PyYAML (pip install pyyaml), or write the spec as JSON") from e
        return yaml.safe_load(text)
    return json.loads(text)


def _resolve(spec: dict, base: Path) -> dict:
    out = dict(spec)
    for k in MEDIA_KEYS:
        v = out.get(k)
        if isinstance(v, str) and not Path(v).is_absolute():
            out[k] = str(base / v)
        elif isinstance(v, list):
            out[k] = [str(base / x) if isinstance(x, str) and not Path(x).is_absolute() else x for x in v]
        elif isinstance(v, dict):
            out[k] = _resolve(v, base)
    for k in ("left", "right"):
        if isinstance(out.get(k), dict):
            out[k] = _resolve(out[k], base)
    return out


def _theme(spec):
    return theme(spec.get("theme", "explainer"), **spec.get("colors", {}), **spec.get("fonts", {}))


def build(spec: dict, out: str | Path, base: str | Path = ".", preview: bool = False) -> list[Path]:
    """Render spec to out. Stills: out is a .png/.jpg file (or a folder for carousels). Video: an .mp4 path."""
    if spec.get("brand"):
        spec = brandkit.apply({k: v for k, v in spec.items() if k != "brand"}, brandkit.load(spec["brand"], Path(base)))
    spec = _resolve(spec, Path(base))
    out = Path(out)
    kind = spec.get("kind")
    t = _theme(spec)
    if kind == "carousel":
        out.mkdir(parents=True, exist_ok=True)
        slides = spec["slides"]
        shared = {k: v for k, v in spec.items() if k in ("size", "handle", "logo", "logo_position", "logo_size")}
        imgs, paths = [], []
        for i, s in enumerate(slides, 1):
            s = {**shared, **_resolve(s, Path(base)), "_index": i, "_total": len(slides)}
            st = _theme({**spec, **{k: s[k] for k in ("theme", "colors", "fonts") if k in s}})
            img = brandkit.stamp(stills.KINDS[s["kind"]](s, st), s)
            imgs.append(img.convert("RGB"))
            paths.append(_save(img, out / f"{i:02d}.png", preview))
        if spec.get("pdf"):
            pdf = out / "carousel.pdf"
            imgs[0].save(pdf, save_all=True, append_images=imgs[1:], resolution=144)
            paths.append(pdf)
        return paths
    if kind in stills.KINDS:
        return [_save(brandkit.stamp(stills.KINDS[kind](spec, t), spec), out, preview)]
    if kind in video.KINDS:
        out.parent.mkdir(parents=True, exist_ok=True)
        res = video.KINDS[kind]({**spec, "preview": preview or spec.get("preview", False)}, t, out)
        if spec.get("logo"):
            video.overlay_logo(res, spec)
        return [res]
    raise KeyError(f"unknown kind {kind!r}; run `medialab kinds`")


def _save(img, out: Path, preview: bool) -> Path:
    from .core import save, save_jpg
    return save_jpg(img, out, 540 if img.width <= 1100 else 640) if preview else save(img, out)
