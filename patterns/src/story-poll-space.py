"""Story with poll space: Question at the top of the safe area, empty dashed space where the app's poll sticker goes, nothing under the reply bar.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"story","theme":"soft-pastel","kicker":"Quick one","title":"Which should we post first?","body":"Two drafts, both finished. You pick.","sticker":"poll sticker goes here"}


def render(out: Path) -> Path:
    return from_spec("story-poll-space", SPEC, out)
