"""Text story in the safe area: A plain-surface story where every line sits between y 300 and 1500, so no profile bar or reply box covers it.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"story","theme":"editorial","kicker":"Studio update","title":"We are closed this Friday","body":"Back Saturday at 8 with a new bun. Orders placed before Thursday still go out on time."}


def render(out: Path) -> Path:
    return from_spec("story-text-safe", SPEC, out)
