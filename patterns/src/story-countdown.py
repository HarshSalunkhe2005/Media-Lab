"""Event countdown story: Real photo, the event and place at the top, the days-left number huge above the reply bar.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"story","theme":"campus-event","kicker":"Inter-college finals","title":"Court 2, north gym","body":"Tip-off 7 pm. Bring noise.","countdown":"3 days","photo":ph("courtaerial"),"focus":[0.5,0.5]}


def render(out: Path) -> Path:
    return from_spec("story-countdown", SPEC, out)
