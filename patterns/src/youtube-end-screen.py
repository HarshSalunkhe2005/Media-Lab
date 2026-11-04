"""End screen layout: The last 5-20 s of a video: one line on what to watch next and empty zones where YouTube's elements sit.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"endscreen","theme":"tech-launch","line":"If the sorter saved you time, the build log is next","photo":ph("desk")}


def render(out: Path) -> Path:
    return from_spec("youtube-end-screen", SPEC, out)
