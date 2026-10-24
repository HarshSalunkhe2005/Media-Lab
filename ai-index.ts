/*
 * Generates the machine-readable layer from src/meta.ts, src/worlds.ts and src/router.ts:
 *   /llms.txt        index: what this is, the procedure, every pattern, every world
 *   /llms-full.txt   everything inlined: skill pages, worlds, every pattern with its renderer source
 *   /patterns.json   structured pattern metadata      /worlds.json  structured worlds
 *   /for-claude.md   brief -> world -> patterns router, plus refusals
 *   /docs/<slug>.md  one doc per pattern: metadata, when to use, recipe links, full renderer source
 *   /skill/<path>    every file of the Claude skill (playbook, formats, hooks, recipes, scripts)
 *   /raw/<path>      renderer sources (patterns/lib.py, patterns/src/*.py)
 * Validates on every build: renderer file, preview, recipe paths, world proofs and router slugs must exist.
 */
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs'
import { join, relative, resolve } from 'node:path'
import type { Plugin } from 'vite'
import { CATEGORIES, META } from './src/meta'
import { REFUSE, ROUTES } from './src/router'
import { WORLDS } from './src/worlds'

export const SITE = process.env.SITE_URL ?? 'https://media-lab-harsh.vercel.app'
const REPO = 'https://github.com/HarshSalunkhe2005/Media-Lab'
const SKILL = 'plugins/media-lab/skills/media-lab'

const read = (rel: string) => readFileSync(resolve(__dirname, rel), 'utf-8')
const walk = (dir: string): string[] =>
  readdirSync(resolve(__dirname, dir)).flatMap((f) => {
    const p = join(dir, f)
    return statSync(resolve(__dirname, p)).isDirectory() ? walk(p) : [p.replace(/\\/g, '/')]
  })
const title = (md: string, fb: string) => md.match(/^#\s+(.+)$/m)?.[1] ?? fb
const skillFiles = () => walk(SKILL).filter((f) => /\.(md|py|txt)$/.test(f))

function validate() {
  const errors: string[] = []
  const slugs = new Set(META.map((m) => m.slug))
  if (slugs.size !== META.length) errors.push('duplicate slug in meta.ts')
  for (const m of META) {
    if (!existsSync(resolve(__dirname, `patterns/src/${m.slug}.py`))) errors.push(`${m.slug}: no renderer patterns/src/${m.slug}.py`)
    if (!existsSync(resolve(__dirname, 'public', m.preview))) errors.push(`${m.slug}: preview ${m.preview} missing (run python patterns/render.py ${m.slug})`)
    if (!m.when.length) errors.push(`${m.slug}: needs at least one "when"`)
    for (const r of m.recipe) if (!existsSync(resolve(__dirname, SKILL, r))) errors.push(`${m.slug}: recipe ${r} not found`)
  }
  const worlds = new Set(WORLDS.map((w) => w.id))
  for (const w of WORLDS) for (const p of w.proof) if (!slugs.has(p)) errors.push(`world ${w.id}: unknown proof ${p}`)
  for (const r of ROUTES) {
    if (!worlds.has(r.world)) errors.push(`route "${r.brief}": unknown world ${r.world}`)
    for (const s of r.start) if (!slugs.has(s)) errors.push(`route "${r.brief}": unknown pattern ${s}`)
    for (const f of r.read) if (!existsSync(resolve(__dirname, SKILL, f))) errors.push(`route "${r.brief}": ${f} not found`)
  }
  if (errors.length) throw new Error('Media Lab metadata errors:\n  ' + errors.join('\n  '))
}

function doc(m: (typeof META)[number]) {
  const src = read(`patterns/src/${m.slug}.py`)
  const worlds = WORLDS.filter((w) => w.proof.includes(m.slug)).map((w) => w.name)
  return [
    `# ${m.title}`, '', `> ${m.summary}`, '',
    `- **Category:** ${m.category}`, `- **Format:** ${m.format}`, `- **Tags:** ${m.tags.join(', ')}`,
    worlds.length ? `- **Worlds:** ${worlds.join(', ')}` : '',
    `- **Preview:** ${SITE}/${m.preview}`, `- **Gallery:** ${SITE}/#/p/${m.slug}`,
    `- **Renderer:** ${SITE}/raw/patterns/src/${m.slug}.py (uses ${SITE}/raw/patterns/lib.py)`,
    `- **GitHub:** ${REPO}/blob/main/patterns/src/${m.slug}.py`, '',
    '## When to use', '', ...m.when.map((w) => `- ${w}`), '',
    '## Read first', '', ...m.recipe.map((r) => `- [${r}](${SITE}/skill/${r})`), `- [Taste and the AI-look smell test](${SITE}/skill/playbook/taste.md)`, '',
    '## Render it', '', '```bash', `python patterns/render.py ${m.slug}   # writes public/${m.preview}`, '```', '',
    '## Source', '', '```python', src.trimEnd(), '```', '',
  ].filter((l, i, a) => !(l === '' && a[i - 1] === '')).join('\n')
}

function worldMd(w: (typeof WORLDS)[number]) {
  return [`### ${w.name} (\`${w.id}\`)`, '', `*${w.feel}*`, '', `- Type: ${w.type}`, `- Colour: ${w.colour}`, `- Imagery: ${w.imagery}`,
    `- Motion: ${w.motion}`, `- Rules: ${w.rules.join('; ')}`, `- Avoid: ${w.avoid.join('; ')}`,
    `- Proof: ${w.proof.map((p) => `[${p}](${SITE}/docs/${p}.md)`).join(', ')}`, ''].join('\n')
}

function forClaude() {
  return [
    '# Media Lab for Claude: brief -> world -> patterns', '',
    'Before making any content: write the brief (`/skill/playbook/01-brief.md`), match it to a row below, open the',
    'world and its proof patterns, read the listed skill pages, then build. Run the AI-look smell test',
    `(${SITE}/skill/playbook/taste.md) on every visual before showing it.`, '',
    '| The brief sounds like | World | Start from | Read |', '|---|---|---|---|',
    ...ROUTES.map((r) => `| ${r.brief} | ${WORLDS.find((w) => w.id === r.world)!.name} | ${r.start.map((s) => `[${s}](${SITE}/docs/${s}.md)`).join(', ')} | ${r.read.map((f) => `[${f}](${SITE}/skill/${f})`).join(', ')} |`),
    '', '## Worlds', '', ...WORLDS.map(worldMd), '## Refuse or ask first', '', ...REFUSE.map((r) => `- ${r}`), '',
  ].join('\n')
}

function llms() {
  const lines = [
    '# Media Lab', '',
    '> A reference library for making content (Shorts, Reels, carousels, thumbnails, captions, event media) with a procedure,',
    '> named style worlds, and patterns whose previews are real output of the repo\'s own Python + ffmpeg renderers.', '',
    `- **Claude: read ${SITE}/for-claude.md first.** It routes a brief to a world and the patterns to start from.`,
    `- Structured data: ${SITE}/patterns.json, ${SITE}/worlds.json. Everything in one file: ${SITE}/llms-full.txt`,
    `- Install as a Claude Code plugin: \`/plugin marketplace add HarshSalunkhe2005/Media-Lab\` then \`/plugin install media-lab@media-lab\``, '',
    '## The skill (procedure, formats, hooks, recipes)', '',
    ...skillFiles().filter((f) => f.endsWith('.md')).map((f) => `- [${title(read(f), f)}](${SITE}/skill/${relative(SKILL, f).replace(/\\/g, '/')})`), '',
    '## Worlds', '', ...WORLDS.map((w) => `- ${w.name} (\`${w.id}\`): ${w.feel}`), '',
  ]
  for (const c of CATEGORIES) {
    const items = META.filter((m) => m.category === c)
    lines.push(`## ${c}`, '', ...items.map((m) => `- [${m.title}](${SITE}/docs/${m.slug}.md): ${m.summary} [${m.tags.join(', ')}]`), '')
  }
  return lines.join('\n')
}

function files(): Record<string, string> {
  validate()
  const out: Record<string, string> = {
    'llms.txt': llms(),
    'for-claude.md': forClaude(),
    'patterns.json': JSON.stringify(META.map((m) => ({ ...m, preview: `${SITE}/${m.preview}`, doc: `${SITE}/docs/${m.slug}.md`,
      renderer: `${SITE}/raw/patterns/src/${m.slug}.py`, worlds: WORLDS.filter((w) => w.proof.includes(m.slug)).map((w) => w.id) })), null, 1),
    'worlds.json': JSON.stringify(WORLDS, null, 1),
  }
  for (const m of META) out[`docs/${m.slug}.md`] = doc(m)
  for (const f of skillFiles()) out[`skill/${relative(SKILL, f).replace(/\\/g, '/')}`] = read(f)
  for (const f of ['patterns/lib.py', 'patterns/render.py', ...walk('patterns/src')]) out[`raw/${f}`] = read(f)
  out['llms-full.txt'] = [out['llms.txt'], out['for-claude.md'],
    ...skillFiles().filter((f) => f.endsWith('.md')).map((f) => `\n\n===== ${f} =====\n\n${read(f)}`),
    ...META.map((m) => `\n\n===== docs/${m.slug}.md =====\n\n${out[`docs/${m.slug}.md`]}`)].join('\n')
  return out
}

const TYPES: Record<string, string> = { md: 'text/markdown; charset=utf-8', txt: 'text/plain; charset=utf-8', json: 'application/json', py: 'text/plain; charset=utf-8' }

export function aiIndex(): Plugin {
  return {
    name: 'media-lab-ai-index',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const path = decodeURIComponent((req.url ?? '').split('?')[0]).replace(/^\//, '')
        if (!/\.(md|txt|json|py)$/.test(path)) return next()
        const f = files()[path]
        if (f === undefined) return next()
        res.setHeader('Content-Type', TYPES[path.split('.').pop()!])
        res.end(f)
      })
    },
    buildStart() { validate() },
    generateBundle() {
      for (const [fileName, source] of Object.entries(files())) this.emitFile({ type: 'asset', fileName, source })
    },
  }
}

/** Data for the React app (inlined at build). */
export function skillPages() {
  return Object.fromEntries(skillFiles().filter((f) => f.endsWith('.md')).map((f) => [relative(SKILL, f).replace(/\\/g, '/'), read(f)]))
}
