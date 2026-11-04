"""Three-step process: Numbered dots on one rule, one short line each: a process that fits on one slide without a diagram tool.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"steps","theme":"soft-pastel","title":"How we cut a Short","items":["Write the payoff line first","Film the payoff before anything else","Cut backwards until the hook is the first frame","Watch it muted, then with sound"],"_index":2,"_total":6}


def render(out: Path) -> Path:
    return from_spec("process-steps", SPEC, out)
