# AGENTS.md

Guide for AI agents using or extending Media Lab.

## Using it
1. On the site, read `/for-claude.md` (brief -> world -> patterns). In the repo, read `plugins/media-lab/skills/media-lab/SKILL.md` first (procedure, routing table, hard rules). `recipes/by-goal.md` maps goals to files.
2. Visual work (carousels, quotes, thumbnails, posters): read `playbook/taste.md` first and run its smell test before showing anything.
3. Follow the playbook in order: `01-brief` → `02-package` → `03-script` → `critique` → `04-edit` → `05-verify`.
4. Pull specs from `formats/specs.md`, hooks from `hooks/hooks.md`, commands from `recipes/`. Render with `scripts/medialab make`, then `scripts/medialab check` before showing anything.
5. Final copy under Harsh's name goes through the global `humanize` skill.

## Extending it
- New pattern: prefer a spec-based renderer in `patterns/src/<slug>.py` (a `SPEC` dict passed to `from_spec`, see CONTRIBUTING.md), run `python patterns/render.py <slug>`, entry in `src/meta.ts`. `npm run build` fails on a missing preview, renderer, recipe path or unknown slug.
- New kind (something the CLI can draw): function + `KINDS` entry in `scripts/medialab/stills.py` or `video.py`, starter spec in `examples.py`, row in `recipes/medialab-cli.md`. `npm test` must pass.
- New world: entry in `src/worlds.ts` with proof patterns, matching theme in `scripts/medialab/themes.py`; add a brief row in `src/router.ts`.
- New format: add `formats/<name>.md` (structure table, design rules, checks) and a row in `formats/specs.md`.
- New hook: add a row to `hooks/hooks.md` with a fictional example. Patterns, not lines copied from creators.
- New recipe: only add commands you have run. Note the tool version. Put reusable code in `scripts/`.
- Solved a bug? Add it to "Known bugs already solved" in `playbook/05-verify.md`.
- New research: add to `research/` with links and an evidence level (strong / medium / weak).
- Teardowns: `research/teardowns/<name>.md` using the template in `research/03-inspiration.md`.
- Keep `SKILL.md` routing, `recipes/by-goal.md`, `README.md` and `llms.txt` in sync when adding files. `npm run build` fails if a skill .md is missing from `SKILL.md` or the root `llms.txt`. The site's `/llms.txt` is generated; the root `llms.txt` is the repo-local index.
- Bump `version` (and CHANGELOG.md) in `plugins/media-lab/.claude-plugin/plugin.json` when the skill changes, and run `claude plugin validate .`.

## Rules
- Original content only; fictional names in demos; no copied paid prompts or creator scripts.
- Commit as HarshSalunkhe2005.
