# 4. Assets and edit

## Order of operations (talking head or screen recording)
1. Cut silences and false starts.
2. Clean the voice (denoise, loudness normalise to about -14 LUFS for social).
3. Lay the A-roll, then B-roll or overlays on every claim.
4. Punch-in zooms (105 to 115%) on emphasis, max every few seconds.
5. Captions from word timestamps (see `recipes/ffmpeg.md#captions`).
6. Music bed at -20 to -25 dB under voice; sound hits on cuts, sparingly.
7. Reframe/export per platform (`formats/specs.md`).

## Order of operations (generated / faceless)
1. Voice first (TTS with word timestamps), because it sets the timing.
2. One visual per beat in a single consistent style; no text or logos inside generated images; no real faces.
3. Motion on stills (slow Ken Burns, alternate directions).
4. Captions, music, export.

## Asset rules
- Use footage you shot, licensed stock, or generated visuals. Note the licence of every third-party asset in the job folder.
- Fonts: bundle the font file with the job (captions break silently when the font is missing).
- Keep a job folder per piece: `brief.md`, `script.md`, `assets/`, `out/`, `notes.md` (what you'd change next time).
