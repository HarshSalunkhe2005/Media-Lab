"""Brutalist statement: Black on white, one huge sentence set edge to edge, a single orange word, labels in mono in the corners.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"statement","theme":"brutalist-mono","text":"Nobody reads the caption first.","highlight":"FIRST.","label":"issue 04","label_right":"2026"}


def render(out: Path) -> Path:
    return from_spec("brutalist-statement", SPEC, out)
