# AGENTS.md

Guide for AI agents using or extending Media Lab.

## Using it
1. Read `plugins/media-lab/skills/media-lab/SKILL.md` first (procedure + hard rules).
2. Follow the playbook in order: `01-brief` → `02-package` → `03-script` → `critique` → `04-edit` → `05-verify`.
3. Pull specs from `formats/specs.md`, hooks from `hooks/hooks.md`, commands from `recipes/`.
4. Final copy under Harsh's name goes through the global `humanize` skill.

## Extending it
- New format: add `formats/<name>.md` (structure table, design rules, checks) and a row in `formats/specs.md`.
- New hook: add a row to `hooks/hooks.md` with a fictional example. Patterns, not lines copied from creators.
- New recipe: only add commands you have run. Note the tool version. Put reusable code in `scripts/`.
- Solved a bug? Add it to "Known bugs already solved" in `playbook/05-verify.md`.
- New research: add to `research/` with links and an evidence level (strong / medium / weak).
- Teardowns: `research/teardowns/<name>.md` using the template in `research/03-inspiration.md`.
- Bump `version` in `plugins/media-lab/.claude-plugin/plugin.json` when the skill changes, and run `claude plugin validate .`.

## Rules
- Original content only; fictional names in demos; no copied paid prompts or creator scripts.
- Commit as HarshSalunkhe2005 <nightfuryharsh@gmail.com>. No AI attribution in commits or files.
