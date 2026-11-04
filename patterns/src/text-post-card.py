"""Text post as an image: A short written post set on a card with avatar, name and a quiet timestamp, without any platform's logo or chrome.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"postcard","theme":"explainer","name":"Noor Patel","handle":"@noorbuilds","text":"Shipped the smallest version today. Two people used it. Both found the same bug in the first minute, which is the best news I have had all week.","meta":"9:41 pm · Tuesday"}


def render(out: Path) -> Path:
    return from_spec("text-post-card", SPEC, out)
