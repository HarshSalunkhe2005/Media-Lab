# Changelog

Format: [Keep a Changelog](https://keepachangelog.com). Versions follow the plugin (`plugins/media-lab/.claude-plugin/plugin.json`).

## 1.1.0

### Added
- Brand kits: one `brand.json` (base theme, colours, fonts, handle, logo, logo corner and size) applied to any
  spec with `"brand"` or `medialab make --brand`. Spec values still win. Logos are stamped on stills and burned into
  video, kept inside the 9:16 safe area.
- `medialab brand init` (starter file, never overwrites) and `medialab brand check` (text, muted and accent contrast,
  fonts, logo transparency and size, position; exit 1 on fail).
- Three fictional example kits in `examples/brand/`, the `brand-kit-three-ways` pattern (59 total), `recipes/brand-kit.md`.

### Changed
- The slide counter moves to the bottom-right when a logo takes the top-right corner.

## 1.0.0

### Added
- `scripts/medialab`: a CLI and Python package. `make` renders a JSON/YAML spec to PNG, PDF or MP4
  (24 still kinds, 7 video kinds, carousels with LinkedIn PDF export); `check` tests a file against a platform
  spec (canvas, duration, codec, pixel format, faststart, black opening, loudness, true peak, silent start,
  UI zones, contrast at feed size); `kinds`, `themes` and `example <kind>` for discovery.
- 36 patterns (58 total) and two categories, Posts and Stories: checklist, myth/fact, steps, bar chart,
  timeline, code card, LinkedIn document, editorial quote, pastel quote, testimonial, text post card, retro
  poster, halftone and brutalist statements, magazine cover, before/after, menu board, link preview image, four
  story frames, face + words and versus thumbnails, YouTube end screen, speaker card, recap grid, lineup poster,
  kinetic hook, progress bar, split screen, picture-in-picture, beat-cut slideshow, countdown list, audiogram.
- 4 worlds (12 total): Editorial, Retro Print, Brutalist Mono, Soft Pastel. Router rows for stories, podcast
  clips, LinkedIn PDFs, posters, testimonials.
- Bundled OFL fonts (EB Garamond, Inter, Oswald, JetBrains Mono, Archivo Black, DM Serif Display), so renders
  match on Windows, macOS, Linux and CI.
- `formats/stories.md`, `recipes/medialab-cli.md`, three solved bugs in `playbook/05-verify.md`.
- `tools/test_medialab.py` (fonts, theme contrast, every kind, carousel PDF, video encode, check, CLI),
  `tools/build_skill.py` (validated release zip), CI for site build, tests, offline renders and packaging.
- MIT licence, CONTRIBUTING, this changelog.

### Changed
- `patterns/lib.py` is a thin layer over `medialab.core`; older renderers keep working unchanged.
- All offline previews re-rendered with the bundled fonts.
- Build fails if a renderer has no `meta.ts` entry or a skill page is missing from `SKILL.md` or `llms.txt`.

## 0.4.0
- Browsable site: gallery, worlds, brief router, playbook pages, generated `llms.txt`, `patterns.json`, docs.
- 22 rendered patterns: carousels, event cards, thumbnails, hooks, captions, Shorts, reframes.
- Claude Code plugin with the brief-to-publish playbook, format specs, hook library and recipes.
