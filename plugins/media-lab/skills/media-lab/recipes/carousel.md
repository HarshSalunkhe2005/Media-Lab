# Carousels, posters, cards: HTML/CSS or Pillow

## Option A: HTML/CSS to PNG/PDF (best type control)
1. One HTML file, each slide a `<section class="slide">` of 1080x1350 px, fonts loaded locally or from Google Fonts.
2. Render with Playwright:
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
    pg.goto("file:///C:/path/carousel.html"); pg.wait_for_timeout(500)
    for i, el in enumerate(pg.query_selector_all(".slide"), 1):
        el.screenshot(path=f"slide_{i:02d}.png")
    pg.pdf(path="carousel.pdf", width="1080px", height="1350px", print_background=True)   # LinkedIn document
    b.close()
```
CSS for the PDF: `@page { size: 1080px 1350px; margin: 0 } .slide { break-after: page }`.

## Option B: Pillow (posters and result cards from a template image)
- Keep the template PNG, a fonts folder and a data file per variant; one script renders all variants.
- Draw text with the template's real font; measure with `draw.textbbox` and centre or right-align by the box, not by guesswork.
- Text that sits on photos: add a subtle shadow or gradient so it reads, rather than a box.
- Photos: crop to the slot with the face in the upper third; never stretch. If the photo is too narrow, add dark side panels in the template's style.

## Checks
- Look at every exported slide at phone size.
- Spell-check names, scores and dates against the source.
