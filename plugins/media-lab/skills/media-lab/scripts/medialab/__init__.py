"""Media Lab: spec-driven builders for social and video content, plus pre-publish checks.

    python scripts/medialab make brief.json -o out/
    python scripts/medialab check out/short.mp4 --platform shorts
    python scripts/medialab kinds | themes | example <kind>

Needs Pillow (pip install pillow) and ffmpeg on PATH for video. Fonts are bundled.
"""
__version__ = "1.1.0"
