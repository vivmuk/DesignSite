import { useState, useEffect, useMemo } from 'react';

interface Technique {
  id: string; name: string; domain: string;
  level: 'core' | 'intermediate' | 'advanced' | 'innovative';
  one_line: string; why_pro: string; demo_idea: string;
  libraries?: string[]; spec_url?: string;
  demo_url?: string; prompt_url?: string;
}

const LEVELS = ['core','intermediate','advanced','innovative'] as const;
const LEVEL_META: Record<string, {label: string; color: string; desc: string}> = {
  core:        { label: 'Core',        color: '#3dd68c', desc: 'The fundamentals every pro knows cold' },
  intermediate:{ label: 'Intermediate', color: '#5566ff', desc: 'The working toolkit of production teams' },
  advanced:    { label: 'Advanced',    color: '#e07c3c', desc: 'Specialist techniques that separate great from good' },
  innovative:  { label: 'Innovative',  color: '#e935c1', desc: 'Cutting-edge — new APIs, GPU, AI in the browser' },
};

const DOMAIN_LABELS: Record<string,string> = {
  'css-foundations': 'CSS Foundations', 'layout': 'Layout Systems', 'typography': 'Typography',
  'color-image': 'Color & Image', 'motion': 'Motion & Animation', 'interaction': 'Interaction Patterns',
  'webgl-3d': '3D / WebGL', 'canvas-svg': 'Canvas / SVG / Generative', 'media': 'Audio / Video / Media',
  'data-viz': 'Data Visualization', 'ai-ml': 'AI / ML in Browser', 'emerging': 'Emerging Platform',
  'architecture': 'Architecture & Perf', 'a11y': 'Accessibility & i18n', 'dev-tricks': 'Pro Workflow Tricks',
};

const libsOf = (t: Technique): string[] => {
  const lib = t.libraries as unknown;
  if (Array.isArray(lib)) return lib as string[];
  if (typeof lib === 'string') { try { const a = JSON.parse(lib); return Array.isArray(a) ? a : []; } catch { return []; } }
  return [];
};

// Loads from the live styles-api /techniques endpoint; falls back to static catalog.json
export function TechniquesTab() {
  const [techniques, setTechniques] = useState<Technique[]>([]);
  const [level, setLevel] = useState<string>('all');
  const [domain, setDomain] = useState<string>('all');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Technique | null>(null);

  useEffect(() => {
    (async () => {
      const decorate = (arr: any[]) => arr.map(t => ({
        ...t,
        demo_url: t.demo_url || `/techniques-demos/${t.id}.html`,
        prompt_url: t.prompt_url || `https://styles-api-production.up.railway.app/techniques/${t.id}/prompt`,
      }));
      try {
        const r = await fetch('https://styles-api-production.up.railway.app/techniques');
        if (!r.ok) throw new Error('api down');
        setTechniques(decorate(await r.json()));
      } catch {
        const r = await fetch('/techniques-catalog.json');
        setTechniques(decorate(await r.json()));
      } finally { setLoading(false); }
    })();
  }, []);

  const domains = useMemo(() => Array.from(new Set(techniques.map(t => t.domain))), [techniques]);

  const filtered = useMemo(() => techniques.filter(t =>
    (level === 'all' || t.level === level) &&
    (domain === 'all' || t.domain === domain) &&
    (!search || t.name.toLowerCase().includes(search.toLowerCase()) ||
      t.one_line.toLowerCase().includes(search.toLowerCase()) ||
      t.demo_idea.toLowerCase().includes(search.toLowerCase()))
  ), [techniques, level, domain, search]);

  if (loading) return <div className="tech-loading">Loading the technique compendium…</div>;

  if (selected) {
    const meta = LEVEL_META[selected.level];
    return (
      <div className="tech-detail">
        <button className="tech-back" onClick={()=>setSelected(null)}>← All techniques</button>
        <div className="tech-detail-head">
          <span className="tag" style={{background: meta.color, color: '#000'}}>{meta.label}</span>
          <span className="tag tag-system">{DOMAIN_LABELS[selected.domain] || selected.domain}</span>
          <h1>{selected.name}</h1>
          <p className="tech-oneline">{selected.one_line}</p>
        </div>
        <div className="tech-detail-grid">
          <div className="tech-card">
            <h3>Live demo</h3>
            <p className="tech-why">{selected.why_pro}</p>
            {selected.demo_url
              ? <iframe className="tech-demo-frame" src={selected.demo_url} title={selected.name} loading="lazy" sandbox="allow-scripts allow-same-origin" />
              : <div className="tech-demo-frame tech-demo-empty">Demo generating…</div>}
            {selected.demo_url && <a className="tech-btn primary" href={selected.demo_url} target="_blank" rel="noopener">↗ Open demo full-screen</a>}
          </div>
          <div className="tech-card">
            <h3>Build it with an agent</h3>
            <p className="tech-demo-idea">{selected.demo_idea}</p>
            {libsOf(selected).length > 0 && (
              <div className="tech-libs">{libsOf(selected).map(l => <span key={l} className="tag">{l}</span>)}</div>
            )}
            {selected.prompt_url
              ? <a className="tech-btn" href={selected.prompt_url} target="_blank" rel="noopener">🔌 Agent prompt (JSON) ↗</a>
              : null}
            {selected.spec_url && <a className="tech-btn" href={selected.spec_url} target="_blank" rel="noopener">📖 Spec / docs ↗</a>}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="techniques-tab">
      <h1>Techniques <span className="db-count">{techniques.length}</span></h1>
      <p className="db-sub">The complete compendium of front-end techniques pros use — from first principles to the most innovative work shipping today. Every entry has a live demo and an agent-ready build prompt.</p>
      <div className="tech-levels">
        {LEVELS.map(l => (
          <button key={l} className={`tech-level-chip ${level===l?'active':''}`} style={level===l?{background:LEVEL_META[l].color,borderColor:LEVEL_META[l].color,color:'#000'}:{}} onClick={()=>setLevel(level===l?'all':l)}>
            <span className="dot" style={{background:LEVEL_META[l].color}} /> {LEVEL_META[l].label}
            <span className="db-n">{techniques.filter(t=>t.level===l).length}</span>
          </button>
        ))}
        {level !== 'all' && <button className="tech-level-chip" onClick={()=>setLevel('all')}>✕ clear</button>}
      </div>
      <p className="tech-level-desc">{level === 'all' ? 'Every technique, simple to innovative.' : LEVEL_META[level].desc}</p>
      <div className="db-controls">
        <input className="search-input" placeholder="Search techniques…" value={search} onChange={e=>setSearch(e.target.value)} />
      </div>
      <div className="tech-domains">
        <button className={`db-cat ${domain==='all'?'active':''}`} onClick={()=>setDomain('all')}>🌐 all <span className="db-n">{techniques.length}</span></button>
        {domains.map(d => (
          <button key={d} className={`db-cat ${domain===d?'active':''}`} onClick={()=>setDomain(domain===d?'all':d)}>
            {DOMAIN_LABELS[d] || d} <span className="db-n">{techniques.filter(t=>t.domain===d).length}</span>
          </button>
        ))}
      </div>
      <div className="tech-grid">
        {filtered.map(t => {
          const meta = LEVEL_META[t.level];
          return (
            <div key={t.id} className="tech-card tech-gridcard" onClick={()=>setSelected(t)}>
              <div className="tech-card-top">
                <span className="tag" style={{background: meta.color, color: '#000'}}>{meta.label}</span>
                <span className="tech-domain">{DOMAIN_LABELS[t.domain] || t.domain}</span>
              </div>
              <h3>{t.name}</h3>
              <p className="tech-oneline">{t.one_line}</p>
            </div>
          );
        })}
      </div>
      {filtered.length === 0 && <p className="tech-loading">No techniques match that filter.</p>}
    </div>
  );
}
