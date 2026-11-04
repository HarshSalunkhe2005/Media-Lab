/*
 * The router: brief -> world -> patterns to start from. Rendered into /for-claude.md at build time.
 * World ids and pattern slugs are validated against worlds.ts and meta.ts; the build throws on a typo.
 */
export type Route = {
  /** How the brief reads, in the words someone would actually use. */
  brief: string
  world: string
  /** Patterns to open first. */
  start: string[]
  /** Skill pages to read, relative to plugins/media-lab/skills/media-lab/. */
  read: string[]
}

export const ROUTES: Route[] = [
  { brief: 'poetry, quotes, "something reflective" for Instagram', world: 'quiet-poetry', start: ['poetry-film-photo', 'poetry-paper'], read: ['playbook/taste.md', 'recipes/stock-photos.md', 'formats/carousel.md'] },
  { brief: 'launch my project / app / repo, "show what I built"', world: 'tech-launch', start: ['hook-title-card', 'punch-in-zoom', 'short-word-captions'], read: ['formats/launch-video.md', 'recipes/end-to-end-short.md'] },
  { brief: 'college fest, league, tournament, match results, awards', world: 'campus-event', start: ['event-result-card', 'event-award-card', 'event-schedule-story'], read: ['playbook/06-event-coverage.md', 'recipes/carousel.md'] },
  { brief: 'explain a concept, tips, "how does X work" as a Short', world: 'explainer', start: ['hook-unfinished-number', 'caption-word-highlight'], read: ['formats/short-video.md', 'hooks/hooks.md', 'playbook/critique.md'] },
  { brief: 'turn a report, survey or numbers into a post', world: 'data-story', start: ['data-story-number', 'list-point-slide'], read: ['formats/carousel.md', 'recipes/carousel.md'] },
  { brief: 'dev diary, "what I learned building", progress update', world: 'build-log', start: ['thumb-big-number', 'punch-in-zoom'], read: ['formats/text-posts.md', 'playbook/voice.md'] },
  { brief: 'a café, shop, studio or small business posting about itself', world: 'warm-local', start: ['carousel-cover-promise', 'cta-last-slide'], read: ['playbook/taste.md', 'formats/carousel.md'] },
  { brief: 'faceless channel, story Shorts, history or facts over pictures', world: 'faceless-story', start: ['short-kenburns-stills', 'hook-title-card'], read: ['recipes/end-to-end-short.md', 'recipes/stock-photos.md'] },
  { brief: 'YouTube thumbnail', world: 'explainer', start: ['thumb-object-words', 'thumb-big-number'], read: ['formats/thumbnail.md', 'playbook/taste.md'] },
  { brief: 'repurpose a landscape video for Reels / Shorts', world: 'explainer', start: ['reframe-dark-panels', 'reframe-blur-fill'], read: ['recipes/ffmpeg.md', 'formats/specs.md'] },
  { brief: 'magazine, newsletter or zine issue, interview highlights', world: 'editorial', start: ['magazine-cover', 'editorial-quote-slide'], read: ['playbook/taste.md', 'formats/carousel.md'] },
  { brief: 'gig, market, meetup or fest poster with a date', world: 'retro-print', start: ['retro-event-poster', 'event-lineup-poster', 'halftone-statement'], read: ['playbook/06-event-coverage.md', 'recipes/medialab-cli.md'] },
  { brief: 'a strong opinion, manifesto or launch teaser', world: 'brutalist-mono', start: ['brutalist-statement', 'kinetic-hook'], read: ['playbook/taste.md', 'hooks/hooks.md'] },
  { brief: 'calm community, wellness or newsletter account', world: 'soft-pastel', start: ['quote-card-pastel', 'process-steps', 'story-poll-space'], read: ['formats/text-posts.md', 'playbook/voice.md'] },
  { brief: 'Instagram or WhatsApp story: poll, countdown, link, update', world: 'campus-event', start: ['story-countdown', 'story-poll-space', 'story-link-space'], read: ['formats/stories.md', 'formats/specs.md'] },
  { brief: 'podcast or interview clip for Shorts / Reels', world: 'faceless-story', start: ['audiogram-waveform', 'caption-word-highlight'], read: ['formats/short-video.md', 'recipes/medialab-cli.md'] },
  { brief: 'LinkedIn document / PDF carousel', world: 'data-story', start: ['linkedin-document', 'bar-chart-slide'], read: ['formats/carousel.md', 'recipes/medialab-cli.md'] },
  { brief: 'testimonial, review or before / after for a small business', world: 'warm-local', start: ['testimonial-card', 'before-after-split', 'cafe-menu-board'], read: ['formats/text-posts.md', 'playbook/taste.md'] },
]

/** Refuse or ask before doing these, whatever the brief says. */
export const REFUSE = [
  'Re-uploading or recreating another creator\'s video, script, thumbnail or art',
  'Real people\'s faces or names in demos (use fictional ones) or implying an endorsement',
  'Stating numbers without a source',
  'Posting or uploading anything without the owner\'s explicit go-ahead',
]
