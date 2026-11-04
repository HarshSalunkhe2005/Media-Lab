"""Myth / fact columns: Two columns with one label each: the wrong belief dimmed on the left, the correction in the accent on the right.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"compare","theme":"explainer","title":"Captions","left":["Myth","Bigger captions are always easier to read."],"right":["Fact","Readable at arm's length and clear of the app's buttons beats big."],"_index":3,"_total":8}


def render(out: Path) -> Path:
    return from_spec("myth-fact-compare", SPEC, out)
