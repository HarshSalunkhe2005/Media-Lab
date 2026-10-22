# Choose a tool

| Job | Use | Why |
|---|---|---|
| Cut, trim, reframe, concat, loudness, burn captions on real footage | **ffmpeg** (`ffmpeg.md`) | fastest, scriptable, no project setup |
| Stills + voice into a Short, Ken Burns, word captions | **ffmpeg** + `scripts/captions.py` | what ShortsAgent ships with |
| Python logic over clips (compositing, conditional edits, data-driven) | **MoviePy** (`moviepy.md`) | readable Python; slower renders |
| Kinetic type, animated UI mockups, charts, branded templates rendered many times | **Remotion** (`remotion.md`) | React components as video; install Remotion's own Claude Code plugin for API detail |
| Carousels, posters, thumbnails, result cards | **HTML/CSS → PNG** or **Pillow** (`carousel.md`) | exact type control; one data file per variant |
| Math/diagram animations | Manim | precise geometry and equations |
| Captions from speech | Whisper (local `openai-whisper` or `faster-whisper`) for word timestamps; edge-tts gives timestamps for free when we generate the voice | |
