# Contributing

Thanks for helping. Media Lab stays useful only if everything in it is real: every preview is rendered by the
repo, every command has been run, every claim has a source or an evidence level.

## Setup

```bash
npm install
pip install pillow pyyaml      # plus ffmpeg on PATH for video
npm test                       # python tools/test_medialab.py
npm run build                  # validates metadata and builds the site
```

## Add a pattern

1. Prefer a spec: `patterns/src/<slug>.py` with a `SPEC` dict and `render(out)` calling `from_spec` (copy any
   spec-based pattern, e.g. `checklist-slide.py`). Use `ph("<name>")` for bundled CC0 photos.
2. Need something no kind can draw? Add a kind (below) instead of a one-off renderer, so the CLI gets it too.
3. `python patterns/render.py <slug>`, then look at the preview. Run the smell test in `playbook/taste.md`.
4. Add the entry to `src/meta.ts`; add it as proof to a world in `src/worlds.ts` if it shows that world well.
5. `npm run build` fails on a missing preview, renderer, recipe path or unknown slug.

## Add a kind

1. A function in `scripts/medialab/stills.py` (spec, theme) -> image, or `video.py` (spec, theme, out) -> path.
   First docstring line is what `medialab kinds` prints. Register it in `KINDS`.
2. A starter spec in `scripts/medialab/examples.py` (tests fail without one).
3. A row in the kinds table in `recipes/medialab-cli.md`.

## Add a world

Entry in `src/worlds.ts`, matching theme in `scripts/medialab/themes.py` (tests check both lists match and that
text meets 7:1 contrast), a brief row in `src/router.ts`.

## Add docs, recipes, research

- Only add commands you have run; note the tool version.
- New skill page: link it from `SKILL.md` routing and the root `llms.txt` (the build checks), and add a row to
  `recipes/by-goal.md` when it serves a goal.
- Research goes in `research/` with links and an evidence level (strong / medium / weak).
- Solved a bug? Add it to "Known bugs already solved" in `playbook/05-verify.md`.

## Rules

- Original content only; fictional names in demos; no copied paid prompts or creator scripts.
- Photos: CC0 / public domain, recorded in `patterns/assets/photos/credits.txt`. Fonts: OFL, licence file included.
- Bump `version` in `plugins/media-lab/.claude-plugin/plugin.json` when the skill changes; update CHANGELOG.md;
  run `claude plugin validate .` and `npm run skill`.
