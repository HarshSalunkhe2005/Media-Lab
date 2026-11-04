"""Checklist slide: A titled checklist with drawn boxes, done items dimmed, so the slide reads as a tool people save.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"checklist","theme":"explainer","title":"Before you hit export","items":["[x] First frame is the hook","[x] Captions sit above y = 1400","[ ] Loudness near -14 LUFS","[ ] Watched once on a phone, sound on"],"_index":4,"_total":7}


def render(out: Path) -> Path:
    return from_spec("checklist-slide", SPEC, out)
