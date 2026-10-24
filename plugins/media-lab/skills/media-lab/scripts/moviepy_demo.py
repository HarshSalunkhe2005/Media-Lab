"""MoviePy 2.x recipe, runnable: landscape clip -> 9:16 with dark panels, plus still scenes with a slow zoom.

Usage: python moviepy_demo.py landscape.mp4 still1.jpg [still2.jpg ...] out.mp4
Needs: pip install "moviepy>=2,<3"  (MoviePy 1.x/0.2 APIs differ and will not run this)
"""
import sys

from moviepy import ColorClip, CompositeVideoClip, ImageClip, VideoFileClip, concatenate_videoclips, vfx

W, H, FPS = 1080, 1920, 30


def vertical_from_landscape(path: str) -> CompositeVideoClip:
    src = VideoFileClip(path).resized(width=W)
    bg = ColorClip((W, H), color=(13, 13, 15)).with_duration(src.duration)
    return CompositeVideoClip([bg, src.with_position("center")], size=(W, H)).with_audio(src.audio)


def still_scene(path: str, dur: float = 3.0) -> CompositeVideoClip:
    img = ImageClip(path).with_duration(dur).resized(height=H)
    zoom = img.with_effects([vfx.Resize(lambda t: 1 + 0.04 * t)]).with_position("center")
    return CompositeVideoClip([zoom], size=(W, H))


if __name__ == "__main__":
    *inputs, out = sys.argv[1:]
    clips = [vertical_from_landscape(inputs[0])] + [still_scene(p) for p in inputs[1:]]
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(out, fps=FPS, codec="libx264", audio_codec="aac", preset="medium", logger=None)
    for c in clips:
        c.close()
    print(f"wrote {out} ({final.duration:.1f}s)")
