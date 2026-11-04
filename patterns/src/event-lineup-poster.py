"""Lineup poster: Date hero, event title, the lineup as plain lines, venue in the footer: the one poster that gets screenshotted.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"poster","theme":"campus-event","date":"19-21 JAN","title":"Northfield Spring Fest","details":["Fri  ·  battle of bands, open mic","Sat  ·  3x3 basketball finals","Sun  ·  food street, closing set"],"footer":"Northfield College grounds · fictional event"}


def render(out: Path) -> Path:
    return from_spec("event-lineup-poster", SPEC, out)
