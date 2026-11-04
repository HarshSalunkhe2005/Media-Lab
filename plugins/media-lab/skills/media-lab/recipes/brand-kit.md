# Brand kit: every post looks like the same account

One `brand.json` holds a brand's colours, fonts, handle and logo. Point any spec at it and every slide, post,
story, thumbnail and video comes out on brand, without repeating those settings in each spec.

Tested with Python 3.13, Pillow 12.3, ffmpeg 6.1 (`tools/test_medialab.py`, class `Brand`).

```bash
python scripts/medialab brand init brand.json      # starter file (never overwrites)
python scripts/medialab brand check brand.json     # contrast, fonts, logo, position
python scripts/medialab make post.json --brand brand.json -o out/post.png
```

Or set it inside a spec: `{"kind": "point", "brand": "brand.json", "title": "..."}`.

## The file

```json
{
  "name": "Fern Café",
  "base": "warm-local",
  "handle": "@ferncafe",
  "colors": {"bg": "#f3e7d6", "fg": "#2b1d14", "muted": "#7a6555", "accent": "#2f6b4f"},
  "fonts": {"head": "display-serif", "body": "sans", "num": "display-serif"},
  "logo": "fern-logo.png",
  "logo_position": "top-right",
  "logo_size": 0.09
}
```

| Field | What it does |
|---|---|
| `base` | Theme to start from: any world id (`python scripts/medialab themes`). Anything you leave out comes from here. |
| `colors` | `bg`, `fg` (text), `muted` (secondary text), `accent` (numbers, key words). Any subset. |
| `fonts` | `head`, `body`, `num`: a bundled kind (`serif`, `sans-bold`, `display`, ...) or a path to your `.ttf/.otf/.woff`. |
| `handle` | Default handle for every slide and post. |
| `logo` | PNG with transparency, 600 px+ wide. Paths are relative to `brand.json`. |
| `logo_position` | `top-right` (default) or `bottom-right`. `top-left` and `bottom-left` collide with headlines or the handle. |
| `logo_size` | Fraction of the canvas width (0.09 = 97 px on a 1080 slide). |

Precedence: **spec > brand > base theme**. A one-off post can still override a colour, and `"logo": false` hides
the logo for that render. On 9:16 frames the logo moves inside the safe area, clear of the top bar and the bottom UI.
When the logo takes the top-right corner, the slide counter moves to the bottom-right.

## What `brand check` tests

| Check | PASS | FAIL |
|---|---|---|
| Text on background | 7:1+ | under 4.5:1 |
| Muted on background | 4.5:1+ | under 3:1 |
| Accent on background | 3:1+ (large text) | under 2:1 |
| Fonts | file exists and loads | unknown kind or missing file |
| Logo | found, has transparency (WARN if not), 300 px+ (WARN if smaller) | missing |
| Logo position | top-right, bottom-right | not a corner name |

Exit code 1 on any FAIL. Three working kits, all fictional, are in `examples/brand/` (`fern.json`, `lowtide.json`, `pier.json`).

## Taste rules

- One accent. If the brand has three colours, pick the one that is not the background or the text.
- The logo is a signature, not a headline: small, the same corner on every post, never over a face or the key number.
- Brand fonts that are too thin for 160 px thumbnails: use them for `head` on slides only and keep `display` or
  `sans-black` for thumbnails (override `fonts` in the thumbnail spec).
