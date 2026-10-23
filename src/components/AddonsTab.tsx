import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import './AddonsTab.css';
import {
  visualAddons, addonCategories, addonsByCategory,
  type AddonCategory, type VisualAddon,
} from '../data/visualAddons';

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

function parseHash(): { id: string | null; cat: AddonCategory | 'all'; q: string } {
  const h = window.location.hash;
  const usp = new URLSearchParams(h.split('?')[1] || '');
  const cat = (usp.get('cat') || 'all') as AddonCategory | 'all';
  const q = usp.get('q') || '';
  if (h.startsWith('#/addons/')) {
    return { id: decodeURIComponent(h.slice('#/addons/'.length).split('?')[0].split('/')[0]), cat, q };
  }
  return { id: null, cat, q };
}

/** Renders a demo at a real 1280×800 desktop viewport, scaled to the card.
 *  This keeps the preview honest: the add-on is designed for desktop, and a
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

export function AddonsTab() {
  const [route, setRoute] = useState(parseHash);
  const [visible, setVisible] = useState<Set<string>>(new Set());
  const { copied, copy } = useCopy();

  useEffect(() => {
    const onHash = () => { setRoute(parseHash()); window.scrollTo(0, 0); };
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, []);

  const setHash = useCallback((id: string | null, cat: AddonCategory | 'all', q: string) => {
    const usp = new URLSearchParams();
    if (cat !== 'all') usp.set('cat', cat);
    if (q) usp.set('q', q);
    const qs = usp.toString() ? '?' + usp.toString() : '';
    window.location.hash = id ? `#/addons/${encodeURIComponent(id)}${qs}` : `#/addons${qs}`;
  }, []);

  const filtered = useMemo(() => {
    const q = route.q.toLowerCase();
    return addonsByCategory(route.cat).filter(a =>
      !q || (a.name + ' ' + a.tagline + ' ' + a.what + ' ' + a.surface.join(' ')).toLowerCase().includes(q),
    );
  }, [route.cat, route.q]);

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
    }, { rootMargin: '400px' });
    document.querySelectorAll('[data-aid]').forEach(el => io.observe(el));
    return () => io.disconnect();
  }, [route.id, filtered.length]);

  /* ── DETAIL ─────────────────────────────────────────────── */
  if (route.id) {
    const idx = visualAddons.findIndex(a => a.id === route.id);
    const a = visualAddons[idx];
    if (!a) {
      return (
        <div className="av-missing">
          Add-on not found. <a href="#/addons">← All 25 add-ons</a>
        </div>
      );
    }
    const cat = addonCategories.find(c => c.id === a.category)!;
    const prev = visualAddons[idx - 1];
    const next = visualAddons[idx + 1];
    const pairs = visualAddons
      .filter(x => x.id !== a.id && (x.category === a.category || x.worksWith.some(w => a.worksWith.includes(w))))
      .slice(0, 3);

    return (
      <div className="av-detail">
        <div className="av-detail-top">
          <button className="av-back" onClick={() => setHash(null, route.cat, route.q)}>← All 25 add-ons</button>
          <div className="av-detail-nav">
            {prev && <button onClick={() => setHash(prev.id, route.cat, route.q)}>← {prev.name}</button>}
            <span className="av-posn">{a.n} / {visualAddons.length}</span>
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
            <span className="av-live"><i />LIVE DEMO</span>
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
              <h3>Drop-in snippet</h3>
              <p>Self-contained CSS + markup. Paste into the page, then swap the accent values for your brand tokens.</p>
            </div>
            <button className={`av-btn primary ${copied === 'snippet' ? 'ok' : ''}`} onClick={() => copy('snippet', a.snippet)}>
              {copied === 'snippet' ? '✓ Copied' : '⧉ Copy snippet'}
            </button>
          </div>
          <pre className="av-pre"><code>{a.snippet}</code></pre>
        </section>

        <section className="av-prompt-block">
          <div className="av-code-head">
            <div>
              <h3>Agent prompt</h3>
              <p>Paste this into the coding agent that is building the page. It carries the layout, motion and accessibility constraints.</p>
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
              const pc = addonCategories.find(c => c.id === p.category)!;
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
          <a href="#/stylesdb">Browse the Styles DB →</a>
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
          <p className="av-kicker">Visual add-ons · 25 drop-ins</p>
          <h1>The finish,<br /><em>not the direction.</em></h1>
          <p className="av-lede">
            The Styles DB decides what a page is. These are the layers that make it feel made:
            grain, light, depth, motion and the small interactions at the edges. Every one is a
            self-contained snippet that drops into any of the 150 directions.
          </p>
          <div className="av-stats">
            <div><b>25</b><span>add-ons</span></div>
            <div><b>5</b><span>categories</span></div>
            <div><b>0</b><span>dependencies</span></div>
            <div><b>1</b><span>snippet each</span></div>
          </div>
        </div>
        <aside className="av-howto">
          <h3>HOW TO USE THEM</h3>
          <ol>
            <li><b>Pick a direction</b><span>Start in the Styles DB — one style, not a pile.</span></li>
            <li><b>Add two or three</b><span>One atmosphere, one surface, one motion. Stop there.</span></li>
            <li><b>Copy the snippet</b><span>Swap the accent values for the style’s palette.</span></li>
            <li><b>Check the edges</b><span>Reduced motion, AA contrast, touch fallback.</span></li>
          </ol>
        </aside>
      </header>

      <div className="av-controls">
        <div className="av-cats">
          <button className={`av-cat ${route.cat === 'all' ? 'on' : ''}`} onClick={() => setHash(null, 'all', route.q)}>
            🌐 All <span>{visualAddons.length}</span>
          </button>
          {addonCategories.map(c => (
            <button
              key={c.id}
              className={`av-cat ${route.cat === c.id ? 'on' : ''}`}
              onClick={() => setHash(null, c.id, route.q)}
              style={route.cat === c.id ? { borderColor: c.color + '88', color: c.color } : undefined}
            >
              <i className="av-dot" style={{ background: c.color }} />
              {c.label} <span>{addonsByCategory(c.id).length}</span>
            </button>
          ))}
        </div>
        <input
          className="av-search"
          placeholder="Search effects, surfaces, snippets…"
          defaultValue={route.q}
          onKeyDown={e => { if (e.key === 'Enter') setHash(null, route.cat, (e.target as HTMLInputElement).value); }}
        />
      </div>

      {route.cat !== 'all' && (
        <p className="av-cat-blurb">{addonCategories.find(c => c.id === route.cat)!.blurb}</p>
      )}

      <div className="av-grid">
        {filtered.map(a => {
          const cat = addonCategories.find(c => c.id === a.category)!;
          return (
            <article key={a.id} className="av-card" data-aid={a.id} onClick={() => setHash(a.id, route.cat, route.q)}>
              <div className="av-thumb-wrap">
                {visible.has(a.id) ? (
                  <ScaledPreview src={a.demo} title={a.name} />
                ) : (
                  <div className="av-thumb" style={{ height: 248 }}>
                    <div className="av-thumb-placeholder">PREVIEW LOADS ON SCROLL</div>
                  </div>
                )}
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
                  <span>Open add-on →</span>
                  <span className="av-surfaces">{a.surface.slice(0, 2).join(' · ')}</span>
                </div>
              </div>
            </article>
          );
        })}
      </div>

      {filtered.length === 0 && (
        <div className="av-empty">No add-ons match “{route.q}”. <button onClick={() => setHash(null, 'all', '')}>Clear</button></div>
      )}

      <section className="av-principles">
        <h2>Rules that keep add-ons from becoming noise</h2>
        <div className="av-principles-grid">
          <div><b>01</b><h3>One light source</h3><p>Never run a cursor spotlight and a section glow in the same viewport. The eye can only believe one.</p></div>
          <div><b>02</b><h3>Two per page, three max</h3><p>Atmosphere + surface is a page. Add motion only if something actually enters or moves.</p></div>
          <div><b>03</b><h3>Motion earns its keep</h3><p>Every effect gets a prefers-reduced-motion branch and a static fallback that still looks designed.</p></div>
          <div><b>04</b><h3>Contrast is not negotiable</h3><p>Grain, glass and duotone all reduce legibility. Check body text at AA after the effect, not before.</p></div>
        </div>
      </section>
    </div>
  );
}
