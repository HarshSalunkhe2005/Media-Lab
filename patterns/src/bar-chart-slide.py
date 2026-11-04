"""One-highlight bar chart: Horizontal bars labelled directly, one bar in the accent, no legend or gridlines, source at the bottom.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"bars","theme":"data-story","title":"Where readers stopped swiping","data":[["Slide 1",100],["Slide 2",64],["Slide 3",51],["Slide 5",38],["Last slide",29]],"highlight":"Slide 2","fmt":"{}%","source":"Tidewater reader panel, n=212 (fictional data)"}


def render(out: Path) -> Path:
    return from_spec("bar-chart-slide", SPEC, out)
