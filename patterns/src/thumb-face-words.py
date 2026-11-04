"""Subject + three words: Subject on one side fading into dark, three heavy words on the other, one of them in the accent.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"thumbnail","theme":"explainer","words":"I quit editing","highlight":"quit","photo":ph("rain"),"side":"left","focus":[0.75,0.4]}


def render(out: Path) -> Path:
    return from_spec("thumb-face-words", SPEC, out)
