# ffmpeg recipes (tested on ffmpeg 7/8, Windows Git Bash)

Run from the job folder so relative paths work (Windows drive letters break the `subtitles` filter).

## Reframe 16:9 to 9:16 with a blurred fill
```bash
ffmpeg -i in.mp4 -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24:2,eq=brightness=-0.08[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:a copy -r 30 out_9x16.mp4
```
Prefer a centre crop when the subject stays in the middle: `-vf "crop=ih*9/16:ih,scale=1080:1920"`.

## Dark side panels instead of blur (looks less "edited")
```bash
ffmpeg -i in.mp4 -vf "scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x0d0d0f" out.mp4
```

## Trim without re-encode (cuts on keyframes) / frame-accurate
```bash
ffmpeg -ss 00:00:05 -to 00:00:20 -i in.mp4 -c copy cut.mp4
ffmpeg -ss 00:00:05 -to 00:00:20 -i in.mp4 -c:v libx264 -crf 18 -c:a aac cut_exact.mp4
```

## Remove silences (talking head first pass)
```bash
ffmpeg -i in.mp4 -af "silenceremove=start_periods=1:stop_periods=-1:stop_duration=0.35:stop_threshold=-35dB" -vn voice_tight.wav
```
For video, detect with `silencedetect` and cut both streams with the timestamps (`scripts/` can be extended).

## Loudness to -14 LUFS (two-pass is more accurate; one pass is fine for social)
```bash
ffmpeg -i in.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v copy out.mp4
```

## Music bed ducked under voice
```bash
ffmpeg -i voice.mp4 -i music.mp3 -filter_complex "[1:a]volume=0.25[m];[m][0:a]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=300[duck];[0:a][duck]amix=inputs=2:duration=first[a]" -map 0:v -map "[a]" -c:v copy out.mp4
```

## Ken Burns on a still (render big, then scale, to avoid jitter)
```bash
ffmpeg -loop 1 -i still.jpg -t 4 -vf "scale=2160:3840,zoompan=z='min(zoom+0.0012,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=120:s=1080x1920:fps=30" -pix_fmt yuv420p scene.mp4
```

## Concatenate same-format clips
```bash
printf "file '%s'\n" scene*.mp4 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy joined.mp4
```

## Captions
Build an ASS file from word timestamps with `scripts/captions.py`, then:
```bash
ffmpeg -i joined.mp4 -vf "subtitles=captions.ass:fontsdir=fonts" -c:a copy captioned.mp4
```

## Punch-in zoom on a section (110% from 3 s to 5 s, input already 1080x1920)
```bash
ffmpeg -i in.mp4 -vf "scale=w='if(between(t,3,5),1188,1080)':h='if(between(t,3,5),2112,1920)':eval=frame,crop=1080:1920" out.mp4
```
Use fixed pixel sizes: `iw*1.1` with `h=-2` fails on landscape input because the crop no longer fits.

## Checks
```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate:format=duration -of compact in.mp4
ffmpeg -i out.mp4 -af loudnorm=print_format=summary -f null - 2>&1 | grep "Input Integrated"
ffmpeg -ss 1 -i out.mp4 -frames:v 1 -y check.jpg
```

## Final export for upload
```bash
ffmpeg -i edit.mp4 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart final.mp4
```
