"""Soft quote card: Square quote on a pale tint with a short accent rule: calm, readable, no quotation-mark clip art.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"quote","theme":"soft-pastel","size":"1:1","font":"sans-semibold","text":"You do not need a content calendar. You need one thing worth saying this week.","by":"from the Pebble Club newsletter"}


def render(out: Path) -> Path:
    return from_spec("quote-card-pastel", SPEC, out)
