# MoviePy recipes (MoviePy 2.x API)

> Status: tested 2026-10-25 with MoviePy 2.1.2 (Python 3.13, Windows). The runnable version is `scripts/moviepy_demo.py`:
> `python moviepy_demo.py landscape.mp4 still1.jpg out.mp4` gives a 1080x1920 MP4 with audio. The snippet below is the same logic, annotated.
> Install into its own venv (`pip install "moviepy>=2,<3"`); an old global MoviePy 0.2/1.x will not run it.

Use MoviePy when the edit needs Python logic. For plain cuts and filters, ffmpeg is faster.

```python
from moviepy import ColorClip, VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip, vfx

W, H = 1080, 1920

# 1. Reframe landscape footage into 9:16 with dark panels
src = VideoFileClip("in.mp4").resized(width=W)
bg = ColorClip((W, H), color=(13, 13, 15)).with_duration(src.duration)
vertical = CompositeVideoClip([bg, src.with_position("center")], size=(W, H))

# 2. Stills to scenes with a slow zoom
def scene(path, dur):
    return (ImageClip(path).with_duration(dur).resized(height=H)
            .with_effects([vfx.Resize(lambda t: 1 + 0.03 * t)]).with_position("center"))

clips = [scene(p, 3.5) for p in ["s1.jpg", "s2.jpg", "s3.jpg"]]
body = CompositeVideoClip([concatenate_videoclips(clips, method="compose")], size=(W, H))

# 3. Voice + music bed
voice = AudioFileClip("voice.mp3")
final = body.with_duration(voice.duration).with_audio(voice)
final.write_videofile("out.mp4", fps=30, codec="libx264", audio_codec="aac", preset="medium")
```

Captions: generate ASS with `scripts/captions.py` and burn with ffmpeg afterwards; MoviePy TextClip captions are slow
and need ImageMagick-free font paths.

Gotchas:
- MoviePy 2 renamed methods (`resized`, `with_duration`, `with_position`, `with_effects`); 1.x tutorials won't run as-is.
- Close clips (`clip.close()`) in loops or Windows keeps the files locked.
