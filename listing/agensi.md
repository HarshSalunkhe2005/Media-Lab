# Agensi listing kit: Media Lab

Copy-paste material for the marketplace form. Upload `release/media-lab-skill-<version>.zip` (`npm run skill`)
and `public/showcase.jpg` as the cover. Price: **free** (see "Why free" below).

**Name:** Media Lab

**Tagline:** Content that reads as made by a person, rendered to real PNG, PDF and MP4 files and checked before you post.

**Best for:** Turns a short brief into finished carousels, LinkedIn PDFs, stories, posts, thumbnails and Shorts with
a gated procedure, 12 style worlds and a CLI, then tests each file against the platform's specs.

**Description**

Most content skills stop at advice. Media Lab writes the brief, picks a style world, drafts the hook with a
critique rubric, and then renders the actual file: a 4:5 carousel plus its LinkedIn PDF, a 9:16 story with room
left for the poll sticker, a 16:9 thumbnail that still reads at 160 px, a kinetic hook, an audiogram or a beat-cut
slideshow. Before anything goes out, `medialab check` measures canvas, codec, pixel format, faststart, black
openings, EBU R128 loudness, true peak, text inside the app's UI zones and contrast at feed size, and exits non-zero
on a failure.

- Brand kits: one brand.json keeps colours, fonts, handle and logo consistent across every render
- 59 patterns across carousels, posts, stories, event media, thumbnails, hooks, captions, Shorts and reframes
- 12 worlds (Editorial, Retro Print, Brutalist Mono, Soft Pastel, Tech Launch, Campus Event and more) with
  "avoid" rules that keep output from looking generated
- 24 still kinds and 7 video kinds from one JSON or YAML spec; bundled OFL fonts, so output matches on every OS
- Format specs and safe zones, a hook library, a taste smell test, tested ffmpeg, MoviePy and Remotion recipes
- Original-content rules built in: no recreating other creators' work, fictional names in demos, sourced numbers

**Use cases**
1. "Turn this report into a LinkedIn document": slides plus a PDF, one finding per slide, source on the slide.
2. "Make a story sequence for Friday's finals": countdown, poll and link frames inside the safe area.
3. "Launch Short for my repo": kinetic hook, picture-in-picture over the screen recording, captions, loudness checked.
4. "Is this thumbnail ready?": `check -p yt-thumb` for size, the duration-badge zone and contrast at 160 px.
5. Café, shop or league accounts: menu boards, testimonials, result cards, recap grids in one consistent style.

**Requires:** terminal, read/write files, Python 3.10+ with Pillow; ffmpeg for video. No network, no API keys.

**Compatibility:** Claude Code (plugin or `~/.claude/skills`), any agent that loads a `SKILL.md` folder.

**Tags:** content creation, social media, carousel, linkedin, instagram, youtube shorts, reels, thumbnail, ffmpeg, video editing

## Why free

The closest listings in this space (video editing, reframing, repurposing, $5-10) showed 0 uses when checked on
2026-11-04. A free skill that renders real files is the fastest way to collect the first uses and ratings. A paid
tier can come later with more worlds or brand-kit support, sold as an add-on, not by taking features out.

## Before submitting
- [ ] `npm test` and `npm run build` pass; CI is green
- [ ] `npm run skill` produced the zip; install it into a clean `~/.claude/skills` and run `python scripts/medialab kinds`
- [ ] Cover image is `public/showcase.jpg`; add 2-3 previews (a carousel slide, a story, a Short frame)
