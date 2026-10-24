"""Caption style for quiet content: lowercase serif, no highlight or pop, soft shadow only. For poetry and slow vlogs."""
from pathlib import Path

from _captions_common import burn, default_ass


def render(out: Path) -> Path:
    ass = default_ass(font="Garamond", size=72, chunk=4, color="&H00F0F0F0", highlight="&H00F0F0F0", upper=False)
    ass = ass.replace(",-1,0,0,0,100,100,0,0,1,6,2,2,", ",0,0,0,0,100,100,0,0,1,0,3,2,").replace("\\fscx108\\fscy108", "")
    return burn(ass, out / "caption-quiet-lowercase.jpg", photo="rain")
