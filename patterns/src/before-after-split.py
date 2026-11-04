"""Before / after split: The same subject twice, stacked, with plain label boxes: the change is the content, nothing else competes.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"split","theme":"explainer","stack":True,"title":"Same photo, one grade","left":{"label":"Before","photo":ph("leaves"),"grade":"flat"},"right":{"label":"After","photo":ph("leaves")}}


def render(out: Path) -> Path:
    return from_spec("before-after-split", SPEC, out)
