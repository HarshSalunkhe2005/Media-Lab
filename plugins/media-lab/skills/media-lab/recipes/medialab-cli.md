# medialab CLI: brief file in, finished file out

`scripts/medialab` is a small Python package: 24 still kinds, 7 video kinds, carousels with PDF export, and
`check`, which tests a file against a platform spec before you post it. Every gallery pattern added after
v0.4 is one of these specs, so the gallery doubles as a library of working examples.

Tested with Python 3.12 and 3.13, Pillow 12.3, ffmpeg 6.1. Fonts are bundled (SIL OFL, `assets/fonts/`), so output
looks the same on every machine. Video kinds and `check` on video need ffmpeg + ffprobe on PATH.

```bash
pip install pillow                      # pyyaml too if you want YAML specs
python scripts/medialab kinds           # what a spec can be
python scripts/medialab themes          # one theme per world
python scripts/medialab example carousel > brief.json
python scripts/medialab make brief.json -o out/
python scripts/medialab check out/01.png --platform carousel
```

## A spec

```json
{
  "kind": "carousel", "theme": "explainer", "size": "4:5", "handle": "@lowtide.studio", "pdf": true,
  "slides": [
    {"kind": "cover", "kicker": "Field notes", "title": "Five edits that make a Short feel shot", "photo": "desk.jpg"},
    {"kind": "point", "title": "Cut the first second", "body": "Open on the action, not on you getting ready."},
    {"kind": "checklist", "title": "Before you export", "items": ["[x] Captions above y = 1400", "[ ] Loudness near -14 LUFS"]},
    {"kind": "cta", "ask": "Save this for your next edit", "why": "Five checks, two minutes"}
  ]
}
```

- Paths (`photo`, `photos`, `audio`, `video`, `top`, `bottom`, `main`, `inset`) are relative to the spec file.
- `theme` is a world id; override pieces with `"colors": {"accent": "#ff5a36"}` or `"fonts": {"head": "display"}`.
  Font values are bundled kinds (`medialab/core.py` FONTS) or a path to your own `.ttf/.otf/.woff`.
- `size`: `4:5`, `1:1`, `9:16`, `16:9`, `x` (1200x675), `og` (1200x630), `linkedin`, or `[w, h]`.
- A carousel writes `01.png ... NN.png`; `"pdf": true` adds `carousel.pdf` for a LinkedIn document.
- Slides inherit the carousel's `theme`, `size` and `handle`; any slide can override them.
- `"brand": "brand.json"` (or `make --brand brand.json`) applies a brand kit: colours, fonts, handle, logo.
  See `recipes/brand-kit.md`; `brand init` and `brand check` create and validate one.

## Kinds

| Kind | Use for | Key fields |
|---|---|---|
| `cover` | Carousel slide 1, link previews | `title`, `kicker`, `photo`, `focus` |
| `point` | Numbered tip slide | `n`, `title`, `body` |
| `number` | One statistic | `value`, `caption`, `source` |
| `quote` | Quote or poem, on photo or surface | `text` (newlines kept), `by`, `font`, `photo` |
| `checklist` | Saveable lists | `title`, `items` (`[x]` done / `[ ]` open) |
| `compare` | Myth / fact, do / don't | `title`, `left` [label, text], `right` |
| `steps` | 3-5 step process | `title`, `items` |
| `bars` | Bar chart, one highlighted bar | `title`, `data` [[label, value]], `highlight`, `fmt`, `source` |
| `timeline` | Dated history or build log | `title`, `items` [[when, what]] |
| `code` | Snippet on a card | `title`, `code`, `highlight` (line no.), `caption` |
| `cta` | Last slide | `ask`, `why`, `photo`, `handle` |
| `text` | A paragraph slide | `title`, `body` |
| `thumbnail` | 16:9, 160 px readable | `words` (<= 4), `highlight`, `photo`, `side` |
| `testimonial` | Social proof | `text`, `name`, `role`, `result`, `photo` |
| `postcard` | A text post as an image (no platform logos) | `name`, `handle`, `text`, `meta`, `photo` |
| `poster` | Event / announcement | `date`, `title`, `details` [], `footer`, `photo`, `grade` |
| `statement` | One huge sentence | `text`, `highlight`, `label`, `photo` (halftone) |
| `cover_magazine` | Editorial cover | `masthead`, `issue`, `line`, `sub`, `photo` |
| `split` | Before / after, this vs that | `left`/`right` {label, photo, grade}, `title`, `stack` |
| `story` | 9:16 story inside the safe area | `kicker`, `title`, `body`, `sticker`, `countdown`, `photo` |
| `endscreen` | YouTube end screen | `line`, `subscribe`, `guides` (false for export) |
| `grid` | Recap collage | `photos`, `cols`, `caption`, `sub` |
| `speaker` | Speaker / guest card | `name`, `talk`, `when`, `label`, `photo` |
| `menu` | Price list | `title`, `items` [[name, price, note?]], `footer` |
| `kinetic` (video) | Word-by-word hook | `text`, `highlight` [], `beat`, `hold`, `photo`, `audio` |
| `beatcut` (video) | Photos cut on the beat | `photos`, `bpm`, `beats_per_cut`, `audio` |
| `progress` (video) | Progress bar over a slideshow or video | `photos` or `video`, `seconds_per_photo`, `bar` |
| `splitscreen` (video) | Two sources stacked | `top`, `bottom` (photo or video), `duration` |
| `pip` (video) | Picture-in-picture | `main`, `inset`, `scale`, `duration` |
| `countdown` (video) | 3-2-1 list | `items`, `seconds_per_item`, `photos` |
| `audiogram` (video) | Waveform for a voice clip | `audio`, `title`, `show`, `speaker`, `photo` |

`story` and `endscreen` draw dashed guides for stickers and end-screen elements; set `"guides": false` for the
file you upload (the app adds the real elements there).

## check

```bash
python scripts/medialab check short.mp4 --platform shorts
python scripts/medialab check thumb.jpg -p yt-thumb --json
```

Platforms: `shorts`, `reels`, `tiktok`, `story`, `carousel`, `ig-feed`, `linkedin`, `x`, `yt-thumb`, `youtube`.

| Check | What it measures | Fails when |
|---|---|---|
| canvas | Size and aspect | Aspect differs from the platform (it would crop) |
| duration | Seconds | Over the platform max |
| codec, pixel format | H.264, yuv420p | Not yuv420p (black or green on some phones) |
| frame rate | fps | WARN outside 24-60 |
| faststart | moov atom before mdat | WARN: slow start on upload previews |
| first frame | blackdetect on the first 2 s | Opens on black |
| loudness, true peak | EBU R128 | WARN outside -16 to -12 LUFS or above -1 dBTP |
| audio opening | silencedetect | WARN when the first 0.8 s is silent |
| ui zone | Edge density in each app's UI area vs the body | WARN when detail or text sits where buttons and captions go |
| contrast at 160 px | 5-95 % luminance spread at feed size | FAIL under 70, WARN under 110 |

Exit code is 1 when any check fails, so it can gate a script or CI. It measures; it does not judge taste.
Run `playbook/critique.md` and the smell test in `playbook/taste.md` as well.

## From Python

```python
import sys; sys.path.insert(0, "scripts")
from medialab.make import build
build({"kind": "thumbnail", "theme": "explainer", "words": "Stop doing this", "highlight": "stop"}, "thumb.png")
```
