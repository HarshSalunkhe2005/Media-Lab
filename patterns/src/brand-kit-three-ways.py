"""Brand kit: one spec, three brand.json files, three accounts that each look like themselves.
Colours, fonts, handle and logo come from the kit; the words and layout come from the spec."""
from pathlib import Path

from PIL import Image

from lib import SCRIPTS, build, save_jpg

KITS = SCRIPTS.parent / "examples" / "brand"
SPEC = {"kind": "point", "n": 3, "title": "Post the hours on every post",
        "body": "People screenshot the slide, not the bio. Put the one fact they need where they will look.",
        "_index": 4, "_total": 7}


def render(out: Path) -> Path:
    tmp = out / "_brand_tmp"
    tiles = []
    for kit in ("fern", "lowtide", "pier"):
        p = build({**SPEC, "brand": str(KITS / f"{kit}.json")}, tmp / f"{kit}.png")[0]
        with Image.open(p) as im:
            tiles.append(im.convert("RGB"))
        p.unlink()
    tmp.rmdir()
    g = 40
    w, h = tiles[0].size
    sheet = Image.new("RGB", (3 * w + 4 * g, h + 2 * g), (226, 229, 234))
    for i, t in enumerate(tiles):
        sheet.paste(t, (g + i * (w + g), g))
    return save_jpg(sheet, out / "brand-kit-three-ways.jpg", preview_width=960)
