# Free real photos, sourced legally

Tested 2026-10-25: Openverse API search, then download and `scripts/photo_slide.py` render.

## Openverse (no API key)
```bash
curl -s "https://api.openverse.org/v1/images/?q=rain%20window&license=cc0,pdm&size=large&page_size=20"
```
- `license=cc0,pdm` gives public domain only, so no attribution is legally required. Keep a `credits.txt` anyway
  (title, creator, `foreign_landing_url`, licence). It's courteous and it proves the licence later.
- `size=large` drops tiny images. Check `width`/`height` in the result: you need at least 1080 px wide for a 4:5 slide, ideally 2000+.
- Download with a browser-like `User-Agent` header. Some hosts return an HTML page (hotlink protection) to bare clients,
  so check the first bytes are JPEG/PNG. The fallback is `https://api.openverse.org/v1/images/<id>/thumb/?full_size=true`.
- Other useful filters: `aspect_ratio=tall` (portrait), `category=photograph`, `source=stocksnap,rawpixel,flickr`.

```python
import json, urllib.request
H = {"User-Agent": "Mozilla/5.0 media-lab"}
res = json.load(urllib.request.urlopen(urllib.request.Request(
    "https://api.openverse.org/v1/images/?q=empty%20platform&license=cc0,pdm&size=large&aspect_ratio=tall", headers=H)))
for r in res["results"][:5]:
    data = urllib.request.urlopen(urllib.request.Request(r["url"], headers=H), timeout=30).read()
    if data[:3] == b"\xff\xd8\xff":
        open(f"{r['id']}.jpg", "wb").write(data)
        open("credits.txt", "a").write(f"{r['title']} | {r.get('creator')} | {r['license']} | {r['foreign_landing_url']}\n")
```

## Unsplash and Pexels
- Both licences allow free commercial and personal use without attribution (credit is appreciated).
- You may not sell the photos unaltered (prints, stock resale), or build a competing photo service with them.
- Don't imply that a recognisable person or brand in the photo endorses anything.
- The Unsplash API needs a free access key (and asks you to trigger its download endpoint when you use a photo). The Pexels API needs a free key too.
  Without keys, pick by hand on the website and note the photo URL in `credits.txt`.
- Re-check each site's licence page before a commercial client job; these terms change.

## Make the slide (Pillow)
```bash
python scripts/photo_slide.py photo.jpg "Some evenings the rain says everything." slide.png --where bottom --focus 0.4
```
- Crops to 1080x1350 (4:5) by scale-to-cover. `--focus` (0 left, 1 right) keeps the subject in frame.
- Darkens only a soft band behind the text (about 45% max), not the whole photo. Never blur the whole image.
- Wraps so the last line is never a single word. Default font Georgia, off-white text; pass `--font` for another.

## Picking a photo whose negative space fits the text
- Look for a calm third of the frame: sky, wall, water, floor, a blurred background. That's where the text goes.
- Portrait (tall) photos crop to 4:5 with the least loss; landscape loses the sides, so check `--focus`.
- Busy everywhere (crowds, foliage)? Put the text on a plain paper slide next to it instead of over it.
- Shoot your own when you can. A phone photo of the real place beats any stock image.
- Before showing anything, run the smell test in `playbook/taste.md`.
