"""Progress bar: A thin bar just below the top UI zone fills over the video, so viewers see how much is left.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"progress","theme":"explainer","photos":[ph("coffee"),ph("leaves"),ph("street")],"seconds_per_photo":1.6}


def render(out: Path) -> Path:
    return from_spec("progress-bar-short", SPEC, out)
