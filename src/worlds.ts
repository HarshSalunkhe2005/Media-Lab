/*
 * Worlds: named content styles. Each one is a direction with taste rules and proof patterns.
 * playbook/taste.md (the AI-look smell test) applies to every world. Proof slugs are validated at build time.
 */
export type World = {
  id: string
  name: string
  /** One line: what it feels like. */
  feel: string
  type: string
  colour: string
  imagery: string
  motion: string
  /** Rules that keep it from looking generated. */
  rules: string[]
  avoid: string[]
  proof: string[]
}

export const WORLDS: World[] = [
  { id: 'quiet-poetry', name: 'Quiet Poetry', feel: 'Like a page torn from someone\'s notebook and left on a train seat.',
    type: 'One serif (Garamond), regular weight, sentence case, two sizes at most.', colour: 'Taken from the photo; off-white or ink text.',
    imagery: 'Real CC0 photos with one shared film grade; paper slides between them.', motion: 'None, or a very slow push.',
    rules: ['Text sits in the photo\'s darkest or calmest edge', 'One stanza or thought per slide', 'Concrete nouns, not "soul" and "journey"'],
    avoid: ['Gold italic on black', 'Glows, moons, bokeh blobs', 'Centred quote boxes'], proof: ['poetry-film-photo', 'poetry-paper', 'caption-quiet-lowercase', 'editorial-quote-slide'] },
  { id: 'tech-launch', name: 'Tech Launch', feel: 'A demo that works, shown fast, with one number that matters.',
    type: 'A plain grotesk (Segoe/Inter-like), bold for the hook, regular for support.', colour: 'Product colours; one accent.',
    imagery: 'Real UI recorded at 2x, zoomed on the cursor; desk photos only as context.', motion: 'Punch-ins on each step, cut on the beat.',
    rules: ['Result in the first 2 seconds', 'Every claim shown on screen', 'Name and where to get it at the end'],
    avoid: ['Mockup devices floating in gradients', 'Stock "futuristic" imagery'], proof: ['hook-title-card', 'punch-in-zoom', 'thumb-big-number', 'short-word-captions', 'kinetic-hook', 'pip-inset', 'launch-og-image', 'story-link-space', 'youtube-end-screen'] },
  { id: 'campus-event', name: 'Campus Event', feel: 'The league\'s own page: consistent, current, a bit proud.',
    type: 'A condensed face for scores and days, a plain sans for everything else.', colour: 'The event\'s colours, used the same way on every post.',
    imagery: 'Real photos from the day; faces and hands never cropped.', motion: 'Highlight reels: best moment first, fast cuts.',
    rules: ['Data (scores, fixtures) comes from the official source', 'One template set for the whole event', 'Names checked before export'],
    avoid: ['Pasting patches over old poster text', 'Stretched photos'], proof: ['event-result-card', 'event-award-card', 'event-schedule-story', 'event-speaker-card', 'event-recap-grid', 'story-countdown', 'beat-cut-slideshow'] },
  { id: 'explainer', name: 'Explainer', feel: 'A friend who knows the topic, explaining it on a napkin.',
    type: 'Bold sans hooks, readable captions.', colour: 'Neutral base, one highlight colour for the key word.',
    imagery: 'Diagrams, screen recordings or real stills per beat.', motion: 'Something changes every 2-4 s.',
    rules: ['One idea per Short', 'Facts with sources; opinions labelled', 'Payoff in the last beat'],
    avoid: ['Stock footage that only illustrates nouns', 'Unsourced stats'], proof: ['hook-unfinished-number', 'caption-word-highlight', 'short-kenburns-stills', 'checklist-slide', 'myth-fact-compare', 'countdown-list-short', 'progress-bar-short', 'split-screen-stack', 'thumb-face-words'] },
  { id: 'data-story', name: 'Data Story', feel: 'A poster in a good newspaper: one figure, said plainly.',
    type: 'Condensed numerals, plain sans text, a ruled grid.', colour: 'Paper, ink, one accent for the number.',
    imagery: 'Mostly none; the number is the image.', motion: 'Count-up only if it adds meaning.',
    rules: ['One giant number per slide, earned', 'Say what it means in one sentence', 'Source on the slide'],
    avoid: ['3D charts', 'Five numbers fighting on one slide'], proof: ['data-story-number', 'thumb-big-number', 'list-point-slide', 'bar-chart-slide', 'linkedin-document'] },
  { id: 'build-log', name: 'Build Log', feel: 'Notes from someone actually making the thing.',
    type: 'Plain sans; code in a mono face only when showing code.', colour: 'Muted, from the screen and the desk.',
    imagery: 'Real desk and screen shots, including the mess.', motion: 'Screen recordings with punch-ins.',
    rules: ['Concrete numbers: hours, files, errors', 'Show the failure before the fix', 'Sentence-case captions'],
    avoid: ['Hustle-culture captions', 'Perfect staged desks'], proof: ['thumb-big-number', 'hook-unfinished-number', 'punch-in-zoom', 'code-card-slide', 'timeline-slide', 'text-post-card'] },
  { id: 'warm-local', name: 'Warm Local', feel: 'The café or shop posting about its own week.',
    type: 'A friendly serif or rounded sans; one face.', colour: 'Warm, from the place itself.',
    imagery: 'Real photos of the place, people (with permission) and products; natural light.', motion: 'Slow stills, ambient sound.',
    rules: ['Useful info on every post (hours, price, date)', 'Photos taken there, not stock when possible'],
    avoid: ['Stock smiling people', 'Neon gradients'], proof: ['carousel-cover-promise', 'cta-last-slide', 'short-kenburns-stills', 'cafe-menu-board', 'testimonial-card', 'before-after-split', 'brand-kit-three-ways'] },
  { id: 'faceless-story', name: 'Faceless Story', feel: 'A story told over pictures, held together by captions.',
    type: 'Bold captions, highlighted word, hook title in the first 2 s.', colour: 'Graded stills; captions in white and one highlight.',
    imagery: 'Real stills or footage per beat; never another creator\'s clips.', motion: 'Ken Burns on every still, cut per beat.',
    rules: ['Hook is an unresolved situation', 'Loop the ending into the start', 'Disclose synthetic voice'],
    avoid: ['Re-uploaded clips', 'Generated faces of real people'], proof: ['short-kenburns-stills', 'hook-title-card', 'caption-boxed', 'reframe-dark-panels', 'audiogram-waveform'] },
  { id: 'editorial', name: 'Editorial', feel: 'A feature page from a magazine that still pays its photographers.',
    type: 'A display serif (DM Serif Display) for heads, a book serif for text; tight leading on big type.', colour: 'Off-white paper, near-black ink, one deep red.',
    imagery: 'One strong full-bleed photo per piece; nothing decorative.', motion: 'Slow push or none; cuts on the sentence.',
    rules: ['One cover line, not five', 'Pull quotes are real quotes, attributed', 'White space is part of the layout'],
    avoid: ['Script fonts pretending to be elegant', 'Gold foil and marble textures'], proof: ['magazine-cover', 'editorial-quote-slide', 'story-text-safe'] },
  { id: 'retro-print', name: 'Retro Print', feel: 'A screen-printed gig poster stapled to a lamp post.',
    type: 'One heavy grotesk (Archivo Black) in caps for the hero, a plain sans for details.', colour: 'Two inks on cream: navy and red. Photos go duotone or halftone.',
    imagery: 'Real photos turned into two-colour print; the texture comes from the dots, not a filter.', motion: 'Hard cuts, slight registration shift at most.',
    rules: ['The date or the one word is the hero', 'Two inks, no gradients', 'Details in one plain column'],
    avoid: ['Fake grunge overlays', 'More than two ink colours'], proof: ['retro-event-poster', 'halftone-statement', 'event-lineup-poster'] },
  { id: 'brutalist-mono', name: 'Brutalist Mono', feel: 'A blunt opinion set in the biggest type that fits.',
    type: 'Inter Black in caps edge to edge; labels in JetBrains Mono.', colour: 'Black on white, one signal orange word.',
    imagery: 'None. The sentence is the image.', motion: 'Words slam in on the beat (kinetic).',
    rules: ['One sentence per post', 'Size until it nearly touches the margins', 'One accent word, never two'],
    avoid: ['Drop shadows', 'Centred everything', 'Stock photos behind the text'], proof: ['brutalist-statement', 'kinetic-hook', 'thumb-versus'] },
  { id: 'soft-pastel', name: 'Soft Pastel', feel: 'A calm, kind account that people follow to feel less rushed.',
    type: 'Inter SemiBold for heads, regular for text; generous line height.', colour: 'Pale lilac or mint base, one saturated violet accent.',
    imagery: 'Few photos; soft daylight when used. Shapes stay simple.', motion: 'Gentle fades and slow builds.',
    rules: ['Short sentences, warm verbs', 'Lots of air around each idea', 'Accent used once per slide'],
    avoid: ['Pastel rainbow gradients', 'Cartoon blobs and sparkles', 'Tiny grey text on tint'], proof: ['quote-card-pastel', 'process-steps', 'story-poll-space'] },
]
