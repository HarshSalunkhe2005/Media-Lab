"""Editorial pull quote: A pull quote on off-white in a display serif with a short accent rule above and the speaker under it.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"quote","theme":"editorial","font":"display-serif","text":"We kept the shop small on purpose. Small means I still know what every regular orders.","by":"Ira Velasco, Fern Café","_index":2,"_total":6}


def render(out: Path) -> Path:
    return from_spec("editorial-quote-slide", SPEC, out)
