import { useEffect, useMemo, useState } from 'react'
import { marked } from 'marked'
import { CATEGORIES, META, type PatternMeta } from './meta'
import { WORLDS } from './worlds'
import { REFUSE, ROUTES } from './router'

const SKILL = import.meta.glob('../plugins/media-lab/skills/media-lab/**/*.md', { query: '?raw', import: 'default', eager: true }) as Record<string, string>
const SOURCES = import.meta.glob('../patterns/src/*.py', { query: '?raw', import: 'default', eager: true }) as Record<string, string>
const skillPage = (p: string) => SKILL[`../plugins/media-lab/skills/media-lab/${p}`]
const source = (slug: string) => SOURCES[`../patterns/src/${slug}.py`] ?? ''
const REPO = 'https://github.com/HarshSalunkhe2005/Media-Lab'

function useRoute() {
  const get = () => window.location.hash.replace(/^#\/?/, '') || ''
  const [r, setR] = useState(get)
  useEffect(() => {
    const on = () => { setR(get()); window.scrollTo(0, 0) }
    window.addEventListener('hashchange', on)
    return () => window.removeEventListener('hashchange', on)
  }, [])
  return r
}

function Preview({ m, big }: { m: PatternMeta; big?: boolean }) {
  const cls = big ? 'pv big' : 'pv'
  return m.preview.endsWith('.mp4')
    ? <video className={cls} src={'/' + m.preview} muted loop playsInline autoPlay={big} controls={big} preload="metadata"
        onMouseEnter={(e) => !big && e.currentTarget.play()} onMouseLeave={(e) => !big && e.currentTarget.pause()} aria-label={m.title} />
    : <img className={cls} src={'/' + m.preview} alt={`${m.title}: ${m.summary}`} loading="lazy" />
}

function Gallery() {
  const [q, setQ] = useState('')
  const [cat, setCat] = useState<string>('All')
  const items = useMemo(() => META.filter((m) => (cat === 'All' || m.category === cat) &&
    (m.title + m.summary + m.tags.join(' ')).toLowerCase().includes(q.toLowerCase())), [q, cat])
  return (
    <>
      <section className="intro">
        <h1>Content that reads as made by a person.</h1>
        <p>Media Lab is a working library for Shorts, carousels, thumbnails, captions and event media: a procedure, eight style
          worlds, and patterns whose previews are real output of the repo's own Python and ffmpeg renderers. It also installs
          as a Claude Code plugin.</p>
        <p className="small"><a href="#/router">Start from a brief</a> · <a href="#/worlds">Browse worlds</a> · <a href="#/skill/playbook/taste.md">Taste and the smell test</a> · <a href="/llms.txt">llms.txt</a></p>
      </section>
      <div className="filters" role="toolbar" aria-label="Filter patterns">
        <input type="search" placeholder="Search patterns" value={q} onChange={(e) => setQ(e.target.value)} aria-label="Search patterns" />
        {['All', ...CATEGORIES].map((c) => <button key={c} aria-pressed={cat === c} onClick={() => setCat(c)}>{c}</button>)}
      </div>
      <div className="grid">
        {items.map((m) => (
          <a key={m.slug} className="card" href={`#/p/${m.slug}`}>
            <Preview m={m} />
            <div className="meta"><span className="cat">{m.category}</span><h3>{m.title}</h3><p>{m.summary}</p></div>
          </a>
        ))}
        {!items.length && <p>No pattern matches that.</p>}
      </div>
    </>
  )
}

function PatternPage({ slug }: { slug: string }) {
  const m = META.find((x) => x.slug === slug)
  if (!m) return <p>Unknown pattern. <a href="#/">Back to the gallery</a></p>
  const worlds = WORLDS.filter((w) => w.proof.includes(m.slug))
  return (
    <article className="pattern">
      <p className="small"><a href="#/">Gallery</a> / {m.category}</p>
      <div className="split">
        <Preview m={m} big />
        <div>
          <h1>{m.title}</h1>
          <p className="lead">{m.summary}</p>
          <dl>
            <dt>Format</dt><dd>{m.format}</dd>
            <dt>When to use</dt><dd><ul>{m.when.map((w) => <li key={w}>{w}</li>)}</ul></dd>
            {worlds.length > 0 && <><dt>Worlds</dt><dd>{worlds.map((w) => <a key={w.id} href={`#/w/${w.id}`} className="chip">{w.name}</a>)}</dd></>}
            <dt>Read first</dt><dd>{[...new Set([...m.recipe, 'playbook/taste.md'])].map((r) => <a key={r} href={`#/skill/${r}`} className="chip">{r}</a>)}</dd>
            <dt>Render</dt><dd><code>python patterns/render.py {m.slug}</code></dd>
            <dt>For agents</dt><dd><a href={`/docs/${m.slug}.md`}>/docs/{m.slug}.md</a> · <a href={`${REPO}/blob/main/patterns/src/${m.slug}.py`}>GitHub</a></dd>
          </dl>
        </div>
      </div>
      <h2>Renderer source</h2>
      <pre><code>{source(m.slug)}</code></pre>
    </article>
  )
}

function Worlds() {
  return (
    <section>
      <h1>Worlds</h1>
      <p className="lead">Named content styles. Pick one per piece, follow its rules, and run the <a href="#/skill/playbook/taste.md">smell test</a> before showing anything.</p>
      <div className="worlds">
        {WORLDS.map((w) => {
          const first = META.find((m) => m.slug === w.proof[0])!
          return (
            <a key={w.id} className="world" href={`#/w/${w.id}`}>
              <Preview m={first} />
              <div><h3>{w.name}</h3><p>{w.feel}</p></div>
            </a>
          )
        })}
      </div>
    </section>
  )
}

function WorldPage({ id }: { id: string }) {
  const w = WORLDS.find((x) => x.id === id)
  if (!w) return <p>Unknown world. <a href="#/worlds">All worlds</a></p>
  return (
    <article>
      <p className="small"><a href="#/worlds">Worlds</a></p>
      <h1>{w.name}</h1>
      <p className="lead"><em>{w.feel}</em></p>
      <dl className="cols">
        <dt>Type</dt><dd>{w.type}</dd><dt>Colour</dt><dd>{w.colour}</dd><dt>Imagery</dt><dd>{w.imagery}</dd><dt>Motion</dt><dd>{w.motion}</dd>
        <dt>Rules</dt><dd><ul>{w.rules.map((r) => <li key={r}>{r}</li>)}</ul></dd>
        <dt>Avoid</dt><dd><ul>{w.avoid.map((r) => <li key={r}>{r}</li>)}</ul></dd>
      </dl>
      <h2>Proof</h2>
      <div className="grid">
        {w.proof.map((s) => { const m = META.find((x) => x.slug === s)!; return (
          <a key={s} className="card" href={`#/p/${s}`}><Preview m={m} /><div className="meta"><h3>{m.title}</h3></div></a>) })}
      </div>
    </article>
  )
}

function Router() {
  return (
    <section>
      <h1>Start from a brief</h1>
      <p className="lead">Find the row that sounds like the request. Open the world, start from its patterns, read the pages listed. The same table is at <a href="/for-claude.md">/for-claude.md</a> for agents.</p>
      <div className="table-wrap">
        <table>
          <thead><tr><th>The brief sounds like</th><th>World</th><th>Start from</th><th>Read</th></tr></thead>
          <tbody>
            {ROUTES.map((r) => (
              <tr key={r.brief}>
                <td>{r.brief}</td>
                <td><a href={`#/w/${r.world}`}>{WORLDS.find((w) => w.id === r.world)!.name}</a></td>
                <td>{r.start.map((s) => <a key={s} className="chip" href={`#/p/${s}`}>{s}</a>)}</td>
                <td>{r.read.map((f) => <a key={f} className="chip" href={`#/skill/${f}`}>{f}</a>)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <h2>Refuse or ask first</h2>
      <ul>{REFUSE.map((r) => <li key={r}>{r}</li>)}</ul>
    </section>
  )
}

const NAV_SKILL = ['SKILL.md', 'playbook/01-brief.md', 'playbook/02-package.md', 'playbook/03-script.md', 'playbook/critique.md',
  'playbook/04-edit.md', 'playbook/05-verify.md', 'playbook/taste.md', 'playbook/voice.md', 'playbook/06-event-coverage.md',
  'formats/specs.md', 'formats/short-video.md', 'formats/carousel.md', 'formats/text-posts.md', 'formats/launch-video.md', 'formats/thumbnail.md',
  'hooks/hooks.md', 'hooks/templates.md', 'recipes/by-goal.md', 'recipes/end-to-end-short.md', 'recipes/stock-photos.md',
  'recipes/ffmpeg.md', 'recipes/moviepy.md', 'recipes/remotion.md', 'recipes/carousel.md', 'recipes/choose-a-tool.md']

function SkillPage({ path }: { path: string }) {
  const md = skillPage(path)
  const html = useMemo(() => (md ? (marked.parse(md.replace(/^---[\s\S]*?---\n/, '')) as string) : ''), [md])
  return (
    <div className="skill">
      <nav aria-label="Playbook pages">
        {NAV_SKILL.map((p) => <a key={p} href={`#/skill/${p}`} aria-current={p === path ? 'page' : undefined}>{p.replace('.md', '')}</a>)}
      </nav>
      {md ? <article className="prose" dangerouslySetInnerHTML={{ __html: html }} /> : <p>Page not found.</p>}
    </div>
  )
}

export default function App() {
  const r = useRoute()
  const [head, ...rest] = r.split('/')
  const tail = rest.join('/')
  let page
  if (head === 'p') page = <PatternPage slug={tail} />
  else if (head === 'worlds') page = <Worlds />
  else if (head === 'w') page = <WorldPage id={tail} />
  else if (head === 'router') page = <Router />
  else if (head === 'skill') page = <SkillPage path={tail || 'SKILL.md'} />
  else page = <Gallery />
  return (
    <>
      <header>
        <a href="#/" className="brand">Media Lab</a>
        <nav aria-label="Main">
          <a href="#/">Patterns</a><a href="#/worlds">Worlds</a><a href="#/router">Brief router</a><a href="#/skill/SKILL.md">Playbook</a><a href={REPO}>GitHub</a>
        </nav>
      </header>
      <main>{page}</main>
      <footer>
        <p>Photos: CC0 / public domain via Openverse (credits in <code>patterns/assets/photos/credits.txt</code>). Names, teams and lines in examples are fictional.</p>
        <p>For agents: <a href="/llms.txt">llms.txt</a> · <a href="/llms-full.txt">llms-full.txt</a> · <a href="/patterns.json">patterns.json</a> · <a href="/worlds.json">worlds.json</a> · <a href="/for-claude.md">for-claude.md</a></p>
      </footer>
    </>
  )
}
