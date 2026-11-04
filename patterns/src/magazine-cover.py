"""Magazine cover: Full-bleed photo, a centred masthead, one cover line low in the frame, the issue line small.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"cover_magazine","theme":"editorial","masthead":"TIDEWATER","issue":"No. 12 · Winter · fictional","line":"The quiet return of the paper zine","sub":"Plus: six shops worth the train","photo":ph("coffee"),"focus":[0.5,0.5]}


def render(out: Path) -> Path:
    return from_spec("magazine-cover", SPEC, out)
