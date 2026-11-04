"""This vs that: Two photos split down the middle with one-word labels: a comparison readable at 160 px.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"split","theme":"tech-launch","size":"16:9","left":{"label":"Cloud","photo":ph("street")},"right":{"label":"Local","photo":ph("desk")}}


def render(out: Path) -> Path:
    return from_spec("thumb-versus", SPEC, out)
