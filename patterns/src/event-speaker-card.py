"""Speaker card: Face uncropped in the top half, a small label, the name big, the talk title and the slot.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"speaker","theme":"tech-launch","label":"Speaker","name":"Dev Malhotra","talk":"What we learned shipping an offline-first app to 40 care homes","when":"Hall B · 11:30","photo":ph("player"),"focus":[0.5,0.2]}


def render(out: Path) -> Path:
    return from_spec("event-speaker-card", SPEC, out)
