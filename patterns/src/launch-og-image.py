"""Link preview image: The card that shows when a link is shared: product name, one line on what it does, the URL, no tiny text.

Spec-driven: the same dict works with `python scripts/medialab make spec.json` (swap ph() for your own paths).
"""
from pathlib import Path

from lib import from_spec, ph  # noqa: F401

SPEC = {"kind":"cover","theme":"tech-launch","size":"og","kicker":"photo-sorter.app (fictional)","title":"Find every duplicate photo in one click","max_lines":2}


def render(out: Path) -> Path:
    return from_spec("launch-og-image", SPEC, out)
