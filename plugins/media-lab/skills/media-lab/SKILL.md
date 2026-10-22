---
name: media-lab
description: Use whenever you make social or video content - YouTube Shorts, Instagram Reels, TikToks, carousels, LinkedIn or X posts, threads, launch or promo videos, thumbnails, captions, scripts, hooks, event posters/stories - or edit, caption, reframe or render video with ffmpeg, MoviePy or Remotion. Gives the brief-to-publish procedure, format specs and safe zones, a hook library, a critique rubric and tested tooling recipes. Not for website UI (use ui-lab).
---

# Media Lab: content with judgement, not templates

Media Lab is Harsh's reference library for content creation. Repo: `C:\Users\Harsh\Projects\Media-Lab`
(GitHub `HarshSalunkhe2005/Media-Lab`, private). This skill folder holds everything an agent needs; the repo root adds
`research/` (sources and evidence levels) and `tools/`.

## Procedure (do not skip steps)

1. **Brief** (`playbook/01-brief.md`): audience, one idea, platform, goal metric, voice. Write it down first.
2. **Package first** (`playbook/02-package.md`): title, hook line, thumbnail or cover idea before any production.
3. **Script** (`playbook/03-script.md`): pick a hook from `hooks/hooks.md`, follow the format file, then run the
   critique rubric (`playbook/critique.md`). Revise until it scores "ship". Kill weak ideas instead of polishing them.
4. **Assets and edit** (`playbook/04-edit.md`): pick the tool with `recipes/choose-a-tool.md`, then follow
   `recipes/ffmpeg.md`, `recipes/moviepy.md` or `recipes/remotion.md`.
5. **Verify** (`playbook/05-verify.md`): watch the output, check safe zones, captions, audio levels, length, file specs.
6. **Publish and learn**: caption and post copy go through the `humanize` skill; log one metric to compare next time.

## Where things are

| What | File |
|---|---|
| Format specs (sizes, lengths, safe zones) | `formats/specs.md` |
| Per-format structures | `formats/short-video.md`, `formats/carousel.md`, `formats/text-posts.md`, `formats/launch-video.md`, `formats/thumbnail.md` |
| Hook library + ending library | `hooks/hooks.md` |
| Fill-in templates (script, carousel, post) | `hooks/templates.md` |
| Voice rules | `playbook/voice.md` (defers to `humanize`) |
| Event / college media (posters, stories, sorting photos) | `playbook/06-event-coverage.md` |
| Tool recipes | `recipes/` |

## Hard rules

- Original content only. Never clip, re-upload or recreate another creator's video, script, thumbnail or art.
  Study techniques, rebuild in our own words.
- Demos and examples use fictional names and brands.
- Never state a number as fact unless it comes from a source you can cite. Vendor "stats" are hypotheses.
- AI-generated or synthetic media is disclosed where the platform asks (YouTube's altered/synthetic flag).
- Anything posted under Harsh's name goes through `humanize`. No AI tells, no "AI made this" credits in his work.
- Do not publish, post or upload without Harsh's explicit go-ahead for that piece.
