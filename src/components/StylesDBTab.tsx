import { useState, useEffect } from 'react';

interface DBStyle {
  n: number; id: string; name: string; category: string; tagline: string;
  techniques: string[]; best_for: string[]; component_focus: string[];
  palette: Record<string, string>; image_url: string; spec_url: string;
}

const CATS = ['all','classic','contemporary','dark-tech','immersive-3d','scrollcraft','expressive','luxe-brand','data-pro','cultural','component-kit'];
const CAT_EMOJI: Record<string,string> = {
  'all':'🌐', 'classic':'🏛️', 'contemporary':'✨', 'dark-tech':'🖥️', 'immersive-3d':'🧊',
  'scrollcraft':'📜', 'expressive':'🎨', 'luxe-brand':'💎', 'data-pro':'📊', 'cultural':'🌍', 'component-kit':'🧩'
};

// Fetches from the live styles-api; falls back to the static dataset snapshot if API is unreachable
export function StylesDBTab() {
  const [styles, setStyles] = useState<DBStyle[]>([]);
  const [cat, setCat] = useState('all');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [source, setSource] = useState<'api'|'static'>('api');
  const [selected, setSelected] = useState<DBStyle | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const r = await fetch('https://styles-api-production.up.railway.app/styles?limit=200');
        if (!r.ok) throw new Error('api down');
        setStyles(await r.json());
        setSource('api');
      } catch {
        const r = await fetch('/styles-dataset.json');
        const full = await r.json();
        setStyles(full.map((s: any) => ({
          n: s.n, id: s.id, name: s.name, category: s.category, tagline: s.tagline,
          techniques: s.techniques, best_for: s.best_for, component_focus: s.component_focus,
          palette: s.palette,
          image_url: `/styles-images/${s.id}.png`, spec_url: `/styles-specs/${s.id}.html`,
        })));
        setSource('static');
      } finally { setLoading(false); }
    })();
  }, []);

  const filtered = styles.filter(s =>
    (cat === 'all' || s.category === cat) &&
    (!search || s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.tagline.toLowerCase().includes(search.toLowerCase()) ||
      (s.techniques||[]).some(t => t.toLowerCase().includes(search.toLowerCase())))
  );

  if (loading) return <div className="db-loading">Loading 100-style database…</div>;

  if (selected) {
    const p = selected.palette || {} as any;
    return (
      <div className="db-detail">
        <button className="db-back" onClick={()=>setSelected(null)}>← Back to Styles DB</button>
        <img className="db-hero" src={selected.image_url} alt={selected.name} />
        <div className="db-detail-head">
          <h1>{selected.name}</h1>
          <p className="db-tagline">{selected.tagline}</p>
          <div className="db-tags">
            <span className="tag tag-system">{selected.category}</span>
            {(selected.techniques||[]).map(t => <span key={t} className="tag">{t}</span>)}
          </div>
        </div>
        <div className="db-detail-grid">
          <div className="db-card">
            <h3>Palette</h3>
            <div className="db-swatches">
              {Object.entries(p).filter(([k,v]) => k !== 'gradient' && typeof v === 'string' && v.startsWith('#')).map(([k,v]) => (
                <div key={k} className="db-swatch"><div className="db-chip" style={{background:v}} /><code>{k}<br/>{v}</code></div>
              ))}
            </div>
            {p.gradient && <code className="db-gradient">{p.gradient}</code>}
          </div>
          <div className="db-card">
            <h3>Agent handoff</h3>
            <p>Everything an AI agent needs: full build prompt, palette, fonts, and a working HTML starter.</p>
            <a className="db-btn primary" href={selected.spec_url} target="_blank" rel="noopener">📄 Open spec sheet ↗</a>
            <a className="db-btn" href={`https://styles-api-production.up.railway.app/styles/${selected.id}/prompt`} target="_blank" rel="noopener">🔌 Agent prompt (JSON) ↗</a>
            <a className="db-btn" href={`https://styles-api-production.up.railway.app/styles/${selected.id}/html`} target="_blank" rel="noopener">🏗️ HTML shell ↗</a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="stylesdb-tab">
      <h1>Styles DB <span className="db-count">{styles.length} styles</span></h1>
      <p className="db-sub">100 hand-authored design directions — each with palette, fonts, motion recipes, agent build prompt, Muse preview, and a downloadable spec sheet. {source === 'api' ? 'Live from the styles API.' : 'From static snapshot (API offline).'}</p>
      <div className="db-controls">
        <input className="search-input" placeholder="Search styles, techniques…" value={search} onChange={e=>setSearch(e.target.value)} />
      </div>
      <div className="db-cats">
        {CATS.map(c => (
          <button key={c} className={`db-cat ${cat===c?'active':''}`} onClick={()=>setCat(c)}>
            {CAT_EMOJI[c]} {c.replace('-',' ')} <span className="db-n">{c==='all'?styles.length:styles.filter(s=>s.category===c).length}</span>
          </button>
        ))}
      </div>
      <div className="db-grid">
        {filtered.map(s => (
          <div key={s.id} className="db-card" onClick={()=>setSelected(s)}>
            <div className="db-thumb"><img src={s.image_url} alt={s.name} loading="lazy" /></div>
            <div className="db-info">
              <div className="db-tags"><span className="tag tag-system">{s.category}</span></div>
              <h3>{s.name}</h3>
              <p className="db-tagline">{s.tagline}</p>
              <div className="db-mini-swatches">
                {['bg','accent','fg'].map(k => s.palette?.[k] && <div key={k} className="db-chip" style={{background:s.palette[k]}} title={k} />)}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
