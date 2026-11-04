"""Beat-cut photo slideshow: Real photos with a slow push, hard-cut every two beats at a set BPM; lay your track under it.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"beatcut","theme":"campus-event","photos":[ph("courtaerial"),ph("player"),ph("street"),ph("coffee")],"bpm":128,"beats_per_cut":2}


def render(out: Path) -> Path:
    return from_spec("beat-cut-slideshow", SPEC, out)
