import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import './AddonsTab.css';
import {
  visualAddons, addonCategories,
  type AddonCategory, type VisualAddon, type AddonGroup,
} from '../data/visualAddons';
import { ShareLink } from './ShareLink';
import { interactiveAddons, interactiveCategories } from '../data/interactiveAddons';
import { interactiveAddonsExtra } from '../data/interactiveAddonsExtra';
import { interactiveAddonsExtra2 } from '../data/interactiveAddonsExtra2';

/** The Interactive tab grew from 25 to 125 playgrounds; the original 25 keep
 *  their order and the batch of 50 appends after them. */
const allInteractive = [...interactiveAddons, ...interactiveAddonsExtra, ...interactiveAddonsExtra2];

const INTENSITY_DOTS: Record<VisualAddon['intensity'], number> = { subtle: 1, medium: 2, bold: 3 };

const STYLE_LABEL: Record<string, string> = {
  classic: 'Classic', contemporary: 'Contemporary', 'dark-tech': 'Dark Tech',
  'immersive-3d': 'Immersive 3D', scrollcraft: 'Scrollcraft', expressive: 'Expressive',
  'luxe-brand': 'Luxe Brand', 'data-pro': 'Data Pro', cultural: 'Cultural',
  'component-kit': 'Component Kit',
};
const styleLabel = (s: string) => STYLE_LABEL[s] || s;

function copyText(text: string): Promise<boolean> {
  return navigator.clipboard.writeText(text).then(
    () => true,
    () => {
      try {
        const ta = document.createElement('textarea');
        ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        const ok = document.execCommand('copy');
        document.body.removeChild(ta);
        return ok;
      } catch { return false; }
    },
  );
}

function parseHash(base: string): { id: string | null; cat: AddonCategory | 'all'; q: string } {
  const h = window.location.hash;
  const usp = new URLSearchParams(h.split('?')[1] || '');
  const cat = (usp.get('cat') || 'all') as AddonCategory | 'all';
  const q = usp.get('q') || '';
  const prefix = base + '/';
  if (h.startsWith(prefix)) {
    return { id: decodeURIComponent(h.slice(prefix.length).split('?')[0].split('/')[0]), cat, q };
  }
  return { id: null, cat, q };
}

/** Renders a demo at a real 960×800 desktop viewport, scaled to the card.
 *  This keeps the preview honest: the piece is designed for desktop, and a
 *  300px-wide iframe would silently switch every demo into its mobile layout. */
function ScaledPreview({ src, title }: { src: string; title: string }) {
  const wrap = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(0.34);
  useEffect(() => {
    const el = wrap.current;
    if (!el) return;
    const measure = () => setScale(Math.max(.2, el.clientWidth / 960));
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return (
    <div className="av-thumb" ref={wrap} style={{ height: Math.round(800 * scale) }}>
      <iframe
        src={src}
        title={title}
        className="av-thumb-frame"
        style={{ width: 960, height: 800, transform: `scale(${scale})` }}
        sandbox="allow-scripts allow-same-origin"
        loading="lazy"
        tabIndex={-1}
      />
    </div>
  );
}

function useCopy() {
  const [copied, setCopied] = useState<string | null>(null);
  const copy = useCallback(async (key: string, text: string) => {
    if (await copyText(text)) {
      setCopied(key);
      setTimeout(() => setCopied(null), 1800);
    }
  }, []);
  return { copied, copy };
}

type GroupConfig = {
  base: string;
  list: VisualAddon[];
  cats: typeof addonCategories;
  noun: string;
  kicker: string;
  headline: React.ReactNode;
  lede: string;
  stats: [string, string][];
  howto: [string, string][];
  howtoTitle: string;
  searchPlaceholder: string;
  snippetNote: string;
  principles: [string, string, string][];
  other: { href: string; label: string; blurb: string };
};

const CONFIG: Record<AddonGroup, GroupConfig> = {
  visual: {
    base: '#/addons',
    list: visualAddons,
    cats: addonCategories,
    noun: 'add-on',
    kicker: 'Visual add-ons · 25 drop-ins',
    headline: <>The finish,<br /><em>not the direction.</em></>,
    lede: 'The Styles DB decides what a page is. These are the layers that make it feel made: grain, light, depth, motion and the small interactions at the edges. Every one is a self-contained snippet that drops into any of the 150 directions.',
    stats: [['25', 'add-ons'], ['5', 'categories'], ['0', 'dependencies'], ['1', 'snippet each']],
    howtoTitle: 'HOW TO USE THEM',
    howto: [
      ['Pick a direction', 'Start in the Styles DB — one style, not a pile.'],
      ['Add two or three', 'One atmosphere, one surface, one motion. Stop there.'],
      ['Copy the snippet', 'Swap the accent values for the style’s palette.'],
      ['Check the edges', 'Reduced motion, AA contrast, touch fallback.'],
    ],
    searchPlaceholder: 'Search effects, surfaces, snippets…',
    snippetNote: 'Self-contained CSS + markup. Paste into the page, then swap the accent values for your brand tokens.',
    principles: [
      ['01', 'One light source', 'Never run a cursor spotlight and a section glow in the same viewport. The eye can only believe one.'],
      ['02', 'Two per page, three max', 'Atmosphere + surface is a page. Add motion only if something actually enters or moves.'],
      ['03', 'Motion earns its keep', 'Every effect gets a prefers-reduced-motion branch and a static fallback that still looks designed.'],
      ['04', 'Contrast is not negotiable', 'Grain, glass and duotone all reduce legibility. Check body text at AA after the effect, not before.'],
    ],
    other: {
      href: '#/interactive',
      label: 'Interactive elements →',
      blurb: 'Want the visitor to touch something? The 125 playgrounds.',
    },
  },
  interactive: {
    base: '#/interactive',
    list: allInteractive,
    cats: interactiveCategories,
    noun: 'element',
    kicker: 'Interactive elements · 125 playgrounds',
    headline: <>Not a picture.<br /><em>A playground.</em></>,
    lede: 'These are the parts a visitor can grab: generative canvases, pointer physics, 3D depth, type that bends, sound that draws itself. Each one is a single HTML file with no libraries — open it, drag it, then copy the core loop into the page.',
    stats: [['125', 'playgrounds'], ['5', 'families'], ['0', 'libraries'], ['60', 'fps target']],
    howtoTitle: 'HOW TO USE THEM',
    howto: [
      ['Pick the moment', 'Hero, product reveal, success state, gallery. One job per piece.'],
      ['Keep it contained', 'One interactive canvas per viewport. It should not fight the copy.'],
      ['Start from the loop', 'Copy the core loop, then add your palette and real content.'],
      ['Design the edges', 'Touch, reduced motion, keyboard and a paused fallback.'],
    ],
    searchPlaceholder: 'Search canvases, physics, 3D, type…',
    snippetNote: 'The core loop, stripped to the essentials. The live demo adds the artwork, controls and polish — open it full screen to see the full file.',
    principles: [
      ['01', 'One playground per viewport', 'Two animated canvases compete for the same attention. Pick the one that carries the message.'],
      ['02', 'The pointer is not the only input', 'Every draggable piece needs a keyboard or button equivalent, and a touch path.'],
      ['03', 'Cheap beats clever', 'Canvas at 60fps, capped DPR, no libraries. If it cannot hold 60, cut particle count before cutting frames.'],
      ['04', 'Always have a still', 'Pause the loop when off-screen and give reduced-motion visitors the same composition, frozen.'],
    ],
    other: {
      href: '#/addons',
      label: 'Visual add-ons →',
      blurb: 'Need the finishing layer? Grain, light, borders and depth.',
    },
  },
};

export function AddonsTab({ group = 'visual' }: { group?: AddonGroup }) {
  const cfg = CONFIG[group];
  const [route, setRoute] = useState(() => parseHash(cfg.base));
  const [visible, setVisible] = useState<Set<string>>(new Set());
  const [query, setQuery] = useState(route.q);
  const { copied, copy } = useCopy();

  useEffect(() => {
    const onHash = () => {
      const next = parseHash(cfg.base);
      setRoute(next);
      setQuery(next.q);
      window.scrollTo(0, 0);
    };
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, [cfg.base]);

  const setHash = useCallback((id: string | null, cat: AddonCategory | 'all', q: string) => {
    const usp = new URLSearchParams();
    if (cat !== 'all') usp.set('cat', cat);
    if (q) usp.set('q', q);
    const qs = usp.toString() ? '?' + usp.toString() : '';
    window.location.hash = id ? `${cfg.base}/${encodeURIComponent(id)}${qs}` : `${cfg.base}${qs}`;
  }, [cfg.base]);

  const filtered = useMemo(() => {
    const q = route.q.toLowerCase();
    const byCat = route.cat === 'all' ? cfg.list : cfg.list.filter(a => a.category === route.cat);
    return byCat.filter(a =>
      !q || (a.name + ' ' + a.tagline + ' ' + a.what + ' ' + a.surface.join(' ')).toLowerCase().includes(q),
    );
  }, [cfg.list, route.cat, route.q]);

  /* lazy iframes: only mount previews when the card is near the viewport */
  useEffect(() => {
    if (route.id) { setVisible(new Set()); return; }
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        const id = (e.target as HTMLElement).dataset.aid;
        if (!id) return;
        setVisible(prev => {
          const n = new Set(prev);
          if (e.isIntersecting) n.add(id); else n.delete(id);
          return n;
        });
      });
    }, { rootMargin: '320px' });
    document.querySelectorAll('[data-aid]').forEach(el => io.observe(el));
    return () => io.disconnect();
  }, [route.id, filtered.length]);

  /* ── DETAIL ─────────────────────────────────────────────── */
  if (route.id) {
    const idx = cfg.list.findIndex(a => a.id === route.id);
    const a = cfg.list[idx];
    if (!a) {
      return (
        <div className="av-missing">
          Not found. <a href={cfg.base}>← All {cfg.list.length} {cfg.noun}s</a>
        </div>
      );
    }
    const cat = cfg.cats.find(c => c.id === a.category)!;
    const prev = cfg.list[idx - 1];
    const next = cfg.list[idx + 1];
    const pairs = cfg.list
      .filter(x => x.id !== a.id && (x.category === a.category || x.worksWith.some(w => a.worksWith.includes(w))))
      .slice(0, 3);

    return (
      <div className="av-detail">
        <div className="av-detail-top">
          <button className="av-back" onClick={() => setHash(null, route.cat, route.q)}>← All {cfg.list.length} {cfg.noun}s</button>
          <div className="av-detail-actions">
            <ShareLink section={group === 'interactive' ? 'interactive' : 'addons'} id={a.id} label={a.name} />
          </div>
          <div className="av-detail-nav">
            {prev && <button onClick={() => setHash(prev.id, route.cat, route.q)}>← {prev.name}</button>}
            <span className="av-posn">{a.n} of {cfg.list.length}</span>
            {next && <button onClick={() => setHash(next.id, route.cat, route.q)}>{next.name} →</button>}
          </div>
        </div>

        <header className="av-head">
          <div className="av-head-meta">
            <span className="av-cat-chip" style={{ color: cat.color, borderColor: cat.color + '55', background: cat.color + '16' }}>
              {cat.emoji} {cat.label}
            </span>
            <span className="av-intensity" title={`${a.intensity} intensity`}>
              {[0, 1, 2].map(i => (
                <i key={i} style={{ background: i < INTENSITY_DOTS[a.intensity] ? cat.color : '#2a303c' }} />
              ))}
              {a.intensity}
            </span>
          </div>
          <h1>{a.name}</h1>
          <p className="av-tagline">{a.tagline}</p>
        </header>

        <div className="av-demo">
          <div className="av-demo-bar">
            <span className="av-live"><i />LIVE DEMO — INTERACT WITH IT</span>
            <div>
              <button className="av-btn primary" onClick={() => copy('prompt', a.prompt)}>
                {copied === 'prompt' ? '✓ Prompt copied' : '🪄 Copy agent prompt'}
              </button>
              <a className="av-btn" href={a.demo} target="_blank" rel="noreferrer">↗ Full screen</a>
            </div>
          </div>
          <iframe className="av-demo-frame" src={a.demo} sandbox="allow-scripts allow-same-origin" loading="lazy" title={a.name} />
        </div>

        <div className="av-explain">
          <div className="av-explain-card">
            <h3>WHAT IT IS</h3>
            <p>{a.what}</p>
          </div>
          <div className="av-explain-card">
            <h3>WHY IT WORKS</h3>
            <p>{a.why}</p>
          </div>
        </div>

        <div className="av-tags-row">
          <span className="av-tags-label">BEST ON</span>
          {a.surface.map(s => <span key={s} className="av-tag">{s}</span>)}
          <span className="av-tags-label" style={{ marginLeft: 14 }}>PAIRS WITH STYLES</span>
          {a.worksWith.map(s => <span key={s} className="av-tag style">{styleLabel(s)}</span>)}
        </div>

        <section className="av-code-block">
          <div className="av-code-head">
            <div>
              <h3>{group === 'interactive' ? 'Core loop' : 'Drop-in snippet'}</h3>
              <p>{cfg.snippetNote}</p>
            </div>
            <button className={`av-btn primary ${copied === 'snippet' ? 'ok' : ''}`} onClick={() => copy('snippet', a.snippet)}>
              {copied === 'snippet' ? '✓ Copied' : '⧉ Copy code'}
            </button>
          </div>
          <pre className="av-pre"><code>{a.snippet}</code></pre>
        </section>

        <section className="av-prompt-block">
          <div className="av-code-head">
            <div>
              <h3>Agent prompt</h3>
              <p>Paste this into the coding agent that is building the page. It carries the interaction, performance and accessibility constraints.</p>
            </div>
            <button className="av-btn" onClick={() => copy('prompt2', a.prompt)}>
              {copied === 'prompt2' ? '✓ Copied' : '⧉ Copy prompt'}
            </button>
          </div>
          <pre className="av-pre prompt"><code>{a.prompt}</code></pre>
        </section>

        <section className="av-pairs">
          <h3>Pairs well with</h3>
          <div className="av-pairs-grid">
            {pairs.map(p => {
              const pc = cfg.cats.find(c => c.id === p.category)!;
              return (
                <button key={p.id} className="av-pair" onClick={() => setHash(p.id, route.cat, route.q)}>
                  <span className="av-cat-chip small" style={{ color: pc.color, borderColor: pc.color + '55', background: pc.color + '16' }}>
                    {pc.emoji} {pc.label}
                  </span>
                  <b>{p.name}</b>
                  <span>{p.tagline}</span>
                </button>
              );
            })}
          </div>
        </section>

        <div className="av-foot-nav">
          {prev ? <button onClick={() => setHash(prev.id, route.cat, route.q)}>← {prev.name}</button> : <span />}
          <a href={cfg.other.href}>{cfg.other.label}</a>
          {next ? <button onClick={() => setHash(next.id, route.cat, route.q)}>{next.name} →</button> : <span />}
        </div>
      </div>
    );
  }

  /* ── INDEX ──────────────────────────────────────────────── */
  return (
    <div className="av-index">
      <header className="av-hero">
        <div className="av-hero-copy">
          <p className="av-kicker">{cfg.kicker}</p>
          <h1>{cfg.headline}</h1>
          <p className="av-lede">{cfg.lede}</p>
          <div className="av-stats">
            {cfg.stats.map(([n, label]) => (
              <div key={label}><b>{n}</b><span>{label}</span></div>
            ))}
          </div>
          <a className="av-crosslink" href={cfg.other.href}>
            <span>{cfg.other.blurb}</span>
            <b>{cfg.other.label}</b>
          </a>
        </div>
        <aside className="av-howto">
          <h3>{cfg.howtoTitle}</h3>
          <ol>
            {cfg.howto.map(([b, span]) => (
              <li key={b}><b>{b}</b><span>{span}</span></li>
            ))}
          </ol>
        </aside>
      </header>

      <div className="av-controls">
        <div className="av-cats">
          <button className={`av-cat ${route.cat === 'all' ? 'on' : ''}`} onClick={() => setHash(null, 'all', route.q)}>
            🌐 All <span>{cfg.list.length}</span>
          </button>
          {cfg.cats.map(c => (
            <button
              key={c.id}
              className={`av-cat ${route.cat === c.id ? 'on' : ''}`}
              onClick={() => setHash(null, c.id, route.q)}
              style={route.cat === c.id ? { borderColor: c.color + '88', color: c.color } : undefined}
            >
              <i className="av-dot" style={{ background: c.color }} />
              {c.label} <span>{cfg.list.filter(a => a.category === c.id).length}</span>
            </button>
          ))}
        </div>
        <input
          className="av-search"
          placeholder={cfg.searchPlaceholder}
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter') setHash(null, route.cat, query); }}
        />
      </div>

      {route.cat !== 'all' && (
        <p className="av-cat-blurb">{cfg.cats.find(c => c.id === route.cat)!.blurb}</p>
      )}

      <div className="av-grid">
        {filtered.map(a => {
          const cat = cfg.cats.find(c => c.id === a.category)!;
          // Interactive cards ship an animated GIF illustration of the engine.
          const thumb = a.thumb || (group === 'interactive' ? `/interactive/thumbs/${a.id}.gif` : null);
          return (
            <article key={a.id} className="av-card" data-aid={a.id} onClick={() => setHash(a.id, route.cat, route.q)}>
              <div className="av-thumb-wrap">
                {thumb ? (
                  <img className="av-thumb-gif" src={thumb} alt={`${a.name} animated preview`} loading="lazy" decoding="async" />
                ) : visible.has(a.id) ? (
                  <ScaledPreview src={a.demo} title={a.name} />
                ) : (
                  <div className="av-thumb" style={{ height: 248 }}>
                    <div className="av-thumb-placeholder">PREVIEW LOADS ON SCROLL</div>
                  </div>
                )}
                <ShareLink section={group === 'interactive' ? 'interactive' : 'addons'} id={a.id} label={a.name} compact className="corner" />
                <span className="av-num">{String(a.n).padStart(2, '0')}</span>
              </div>
              <div className="av-card-body">
                <div className="av-card-meta">
                  <span className="av-cat-chip small" style={{ color: cat.color, borderColor: cat.color + '55', background: cat.color + '16' }}>
                    {cat.emoji} {cat.label}
                  </span>
                  <span className="av-intensity" title={`${a.intensity} intensity`}>
                    {[0, 1, 2].map(i => (
                      <i key={i} style={{ background: i < INTENSITY_DOTS[a.intensity] ? cat.color : '#2a303c' }} />
                    ))}
                  </span>
                </div>
                <h3>{a.name}</h3>
                <p>{a.tagline}</p>
                <div className="av-card-foot">
                  <span>Open {cfg.noun} →</span>
                  <span className="av-surfaces">{a.surface.slice(0, 2).join(' · ')}</span>
                </div>
              </div>
            </article>
          );
        })}
      </div>

      {filtered.length === 0 && (
        <div className="av-empty">No {cfg.noun}s match “{route.q}”. <button onClick={() => { setQuery(''); setHash(null, 'all', ''); }}>Clear</button></div>
      )}

      <section className="av-principles">
        <h2>{group === 'interactive' ? 'Rules that keep interaction from becoming a gimmick' : 'Rules that keep add-ons from becoming noise'}</h2>
        <div className="av-principles-grid">
          {cfg.principles.map(([n, h, p]) => (
            <div key={n}><b>{n}</b><h3>{h}</h3><p>{p}</p></div>
          ))}
        </div>
      </section>
    </div>
  );
}
