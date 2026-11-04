"""Code on a card: A short real snippet in mono on a raised card, one line highlighted, one sentence on why it matters.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"code","theme":"build-log","title":"the one-line fix","code":"# before: one disk read per file\nfor f in files:\n    load(f)\n\n# after: one batched read\nload_many(files)","highlight":6,"caption":"Batching cut cold start from 9 s to 2 s on a 4,000-photo folder.","_index":3,"_total":5}


def render(out: Path) -> Path:
    return from_spec("code-card-slide", SPEC, out)
