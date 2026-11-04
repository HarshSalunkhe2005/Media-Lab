"""Café menu board: Items left, prices right, dotted leaders, one small note per item, opening hours in the accent.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"menu","theme":"warm-local","title":"This week","items":[["Cardamom bun","₹140","baked at 7, gone by 11"],["Flat white","₹180"],["Filter coffee","₹90","served in a steel tumbler"],["Banana bread","₹120"]],"footer":"Open 8 to 6 · closed Mondays · Fern Café (fictional)"}


def render(out: Path) -> Path:
    return from_spec("cafe-menu-board", SPEC, out)
