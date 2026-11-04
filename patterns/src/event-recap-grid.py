"""Recap grid: Four real photos from the day in a tight grid with one caption bar: the whole event in one post.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"grid","theme":"campus-event","photos":[ph("courtaerial"),ph("player"),ph("street"),ph("coffee")],"caption":"Day 2 in four frames","sub":"Full gallery at the link in bio"}


def render(out: Path) -> Path:
    return from_spec("event-recap-grid", SPEC, out)
