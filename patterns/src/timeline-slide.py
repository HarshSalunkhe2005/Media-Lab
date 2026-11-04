"""Timeline slide: Dates in the number face, events beside them, the latest row in the accent: a build or history recap on one slide.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"timeline","theme":"build-log","title":"Six weeks, one sorter","items":[["week 1","paper sketch, no code"],["week 2","hash-based duplicate finder"],["week 4","first stranger used it"],["week 6","public launch, 212 duplicates on day one"]]}


def render(out: Path) -> Path:
    return from_spec("timeline-slide", SPEC, out)
