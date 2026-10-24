"""Caption style: opaque black box behind each chunk (ASS BorderStyle 3). Most readable on busy footage."""
from pathlib import Path

from _captions_common import burn, default_ass


def render(out: Path) -> Path:
    ass = default_ass(highlight="&H00FFFFFF").replace(",-1,0,0,0,100,100,0,0,1,6,2,2,", ",-1,0,0,0,100,100,0,0,3,14,0,2,")
    ass = ass.replace("&H64000000", "&H00000000")
    return burn(ass, out / "caption-boxed.jpg", photo="desk")
