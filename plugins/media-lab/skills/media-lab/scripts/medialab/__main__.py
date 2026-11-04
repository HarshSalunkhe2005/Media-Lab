"""CLI: python scripts/medialab <command>. Run with no arguments for help."""
from __future__ import annotations

import argparse
import inspect
import json
import sys
from pathlib import Path

if __package__ in (None, ""):  # `python scripts/medialab ...` runs this file directly
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "medialab"

from medialab import __version__, stills, video  # noqa: E402
from medialab.check import PLATFORMS, check, report  # noqa: E402
from medialab.examples import EXAMPLES  # noqa: E402
from medialab.make import build, load  # noqa: E402
from medialab.themes import THEMES  # noqa: E402


def _doc(fn):
    return (inspect.getdoc(fn) or "").split("\n")[0]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="medialab", description="Build social/video content from a spec, then check it.")
    ap.add_argument("--version", action="version", version=__version__)
    sub = ap.add_subparsers(dest="cmd")
    m = sub.add_parser("make", help="render a spec file (JSON or YAML)")
    m.add_argument("spec")
    m.add_argument("-o", "--out", help="output file, or folder for a carousel (default: next to the spec)")
    c = sub.add_parser("check", help="pre-publish checks for an image or video")
    c.add_argument("file")
    c.add_argument("--platform", "-p", required=True, choices=sorted(PLATFORMS))
    c.add_argument("--json", action="store_true")
    sub.add_parser("kinds", help="list every kind a spec can use")
    sub.add_parser("themes", help="list themes (one per world)")
    e = sub.add_parser("example", help="print a starter spec for a kind")
    e.add_argument("kind")
    a = ap.parse_args(argv)

    if a.cmd == "make":
        spec = load(a.spec)
        src = Path(a.spec)
        default = src.with_suffix("") if spec.get("kind") == "carousel" else src.with_suffix(".mp4" if spec.get("kind") in video.KINDS else ".png")
        for p in build(spec, a.out or default, base=src.parent):
            print(p)
        return 0
    if a.cmd == "check":
        res = check(a.file, a.platform)
        print(report(a.file, a.platform, res, a.json))
        return 1 if any(r.status == "FAIL" for r in res) else 0
    if a.cmd == "kinds":
        print("stills:")
        for k, fn in stills.KINDS.items():
            print(f"  {k:15s} {_doc(fn)}")
        print("video:")
        for k, fn in video.KINDS.items():
            print(f"  {k:15s} {_doc(fn)}")
        print("  carousel        a list of still slides (+ optional PDF for LinkedIn documents)")
        return 0
    if a.cmd == "themes":
        for k, t in THEMES.items():
            print(f"  {k:15s} head={t['head']:20s} accent={t['accent']}")
        return 0
    if a.cmd == "example":
        if a.kind not in EXAMPLES:
            print(f"no example for {a.kind!r}; one of: {', '.join(EXAMPLES)}", file=sys.stderr)
            return 2
        print(json.dumps(EXAMPLES[a.kind], indent=2, ensure_ascii=False))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
