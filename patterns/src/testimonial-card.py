"""Customer testimonial: The customer's words big, their face small and round, name and role, one measured result in the accent.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"testimonial","theme":"warm-local","text":"We stopped guessing which posts would work. Now we plan two a week and both get saved.","name":"Ira Velasco","role":"Owner, Fern Café (fictional)","result":"3x saves in the first month","photo":ph("player")}


def render(out: Path) -> Path:
    return from_spec("testimonial-card", SPEC, out)
