# End-to-end Short (free tools only)

Script → edge-tts voice with word timings → 9:16 visuals → word-highlight captions + hook title → loudness-normalised MP4.
Tested 2026-10-25: ffmpeg 8, Python 3.13, edge-tts 7, Windows. No API keys; edge-tts needs internet.

```bash
pip install edge-tts
python scripts/make_short.py examples/photo-sorter-short.txt out/            # gradient cards, zero assets
python scripts/make_short.py script.txt out/ --images s1.jpg s2.jpg s3.jpg   # one image per beat (Ken Burns)
python scripts/make_short.py script.txt out/ --voice en-IN-PrabhatNeural     # list voices: edge-tts --list-voices
```

Script file: one beat per line. Line 1 is the hook and also appears as the on-screen title for the first 2.2 s.
The example (`examples/photo-sorter-short.txt`, fictional club) gives a 24 s, 1080x1920 file with 68 captioned words at about -15 LUFS.
`examples/photo-sorter-short_frame1s.jpg` shows the frame at 1 s.

Output folder: `voice.mp3`, `words.json` (re-usable for other caption styles), `captions.ass`, `short.mp4`.

Then run `playbook/05-verify.md` on `short.mp4`, write the description with `humanize`, and set the platform's
synthetic-voice disclosure (the voice is TTS).

Limits (honest):
- Captions are chunked every 3 words and can run across a sentence boundary.
- Beat timing comes from word counts, so a beat with long words gets slightly short visuals.
- Gradient cards are placeholders. Real footage or images are what make it watchable.
