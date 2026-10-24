/*
 * Pattern metadata: plain data, no React. Single source of truth for the gallery, /llms.txt, /patterns.json,
 * /docs/<slug>.md and the router. Add a pattern = a renderer in patterns/src/<slug>.py + an entry here,
 * then `python patterns/render.py <slug>` to make its preview. The build fails if the preview or file is missing.
 */
export const CATEGORIES = ['Carousels', 'Event media', 'Thumbnails', 'Hooks', 'Captions', 'Shorts', 'Reframes'] as const
export type Category = (typeof CATEGORIES)[number]

export type PatternMeta = {
  slug: string
  title: string
  category: Category
  summary: string
  /** When to reach for this. At least one. */
  when: string[]
  /** Canvas and length, e.g. "1080x1350 (4:5)". */
  format: string
  /** Skill pages that explain the technique, relative to plugins/media-lab/skills/media-lab/. */
  recipe: string[]
  tags: string[]
  /** Renders in the gallery; always real output of the renderer. */
  preview: string
}

const P = (slug: string, ext: 'jpg' | 'mp4' = 'jpg') => `previews/${slug}.${ext}`

export const META: PatternMeta[] = [
  // Carousels
  { slug: 'poetry-film-photo', title: 'Poetry on a graded photo', category: 'Carousels', format: '1080x1350 (4:5)',
    summary: 'Real CC0 photo, one muted film grade, plain Garamond set in the darkest edge, small slide counter.',
    when: ['Poetry, quotes or reflective captions', 'A set that must look shot, not generated', 'Instagram carousels aimed at saves and sends'],
    recipe: ['playbook/taste.md', 'recipes/stock-photos.md', 'formats/carousel.md'], tags: ['poetry', 'quote', 'film grade', 'garamond', 'real photo'], preview: P('poetry-film-photo') },
  { slug: 'poetry-paper', title: 'Stanza on paper', category: 'Carousels', format: '1080x1350 (4:5)',
    summary: 'No photo: a warm paper tone, wide margins, one serif, the stanza keeps its own line breaks.',
    when: ['Breather slide between photo slides', 'Longer stanzas that would fight a busy photo'],
    recipe: ['playbook/taste.md', 'formats/carousel.md'], tags: ['poetry', 'paper', 'serif', 'typography'], preview: P('poetry-paper') },
  { slug: 'carousel-cover-promise', title: 'Cover slide with a promise', category: 'Carousels', format: '1080x1350 (4:5)',
    summary: 'Slide 1: one sentence-case promise in the photo\'s calm area, darkened only behind the text, plus a 1/7 cue.',
    when: ['First slide of any educational carousel', 'LinkedIn document covers'],
    recipe: ['formats/carousel.md', 'playbook/02-package.md'], tags: ['cover', 'hook', 'carousel', 'linkedin document'], preview: P('carousel-cover-promise') },
  { slug: 'list-point-slide', title: 'Numbered point slide', category: 'Carousels', format: '1080x1350 (4:5)',
    summary: 'Middle slide: big number, short headline, two supporting lines, the same grid on every slide.',
    when: ['List and tip carousels', 'Turning a checklist into slides'],
    recipe: ['formats/carousel.md', 'hooks/templates.md'], tags: ['list', 'tips', 'grid'], preview: P('list-point-slide') },
  { slug: 'data-story-number', title: 'One giant number', category: 'Carousels', format: '1080x1350 (4:5)',
    summary: 'A single earned statistic, one plain sentence on what it means, and the source in small type.',
    when: ['Reports and recaps turned into posts', 'Data stories where one figure carries the point'],
    recipe: ['formats/carousel.md', 'recipes/carousel.md'], tags: ['data', 'statistic', 'swiss', 'report'], preview: P('data-story-number') },
  { slug: 'cta-last-slide', title: 'Last slide with one ask', category: 'Carousels', format: '1080x1350 (4:5)',
    summary: 'Closing slide with a single clear ask (save, send) tied to the goal metric, in the set\'s photo style.',
    when: ['Final slide of every carousel', 'When the goal is saves or sends'],
    recipe: ['formats/carousel.md', 'hooks/hooks.md'], tags: ['cta', 'save', 'send', 'ending'], preview: P('cta-last-slide') },
  // Event media
  { slug: 'event-result-card', title: 'Match result card', category: 'Event media', format: '1080x1350 (4:5)',
    summary: 'Score as the hero over a real court photo, both teams, one moment from the match and the next fixture.',
    when: ['Sports leagues and tournaments', 'Any competition result post'],
    recipe: ['playbook/06-event-coverage.md', 'recipes/carousel.md'], tags: ['sports', 'score', 'result', 'league'], preview: P('event-result-card') },
  { slug: 'event-award-card', title: 'Player award card', category: 'Event media', format: '1080x1350 (4:5)',
    summary: 'Photo with the subject uncropped, the award small, the name big, one real stat underneath.',
    when: ['MVP, best player and award announcements', 'Speaker or winner spotlights'],
    recipe: ['playbook/06-event-coverage.md', 'formats/thumbnail.md'], tags: ['award', 'mvp', 'portrait', 'sports'], preview: P('event-award-card') },
  { slug: 'event-schedule-story', title: 'Daily schedule story', category: 'Event media', format: '1080x1920 (9:16 story)',
    summary: 'Plain fixtures table inside the story safe zone, rendered from a data list so each day is one command.',
    when: ['Multi-day events posting a daily schedule', 'Any timetable that changes every day'],
    recipe: ['playbook/06-event-coverage.md', 'formats/specs.md'], tags: ['schedule', 'story', 'fixtures', 'table'], preview: P('event-schedule-story') },
  // Thumbnails
  { slug: 'thumb-object-words', title: 'Object and three words', category: 'Thumbnails', format: '1280x720 (16:9)',
    summary: 'One real object, three words that add what the title does not say, kept clear of the duration badge.',
    when: ['YouTube long-form and tutorials', 'When there is no face to use'],
    recipe: ['formats/thumbnail.md'], tags: ['thumbnail', 'youtube', 'object', 'text'], preview: P('thumb-object-words') },
  { slug: 'thumb-big-number', title: 'Big number thumbnail', category: 'Thumbnails', format: '1280x720 (16:9)',
    summary: 'A huge numeral and one context word over a darkened real photo; still readable at 160 px wide.',
    when: ['Results, experiments and counts', 'Build logs with a measurable outcome'],
    recipe: ['formats/thumbnail.md'], tags: ['thumbnail', 'number', 'contrast'], preview: P('thumb-big-number') },
  // Hooks
  { slug: 'hook-title-card', title: 'Result-first hook title', category: 'Hooks', format: '1080x1920 (first 2 s)',
    summary: 'The hook as on-screen text for the first two seconds: wrapped by hand, one box per line, upper safe zone.',
    when: ['Every Short that opens on a claim or result', 'Muted autoplay feeds'],
    recipe: ['hooks/hooks.md', 'formats/thumbnail.md'], tags: ['hook', 'title', 'shorts', 'reels'], preview: P('hook-title-card') },
  { slug: 'hook-unfinished-number', title: 'Unfinished-number hook', category: 'Hooks', format: '1080x1920 (first 2 s)',
    summary: 'A countdown promise ("4 ... the last one ...") with a number badge, so viewers wait for the payoff.',
    when: ['List and tips Shorts', 'Tool roundups'],
    recipe: ['hooks/hooks.md'], tags: ['hook', 'countdown', 'list'], preview: P('hook-unfinished-number') },
  // Captions
  { slug: 'caption-word-highlight', title: 'Word-highlight captions', category: 'Captions', format: '1080x1920',
    summary: 'Three-word chunks, uppercase, the spoken word in yellow and slightly larger. The Shorts default.',
    when: ['Talking head and voiceover Shorts', 'Content watched muted'],
    recipe: ['scripts/captions.py', 'formats/specs.md'], tags: ['captions', 'subtitles', 'ass', 'highlight'], preview: P('caption-word-highlight') },
  { slug: 'caption-boxed', title: 'Boxed captions', category: 'Captions', format: '1080x1920',
    summary: 'Opaque box behind each chunk (ASS BorderStyle 3). The most readable choice on busy, bright footage.',
    when: ['Busy or bright backgrounds', 'Accessibility first'],
    recipe: ['scripts/captions.py'], tags: ['captions', 'box', 'readability'], preview: P('caption-boxed') },
  { slug: 'caption-quiet-lowercase', title: 'Quiet lowercase captions', category: 'Captions', format: '1080x1920',
    summary: 'Lowercase serif, no highlight or pop, only a soft shadow. Captions that do not shout.',
    when: ['Poetry, slow vlogs, ambient edits', 'When loud captions would fight the mood'],
    recipe: ['scripts/captions.py', 'playbook/taste.md'], tags: ['captions', 'serif', 'lowercase', 'calm'], preview: P('caption-quiet-lowercase') },
  // Shorts
  { slug: 'short-word-captions', title: 'Zero-asset voiceover Short', category: 'Shorts', format: '1080x1920, 20-45 s',
    summary: 'Script to edge-tts voice, gradient cards, word captions and a hook title. Runs with no footage at all.',
    when: ['Drafting a Short before footage exists', 'Explainers where the words carry it'],
    recipe: ['recipes/end-to-end-short.md', 'scripts/make_short.py'], tags: ['short', 'tts', 'edge-tts', 'faceless'], preview: P('short-word-captions', 'mp4') },
  { slug: 'short-kenburns-stills', title: 'Real stills with Ken Burns', category: 'Shorts', format: '1080x1920, 20-45 s',
    summary: 'One CC0 photo per beat with a slow push, voice and captions on top. Real images make it watchable.',
    when: ['Story and mood Shorts', 'Recaps built from photos'],
    recipe: ['recipes/end-to-end-short.md', 'recipes/stock-photos.md'], tags: ['short', 'ken burns', 'stills', 'photos'], preview: P('short-kenburns-stills', 'mp4') },
  { slug: 'punch-in-zoom', title: 'Punch-in on emphasis', category: 'Shorts', format: '1080x1920',
    summary: 'Jump to 110% for the key line, then back. Fixed pixel sizes so the crop always fits.',
    when: ['Talking head emphasis', 'Breaking up a static stretch'],
    recipe: ['recipes/ffmpeg.md'], tags: ['zoom', 'edit', 'ffmpeg'], preview: P('punch-in-zoom', 'mp4') },
  // Reframes
  { slug: 'reframe-dark-panels', title: '16:9 to 9:16 with dark panels', category: 'Reframes', format: '1920x1080 in, 1080x1920 out',
    summary: 'Landscape footage centred on near-black panels. Reads as intentional rather than edited.',
    when: ['Repurposing landscape video for Shorts', 'When the whole frame matters'],
    recipe: ['recipes/ffmpeg.md', 'formats/specs.md'], tags: ['reframe', 'vertical', 'ffmpeg'], preview: P('reframe-dark-panels', 'mp4') },
  { slug: 'reframe-blur-fill', title: '16:9 to 9:16 with blur fill', category: 'Reframes', format: '1920x1080 in, 1080x1920 out',
    summary: 'A blurred, darkened copy fills the background behind the centred footage.',
    when: ['When dark panels look too empty', 'Colourful footage'],
    recipe: ['recipes/ffmpeg.md'], tags: ['reframe', 'blur', 'vertical', 'ffmpeg'], preview: P('reframe-blur-fill', 'mp4') },
]
