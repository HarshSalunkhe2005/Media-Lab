# Recipes by goal

Pick the goal, read the files in order. Every route starts with `playbook/01-brief.md` and ends with `playbook/05-verify.md`.

| Goal | Format | Hooks | Build with | Notes |
|---|---|---|---|---|
| **Turn a project into a 30 s launch Short** | `formats/launch-video.md`, `formats/short-video.md` | Result first, Before/after flash, Build-log hooks (`hooks/hooks.md`) | `recipes/end-to-end-short.md` with screen-recording stills, or `recipes/ffmpeg.md` on real footage | Record UI at 2x, zoom on the cursor. `brag` skill can draft it; review against launch-video.md. |
| **LinkedIn carousel from a report** | `formats/carousel.md`, `formats/text-posts.md` | Unfinished number, Contrarian, Proof object | `recipes/carousel.md` (HTML → PDF) | One finding per slide; real numbers from the report only; link in first comment. |
| **Event highlight reel** | `formats/short-video.md` (Event recap row) | Mid-action, Visible stakes, Proof object | `recipes/ffmpeg.md` (trim, concat, reframe, music duck) | Best moment first; result card at the end; `playbook/06-event-coverage.md`. |
| **Daily schedule / standings story for an event** | `formats/specs.md` (story row) | headline = the one number or name | `recipes/carousel.md` Option B (Pillow + data file per day) | Pull data from the official source, never memory. |
| **Award / result poster** | `formats/thumbnail.md` (overlay checklist) | — | `recipes/carousel.md` Option B | Native-looking text, faces not cropped, names checked. |
| **Faceless explainer Short** | `formats/short-video.md` | Specific question, Myth bust | `recipes/end-to-end-short.md` | Facts need sources; disclose synthetic voice. |
| **Talking-head tip video** | `formats/short-video.md` | Direct callout, Mistake reveal | `playbook/04-edit.md` order + `recipes/ffmpeg.md` (silence cut, loudnorm, punch-in, captions) | |
| **YouTube thumbnail** | `formats/thumbnail.md` | text adds what the title doesn't | Pillow or HTML; test at 160 px | 2-3 different variants for Test & Compare. |
| **X thread from a blog post** | `formats/text-posts.md` | Result first, Unfinished number | — | Tweet 1 stands alone; link in reply. |
| **Reframe a landscape video for Reels** | `formats/specs.md` safe zones | — | `recipes/ffmpeg.md` (centre crop, dark panels, blur) or `scripts/moviepy_demo.py` | Prefer crop when the subject stays centred. |
| **Burn captions onto an existing clip** | `formats/specs.md` safe zones | — | Whisper word timestamps → `scripts/captions.py` → ffmpeg `subtitles` | Run ffmpeg from the job folder (relative paths). |
