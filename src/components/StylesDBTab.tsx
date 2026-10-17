import { useState, useEffect, useRef, type MouseEvent as ReactMouseEvent } from 'react';

interface DBStyle {
  n: number; id: string; name: string; category: string; tagline: string;
  techniques: string[]; best_for: string[]; component_focus: string[];
  palette: Record<string, string>; image_url: string; spec_url: string;
  agent_prompt?: string; fonts?: Record<string, string>; html_shell?: string;
}

const CATS = ['all','classic','contemporary','dark-tech','immersive-3d','scrollcraft','expressive','luxe-brand','data-pro','cultural','component-kit'];
const CAT_EMOJI: Record<string,string> = {
  'all':'🌐', 'classic':'🏛️', 'contemporary':'✨', 'dark-tech':'🖥️', 'immersive-3d':'🧊',
  'scrollcraft':'📜', 'expressive':'🎨', 'luxe-brand':'💎', 'data-pro':'📊', 'cultural':'🌍', 'component-kit':'🧩'
};
const API = 'https://styles-api-production.up.railway.app';

// Fallback prompt builder — guarantees every style yields a usable build prompt
// even when the live API is unreachable and the static snapshot has no agent_prompt field.
function buildPromptFromFields(s: DBStyle): string {
  const p = s.palette || {};
  const f = s.fonts || {};
  const pal = Object.entries(p).filter(([k,v]) => typeof v === 'string' && v.startsWith('#')).map(([k,v]) => `${k} ${v}`).join(', ');
  const fontBits = [f.display && `display: ${f.display}`, f.body && `body: ${f.body}`, f.mono && `mono: ${f.mono}`].filter(Boolean).join('; ');
  return [
    `ROLE: You are a senior front-end engineer. Build a single-page website in the "${s.name}" design style — ${s.tagline}.`,
    `LOOK: Palette — ${pal || 'choose a cohesive palette true to the style'}.${fontBits ? ` Typography — ${fontBits}.` : ''} Define every color as a CSS custom property on :root.`,
    `LAYOUT: (1) sticky nav with wordmark and 4-5 links; (2) hero with kicker, headline, lede, one primary CTA; (3) stats or feature band; (4) three-card feature grid; (5) CTA band; (6) footer. Sections: ${s.best_for?.join(', ') || 'general landing'} audience.`,
    `MOTION: Four named recipes, 150-600ms, ease-out curves; wrap ambient loops in prefers-reduced-motion.`,
    `SIGNATURE: ${s.component_focus?.join(', ')} treated in the "${s.name}" idiom; techniques to apply: ${s.techniques?.join(', ')}.`,
    `CONSTRAINTS: semantic HTML, WCAG AA contrast, responsive single column under 720px, no layout shift, defer JS.`,
    `DELIVERY: One self-contained index.html — inline CSS, Google Fonts via link with display=swap, vanilla JS only.`,
  ].join('\n');
}

async function copyText(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    try {
      const ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      const ok = document.execCommand('copy');
      document.body.removeChild(ta);
      return ok;
    } catch { return false; }
  }
}

// Fetches from the live styles-api; falls back to the static dataset snapshot if API is unreachable
export function StylesDBTab() {
  const [styles, setStyles] = useState<DBStyle[]>([]);
  const [cat, setCat] = useState('all');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [source, setSource] = useState<'api'|'static'>('static');
  const [apiAlive, setApiAlive] = useState(false);
  const [selected, setSelected] = useState<DBStyle | null>(null);
  const [prompt, setPrompt] = useState<string>('');
  const [promptLoading, setPromptLoading] = useState(false);
  const [promptSrc, setPromptSrc] = useState<'api'|'static'|'generated'>('api');
  const [copied, setCopied] = useState(false);
  const [shellHtml, setShellHtml] = useState<string>('');
  const [shellLoading, setShellLoading] = useState(false);
  const promptBoxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    (async () => {
      // The bundled dataset is the source of truth — it ships with the app and always
      // matches the deployed assets (images, specs, shells). The live API is enrichment.
      try {
        const r = await fetch('/styles-dataset.json');
        if (!r.ok) throw new Error('no dataset');
        const full = await r.json();
        setStyles(full.map((s: any) => ({
          n: s.n, id: s.id, name: s.name, category: s.category, tagline: s.tagline,
          techniques: s.techniques, best_for: s.best_for, component_focus: s.component_focus,
          palette: s.palette, fonts: s.fonts,
          agent_prompt: s.agent_prompt,
          html_shell: s.html_shell,
          image_url: `/styles-images-jpg/${s.id}.jpg`, spec_url: `/styles-specs/${s.id}.html`,
        })));
        setSource('static');
        // Probe the live API in the background (badge only; list stays from the bundle)
        try {
          const a = await fetch(`${API}/health`);
          if (a.ok) setApiAlive(true);
        } catch { /* API offline — fine */ }
      } finally { setLoading(false); }
    })();
  }, []);

  // When a style is selected, resolve its full build prompt:
  // 1) already on the record (static snapshot or API full row) → use directly
  // 2) else fetch /styles/:id/prompt from the API
  // 3) else synthesize from the record's own fields — never empty
  useEffect(() => {
    if (!selected) return;
    let alive = true;
    setCopied(false); setShellHtml(''); setShellLoading(false);
    (async () => {
      if (selected.agent_prompt) {
        setPrompt(selected.agent_prompt);
        setPromptSrc(source === 'api' ? 'api' : 'static');
      } else {
        setPromptLoading(true);
        try {
          const r = await fetch(`${API}/styles/${selected.id}/prompt`);
          if (!r.ok) throw new Error('no prompt');
          const j = await r.json();
          if (!alive) return;
          const text = j.agent_prompt || j.prompt || '';
          if (text) { setPrompt(text); setPromptSrc('api'); }
          else throw new Error('empty');
        } catch {
          if (!alive) return;
          setPrompt(buildPromptFromFields(selected));
          setPromptSrc('generated');
        } finally { if (alive) setPromptLoading(false); }
      }
    })();
    return () => { alive = false; };
  }, [selected]);

  const onCopyPrompt = async () => {
    if (!prompt) return;
    const ok = await copyText(prompt);
    if (ok) { setCopied(true); setTimeout(() => setCopied(false), 2000); }
    else {
      // Last resort: select the prompt text so a manual Cmd/Ctrl+C copies it
      const range = document.createRange();
      range.selectNodeContents(promptBoxRef.current!);
      const sel = window.getSelection();
      sel?.removeAllRanges();
      sel?.addRange(range);
    }
  };

  const onCopyFromCard = async (e: ReactMouseEvent, s: DBStyle) => {
    e.stopPropagation();
    const text = s.agent_prompt || buildPromptFromFields(s);
    await copyText(text);
  };

  const loadShell = async () => {
    if (shellHtml || !selected) return;
    setShellLoading(true);
    try {
      // Bundled shell first (works for all 150 styles, offline) — API as fallback
      if (selected.html_shell) { setShellHtml(selected.html_shell); return; }
      const r = await fetch(`${API}/styles/${selected.id}/html`);
      if (!r.ok) throw new Error();
      setShellHtml(await r.text());
    } catch {
      setShellHtml('');
    } finally { setShellLoading(false); }
  };

  const filtered = styles.filter(s =>
    (cat === 'all' || s.category === cat) &&
    (!search || s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.tagline.toLowerCase().includes(search.toLowerCase()) ||
      (s.techniques||[]).some(t => t.toLowerCase().includes(search.toLowerCase())))
  );

  if (loading) return <div className="db-loading">Loading 150-style database…</div>;

  if (selected) {
    const p = selected.palette || {} as any;
    return (
      <div className="db-detail">
        <button className="db-back" onClick={()=>setSelected(null)}>← Back to Styles DB</button>
        <img className="db-hero" src={selected.image_url.replace('/styles-images/','/styles-images-jpg/').replace('.png','.jpg')} alt={selected.name} />
        <div className="db-detail-head">
          <h1>{selected.name}</h1>
          <p className="db-tagline">{selected.tagline}</p>
          <div className="db-tags">
            <span className="tag tag-system">{selected.category}</span>
            {(selected.techniques||[]).map(t => <span key={t} className="tag">{t}</span>)}
          </div>
        </div>

        <div className="db-prompt-panel">
          <div className="db-prompt-head">
            <h3>Website build prompt</h3>
            <div className="db-prompt-meta">
              {promptSrc === 'api' && <span className="db-src api">live API</span>}
              {promptSrc === 'static' && <span className="db-src static">bundled</span>}
              {promptSrc === 'generated' && <span className="db-src gen">assembled from spec</span>}
              <span className="db-prompt-bytes">{prompt ? `${(prompt.length/1000).toFixed(1)}k chars` : '…'}</span>
            </div>
          </div>
          <p className="db-prompt-sub">Paste into any AI agent or site generator to build a website in this exact style.</p>
          <div ref={promptBoxRef} className="db-prompt-box">{promptLoading ? 'Fetching prompt…' : prompt}</div>
          <div className="db-prompt-actions">
            <button className={`db-btn primary db-copy-btn ${copied ? 'copied' : ''}`} onClick={onCopyPrompt} disabled={promptLoading || !prompt}>
              {copied ? '✓ Copied to clipboard' : '⧉ Copy build prompt'}
            </button>
            <a className="db-btn" href={`mailto:?subject=${encodeURIComponent('Build prompt — ' + selected.name)}&body=${encodeURIComponent(prompt.slice(0, 1800))}`}>✉ Email prompt</a>
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
            <a className="db-btn" href={`${API}/styles/${selected.id}/prompt`} target="_blank" rel="noopener">🔌 Agent prompt (JSON) ↗</a>
            <a className="db-btn" href={`${API}/styles/${selected.id}/html`} target="_blank" rel="noopener">🏗️ HTML shell ↗</a>
          </div>
        </div>

        <div className="db-shell-preview">
          <h3>Live HTML shell</h3>
          {!shellHtml && !shellLoading && <button className="db-btn primary" onClick={loadShell}>▶ Load live demo</button>}
          {shellLoading && <p className="db-shell-note">Loading shell…</p>}
          {shellHtml && <iframe className="db-shell-frame" title={`${selected.name} shell`} srcDoc={shellHtml} sandbox="allow-same-origin" />}
        </div>
      </div>
    );
  }

  return (
    <div className="stylesdb-tab">
      <h1>Styles DB <span className="db-count">{styles.length} styles</span></h1>
      <p className="db-sub">150 hand-authored design directions — each with palette, fonts, motion recipes, agent build prompt, Muse preview, and a downloadable spec sheet. {source === 'api' ? 'Live from the styles API.' : 'Bundled dataset — offline-proof.'}{apiAlive ? ' Styles API online for agents ↗' : ''}</p>
      <div className="db-controls">
        <input className="search-input" placeholder="Search styles, techniques…  (⌘/Ctrl+K)" value={search} onChange={e=>setSearch(e.target.value)} />
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
            <div className="db-thumb"><img src={s.image_url.replace('/styles-images/','/styles-images-jpg/').replace('.png','.jpg')} alt={s.name} loading="lazy" /></div>
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
