# 5. Verify (bounded, every time)

Watch the exported file, not the timeline. Then check:

- [ ] Specs: resolution, fps, aspect, length within the platform limit (`ffprobe -v error -show_entries stream=width,height,r_frame_rate:format=duration out.mp4`)
- [ ] First frame works as a cover (many feeds show it before play)
- [ ] Hook is spoken AND on screen within 2 s
- [ ] Captions: no word hidden under platform UI (safe zones), no line wider than ~80% of frame, no misspelled names
- [ ] Audio: voice clearly above music, no clipping, loudness about -14 LUFS (`ffmpeg -i out.mp4 -af loudnorm=print_format=summary -f null -`)
- [ ] No black frames or frozen frames at cuts
- [ ] Nothing copyrighted or third-party you do not have rights to; names in demos are fictional
- [ ] Post copy humanized; facts sourced
- [ ] Harsh approved before anything is posted

Grab proof frames: `ffmpeg -ss 1 -i out.mp4 -frames:v 1 check_1s.jpg` (repeat at a few timestamps) and look at them.

## Known bugs already solved
- **Captions missing in render**: ffmpeg `subtitles=` filter on Windows chokes on absolute paths with `C:`. Run ffmpeg with
  `cwd` set to the job folder and pass a relative path; pass `fontsdir=` too.
- **Zoompan jitter**: render stills at 2x output size before `zoompan`, then scale down.
- **WhatsApp-sent media has no camera date**: the send time is not the capture time; sends before ~4 AM belong to the previous day.
- **Duplicate detection by video length alone is wrong**: many different clips share a length. Compare frames, or use file checksums.
- **drawtext box glyphs at line breaks**: a multi-line `textfile` shows a box at each break (ffmpeg 8, Windows). Draw one `drawtext` per line.
- **drawtext uses a monospace fallback / "Fontconfig error"**: Windows ffmpeg has no fontconfig. Pass `fontfile='C\:/Windows/Fonts/arialbd.ttf'` (escape the colon).
- **edge-tts voice comes out around -20 LUFS**: add `loudnorm=I=-14:TP=-1.5:LRA=11` on the final mux.
- **Old MoviePy installed globally**: MoviePy 2 code fails on 0.2/1.x. Use a venv with `moviepy>=2,<3`.
