# Remotion (React as video)

Use for kinetic typography, animated UI mockups, charts, and branded templates rendered many times with different data.

## Setup
- Install Remotion's official Claude Code plugin for API-level guidance: see https://remotion.dev/docs/ai/claude-code-plugin
  (it ships Remotion's own skills for setup, animation, rendering and captions). Media Lab does not duplicate those.
- New project: `npx create-video@latest` (pick the blank or TikTok template). Preview: `npx remotion studio`.
- Render: `npx remotion render <CompositionId> out.mp4 --props=data.json`.

## How it fits our pipeline
1. Brief, package and script as usual (playbook).
2. Make one composition per format at the spec size (1080x1920 at 30 fps for vertical).
3. Drive it with a JSON props file per variant (event result, stat, quote), the same way the poster scripts use a data file per day.
4. Captions: Remotion's caption helpers or our ASS file burned afterwards with ffmpeg.
5. Verify the rendered MP4 with `playbook/05-verify.md`.

Licence note: Remotion is free for individuals and small teams; companies above its size threshold need a company licence. Check before using it for a client.
