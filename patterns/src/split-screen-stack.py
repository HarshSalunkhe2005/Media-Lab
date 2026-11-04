"""Stacked split screen: Two sources stacked, each filling half the frame: the thing on top, the result or reaction underneath.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"splitscreen","theme":"explainer","top":ph("desk"),"bottom":ph("coffee"),"duration":3}


def render(out: Path) -> Path:
    return from_spec("split-screen-stack", SPEC, out)
