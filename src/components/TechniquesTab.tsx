import { useState, useEffect, useRef, useCallback } from 'react';

interface Technique {
  id: string; name: string; domain: string;
  level: 'core' | 'intermediate' | 'advanced' | 'innovative';
  one_line: string; why_pro?: string; demo_idea?: string;
  libraries?: unknown; spec_url?: string; demo_url?: string; prompt_url?: string;
}

const LEVELS = [
  { key: 'core', label: 'Core', color: '#3ddc84' },
  { key: 'intermediate', label: 'Intermediate', color: '#4d9fff' },
  { key: 'advanced', label: 'Advanced', color: '#ff9f43' },
  { key: 'innovative', label: 'Innovative', color: '#ff5c8a' },
] as const;

const PER_PAGE = 50;

const libsOf = (t: Technique): string[] => {
  const lib = t.libraries as unknown;
  if (Array.isArray(lib)) return lib as string[];
  if (typeof lib === 'string') { try { const a = JSON.parse(lib); return Array.isArray(a) ? a : []; } catch { return []; } }
  return [];
};

const levelColor = (lv: string) => LEVELS.find(l => l.key === lv)?.color || '#888';
const demoUrl = (t: Technique) => t.demo_url || `/techniques-demos/${t.id}.html`;
const promptUrl = (t: Technique) => t.prompt_url || `https://styles-api-production.up.railway.app/techniques/${t.id}/prompt`;

/** Hash router: #/techniques?p=3&lv=core&q=... | #/techniques/{id}?p=3 — state survives navigation */
function parseHash(): { id: string | null; page: number; level: string | null; q: string } {
  const h = window.location.hash;
  if (h.startsWith('#/techniques/')) {
    const id = h.slice('#/techniques/'.length).split('?')[0].split('/')[0];
    const usp = new URLSearchParams(h.split('?')[1] || '');
    return { id: decodeURIComponent(id), page: +(usp.get('p') || 1), level: usp.get('lv'), q: usp.get('q') || '' };
  }
  if (h.startsWith('#/techniques')) {
    const usp = new URLSearchParams(h.split('?')[1] || '');
    return { id: null, page: +(usp.get('p') || 1), level: usp.get('lv'), q: usp.get('q') || '' };
  }
  return { id: null, page: 1, level: null, q: '' };
}

export function TechniquesTab() {
  const [techniques, setTechniques] = useState<Technique[]>([]);
  const [loading, setLoading] = useState(true);
  const [route, setRoute] = useState(parseHash());
  const [visibleDemos, setVisibleDemos] = useState<Set<string>>(new Set());

  useEffect(() => {
    const decorate = (arr: any[]) => arr.map(t => ({
      ...t,
      demo_url: t.demo_url || `/techniques-demos/${t.id}.html`,
      prompt_url: t.prompt_url || `https://styles-api-production.up.railway.app/techniques/${t.id}/prompt`,
    }));
    (async () => {
      try {
        const r = await fetch('https://styles-api-production.up.railway.app/techniques');
        if (!r.ok) throw new Error('api down');
        setTechniques(decorate(await r.json()));
      } catch {
        try {
          const r = await fetch('/techniques-catalog.json');
          setTechniques(decorate(await r.json()));
        } catch { /* offline */ }
      } finally { setLoading(false); }
    })();
  }, []);

  useEffect(() => {
    const onHash = () => { setRoute(parseHash()); window.scrollTo(0, 0); };
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, []);

  const filtered = techniques.filter(t =>
    (!route.level || t.level === route.level) &&
    (!route.q || (t.name + ' ' + t.one_line + ' ' + t.domain).toLowerCase().includes(route.q.toLowerCase()))
  );

  const pages = Math.max(1, Math.ceil(filtered.length / PER_PAGE));
  const page = Math.min(Math.max(1, route.page), pages);
  const pageItems = filtered.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  const setHash = useCallback((id: string | null, p: number, lv: string | null, q: string) => {
    const usp = new URLSearchParams();
    if (p !== 1) usp.set('p', String(p));
    if (lv) usp.set('lv', lv);
    if (q) usp.set('q', q);
    const qs = usp.toString() ? '?' + usp.toString() : '';
    window.location.hash = id ? `#/techniques/${encodeURIComponent(id)}${qs}` : `#/techniques${qs}`;
  }, []);

  // Lazy-activate demos: IntersectionObserver so iframes only load when scrolled into view
  useEffect(() => {
    if (route.id) { setVisibleDemos(new Set([route.id])); return; }
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        const id = (e.target as HTMLElement).dataset.tid;
        if (e.isIntersecting && id) setVisibleDemos(prev => { const n = new Set(prev); n.add(id); return n; });
      });
    }, { rootMargin: '300px' });
    document.querySelectorAll('[data-tid]').forEach(el => io.observe(el));
    return () => io.disconnect();
  }, [route, pageItems.length]);

  if (loading) return <div className="tab-loading">Loading techniques…</div>;

  /* ---------- DETAIL PAGE: each technique gets its own full page ---------- */
  if (route.id) {
    const idx = techniques.findIndex(t => t.id === route.id);
    const t = techniques[idx];
    if (!t) return <div className="tab-loading">Technique not found. <a href="#/techniques" style={{color:'#4dd0e1'}}>← All techniques</a></div>;
    const prev = techniques[idx - 1], next = techniques[idx + 1];
    return (
      <div className="tech-page">
        <div className="tech-page-top">
          <button className="tech-back" onClick={() => setHash(null, page, route.level, route.q)}>← Back to list (page {page})</button>
          <div className="tech-page-nav">
            {prev && <button onClick={() => setHash(prev.id, page, route.level, route.q)}>← {prev.name}</button>}
            <span className="tech-posn">{idx + 1} / {techniques.length}</span>
            {next && <button onClick={() => setHash(next.id, page, route.level, route.q)}>{next.name} →</button>}
          </div>
        </div>
        <div className="tech-page-head">
          <span className="tech-lvl-badge" style={{ background: levelColor(t.level) }}>{t.level}</span>
          <span className="tech-dom-tag">{t.domain}</span>
          <h1>{t.name}</h1>
          <p className="tech-oneline">{t.one_line}</p>
          {t.why_pro && <p className="tech-whypro">⚡ {t.why_pro}</p>}
          {libsOf(t).length > 0 && <div className="tech-libs">{libsOf(t).map(l => <span key={l} className="tag">{l}</span>)}</div>}
        </div>
        <div className="tech-page-demo">
          <div className="tech-demo-bar">
            <span className="tech-demo-live"><i />LIVE DEMO</span>
            <div>
              <a className="tech-btn primary" href={demoUrl(t)} target="_blank" rel="noreferrer">↗ Full-screen</a>
              <a className="tech-btn" href={promptUrl(t)} target="_blank" rel="noreferrer">🪄 Agent prompt (JSON)</a>
              {t.spec_url && <a className="tech-btn" href={t.spec_url} target="_blank" rel="noreferrer">📖 Spec / docs</a>}
            </div>
          </div>
          <iframe
            className="tech-demo-frame"
            src={demoUrl(t)}
            sandbox="allow-scripts allow-same-origin allow-popups"
            loading="lazy"
            title={t.name}
          />
        </div>
        {t.demo_idea && (
          <div className="tech-page-idea">
            <h3>WHAT YOU'RE LOOKING AT</h3>
            <p>{t.demo_idea}</p>
          </div>
        )}
      </div>
    );
  }

  /* ---------- LIST: 5 per page, live demos embedded in cards ---------- */
  return (
    <div className="tech-page">
      <div className="tech-head">
        <h1>Techniques <span className="db-count-badge">{filtered.length}</span></h1>
        <p>The complete compendium of front-end techniques — every one with a live demo embedded and an agent-ready build prompt.</p>
        <div className="tech-level-chips">
          <button className={`tech-level-chip ${!route.level ? 'on' : ''}`} onClick={() => setHash(null, 1, null, route.q)}>
            <i style={{ background: '#aaa' }} /> All {techniques.length}
          </button>
          {LEVELS.map(l => {
            const n = techniques.filter(t => t.level === l.key).length;
            return (
              <button key={l.key} className={`tech-level-chip ${route.level === l.key ? 'on' : ''}`} onClick={() => setHash(null, 1, l.key, route.q)}>
                <i style={{ background: l.color }} /> {l.label} {n}
              </button>
            );
          })}
        </div>
        <input
          className="tech-search"
          placeholder="Search techniques…"
          defaultValue={route.q}
          onKeyDown={e => { if (e.key === 'Enter') setHash(null, 1, route.level, (e.target as HTMLInputElement).value); }}
        />
      </div>

      <div className="tech-list">
        {pageItems.map(t => (
          <div key={t.id} className="tech-card-row" data-tid={t.id}>
            <div className="tech-card-info">
              <div className="tech-card-meta">
                <span className="tech-lvl-badge" style={{ background: levelColor(t.level) }}>{t.level}</span>
                <span className="tech-dom-tag">{t.domain}</span>
              </div>
              <h2 onClick={() => setHash(t.id, page, route.level, route.q)} style={{ cursor: 'pointer' }}>{t.name}</h2>
              <p>{t.one_line}</p>
              {t.why_pro && <p className="tech-whypro">⚡ {t.why_pro}</p>}
              {libsOf(t).length > 0 && <div className="tech-libs">{libsOf(t).slice(0, 4).map(l => <span key={l} className="tag">{l}</span>)}</div>}
              <div className="tech-card-actions">
                <button onClick={() => setHash(t.id, page, route.level, route.q)}>Open full page →</button>
                <a href={promptUrl(t)} target="_blank" rel="noreferrer">🪄 Agent prompt</a>
              </div>
            </div>
            <div className="tech-card-demo" onClick={() => setHash(t.id, page, route.level, route.q)}>
              {visibleDemos.has(t.id) ? (
                <iframe
                  src={demoUrl(t)}
                  sandbox="allow-scripts allow-same-origin allow-popups"
                  loading="lazy"
                  title={t.name}
                  className="tech-demo-thumb"
                />
              ) : <div className="tech-demo-placeholder">demo loads on scroll…</div>}
            </div>
          </div>
        ))}
      </div>

      <div className="tech-pager">
        <button disabled={page <= 1} onClick={() => setHash(null, page - 1, route.level, route.q)}>← Prev</button>
        {Array.from({ length: pages }, (_, i) => i + 1)
          .filter(p2 => p2 === 1 || p2 === pages || Math.abs(p2 - page) <= 2)
          .map((p2, i, arr) => (
            <span key={p2} className="tech-pager-num-wrap">
              {i > 0 && arr[i - 1] !== p2 - 1 && <span className="tech-dots">…</span>}
              <button className={`tech-pager-num ${p2 === page ? 'on' : ''}`} onClick={() => setHash(null, p2, route.level, route.q)}>{p2}</button>
            </span>
          ))}
        <button disabled={page >= pages} onClick={() => setHash(null, page + 1, route.level, route.q)}>Next →</button>
        <span className="tech-pager-info">{(page - 1) * PER_PAGE + 1}–{Math.min(page * PER_PAGE, filtered.length)} of {filtered.length}</span>
      </div>
    </div>
  );
}
