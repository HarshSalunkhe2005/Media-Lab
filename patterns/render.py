"""Render every pattern preview into public/previews/ (or only the slugs given).

Usage: python patterns/render.py [slug ...]
Needs Pillow, ffmpeg on PATH, and edge-tts (+ internet) for the two short-* patterns.
"""
import importlib.util
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE / "src")]
OUT = HERE.parent / "public" / "previews"


def load(slug: str):
    spec = importlib.util.spec_from_file_location(slug.replace("-", "_"), HERE / "src" / f"{slug}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    slugs = sys.argv[1:] or sorted(p.stem for p in (HERE / "src").glob("*.py") if not p.stem.startswith("_"))
    failed = []
    for s in slugs:
        t = time.time()
        try:
            path = load(s).render(OUT)
            print(f"ok   {s:28s} {path.name} ({path.stat().st_size // 1024} KB, {time.time() - t:.1f}s)")
        except Exception as e:  # keep going, report at the end
            failed.append(s)
            print(f"FAIL {s}: {e}")
    sys.exit(1 if failed else 0)
