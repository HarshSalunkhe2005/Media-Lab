# Event coverage (college fests, leagues, launches)

Learned running media for a college sports league. Applies to any multi-day event.

## Before the event
- Lock a template set early: schedule story, standings, match result, player award, champions/runners-up, recap.
  Same fonts, palette, safe zones and date format across all of them.
- Build templates as code (Pillow/HTML) with a data file per day, so updates are one command, not a redesign.
- Agree on the source of truth for results (official site or sheet) and pull from it, never from memory.

## Templates that look native, not edited
- When re-using a previous poster as a template, rebuild text layers in the original font and fill; never paste a patch box over old text.
- Photos: frame faces with headroom; never crop hands or heads; remove distracting background people only when it looks untouched.
- Do not stretch photos to fill. If the aspect doesn't fit, use dark side panels in the template's style, not blur.
- Check date alignment, spelling of names and team names against the source before export.

## During the event
- One shared drop folder per day; ask shooters to upload originals (not WhatsApp-compressed) when possible.
- Post the schedule and standings stories at the same time each day.

## After: sorting the media
- Date by camera EXIF or camera filename first; WhatsApp send time only as a fallback (before ~4 AM counts as the previous day).
- Dedupe in this order: exact checksum (safe), then perceptual image hash with a tight threshold, then frame comparison for video.
  Never dedupe videos by duration alone. Anything uncertain goes to a `not_sure/` folder for a human, never silently dropped.
- Stage in your own drive first, verify counts per folder, then copy (not move) to the shared final drive.
