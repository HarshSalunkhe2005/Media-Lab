"""Picture-in-picture inset: Main source full frame, a small rounded inset (face or detail) in the lower half, clear of the action column.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"pip","theme":"tech-launch","main":ph("street"),"inset":ph("player"),"duration":3}


def render(out: Path) -> Path:
    return from_spec("pip-inset", SPEC, out)
