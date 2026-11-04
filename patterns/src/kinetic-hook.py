"""Kinetic text hook: The hook line lands word by word on a darkened photo, the key number in the accent, then holds.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"kinetic","theme":"tech-launch","text":"I deleted 212 duplicate photos in one click","highlight":["212"],"photo":ph("desk"),"beat":0.3,"hold":1.2}


def render(out: Path) -> Path:
    return from_spec("kinetic-hook", SPEC, out)
