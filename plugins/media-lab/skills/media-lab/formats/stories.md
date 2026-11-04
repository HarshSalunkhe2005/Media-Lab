# Stories (Instagram, WhatsApp, Facebook)

Canvas 1080x1920. A still frame is on screen for a few seconds, so each one carries one idea.

| Zone | Pixels (1080x1920) | What covers it |
|---|---|---|
| Top | y 0-250 | Profile picture, name, progress segments, close button |
| Bottom | y 1620-1920 | Reply box, reactions, send |
| Middle | y 250-1620 | Yours. Keep every line of text inside x 96-984 |

| Frame type | Job | Pattern |
|---|---|---|
| Poll / question | Ask one thing; leave a calm block for the sticker | `story-poll-space` |
| Countdown | The event, the place, the days left as the hero | `story-countdown` |
| Link | One line on why to tap, empty space for the link sticker | `story-link-space` |
| Update | Plain text that would also work as a notice on a door | `story-text-safe` |

Design rules:
- One idea per frame; 3-6 frames per sequence. The first frame says what the sequence is about.
- Leave the sticker area empty in the export (`"guides": false`): the app adds the sticker on top.
- Text at least 40 px at 1080 width; headline 90-110 px.
- Photos darkened only at the top, where the text sits; the rest stays as shot.

Checks before posting:
- `python scripts/medialab check frame.png --platform story` (UI zones, contrast at feed size).
- Tap through on a phone: nothing important under the name bar or the reply box.
- Dates and times match the official source.

Evidence: zone sizes follow `formats/specs.md` (medium; apps change their chrome, re-check on a phone before a launch).
