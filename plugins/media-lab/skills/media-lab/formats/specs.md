# Format specs

Platforms change these often. Check the platform's help page before a big launch; update this file when they change.

| Format | Canvas | Length | Notes |
|---|---|---|---|
| YouTube Shorts | 1080x1920, 9:16, 30 or 60 fps | up to 3 min; sweet spot often 25-45 s (weak evidence) | Title matters; first frame often shown as cover |
| Instagram Reels | 1080x1920, 9:16 | up to 3 min in-app; keep most under 60 s | Cover is cropped to 4:5 (1080x1350) in the profile grid |
| TikTok | 1080x1920, 9:16 | 15 s to 10 min | Captions and right-side buttons cover a lot of frame |
| IG carousel | 1080x1350 (4:5) or 1080x1440 (3:4); up to 20 slides | 6-10 slides typical | Every slide same size; slide 2 is a second hook |
| LinkedIn document | PDF, 1080x1350 or 1080x1080 pages | 5-10 pages | Upload as document; title shows on the cover |
| LinkedIn / X image | 1200x627 (link-style) or 1080x1350 | | X crops tall images in the feed preview |
| YouTube thumbnail | 1280x720, 16:9, under 2 MB | | Readable at 160 px wide; avoid bottom-right (duration badge) |
| YouTube long | 1920x1080 or 3840x2160 | | Chapters in description |
| IG/WhatsApp story | 1080x1920 | 15 s per frame (IG) | Top 250 px and bottom 300 px get covered |

## Safe zones for 9:16 (1080x1920)

Keep captions and key text inside **x 90-990, y 250-1500**. Avoid:
- top ~250 px: account name, progress bar, search
- bottom ~420 px: caption text, audio name, buttons (TikTok worst, Shorts similar)
- right ~120 px: like/comment/share column

A caption baseline around y = 1250-1400 sits above the UI on all three apps.

## Export settings that upload cleanly
`-c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart`
