"""Word-timestamp JSON -> ASS subtitles with the spoken word highlighted (Shorts/Reels style).

Input JSON: [{"word": "Hello", "start": 0.12, "end": 0.40}, ...]  (Whisper word_timestamps or edge-tts output)
Usage: python captions.py words.json captions.ass [--font "Montserrat ExtraBold"] [--size 84] [--chunk 3] [--y 1320]
Then:  ffmpeg -i video.mp4 -vf "subtitles=captions.ass:fontsdir=fonts" -c:a copy out.mp4
"""
import argparse
import json
import re


def ts(t: float) -> str:
    h, rem = divmod(max(t, 0), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def clean(w: str) -> str:
    return re.sub(r"[{}\\]", "", w).strip()


def build(words, font, size, chunk, y, color, highlight, upper=True):
    case = str.upper if upper else str.lower
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{font},{size},{color},{color},&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,2,2,90,90,{1920 - y},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    words = [w for w in words if clean(w["word"])]
    lines = []
    for i in range(0, len(words), chunk):
        group = words[i:i + chunk]
        for j, w in enumerate(group):
            end = group[j + 1]["start"] if j + 1 < len(group) else w["end"]
            text = " ".join(
                (f"{{\\c{highlight}\\fscx108\\fscy108}}{case(clean(g['word']))}{{\\r}}" if k == j else case(clean(g["word"])))
                for k, g in enumerate(group))
            lines.append(f"Dialogue: 0,{ts(w['start'])},{ts(max(end, w['start'] + 0.05))},Cap,,0,0,0,,{text}")
    return head + "\n".join(lines) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("words")
    ap.add_argument("out")
    ap.add_argument("--font", default="Arial")
    ap.add_argument("--size", type=int, default=84)
    ap.add_argument("--chunk", type=int, default=3)
    ap.add_argument("--y", type=int, default=1320, help="caption baseline from top, inside the 9:16 safe zone")
    ap.add_argument("--color", default="&H00FFFFFF")
    ap.add_argument("--lower", action="store_true", help="lowercase captions (quiet styles)")
    ap.add_argument("--highlight", default="&H0000E5FF", help="ASS BGR colour of the spoken word (default yellow)")
    a = ap.parse_args()
    words = json.load(open(a.words, encoding="utf-8"))
    open(a.out, "w", encoding="utf-8").write(build(words, a.font, a.size, a.chunk, a.y, a.color, a.highlight, upper=not a.lower))
    print(f"wrote {a.out} ({len(words)} words)")
