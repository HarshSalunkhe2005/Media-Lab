"""Retro print poster: Duotone photo band, the date as the hero in a heavy face, what and where below, a ruled footer.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"poster","theme":"retro-print","date":"Sat 14 Dec","title":"Night market on Pier Road","details":["6 pm to midnight","40 stalls · live brass band"],"footer":"Free entry · Pier Road car park (fictional)","photo":ph("street"),"focus":[0.5,0.55]}


def render(out: Path) -> Path:
    return from_spec("retro-event-poster", SPEC, out)
