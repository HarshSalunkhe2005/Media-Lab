"""Tests for the medialab package and CLI. Stdlib unittest; needs Pillow, plus ffmpeg/ffprobe for the video tests
(skipped without them). Run: python tools/test_medialab.py   (or npm test)
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins" / "media-lab" / "skills" / "media-lab"
PHOTOS = ROOT / "patterns" / "assets" / "photos"
sys.path.insert(0, str(SKILL / "scripts"))

from PIL import Image  # noqa: E402

from medialab import stills, video  # noqa: E402
from medialab.check import check  # noqa: E402
from medialab.core import FONT_DIR, FONTS, contrast_ratio, font, wrap  # noqa: E402
from medialab.examples import EXAMPLES  # noqa: E402
from medialab.make import build  # noqa: E402
from medialab.themes import SIZES, THEMES  # noqa: E402

HAS_FF = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))
PHOTO_LIST = sorted(str(p) for p in PHOTOS.glob("*.jpg"))
CLI = [sys.executable, str(SKILL / "scripts" / "medialab")]


def with_media(spec, tmp: Path):
    """Swap the example's placeholder file names for bundled photos (and a generated clip for audio)."""
    s = json.loads(json.dumps(spec))
    k = iter(PHOTO_LIST * 4)

    def sub(v):
        if isinstance(v, str) and v.endswith((".jpg", ".png")):
            return next(k)
        if isinstance(v, str) and v.endswith((".mp4", ".mov")):
            return next(k)  # photo stands in for a clip; builders turn photos into clips
        if isinstance(v, str) and v.endswith((".mp3", ".wav")):
            return str(tone(tmp))
        if isinstance(v, list):
            return [sub(x) for x in v]
        if isinstance(v, dict):
            return {a: sub(b) for a, b in v.items()}
        return v
    return {a: sub(b) for a, b in s.items()}


def tone(tmp: Path) -> Path:
    p = tmp / "tone.wav"
    if not p.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=f=220:d=2", str(p)], check=True)
    return p


def probe(path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,pix_fmt,codec_name:format=duration", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    return {**j["streams"][0], "duration": float(j["format"]["duration"])}


class Fonts(unittest.TestCase):
    def test_every_bundled_font_loads(self):
        for kind, f in FONTS.items():
            self.assertTrue((FONT_DIR / f).exists(), f)
            self.assertGreater(font(kind, 40).getlength("Hamburg 2026"), 50, kind)

    def test_licences_present(self):
        families = {f.split("-latin")[0] for f in FONTS.values()}
        for fam in families:
            self.assertTrue((FONT_DIR / f"OFL-{fam}.txt").exists(), fam)


class Themes(unittest.TestCase):
    def test_every_world_has_a_theme(self):
        ids = re.findall(r"\{ id: '([a-z-]+)'", (ROOT / "src" / "worlds.ts").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(ids), 12)
        self.assertEqual(sorted(ids), sorted(THEMES), "src/worlds.ts and medialab/themes.py must list the same worlds")

    def test_theme_text_contrast(self):
        for tid, t in THEMES.items():
            self.assertGreaterEqual(contrast_ratio(t["fg"], t["bg"]), 7, f"{tid}: body text under 7:1")
            self.assertGreaterEqual(contrast_ratio(t["muted"], t["bg"]), 3, f"{tid}: muted text under 3:1")


class Wrap(unittest.TestCase):
    def test_lines_fit_and_keep_breaks(self):
        f = font("sans", 48)
        lines = wrap("one two three four five six seven eight nine ten eleven twelve", f, 500)
        self.assertTrue(all(f.getlength(ln) <= 500 for ln in lines))
        self.assertEqual(wrap("a\nb", f, 500), ["a", "b"])


class Stills(unittest.TestCase):
    def test_every_still_kind_has_an_example_and_renders_at_its_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            for kind in stills.KINDS:
                self.assertIn(kind, EXAMPLES, f"add a starter spec for {kind} to medialab/examples.py")
                spec = with_media(EXAMPLES[kind], tmp)
                out = build(spec, tmp / f"{kind}.png")[0]
                with Image.open(out) as img:
                    got = img.size
                size = spec.get("size") or {"thumbnail": "16:9", "endscreen": "16:9", "story": "9:16",
                                            "testimonial": "1:1"}.get(kind, "4:5")
                self.assertEqual(got, SIZES[size], kind)

    def test_every_theme_renders_a_cover_and_point(self):
        with tempfile.TemporaryDirectory() as tmp:
            for tid in THEMES:
                for kind in ("cover", "point"):
                    build({**EXAMPLES[kind], "theme": tid, "photo": None}, Path(tmp) / f"{tid}-{kind}.png")

    def test_carousel_writes_slides_and_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = build(with_media(EXAMPLES["carousel"], Path(tmp)), Path(tmp) / "c")
            pngs = [p for p in paths if p.suffix == ".png"]
            self.assertEqual(len(pngs), len(EXAMPLES["carousel"]["slides"]))
            pdf = [p for p in paths if p.suffix == ".pdf"][0]
            self.assertTrue(pdf.read_bytes().startswith(b"%PDF-"))
            raw = pdf.read_bytes()
            self.assertEqual(raw.count(b"/Type /Page") - raw.count(b"/Type /Pages"), len(pngs), "one PDF page per slide")

    def test_missing_photo_is_a_clear_error(self):
        with self.assertRaises(FileNotFoundError):
            build({"kind": "cover", "title": "x", "photo": "/nope.jpg"}, Path(tempfile.gettempdir()) / "x.png")

    def test_unknown_kind_and_theme(self):
        with self.assertRaises(KeyError):
            build({"kind": "hologram"}, Path(tempfile.gettempdir()) / "x.png")
        with self.assertRaises(KeyError):
            build({"kind": "cover", "title": "x", "theme": "vaporwave"}, Path(tempfile.gettempdir()) / "x.png")


@unittest.skipUnless(HAS_FF, "ffmpeg/ffprobe not on PATH")
class Video(unittest.TestCase):
    def test_every_video_kind_renders_h264_yuv420p_9x16(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            for kind in video.KINDS:
                self.assertIn(kind, EXAMPLES, kind)
                spec = with_media(EXAMPLES[kind], tmp)
                spec.update({"duration": 1.5, "seconds_per_item": 0.5, "seconds_per_photo": 0.6, "hold": 0.3, "beat": 0.1})
                if kind == "beatcut":
                    spec["photos"] = spec["photos"][:2]
                if kind == "countdown":
                    spec["items"] = spec["items"][:2]
                out = build(spec, tmp / f"{kind}.mp4", preview=True)[0]
                p = probe(out)
                self.assertEqual((p["codec_name"], p["pix_fmt"]), ("h264", "yuv420p"), kind)
                self.assertAlmostEqual(p["width"] / p["height"], 9 / 16, places=2, msg=kind)
                self.assertGreater(p["duration"], 0.3, kind)


class Check(unittest.TestCase):
    def test_right_and_wrong_canvas(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = build(with_media(EXAMPLES["thumbnail"], Path(tmp)), Path(tmp) / "t.jpg")[0]
            res = {r.check: r.status for r in check(good, "yt-thumb")}
            self.assertEqual(res["canvas"], "PASS")
            self.assertEqual(res["file size"], "PASS")
            sq = Path(tmp) / "sq.png"
            Image.new("RGB", (1000, 1000), (128, 128, 128)).save(sq)
            res = {r.check: r.status for r in check(sq, "yt-thumb")}
            self.assertEqual(res["canvas"], "FAIL")
            self.assertEqual(res["contrast at 160 px"], "FAIL")

    def test_text_in_ui_zone_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            img = Image.new("RGB", (1080, 1920), (20, 20, 20))
            from PIL import ImageDraw
            d = ImageDraw.Draw(img)
            for y in range(1560, 1880, 60):
                d.text((60, y), "caption text under the buttons " * 2, font=font("sans-bold", 44), fill="white")
            p = Path(tmp) / "s.png"
            img.save(p)
            res = {r.check: r.status for r in check(p, "reels")}
            self.assertEqual(res["ui zone: caption + audio"], "WARN")

    @unittest.skipUnless(HAS_FF, "ffmpeg not on PATH")
    def test_black_opening_and_bad_pixfmt_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=black:s=1080x1920:d=2", "-pix_fmt", "yuv444p",
                            "-c:v", "libx264", str(p)], check=True)
            res = {r.check: r.status for r in check(p, "shorts")}
            self.assertEqual(res["first frame"], "FAIL")
            self.assertEqual(res["pixel format"], "FAIL")
            self.assertEqual(res["canvas"], "PASS")


class Cli(unittest.TestCase):
    def run_cli(self, *args, ok=True):
        r = subprocess.run([*CLI, *args], capture_output=True, text=True)
        if ok:
            self.assertEqual(r.returncode, 0, r.stderr)
        return r

    def test_kinds_themes_example(self):
        self.assertIn("carousel", self.run_cli("kinds").stdout)
        self.assertIn("brutalist-mono", self.run_cli("themes").stdout)
        self.assertEqual(json.loads(self.run_cli("example", "poster").stdout)["kind"], "poster")
        self.assertEqual(self.run_cli("example", "nope", ok=False).returncode, 2)

    def test_make_then_check_from_a_spec_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            shutil.copy(PHOTO_LIST[0], tmp / "photo.jpg")
            (tmp / "brief.json").write_text(json.dumps(EXAMPLES["cover"]), encoding="utf-8")
            out = self.run_cli("make", str(tmp / "brief.json"), "-o", str(tmp / "cover.png")).stdout.strip()
            self.assertTrue(Path(out).exists())
            r = self.run_cli("check", out, "-p", "carousel", "--json")
            self.assertEqual(json.loads(r.stdout)["platform"], "carousel")
            self.assertEqual(self.run_cli("check", out, "-p", "yt-thumb", ok=False).returncode, 1)


class Patterns(unittest.TestCase):
    def test_spec_patterns_use_known_kinds_and_themes(self):
        for f in sorted((ROOT / "patterns" / "src").glob("*.py")):
            src = f.read_text(encoding="utf-8")
            for kind in re.findall(r'"kind":\s*"([a-z_]+)"', src):
                self.assertTrue(kind in stills.KINDS or kind in video.KINDS or kind == "carousel", f"{f.name}: {kind}")
            for tid in re.findall(r'"theme":\s*"([a-z-]+)"', src):
                self.assertIn(tid, THEMES, f.name)


if __name__ == "__main__":
    unittest.main(verbosity=1)
