"""Caption style: 3-word chunks, uppercase, white with the spoken word in yellow and slightly larger. The Shorts default."""
from pathlib import Path

from _captions_common import burn, default_ass


def render(out: Path) -> Path:
    return burn(default_ass(), out / "caption-word-highlight.jpg")
