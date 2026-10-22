# Existing tools, repos and Claude skills (October 2026 scan)

What already exists for content creation with code and agents, what each is good at, and what Media Lab takes from it.
We rebuild ideas in our own words and code. Nothing here is copied.

## Claude Code skills and plugins

| Project | What it does | What we take |
|---|---|---|
| [Remotion's official Claude Code plugin](https://remotion.dev/docs/ai/claude-code-plugin) | Bundles Remotion agent skills: project setup, layout and animation, rendering, captions, upgrades. Installed through Remotion's own marketplace. | Use it for programmatic motion graphics instead of re-writing Remotion knowledge. Media Lab only adds when to choose Remotion and how it fits the pipeline (`recipes/remotion.md`). |
| [Claude Code Video Toolkit (wilwaldon)](https://github.com/wilwaldon/Claude-Code-Video-Toolkit) | A collection of skills and MCP servers: Remotion, Manim, screen recording, YouTube clipping, FFmpeg post-processing. | Confirms the split between generating video from code and editing footage. Our recipes cover both sides. |
| [HeyGen video-edit skill](https://claudemarketplaces.com/skills/heygen-com/skills/video-edit) | Conversational ffmpeg edits on existing footage. | The pattern of "describe the edit, get one ffmpeg command, verify the output". |
| [Raw recording to published video guide (learnwithhasan)](https://learnwithhasan.com/guide/claude-code-video-editing/) | Six-skill flow: cut silences, visual beats, voice isolation, sound effects, packaging, upload. | The order of operations for talking-head edits (`playbook/04-edit.md`). |
| [Tella's skill roundup](https://www.tella.com/blog/best-claude-code-skills) | List of popular skills with install commands. | Survey only. |

## Open-source pipelines and libraries

| Project | What it does | What we take |
|---|---|---|
| [Captacity](https://github.com/unconv/captacity) / [Captametropolis](https://pypi.org/project/captametropolis) | Whisper + MoviePy auto-captions for Shorts; the fork adds fonts, shadows and word highlighting. | Word-level timestamps are the base unit for captions. Our caption recipe uses ASS subtitles through ffmpeg instead (faster, no ImageMagick). |
| [Auto YouTube Shorts Maker](https://github.com/Binary-Bytes/Auto-YouTube-Shorts-Maker) | MoviePy + gTTS voiceover Shorts. | A minimal end-to-end skeleton. Too thin on scripting quality, which is where most of the value is. |
| [remotion-dev/template-tiktok](https://github.com/orgs/remotion-dev/repositories) and [Remotion resources](https://remotion.dev/resources) | Official TikTok-style caption template plus community helpers. | Starting point when a video needs animated type, not just burned-in captions. |
| [GitHub topic: auto-captions](https://github.com/topics/auto-captions), [topic: moviepy](https://www.GitHub.com/topics/moviepy) | Many small Shorts automation repos. | Most stop at "stitch stock clips + TTS". The gap is judgement: hooks, critique, packaging. Media Lab fills that gap. |

## Harsh's own prior work

- **ShortsAgent / YT-Bot** (`C:\Users\Harsh\Projects\ShortsAgent`): trend scout, writer and critic loop with scored verdicts
  (ship needs hook >= 7, retention >= 7, originality >= 6), edge-tts with word timestamps, per-scene images,
  ffmpeg Ken Burns motion, ASS word-highlight captions, human review bay, private-by-default upload with the
  synthetic-media flag. Media Lab generalises its rules into `hooks/`, `playbook/` and `recipes/ffmpeg.md`.
- **SVL 26-27 media work**: posters, schedule and standings stories, award templates and photo sorting for a college
  volleyball league. Lessons kept in `playbook/06-event-coverage.md` (templates that look native, not edited; date and
  dedupe rules for sorting event media).

## Gaps nobody fills well (why Media Lab exists)

1. A **procedure** that forces a brief and a hook before any asset is made.
2. **Format specs in one place** (sizes, safe zones, lengths, caption rules) that an agent can read in one fetch.
3. A **critique rubric** so drafts are scored and revised instead of shipped on first try.
4. **Honest sourcing**: most "growth" numbers online come from vendors. We mark evidence levels (see `02-what-works.md`).
