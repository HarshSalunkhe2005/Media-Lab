"""Still builders: one function per kind, spec dict in, PIL image out.

Every builder follows playbook/taste.md: real photo or a plain surface, one accent, text in the calm area,
96 px margins (inside every platform's safe zone), sentence case unless the theme says otherwise.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from .core import (block_height, circle, duotone, film, fit, fit_text, font, halftone, paper, rgb, rounded,
                   shade, text_block, wrap)
from .themes import SIZES, cased

M = 96  # outer margin


def _size(spec, default="4:5"):
    s = spec.get("size", default)
    return SIZES[s] if isinstance(s, str) else tuple(s)


def _photo(path: str | None):
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"photo not found: {path}")
    with Image.open(p) as im:
        return im.convert("RGB")


def background(t: dict, size, photo: str | None = None, focus=(0.5, 0.5), where="bottom", grade="film",
               strength=210, start=0.4) -> Image.Image:
    """Photo (graded, darkened toward the text edge) or the theme's surface."""
    w, h = size
    img = _photo(photo)
    if img is not None:
        img = fit(img, w, h, *focus)
        if grade == "film":
            img = film(img)
        elif grade == "duotone":
            img = duotone(img, t["fg"], t["bg"])
        elif grade == "halftone":
            img = halftone(img, 12, t["fg"], t["bg"])
        if where in ("top", "bottom"):
            img = shade(img, where, strength, start)
        return img
    if t["surface"] == "paper":
        return paper(w, h, rgb(t["bg"]))
    return Image.new("RGB", size, rgb(t["bg"]))


def _colours(t, on_photo: bool):
    if on_photo:
        return (246, 244, 240), (214, 210, 204), rgb(t["accent"])
    return rgb(t["fg"]), rgb(t["muted"]), rgb(t["accent"])


def _counter(d, t, w, h, spec, fg):
    n, total = spec.get("_index"), spec.get("_total")
    if n and total and spec.get("counter", True):
        if spec.get("logo") and spec.get("logo_position", "top-right") == "top-right":
            d.text((w - M, h - M + 10), f"{n}/{total}", font=font(t["body"], 30), fill=fg, anchor="rs")  # logo owns the top corner
        else:
            d.text((w - M, M - 20), f"{n}/{total}", font=font(t["body"], 30), fill=fg, anchor="ra")


def _handle(d, t, w, h, spec, fg):
    if spec.get("handle"):
        d.text((M, h - M + 10), spec["handle"], font=font(t["body"], 28), fill=fg, anchor="ls")


# ---------- carousel slide kinds ----------

def cover(spec, t):
    w, h = _size(spec)
    photo = spec.get("photo")
    img = background(t, (w, h), photo, spec.get("focus", (0.5, 0.4)), "bottom")
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, bool(photo))
    f, lines = fit_text(cased(spec["title"], t), t["head"], w - 2 * M, spec.get("max_lines", 4), 112)
    y = h - M - 70 - block_height(lines, f, 1.12)
    if spec.get("kicker"):
        d.text((M, y - 30), cased(spec["kicker"], t, "body"), font=font(t["body"], 34), fill=acc, anchor="ls")
    text_block(d, (M, y), lines, f, fg, 1.12)
    if spec.get("_total"):
        d.text((M, h - M), f"swipe  ·  1/{spec['_total']}", font=font(t["body"], 28), fill=muted, anchor="ls")
    _handle(d, t, w, h, {}, muted)
    return img


def point(spec, t):
    w, h = _size(spec)
    img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    d.text((M, M + 40), str(spec.get("n", spec.get("_index", 1) - 1)).zfill(2), font=font(t["num"], 200), fill=acc, anchor="lt")
    f, lines = fit_text(cased(spec["title"], t), t["head"], w - 2 * M, 3, 84)
    y = text_block(d, (M, 420), lines, f, fg, 1.12) + 40
    if spec.get("body"):
        fb = font(t["body"], 42)
        text_block(d, (M, y), wrap(spec["body"], fb, w - 2 * M - 60), fb, muted, 1.42)
    _counter(d, t, w, h, spec, muted)
    _handle(d, t, w, h, spec, muted)
    return img


def number(spec, t):
    w, h = _size(spec)
    img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    f, _ = fit_text(spec["value"], t["num"], w - 2 * M, 1, 400)
    d.text((M - 8, h * 0.18), spec["value"], font=f, fill=acc, anchor="lt")
    fb = font(t["head"], 56)
    y = text_block(d, (M, h * 0.18 + f.size * 1.1), wrap(spec["caption"], fb, w - 2 * M), fb, fg, 1.25)
    if spec.get("source"):
        d.text((M, h - M), "Source: " + spec["source"], font=font(t["body"], 26), fill=muted, anchor="ls")
    _counter(d, t, w, h, spec, muted)
    return img


def quote(spec, t):
    w, h = _size(spec)
    photo = spec.get("photo")
    img = background(t, (w, h), photo, spec.get("focus", (0.5, 0.5)), "bottom" if photo else None, start=0.3)
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, bool(photo))
    kind = spec.get("font", "serif" if t["head"].startswith("serif") else t["head"])
    f, lines = fit_text(spec["text"], kind, w - 2 * M - 40, spec.get("max_lines", 7), 76)
    bh = block_height(lines, f, 1.32)
    y = (h - M - 90 - bh) if photo else (h - bh) / 2 - 30
    if not photo:
        d.line((M, y - 50, M + 80, y - 50), fill=acc, width=5)
    end = text_block(d, (M, y), lines, f, fg, 1.32)
    if spec.get("by"):
        d.text((M, end + 34), "— " + spec["by"], font=font(t["body"], 34), fill=muted, anchor="lt")
    _counter(d, t, w, h, spec, muted)
    return img


def checklist(spec, t):
    w, h = _size(spec)
    img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    f, lines = fit_text(cased(spec["title"], t), t["head"], w - 2 * M, 2, 80)
    y = text_block(d, (M, M + 60), lines, f, fg, 1.12) + 60
    fi = font(t["body"], 42)
    for item in spec["items"]:
        done = item.startswith("[x]")
        text = item[3:].strip() if item[:3] in ("[x]", "[ ]") else item
        d.rounded_rectangle((M, y + 4, M + 44, y + 48), 8, outline=acc, width=4, fill=acc if done else None)
        if done:
            d.line((M + 10, y + 26, M + 20, y + 37, M + 35, y + 15), fill=rgb(t["bg"]), width=5)
        ln = wrap(text, fi, w - 2 * M - 80)
        y = text_block(d, (M + 76, y), ln, fi, fg if not done else muted, 1.3) + 34
    _counter(d, t, w, h, spec, muted)
    return img


def compare(spec, t):
    """Two columns: myth / fact, before / after, don't / do."""
    w, h = _size(spec)
    img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    if spec.get("title"):
        f, lines = fit_text(cased(spec["title"], t), t["head"], w - 2 * M, 2, 72)
        top = text_block(d, (M, M + 40), lines, f, fg, 1.12) + 50
    else:
        top = M + 40
    col = (w - 2 * M - 48) // 2
    fl, fb = font(t["head"], 46), font(t["body"], 46)
    for i, (label, body) in enumerate([spec["left"], spec["right"]]):
        x = M + i * (col + 48)
        colour = muted if i == 0 else acc
        d.text((x, top), cased(label, t), font=fl, fill=colour, anchor="lt")
        d.line((x, top + 64, x + col, top + 64), fill=colour, width=4)
        text_block(d, (x, top + 96), wrap(body, fb, col), fb, fg if i else muted, 1.4)
    _counter(d, t, w, h, spec, muted)
    return img


def steps(spec, t):
    """A short process: 3-5 numbered steps joined by a rule."""
    w, h = _size(spec)
    img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    f, lines = fit_text(cased(spec["title"], t), t["head"], w - 2 * M, 2, 76)
    y = text_block(d, (M, M + 40), lines, f, fg, 1.12) + 70
    items = spec["items"]
    gap = (h - y - M - 60) / len(items)
    fn, fi = font(t["num"], 44), font(t["body"], 40)
    d.line((M + 34, y + 34, M + 34, y + gap * (len(items) - 1) + 34), fill=muted, width=3)
    for i, item in enumerate(items):
        cy = y + i * gap
        d.ellipse((M, cy, M + 68, cy + 68), fill=acc)
        d.text((M + 34, cy + 34), str(i + 1), font=fn, fill=rgb(t["bg"]), anchor="mm")
        text_block(d, (M + 110, cy + 8), wrap(item, fi, w - 2 * M - 120), fi, fg, 1.3)
    _counter(d, t, w, h, spec, muted)
    return img


def bars(spec, t):
    """Horizontal bar chart, one highlighted bar, values labelled directly (no legend, no gridlines)."""
    w, h = _size(spec)
    img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    f, lines = fit_text(spec["title"], t["head"], w - 2 * M, 3, 68)
    y = text_block(d, (M, M + 40), lines, f, fg, 1.15) + 60
    data = spec["data"]  # [[label, value], ...]
    hi = spec.get("highlight")
    top = max(v for _, v in data)
    fl, fv = font(t["body"], 34), font(t["head"], 38)
    row = min(150, (h - y - M - 60) / len(data))
    for label, v in data:
        d.text((M, y), label, font=fl, fill=fg, anchor="lt")
        bw = (w - 2 * M - 160) * v / top
        d.rectangle((M, y + 48, M + bw, y + 48 + row * 0.32), fill=acc if label == hi else muted)
        d.text((M + bw + 18, y + 48 + row * 0.16), spec.get("fmt", "{}").format(v), font=fv, fill=fg, anchor="lm")
        y += row
    if spec.get("source"):
        d.text((M, h - M), "Source: " + spec["source"], font=font(t["body"], 26), fill=muted, anchor="ls")
    return img


def timeline(spec, t):
    w, h = _size(spec)
    img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    f, lines = fit_text(cased(spec["title"], t), t["head"], w - 2 * M, 2, 76)
    y = text_block(d, (M, M + 40), lines, f, fg, 1.12) + 60
    fd, fe = font(t["num"], 40), font(t["body"], 38)
    rows = spec["items"]  # [[when, what], ...]
    gap = (h - y - M) / len(rows)
    for i, (when, what) in enumerate(rows):
        cy = y + i * gap
        last = i == len(rows) - 1
        d.text((M, cy), when, font=fd, fill=acc if last else fg, anchor="lt")
        text_block(d, (M + 260, cy + 2), wrap(what, fe, w - 2 * M - 260), fe, fg if last else muted, 1.32)
        if not last:
            d.line((M + 230, cy + 10, M + 230, cy + gap - 10), fill=muted, width=2)
    return img


def code(spec, t):
    """Code on a card: mono, real syntax, at most ~14 lines, one highlighted line."""
    w, h = _size(spec)
    img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    f, lines = fit_text(cased(spec["title"], t), t["head"], w - 2 * M, 2, 64)
    y = text_block(d, (M, M + 30), lines, f, fg, 1.15) + 40
    fc = font("mono", 32)
    src = spec["code"].rstrip("\n").split("\n")
    card_h = len(src) * 46 + 70
    bg = rgb(t["bg"])
    card = tuple(min(255, c + 14) if sum(bg) < 380 else max(0, c - 10) for c in bg)
    d.rounded_rectangle((M - 10, y, w - M + 10, y + card_h), 18, fill=card)
    hl = spec.get("highlight", 0)
    for i, ln in enumerate(src):
        ly = y + 35 + i * 46
        if i + 1 == hl:
            d.rectangle((M - 10, ly - 6, w - M + 10, ly + 40), fill=tuple(int(a * 0.25 + b * 0.75) for a, b in zip(acc, card)))
        d.text((M + 20, ly), ln, font=fc, fill=fg if not ln.lstrip().startswith(("#", "//")) else muted)
    if spec.get("caption"):
        fb = font(t["body"], 38)
        text_block(d, (M, y + card_h + 40), wrap(spec["caption"], fb, w - 2 * M), fb, muted, 1.4)
    _counter(d, t, w, h, spec, muted)
    return img


def cta(spec, t):
    w, h = _size(spec)
    photo = spec.get("photo")
    img = background(t, (w, h), photo, spec.get("focus", (0.5, 0.5)), "bottom", strength=225, start=0.25)
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, bool(photo))
    f, lines = fit_text(cased(spec["ask"], t), t["head"], w - 2 * M, 3, 96)
    y = h - M - 110 - block_height(lines, f, 1.12)
    text_block(d, (M, y), lines, f, fg, 1.12)
    if spec.get("why"):
        d.text((M, h - M - 40), spec["why"], font=font(t["body"], 36), fill=acc, anchor="ls")
    _handle(d, t, w, h, {"handle": spec.get("handle")}, muted)
    return img


def text(spec, t):
    w, h = _size(spec)
    img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    y = M + 60
    if spec.get("title"):
        f, lines = fit_text(cased(spec["title"], t), t["head"], w - 2 * M, 3, 80)
        y = text_block(d, (M, y), lines, f, fg, 1.12) + 50
    fb = font(t["body"], spec.get("body_size", 44))
    text_block(d, (M, y), wrap(spec["body"], fb, w - 2 * M), fb, fg if not spec.get("title") else muted, 1.45)
    _counter(d, t, w, h, spec, muted)
    return img


# ---------- standalone kinds ----------

def thumbnail(spec, t):
    """16:9, readable at 160 px wide: <= 4 words, one highlighted, subject on the other side."""
    spec = {"size": "16:9", **spec}
    w, h = _size(spec)
    side = spec.get("side", "left")
    photo = spec.get("photo")
    img = background(t, (w, h), photo, spec.get("focus", (0.7 if side == "left" else 0.3, 0.4)), None,
                     grade=spec.get("grade", "none"))
    if photo:
        mask = Image.linear_gradient("L").rotate(90 if side == "left" else -90).resize((w, h))
        img = Image.composite(img, Image.new("RGB", (w, h), (10, 10, 12)), mask.point(lambda v: min(255, int(v * 1.6))))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, bool(photo) or sum(rgb(t["bg"])) < 380)
    hi = spec.get("highlight", "")
    f, lines = fit_text(cased(spec["words"], t), t["head"], int(w * 0.52), 3, 150, 60)
    bh = block_height(lines, f, 1.02)
    x = 70 if side == "left" else w - 70
    y = (h - bh) / 2
    for ln in lines:
        cx = x
        parts = ln.split()
        if side == "right":
            cx = x - f.getlength(ln)
        for p in parts:
            colour = acc if hi and p.lower().strip(".,!?") == hi.lower() else fg
            d.text((cx, y), p, font=f, fill=colour)
            cx += f.getlength(p + " ")
        y += int(f.size * 1.02)
    return img


def testimonial(spec, t):
    spec = {"size": "1:1", **spec}
    w, h = _size(spec)
    img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    fq, lines = fit_text("“" + spec["text"] + "”", t["head"] if "serif" in t["head"] else "serif", w - 2 * M, 6, 64)
    y = text_block(d, (M, M + 60), lines, fq, fg, 1.3) + 60
    if spec.get("photo"):
        img.paste(av := circle(_photo(spec["photo"]), 120), (M, int(y)), av)
        nx = M + 150
    else:
        nx = M
    d.text((nx, y + 22), spec["name"], font=font(t["head"], 40), fill=fg, anchor="lt")
    d.text((nx, y + 74), spec.get("role", ""), font=font(t["body"], 32), fill=muted, anchor="lt")
    if spec.get("result"):
        d.text((M, h - M), spec["result"], font=font(t["head"], 34), fill=acc, anchor="ls")
    return img


def postcard(spec, t):
    """A text post as an image: avatar, name, handle, the post, a quiet timestamp. No platform logos."""
    spec = {"size": "4:5", **spec}
    w, h = _size(spec)
    img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    bg = rgb(t["bg"])
    card = (255, 255, 255) if sum(bg) > 380 else tuple(min(255, c + 18) for c in bg)
    tfg = (20, 20, 22) if sum(card) > 380 else (240, 240, 240)
    tmuted = (110, 112, 118) if sum(card) > 380 else (150, 150, 155)
    fb = font("sans", 46)
    body = wrap(spec["text"], fb, w - 2 * M - 80)
    ch = 200 + block_height(body, fb, 1.4) + 110
    y0 = (h - ch) / 2
    d.rounded_rectangle((M - 20, y0, w - M + 20, y0 + ch), 36, fill=card)
    ax = M + 30
    if spec.get("photo"):
        img.paste(av := circle(_photo(spec["photo"]), 96), (ax, int(y0 + 40)), av)
    else:
        d.ellipse((ax, y0 + 40, ax + 96, y0 + 136), fill=acc)
        d.text((ax + 48, y0 + 88), spec["name"][:1], font=font("sans-bold", 48), fill=(255, 255, 255), anchor="mm")
    d.text((ax + 122, y0 + 50), spec["name"], font=font("sans-bold", 38), fill=tfg, anchor="lt")
    d.text((ax + 122, y0 + 100), spec.get("handle", ""), font=font("sans", 32), fill=tmuted, anchor="lt")
    y = text_block(d, (ax, y0 + 180), body, fb, tfg, 1.4)
    d.text((ax, y + 40), spec.get("meta", ""), font=font("sans", 28), fill=tmuted, anchor="lt")
    return img


def poster(spec, t):
    """Event / announcement poster: the date is the hero, then what, then where. Optional photo band."""
    w, h = _size(spec)
    img = background(t, (w, h))
    fg, muted, acc = _colours(t, False)
    if spec.get("photo"):
        band = background(t, (w - 2 * M, int(h * spec.get("band", 0.36))), spec["photo"], spec.get("focus", (0.5, 0.5)), None,
                          grade=spec.get("grade", "duotone"))
        img.paste(band, (M, M))
        top = M + band.height + 50
    else:
        top = M + 40
    d = ImageDraw.Draw(img)
    fd, _ = fit_text(cased(spec["date"], t), t["num"], w - 2 * M, 1, 230, 80)
    d.text((M - 6, top), cased(spec["date"], t), font=fd, fill=acc, anchor="lt")
    y = top + fd.size * 1.05 + 10
    f, lines = fit_text(cased(spec["title"], t), t["head"], w - 2 * M, 3, 96)
    y = text_block(d, (M, y), lines, f, fg, 1.08) + 30
    fb = font(t["body"], 38)
    for ln in spec.get("details", []):
        d.text((M, y), ln, font=fb, fill=muted, anchor="lt")
        y += 54
    if spec.get("footer"):
        ry = max(y + 10, h - M - 60)
        d.line((M, ry, w - M, ry), fill=fg, width=3)
        d.text((M, ry + 60), spec["footer"], font=font(t["body"], 30), fill=fg, anchor="ls")
    return img


def statement(spec, t):
    """One huge sentence edge to edge; one word in the accent. Brutalist / editorial covers."""
    w, h = _size(spec)
    if spec.get("photo"):
        # dots in a tint between paper and ink, so the full-strength type always sits on top
        tint = tuple(int(a * 0.3 + b * 0.7) for a, b in zip(rgb(t["fg"]), rgb(t["bg"])))
        img = fit(_photo(spec["photo"]), w, h, *spec.get("focus", (0.5, 0.5)))
        img = halftone(img, 12, tint, t["bg"]) if spec.get("grade", "halftone") == "halftone" else duotone(img, tint, t["bg"])
    else:
        img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    f, lines = fit_text(cased(spec["text"], t), t["head"], w - 2 * M + 20, spec.get("max_lines", 6), 190, 60)
    hi = cased(spec.get("highlight", ""), t)
    y = h - M - 60 - block_height(lines, f, 1.0) if spec.get("bottom", True) else M + 60
    for ln in lines:
        x = M - 6
        for p in ln.split():
            d.text((x, y), p, font=f, fill=acc if hi and p.strip(".,!?") == hi else fg)
            x += f.getlength(p + " ")
        y += int(f.size * 1.0)
    if spec.get("label"):
        d.text((M, M), cased(spec["label"], t, "body"), font=font(t["body"], 30), fill=fg, anchor="lt")
        d.text((w - M, M), spec.get("label_right", ""), font=font(t["body"], 30), fill=fg, anchor="rt")
    return img


def cover_magazine(spec, t):
    """Editorial cover: full-bleed photo, masthead top, one cover line, issue line. Photo carries it."""
    w, h = _size(spec)
    img = background(t, (w, h), spec["photo"], spec.get("focus", (0.5, 0.4)), "bottom", strength=190, start=0.5)
    d = ImageDraw.Draw(img)
    fm, _ = fit_text(spec["masthead"], t["head"], w - 2 * M, 1, 230, 80)
    d.text((w / 2, M - 20), spec["masthead"], font=fm, fill=(250, 248, 244), anchor="mt")
    d.text((w / 2, M + fm.size + 10), spec.get("issue", ""), font=font(t["body"], 28), fill=(230, 226, 220), anchor="mt")
    f, lines = fit_text(spec["line"], t["head"], w - 2 * M, 3, 88)
    y = h - M - 40 - block_height(lines, f, 1.1)
    text_block(d, (M, y), lines, f, (250, 248, 244), 1.1)
    if spec.get("sub"):
        d.text((M, h - M), spec["sub"], font=font(t["body"], 32), fill=rgb(t["accent"]) if t["id"] != "editorial" else (255, 214, 170), anchor="ls")
    return img


def split(spec, t):
    """Before / after or this vs that: two photos side by side (or stacked), labels in plain boxes."""
    w, h = _size(spec)
    vertical = spec.get("stack", h > w * 1.4)
    img = Image.new("RGB", (w, h), rgb(t["bg"]))
    d = ImageDraw.Draw(img)
    fl = font(t["head"], 44 if w > 1000 else 36)
    halves = [spec["left"], spec["right"]]
    for i, half in enumerate(halves):
        if vertical:
            box = (0, i * h // 2, w, (i + 1) * h // 2)
        else:
            box = (i * w // 2, 0, (i + 1) * w // 2, h)
        bw, bh = box[2] - box[0], box[3] - box[1]
        ph = fit(_photo(half["photo"]), bw, bh, *half.get("focus", (0.5, 0.5)))
        if half.get("grade") == "flat":
            from PIL import ImageEnhance
            ph = ImageEnhance.Color(ImageEnhance.Contrast(ph).enhance(0.7)).enhance(0.35)
        img.paste(ph, box[:2])
        label = cased(half["label"], t)
        lw = fl.getlength(label)
        lx, ly = box[0] + 40, box[3] - 40 - fl.size - 24
        d.rectangle((lx, ly, lx + lw + 40, ly + fl.size + 28), fill=rgb(t["accent"]) if i else (20, 20, 22))
        d.text((lx + 20, ly + 14), label, font=fl, fill=(255, 255, 255), anchor="lt")
    if vertical:
        d.line((0, h // 2, w, h // 2), fill=rgb(t["bg"]), width=8)
    else:
        d.line((w // 2, 0, w // 2, h), fill=rgb(t["bg"]), width=8)
    if spec.get("title"):
        ft = font(t["head"], 64 if w > 1000 else 48)
        tw = ft.getlength(spec["title"])
        d.rectangle(((w - tw) / 2 - 30, 50, (w + tw) / 2 + 30, 60 + ft.size + 30), fill=rgb(t["bg"]))
        d.text((w / 2, 68), spec["title"], font=ft, fill=rgb(t["fg"]), anchor="mt")
    return img


def story(spec, t):
    """9:16 story: text kept out of the top 250 px (profile bar) and bottom 340 px (reply bar).
    Optional reserved area for a sticker (poll, link, countdown) the app adds on top."""
    spec = {"size": "9:16", **spec}
    w, h = _size(spec)
    photo = spec.get("photo")
    img = background(t, (w, h), photo, spec.get("focus", (0.5, 0.5)), "top", strength=200, start=0.35)
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, bool(photo))
    y = 300
    if spec.get("kicker"):
        d.text((M, y), cased(spec["kicker"], t, "body"), font=font(t["body"], 38), fill=acc, anchor="lt")
        y += 70
    f, lines = fit_text(cased(spec["title"], t), t["head"], w - 2 * M, 4, 110)
    y = text_block(d, (M, y), lines, f, fg, 1.1) + 30
    if spec.get("body"):
        fb = font(t["body"], 44)
        y = text_block(d, (M, y), wrap(spec["body"], fb, w - 2 * M), fb, fg if photo else muted, 1.4)
    if spec.get("sticker"):
        sy = max(y + 80, h * 0.55)
        box = (M + 40, sy, w - M - 40, sy + spec.get("sticker_h", 300))
        if spec.get("guides", True):
            for x0 in range(int(box[0]), int(box[2]), 36):
                d.line((x0, box[1], min(x0 + 18, box[2]), box[1]), fill=muted, width=3)
                d.line((x0, box[3], min(x0 + 18, box[2]), box[3]), fill=muted, width=3)
            d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), spec["sticker"], font=font(t["body"], 34),
                   fill=muted, anchor="mm")
    if spec.get("countdown"):
        fn = font(t["num"], 260)
        d.text((M - 10, h - 340 - 40), spec["countdown"], font=fn, fill=acc, anchor="ls")
    return img


def endscreen(spec, t):
    """YouTube end screen (16:9, last 5-20 s): leave the element zones empty, say one thing to watch next."""
    spec = {"size": "16:9", **spec}
    w, h = _size(spec)
    img = background(t, (w, h), spec.get("photo"), where=None, grade="film")
    if spec.get("photo"):
        img = Image.blend(img, Image.new("RGB", (w, h), rgb(t["bg"])), 0.72)
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    if sum(rgb(t["bg"])) < 380:
        fg, muted = (244, 244, 244), (170, 172, 178)
    f, lines = fit_text(spec["line"], t["head"], w - 160, 2, 64)
    text_block(d, (80, 70), lines, f, fg, 1.12)
    zones = [("video", (80, 300, 620, 604)), ("video", (660, 300, 1200, 604))]
    if spec.get("subscribe", True):
        zones = [("video", (80, 300, 560, 570)), ("video", (600, 300, 1080, 570)), ("subscribe", (1100, 380, 1210, 490))]
    for label, (x0, y0, x1, y1) in zones:
        if label == "subscribe":
            d.ellipse((x0, y0, x1, y1), outline=muted, width=3)
        else:
            d.rounded_rectangle((x0, y0, x1, y1), 14, outline=muted, width=3)
        if spec.get("guides", True):
            d.text(((x0 + x1) / 2, (y0 + y1) / 2), label, font=font(t["body"], 26), fill=muted, anchor="mm")
    return img


def grid(spec, t):
    """Recap grid: 2x2 or 3x2 real photos with thin gutters and one caption bar."""
    w, h = _size(spec)
    photos = spec["photos"]
    cols = spec.get("cols", 2)
    rows = (len(photos) + cols - 1) // cols
    g = 10
    cap_h = 200 if spec.get("caption") else 0
    img = Image.new("RGB", (w, h), rgb(t["bg"]))
    cw, chh = (w - g * (cols + 1)) // cols, (h - cap_h - g * (rows + 1)) // rows
    for i, p in enumerate(photos):
        r, c = divmod(i, cols)
        img.paste(film(fit(_photo(p), cw, chh)), (g + c * (cw + g), g + r * (chh + g)))
    if cap_h:
        d = ImageDraw.Draw(img)
        fg, muted, acc = _colours(t, False)
        d.text((M - 40, h - cap_h / 2 - 20), cased(spec["caption"], t), font=font(t["head"], 64), fill=fg, anchor="lm")
        if spec.get("sub"):
            d.text((M - 40, h - cap_h / 2 + 40), spec["sub"], font=font(t["body"], 32), fill=acc, anchor="lm")
    return img


def speaker(spec, t):
    """Speaker or guest card: face uncropped on one side, name big, talk title, time."""
    w, h = _size(spec)
    img = background(t, (w, h))
    ph = film(fit(_photo(spec["photo"]), w, int(h * 0.56), *spec.get("focus", (0.5, 0.3))))
    img.paste(ph, (0, 0))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    y = int(h * 0.56) + 50
    d.text((M, y), cased(spec.get("label", "Speaker"), t, "body"), font=font(t["body"], 32), fill=acc, anchor="lt")
    f, lines = fit_text(cased(spec["name"], t), t["head"], w - 2 * M, 2, 104)
    y = text_block(d, (M, y + 50), lines, f, fg, 1.05) + 20
    fb = font(t["body"], 40)
    y = text_block(d, (M, y), wrap(spec["talk"], fb, w - 2 * M), fb, muted, 1.35)
    if spec.get("when"):
        d.text((M, h - M), spec["when"], font=font(t["num"], 44), fill=fg, anchor="ls")
    return img


def menu(spec, t):
    """Board for a café or shop: item names left, prices right, dotted leaders, one note at the bottom."""
    w, h = _size(spec)
    img = background(t, (w, h))
    d = ImageDraw.Draw(img)
    fg, muted, acc = _colours(t, False)
    f = font(t["head"], 96)
    d.text((M, M + 20), cased(spec["title"], t), font=f, fill=fg, anchor="lt")
    y = M + 180
    fi, fp, fs = font(t["head"], 46), font(t["body"], 42), font(t["body"], 30)
    fx = font("sans-ext", 42)
    for name, price, *note in spec["items"]:
        d.text((M, y), name, font=fi, fill=fg, anchor="ls")
        sym = "".join(ch for ch in price if ord(ch) > 0x24F)  # outside Latin: currency signs like ₹
        num = price.replace(sym, "") if sym else price
        d.text((w - M, y), num, font=fp, fill=fg, anchor="rs")
        pw = fp.getlength(num)
        if sym:
            d.text((w - M - pw - 4, y), sym, font=fx, fill=fg, anchor="rs")
            pw += fx.getlength(sym) + 4
        x0, x1 = M + fi.getlength(name) + 20, w - M - pw - 20
        for x in range(int(x0), int(x1), 18):
            d.ellipse((x, y - 10, x + 4, y - 6), fill=muted)
        if note:
            d.text((M, y + 14), note[0], font=fs, fill=muted, anchor="lt")
            y += 46
        y += 110
    if spec.get("footer"):
        d.text((M, h - M), spec["footer"], font=fs, fill=acc, anchor="ls")
    return img


KINDS = {f.__name__: f for f in (cover, point, number, quote, checklist, compare, steps, bars, timeline, code, cta,
                                  text, thumbnail, testimonial, postcard, poster, statement, cover_magazine, split,
                                  story, endscreen, grid, speaker, menu)}
