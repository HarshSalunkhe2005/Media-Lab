# Thumbnails and covers

- 1280x720 for YouTube; Reels cover designed at 1080x1920 with the centre 1080x1350 holding everything important.
- One subject, one idea. A face with a clear emotion, or one object/result shown large.
- 0-4 words of text. The text adds what the title doesn't say; it never repeats the title.
- High contrast between subject and background; test in greyscale.
- Test at 160 px wide (`ffmpeg -i thumb.png -vf scale=160:-1 small.png`). If you can't tell what it is, redo it.
- Keep clear of the bottom-right corner (duration badge).
- Make 2-3 genuinely different variants and use YouTube Test & Compare; it picks by watch-time share. Give each test enough impressions before deciding.
- Never use a real person's face or a brand's logo without rights; never imply an endorsement.

## Text overlay checklist (thumbnails, covers, posters, on-video titles)

- [ ] 0-4 words on thumbnails, max ~6 words for an on-video hook title, one line per idea
- [ ] Font: one bold display face, real font file bundled (fallback fonts change width and break layout)
- [ ] Size: thumbnail text readable at 160 px wide; 9:16 titles at least 64 px on a 1080 canvas
- [ ] Contrast: outline, shadow or a semi-opaque box behind text on busy images (check in greyscale)
- [ ] Placement: inside the safe zone (`specs.md`); nothing in the bottom-right on YouTube; nothing under the like/comment column on vertical
- [ ] Wrap long lines yourself (about 20 characters per line at 72 px on 1080 wide), one draw call per line in ffmpeg
- [ ] No text over faces or the ball/subject
- [ ] Spelling of names, teams, scores and dates checked against the source
- [ ] Same corner and style for the handle/logo across a series
- [ ] Looks native: matches the template's existing type and colours, not a pasted patch
