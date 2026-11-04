"""Countdown list: 3, 2, 1: one item per beat, the rank huge in the accent, the item under it, number one last.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"countdown","theme":"explainer","items":["Name exports by date","Batch your renders overnight","Delete the drafts you will never open"],"seconds_per_item":1.4}


def render(out: Path) -> Path:
    return from_spec("countdown-list-short", SPEC, out)
