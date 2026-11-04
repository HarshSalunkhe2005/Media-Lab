"""Story with link space: Photo darkened at the top for the line, the middle left calm for the link sticker, one reason to tap.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"story","theme":"tech-launch","kicker":"New today","title":"The sorter is live","body":"Free for the first 1,000 photos.","sticker":"link sticker goes here","sticker_h":200,"photo":ph("desk"),"focus":[0.5,0.6]}


def render(out: Path) -> Path:
    return from_spec("story-link-space", SPEC, out)
