# Media Lab

A reference library for making content that reads as made by a person: Shorts, Reels, carousels, thumbnails, captions
and event media. It is the media sibling of [UI Lab](https://ui-lab-weld.vercel.app): a procedure (the playbook), eight
named style **worlds**, and a gallery of **patterns** whose previews are real output of the repo's own Python + ffmpeg
renderers. It also installs as a Claude Code plugin.

## Use it

- **Site:** gallery, worlds, brief router and the full playbook (`npm install && npm run dev`, port 5190).
- **Agents:** `/llms.txt`, `/llms-full.txt`, `/patterns.json`, `/worlds.json`, `/for-claude.md`, `/docs/<slug>.md`, `/skill/<path>`.
- **Claude Code plugin:**
  ```
  /plugin marketplace add HarshSalunkhe2005/Media-Lab
  /plugin install media-lab@media-lab
  ```

## Layout

```
src/meta.ts            patterns: single source of truth (gallery, llms.txt, patterns.json, docs)
src/worlds.ts          8 worlds: type, colour, imagery, motion, rules, avoid, proof patterns
src/router.ts          brief -> world -> patterns (validated at build)
ai-index.ts            Vite plugin: generates the machine-readable files, fails the build on a bad slug/preview/path
patterns/lib.py        shared Pillow/ffmpeg helpers (film grade, text-area shading, balanced wrap)
patterns/src/*.py      one renderer per pattern; patterns/render.py renders previews into public/previews/
patterns/assets/photos CC0 / public-domain photos via Openverse, credits.txt
plugins/media-lab/     the Claude Code plugin: skills/media-lab/ (SKILL.md, playbook, formats, hooks, recipes, scripts)
research/              existing tools, what works (with evidence levels), inspiration + teardown template
```

## Add a pattern

1. Write `patterns/src/<slug>.py` with `render(out: Path) -> Path` (use `patterns/lib.py`).
2. `python patterns/render.py <slug>` (needs Pillow + ffmpeg; the two `short-*` patterns also need `edge-tts` and internet).
3. Add an entry to `src/meta.ts`. Optionally add it as proof to a world in `src/worlds.ts`.
4. `npm run build` validates everything.

## Rules

- Original content only. Study techniques; never copy scripts, footage, thumbnails or paid prompts.
- Examples use fictional names, teams and lines. Photos are CC0 / public domain only.
- Numbers need a source; vendor stats are treated as hypotheses (`research/02-what-works.md`).
- Every visual passes the AI-look smell test in `playbook/taste.md`.
