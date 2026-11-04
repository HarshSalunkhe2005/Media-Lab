---
name: media-lab
description: Use whenever you make social or video content - YouTube Shorts, Instagram Reels, TikToks, carousels, LinkedIn documents, X or LinkedIn posts, stories, launch or promo videos, thumbnails, end screens, audiograms, captions, scripts, hooks, event posters - or edit, caption, reframe or render video with ffmpeg, MoviePy or Remotion. Gives the brief-to-publish procedure, format specs and safe zones, a hook library, a critique rubric, 12 style worlds, and a CLI that renders a JSON brief to finished PNG/PDF/MP4 and checks files against platform specs before posting. Not for website UI (use ui-lab).
---

# Media Lab: content with judgement, not templates

Media Lab is a reference library for content creation (GitHub `HarshSalunkhe2005/Media-Lab`). This skill folder holds
everything an agent needs; the repo root adds `research/` (sources and evidence levels), `patterns/` (rendered examples)
and the browsable site.

## Procedure (do not skip steps)

1. **Brief** (`playbook/01-brief.md`): audience, one idea, platform, goal metric, voice. Write it down first.
2. **Package first** (`playbook/02-package.md`): title, hook line, thumbnail or cover idea before any production.
3. **Script** (`playbook/03-script.md`): pick a hook from `hooks/hooks.md`, follow the format file, then run the
   critique rubric (`playbook/critique.md`). Revise until it scores "ship". Kill weak ideas instead of polishing them.
4. **Assets and edit** (`playbook/04-edit.md`): pick the tool with `recipes/choose-a-tool.md`, then follow
   `recipes/ffmpeg.md`, `recipes/moviepy.md` or `recipes/remotion.md`.
5. **Verify** (`playbook/05-verify.md`): run `python scripts/medialab check <file> --platform <p>` (canvas, codec,
   loudness, black opening, UI zones, contrast at feed size), then watch the output yourself. For anything visual,
   also run the AI-look smell test in `playbook/taste.md`.
6. **Publish and learn**: caption and post copy go through the `humanize` skill; log one metric to compare next time.

## Worlds and rendered patterns

The site (repo root, `/for-claude.md` live) routes a brief to one of twelve **worlds** (Quiet Poetry, Tech Launch,
Campus Event, Explainer, Data Story, Build Log, Warm Local, Faceless Story, Editorial, Retro Print, Brutalist Mono,
Soft Pastel) and to 59 rendered **patterns** (`patterns/src/<slug>.py`, previews in `public/previews/`). Pick a world
first, start from its proof patterns.

## Build with the CLI (fastest path to a real file)

`scripts/medialab` renders a JSON (or YAML) brief to PNG, PDF or MP4. Each world is a theme; fonts are bundled.

```bash
python scripts/medialab example carousel > brief.json   # or: kinds, themes, example <kind>
python scripts/medialab make brief.json -o out/
python scripts/medialab check out/01.png --platform carousel
```

Full reference: `recipes/medialab-cli.md`. For a client or a recurring account, make a `brand.json` once
(`recipes/brand-kit.md`) and pass `--brand brand.json` to every render. Write the words with the playbook first; the CLI only lays them out.

## Read these files for the task (routing)

Always: `playbook/01-brief.md` first, `playbook/05-verify.md` last. Not sure? Use `recipes/by-goal.md`.

| Task | Read |
|---|---|
| Short / Reel / TikTok script | `formats/short-video.md`, `hooks/hooks.md`, `playbook/03-script.md`, `playbook/critique.md` |
| Render a Short from a script (free tools) | `recipes/end-to-end-short.md` → `scripts/make_short.py` |
| Edit real footage (cut, reframe, loudness, captions) | `playbook/04-edit.md`, `recipes/ffmpeg.md`, `formats/specs.md` |
| Python-driven edit | `recipes/moviepy.md` → `scripts/moviepy_demo.py` |
| Animated type / UI mockups | `recipes/remotion.md` |
| Carousel or LinkedIn document | `playbook/taste.md` FIRST, then `formats/carousel.md`, `recipes/stock-photos.md`, `recipes/carousel.md`, `hooks/templates.md` |
| Quote / poetry post | `playbook/taste.md` FIRST, then `recipes/stock-photos.md` → `scripts/photo_slide.py` |
| LinkedIn / X / thread / launch post | `formats/text-posts.md`, `playbook/voice.md`, then `humanize` |
| Launch video for a project | `formats/launch-video.md`, `recipes/by-goal.md` row 1 |
| Thumbnail, cover, poster text | `playbook/taste.md`, `formats/thumbnail.md` (incl. overlay checklist), `recipes/carousel.md` Option B |
| Free real photos (legal sourcing) | `recipes/stock-photos.md` |
| Event coverage / sorting event media | `playbook/06-event-coverage.md` |
| Packaging (title, hook, cover) | `playbook/02-package.md` |
| Captions only | `scripts/captions.py`, `formats/specs.md` safe zones |
| Render any still, carousel, PDF or simple video from a brief | `recipes/medialab-cli.md` → `scripts/medialab` |
| Make every render match one brand (colours, fonts, handle, logo) | `recipes/brand-kit.md` → `scripts/medialab brand` |
| Story frames (poll, countdown, link, update) | `formats/stories.md`, `recipes/medialab-cli.md` |
| Pre-publish file check (any format) | `recipes/medialab-cli.md` (check), then `playbook/05-verify.md` |

## Hard rules

- Original content only. Never clip, re-upload or recreate another creator's video, script, thumbnail or art.
  Study techniques, rebuild in our own words.
- Demos and examples use fictional names and brands.
- Never state a number as fact unless it comes from a source you can cite. Vendor "stats" are hypotheses.
- AI-generated or synthetic media is disclosed where the platform asks (YouTube's altered/synthetic flag).
- Anything posted under Harsh's name goes through `humanize`. No AI tells, no "AI made this" credits in his work.
- Do not publish, post or upload without Harsh's explicit go-ahead for that piece.
