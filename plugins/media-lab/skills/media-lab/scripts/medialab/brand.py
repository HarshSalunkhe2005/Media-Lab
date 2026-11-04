"""Brand kit: one file that makes every render look like the same account.

    {
      "name": "Fern Café",
      "base": "warm-local",                      # a theme to start from (any world id)
      "handle": "@ferncafe",                     # default for every slide / post
      "colors": {"bg": "#f3e7d6", "fg": "#2b1d14", "muted": "#7a6555", "accent": "#2f6b4f"},
      "fonts": {"head": "display-serif", "body": "sans", "num": "display-serif"},   # bundled kind or a font file
      "logo": "logo.png",                        # transparent PNG; optional
      "logo_position": "top-right",              # top-left | top-right | bottom-left | bottom-right
      "logo_size": 0.09                          # fraction of the canvas width
    }

Use it with `"brand": "brand.json"` in any spec, or `medialab make spec.json --brand brand.json`.
Precedence: spec values > brand > base theme. `medialab brand check brand.json` validates it before you use it.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from .core import contrast_ratio, font_path, rgb
from .themes import THEMES

POSITIONS = ("top-left", "top-right", "bottom-left", "bottom-right")
COLOR_KEYS = ("bg", "fg", "muted", "accent")
FONT_KEYS = ("head", "body", "num")

STARTER = {
    "name": "Your brand",
    "base": "explainer",
    "handle": "@yourhandle",
    "colors": {"bg": "#f7f6f2", "fg": "#17181a", "muted": "#5d6066", "accent": "#ff5a36"},
    "fonts": {"head": "sans-bold", "body": "sans", "num": "sans-black"},
    "logo": None,
    "logo_position": "top-right",
    "logo_size": 0.09,
}


def load(src, base: Path | None = None) -> dict:
    """A brand dict, or a path to brand.json. Relative logo/font paths resolve against the brand file's folder."""
    if isinstance(src, dict):
        b, root = dict(src), Path(base or ".")
    else:
        p = Path(src)
        if not p.is_absolute() and base is not None:
            p = Path(base) / p
        if not p.exists():
            raise FileNotFoundError(f"brand file not found: {p}")
        b, root = json.loads(p.read_text(encoding="utf-8")), p.parent
    if b.get("logo") and not Path(b["logo"]).is_absolute():
        b["logo"] = str(root / b["logo"])
    fonts = dict(b.get("fonts") or {})
    for k, v in fonts.items():
        if isinstance(v, str) and v.lower().endswith((".ttf", ".otf", ".woff")) and not Path(v).is_absolute():
            fonts[k] = str(root / v)
    b["fonts"] = fonts
    return b


def apply(spec: dict, brand: dict) -> dict:
    """Merge a brand into a spec. The spec wins where both set something."""
    out = dict(spec)
    out.setdefault("theme", brand.get("base", "explainer"))
    out["colors"] = {**(brand.get("colors") or {}), **(spec.get("colors") or {})}
    out["fonts"] = {**(brand.get("fonts") or {}), **(spec.get("fonts") or {})}
    if brand.get("handle"):
        out.setdefault("handle", brand["handle"])
    if brand.get("logo"):
        out.setdefault("logo", brand["logo"])
        out.setdefault("logo_position", brand.get("logo_position", "top-right"))
        out.setdefault("logo_size", brand.get("logo_size", 0.09))
    return out


def logo_layer(w: int, h: int, spec: dict) -> Image.Image | None:
    """Transparent w x h layer with the logo in its corner, inside the margin (None when there is no logo)."""
    logo = spec.get("logo")
    if not logo:
        return None
    pos = spec.get("logo_position", "top-right")
    if pos not in POSITIONS:
        raise ValueError(f"logo_position must be one of {', '.join(POSITIONS)}")
    with Image.open(logo) as lg:
        lg = lg.convert("RGBA")
    lw = max(24, int(w * float(spec.get("logo_size", 0.09))))
    lg = lg.resize((lw, max(1, round(lg.height * lw / lg.width))), Image.LANCZOS)
    m = round(w * 0.06)  # 64 px at 1080 wide
    x = m if pos.endswith("left") else w - m - lg.width
    y = m if pos.startswith("top") else h - m - lg.height
    if h >= w * 1.7:  # 9:16: keep clear of the top bar and the bottom UI (formats/specs.md), scaled to the frame
        y = round(h * 0.14) if pos.startswith("top") else h - round(h * 0.23) - lg.height
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    layer.alpha_composite(lg, (x, y))
    return layer


def stamp(img: Image.Image, spec: dict) -> Image.Image:
    """Put the logo on a still. Skipped when the spec sets "logo": false or has none."""
    layer = logo_layer(img.width, img.height, spec)
    if layer is None:
        return img
    out = img.convert("RGBA")
    out.alpha_composite(layer)
    return out.convert("RGB")


def check(src, base: Path | None = None) -> list[tuple[str, str, str]]:
    """(status, check, detail) rows. FAIL means renders would be unreadable or would crash."""
    rows = []
    try:
        b = load(src, base)
    except (OSError, json.JSONDecodeError) as e:
        return [("FAIL", "brand file", str(e))]
    base_id = b.get("base", "explainer")
    rows.append(("PASS" if base_id in THEMES else "FAIL", "base theme", base_id if base_id in THEMES else f"{base_id!r} is not one of {', '.join(THEMES)}"))
    t = {**THEMES.get(base_id, THEMES["explainer"]), **(b.get("colors") or {})}
    for k in COLOR_KEYS:
        try:
            rgb(t[k])
        except (ValueError, KeyError):
            rows.append(("FAIL", f"color {k}", f"{t.get(k)!r} is not a #rrggbb colour"))
            return rows
    for name, a, need_pass, need_warn in (("text on background", "fg", 7, 4.5), ("muted on background", "muted", 4.5, 3),
                                          ("accent on background", "accent", 3, 2)):
        r = contrast_ratio(t[a], t["bg"])
        st = "PASS" if r >= need_pass else "WARN" if r >= need_warn else "FAIL"
        rows.append((st, name, f"{r:.1f}:1 (want {need_pass}:1)"))
    for k, v in (b.get("fonts") or {}).items():
        if k not in FONT_KEYS:
            rows.append(("WARN", f"font {k}", "unknown role; use head, body or num"))
            continue
        try:
            font_path(v)
            rows.append(("PASS", f"font {k}", v))
        except KeyError as e:
            rows.append(("FAIL", f"font {k}", str(e)))
    if b.get("logo"):
        p = Path(b["logo"])
        if not p.exists():
            rows.append(("FAIL", "logo", f"not found: {p}"))
        else:
            with Image.open(p) as lg:
                alpha = lg.mode in ("RGBA", "LA") or "transparency" in lg.info
                rows.append(("PASS" if alpha else "WARN", "logo", f"{lg.width}x{lg.height}" + ("" if alpha else ", no transparency: it will sit on a box")))
                if lg.width < 300:
                    rows.append(("WARN", "logo size", f"{lg.width} px wide; use 600 px+ so it stays sharp"))
        pos = b.get("logo_position", "top-right")
        if pos not in POSITIONS:
            rows.append(("FAIL", "logo position", f"{pos!r}; one of {', '.join(POSITIONS)}"))
        elif pos == "top-left":
            rows.append(("WARN", "logo position", "top-left sits where most kinds start the headline or number; prefer top-right or bottom-right"))
        elif pos == "bottom-left":
            rows.append(("WARN", "logo position", "bottom-left shares the corner with the handle; drop one of them"))
        else:
            rows.append(("PASS", "logo position", pos))
    return rows
