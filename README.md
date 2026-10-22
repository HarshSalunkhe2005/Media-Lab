# Media Lab

A reference library for making content: Shorts, Reels, TikToks, carousels, LinkedIn and X posts, launch videos,
thumbnails and event media. It's the media sibling of [UI Lab](https://ui-lab-weld.vercel.app): parts (formats, hooks,
recipes) plus judgement (a procedure and a critique rubric), packaged as a Claude Code plugin.

## Install as a Claude Code plugin

```
/plugin marketplace add HarshSalunkhe2005/Media-Lab
/plugin install media-lab@media-lab
```

The repo is private, so the machine needs GitHub access to it (signed-in `git` credentials or `GITHUB_TOKEN`).
Once installed, the `media-lab` skill loads whenever you work on content.

## What's inside

```
.claude-plugin/marketplace.json      marketplace entry
plugins/media-lab/                   the plugin
  skills/media-lab/SKILL.md          entry point: procedure + hard rules
  skills/media-lab/playbook/         brief, package, script, critique, edit, verify, voice, event coverage
  skills/media-lab/formats/          specs + safe zones, short video, carousel, text posts, launch video, thumbnails
  skills/media-lab/hooks/            hook and ending library, fill-in templates
  skills/media-lab/recipes/          choose a tool, ffmpeg (tested), MoviePy, Remotion, carousels/posters
  skills/media-lab/scripts/          captions.py: word timestamps -> highlighted ASS captions
research/                            existing tools, what works (with evidence levels), inspiration + teardown template
AGENTS.md, llms.txt                  machine-readable index
```

## Rules

- Original content only. Study techniques; never copy scripts, footage, thumbnails or paid prompts.
- Demo content uses fictional names.
- Numbers need a source; vendor stats are treated as hypotheses (see `research/02-what-works.md`).
- Anything posted under Harsh's name goes through the `humanize` skill.
