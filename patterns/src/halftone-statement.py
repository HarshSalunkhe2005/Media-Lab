"""Halftone statement: One blunt sentence over a dot-halftone photo, one word in the accent: print texture without a filter-app look.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"statement","theme":"retro-print","text":"Make the thing before the logo.","highlight":"THING","photo":ph("desk"),"label":"Studio notes","label_right":"No. 07","max_lines":4}


def render(out: Path) -> Path:
    return from_spec("halftone-statement", SPEC, out)
