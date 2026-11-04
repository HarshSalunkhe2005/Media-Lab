"""Package the skill for upload (Agensi, manual install): release/media-lab-skill-<version>.zip.

Validates before zipping: SKILL.md frontmatter, description length, every path SKILL.md mentions exists,
the CLI imports, and the zip stays small. Fails loudly instead of shipping a broken skill.
Run: python tools/build_skill.py
"""
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins" / "media-lab" / "skills" / "media-lab"
VERSION = json.loads((ROOT / "plugins" / "media-lab" / ".claude-plugin" / "plugin.json").read_text())["version"]
MAX_MB = 5


def fail(msg):
    sys.exit(f"build_skill: {msg}")


def main():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"---\nname: ([a-z0-9-]+)\ndescription: (.+?)\n---\n", text, re.S)
    if not m:
        fail("SKILL.md needs frontmatter with name and description")
    if len(m.group(2)) > 1024:
        fail(f"description is {len(m.group(2))} chars; keep it under 1024")
    if len(text.splitlines()) > 500:
        fail("SKILL.md over 500 lines; move detail into reference files")
    for ref in sorted(set(re.findall(r"`((?:playbook|formats|hooks|recipes|scripts|assets|examples)/[\w./-]+)`", text))):
        if not (SKILL / ref.rstrip("/")).exists():
            fail(f"SKILL.md mentions {ref}, which does not exist")
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "medialab"), "kinds"], capture_output=True, text=True)
    if r.returncode:
        fail("CLI does not run:\n" + r.stderr)

    out = ROOT / "release" / f"media-lab-skill-{VERSION}.zip"
    out.parent.mkdir(exist_ok=True)
    files = sorted(p for p in SKILL.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, Path("media-lab") / p.relative_to(SKILL))
    mb = out.stat().st_size / 1e6
    if mb > MAX_MB:
        fail(f"zip is {mb:.1f} MB (limit {MAX_MB})")
    print(f"{out.relative_to(ROOT)}  {len(files)} files, {mb:.2f} MB")


if __name__ == "__main__":
    main()
