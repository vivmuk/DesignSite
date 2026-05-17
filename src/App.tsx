import { useState, useEffect } from 'react';
import { designStyles, mixedStyles, categories, type DesignStyle } from './data/designStyles';
import { openDesignSkills, skillCategories } from './data/openDesignSkills';
import { openDesignSystems, designSystemCategories } from './data/openDesignSystems';
import './App.css';

// ──────────────────────────────────────────────────────────────────────────────
// Showcase Tab
// ──────────────────────────────────────────────────────────────────────────────
// Curated hand-crafted showcase items
const curatedItems = [
  { id: 'stripe-saas-landing', title: 'Flux Analytics — SaaS Landing', skill: 'Frontend Design', system: 'Stripe', direction: 'Modern Minimal', desc: 'Premium fintech landing page with Stripe\'s weight-300 typography, purple accent, and navy hero.', file: '/showcase/stripe-saas-landing.html' },
  { id: 'linear-dashboard', title: 'Nexus — Analytics Dashboard', skill: 'Dashboard', system: 'Linear', direction: 'Modern Minimal', desc: 'Dark sidebar dashboard with metric cards, bar charts, and activity feed. Linear\'s dark precision.', file: '/showcase/linear-dashboard.html' },
  { id: 'brutalist-portfolio', title: 'A.RAW — Artist Portfolio', skill: 'Frontend Design', system: 'Brutalism', direction: 'Brutalist Experimental', desc: 'Heavy borders, oversized uppercase type, yellow+black palette. Confrontational and raw.', file: '/showcase/brutalist-portfolio.html' },
  { id: 'apple-mobile-app', title: 'Still — iOS Meditation App', skill: 'Mobile App', system: 'Apple', direction: 'Warm Soft', desc: 'iOS-native mobile UI with SF Pro, rounded cards, streak tracking, and session cards.', file: '/showcase/apple-mobile-app.html' },
  { id: 'glassmorphism-dashboard', title: 'Prism — Crypto Tracker', skill: 'Dashboard', system: 'Glassmorphism', direction: 'Tech Utility', desc: 'Frosted glass cards on dark bg, ambient glows, purple/cyan gradients. Crypto portfolio app.', file: '/showcase/glassmorphism-dashboard.html' },
  { id: 'editorial-magazine', title: 'Form & Function — Design Magazine', skill: 'Magazine Article', system: 'Editorial', direction: 'Editorial Monocle', desc: 'Print-inspired editorial layout with Libre Baskerville, red pull quotes, and cream paper.', file: '/showcase/editorial-magazine.html' },
  { id: 'neobrutalism-saas', title: 'Blockdrop — SaaS Landing', skill: 'SaaS Landing', system: 'Neobrutalism', direction: 'Brutalist Experimental', desc: 'Yellow+black neo-brutalist SaaS landing with offset shadows, heavy borders, and bold CTAs.', file: '/showcase/neobrutalism-saas.html' },
  { id: 'notion-blog-post', title: 'Blog Post — AI Design Systems', skill: 'Blog Post', system: 'Notion', direction: 'Warm Soft', desc: 'Notion-inspired long-form blog with warm off-white, serif headings, and generous whitespace.', file: '/showcase/notion-blog-post.html' },
  { id: 'vercel-docs-page', title: 'Nexus CLI — Documentation', skill: 'Docs Page', system: 'Vercel', direction: 'Modern Minimal', desc: 'Vercel-style dark documentation with Geist Mono code blocks, sidebar nav, and step-by-step guide.', file: '/showcase/vercel-docs-page.html' },
  { id: 'swiss-international', title: 'Swiss CLI — Terminal Docs', skill: 'Docs Page', system: 'Vercel', direction: 'Tech Utility', desc: 'Monochrome CLI docs with Geist Mono, command reference table, and quick start steps.', file: '/showcase/swiss-international.html' },
];

// Generate dynamic showcase items from data
const systemItems = openDesignSystems.map(ds => ({
  id: `sys-${ds.id}`,
  title: `${ds.name} — Design System`,
  skill: ds.style,
  system: ds.name,
  direction: ds.category,
  desc: ds.description,
  file: `/showcase/systems/${ds.id}.html`,
  type: 'system'
}));

const skillItems = openDesignSkills.map(skill => ({
  id: `skill-${skill.id}`,
  title: `${skill.name} — Skill`,
  skill: skill.category,
  system: skill.name,
  direction: 'Skill',
  desc: skill.description,
  file: `/showcase/skills/${skill.id}.html`,
  type: 'skill'
}));

const directionItems = [
  { id: 'editorial-monocle', name: 'Editorial Monocle', subtitle: 'Monocle / FT Magazine', mood: 'Print-magazine feel. Generous whitespace, large serif headlines, restrained palette of neutral paper + ink + a single brand-justified accent.', refs: ['Monocle', 'Financial Times Weekend', 'NYT Magazine', 'It\'s Nice That'], displayFont: 'Iowan Old Style, Charter, Georgia, serif', bodyFont: 'System-UI sans', palette: { bg: '#faf9f7', surface: '#fff', fg: '#1a1510', accent: '#c94020' } },
  { id: 'modern-minimal', name: 'Modern Minimal', subtitle: 'Linear / Vercel', mood: 'Quiet, precise, software-native. System fonts, crisp neutral foundations, small product palette so the interface feels shipped rather than greyscale.', refs: ['Linear', 'Vercel', 'Notion 2024', 'Stripe Docs'], displayFont: '-apple-system, SF Pro Display, system-ui, sans-serif', bodyFont: '-apple-system, SF Pro Text, system-ui, sans-serif', palette: { bg: '#fafafa', surface: '#fff', fg: '#111', accent: '#5566ff' } },
  { id: 'warm-soft', name: 'Warm Soft', subtitle: 'Calm / Loom / Duolingo', mood: 'Approachable, rounded, warm neutrals. Makes users feel welcomed and safe. Friendly but not childish.', refs: ['Calm', 'Loom', 'Duolingo', 'Notion warm'], displayFont: 'Plus Jakarta Sans, system-ui, sans-serif', bodyFont: 'system-ui, sans-serif', palette: { bg: '#fdf8f2', surface: '#fff9f2', fg: '#1c1612', accent: '#e07c3c' } },
  { id: 'tech-utility', name: 'Tech Utility', subtitle: 'Terminal / GitHub / Warp', mood: 'Monospace-heavy, data-dense, dark backgrounds. Designed for power users who live in the terminal.', refs: ['GitHub', 'Warp Terminal', 'Linear dark', 'Raycast'], displayFont: 'JetBrains Mono, SF Mono, monospace', bodyFont: 'system-ui, sans-serif', palette: { bg: '#0d0d0d', surface: '#141414', fg: '#e4e4e4', accent: '#3dd68c' } },
  { id: 'brutalist-experimental', name: 'Brutalist Experimental', subtitle: 'Raw / Conflicted / Confrontational', mood: 'Raw HTML feel, heavy borders, oversized type, high contrast, broken grids. Design that refuses to be invisible.', refs: ['brutalistwebsites.com', 'Bloomberg', 'Balenciaga', 'Rick Owens'], displayFont: 'Impact, Arial Black, Haettenschweiler, sans-serif', bodyFont: 'system-ui, sans-serif', palette: { bg: '#fafaf0', surface: '#fff', fg: '#0a0a0a', accent: '#ffe500' } },
].map(dir => ({
  id: `dir-${dir.id}`,
  title: `${dir.name} — Direction`,
  skill: dir.subtitle,
  system: dir.name,
  direction: dir.subtitle,
  desc: dir.mood,
  file: `/showcase/directions/${dir.id}.html`,
  type: 'direction'
}));

// All showcase items combined
const allShowcaseItems = [
  ...curatedItems.map(item => ({ ...item, type: 'curated' })),
  ...systemItems,
  ...skillItems,
  ...directionItems
];

const directions = [
  { id: 'editorial-monocle', name: 'Editorial Monocle', subtitle: 'Monocle / FT Magazine', mood: 'Print-magazine feel. Generous whitespace, large serif headlines, restrained palette of neutral paper + ink + a single brand-justified accent.', refs: ['Monocle', 'Financial Times Weekend', 'NYT Magazine', 'It\'s Nice That'], displayFont: 'Iowan Old Style, Charter, Georgia, serif', bodyFont: 'System-UI sans', palette: { bg: '#faf9f7', surface: '#fff', fg: '#1a1510', accent: '#c94020' } },
  { id: 'modern-minimal', name: 'Modern Minimal', subtitle: 'Linear / Vercel', mood: 'Quiet, precise, software-native. System fonts, crisp neutral foundations, small product palette so the interface feels shipped rather than greyscale.', refs: ['Linear', 'Vercel', 'Notion 2024', 'Stripe Docs'], displayFont: '-apple-system, SF Pro Display, system-ui, sans-serif', bodyFont: '-apple-system, SF Pro Text, system-ui, sans-serif', palette: { bg: '#fafafa', surface: '#fff', fg: '#111', accent: '#5566ff' } },
  { id: 'warm-soft', name: 'Warm Soft', subtitle: 'Calm / Loom / Duolingo', mood: 'Approachable, rounded, warm neutrals. Makes users feel welcomed and safe. Friendly but not childish.', refs: ['Calm', 'Loom', 'Duolingo', 'Notion warm'], displayFont: 'Plus Jakarta Sans, system-ui, sans-serif', bodyFont: 'system-ui, sans-serif', palette: { bg: '#fdf8f2', surface: '#fff9f2', fg: '#1c1612', accent: '#e07c3c' } },
  { id: 'tech-utility', name: 'Tech Utility', subtitle: 'Terminal / GitHub / Warp', mood: 'Monospace-heavy, data-dense, dark backgrounds. Designed for power users who live in the terminal.', refs: ['GitHub', 'Warp Terminal', 'Linear dark', 'Raycast'], displayFont: 'JetBrains Mono, SF Mono, monospace', bodyFont: 'system-ui, sans-serif', palette: { bg: '#0d0d0d', surface: '#141414', fg: '#e4e4e4', accent: '#3dd68c' } },
  { id: 'brutalist-experimental', name: 'Brutalist Experimental', subtitle: 'Raw / Conflicted / Confrontational', mood: 'Raw HTML feel, heavy borders, oversized type, high contrast, broken grids. Design that refuses to be invisible.', refs: ['brutalistwebsites.com', 'Bloomberg', 'Balenciaga', 'Rick Owens'], displayFont: 'Impact, Arial Black, Haettenschweiler, sans-serif', bodyFont: 'system-ui, sans-serif', palette: { bg: '#fafaf0', surface: '#fff', fg: '#0a0a0a', accent: '#ffe500' } },
];

function ShowcaseTab() {
  const [selected, setSelected] = useState<string | null>(null);
  const [section, setSection] = useState('all');
  const [search, setSearch] = useState('');
  
  const getItems = () => {
    let items = allShowcaseItems;
    if (section === 'curated') items = curatedItems.map(item => ({ ...item, type: 'curated' }));
    else if (section === 'systems') items = systemItems;
    else if (section === 'skills') items = skillItems;
    else if (section === 'directions') items = directionItems;
    
    if (search) {
      const s = search.toLowerCase();
      items = items.filter(i => 
        i.title.toLowerCase().includes(s) || 
        i.desc.toLowerCase().includes(s) ||
        i.system.toLowerCase().includes(s)
      );
    }
    return items;
  };
  
  const filtered = getItems();
  const selectedItem = allShowcaseItems.find(i => i.id === selected);
  return (
    <div className="showcase-tab">
      <div className="showcase-section-tabs">
        <button className={`section-tab ${section==='curated'?'active':''}`} onClick={()=>setSection('curated')}>
          Curated ({curatedItems.length})
        </button>
        <button className={`section-tab ${section==='systems'?'active':''}`} onClick={()=>setSection('systems')}>
          Design Systems ({systemItems.length})
        </button>
        <button className={`section-tab ${section==='skills'?'active':''}`} onClick={()=>setSection('skills')}>
          Skills ({skillItems.length})
        </button>
        <button className={`section-tab ${section==='directions'?'active':''}`} onClick={()=>setSection('directions')}>
          Directions ({directionItems.length})
        </button>
        <button className={`section-tab ${section==='all'?'active':''}`} onClick={()=>setSection('curated')}>
          All ({allShowcaseItems.length})
        </button>
      </div>
      
      <div className="showcase-search">
        <input 
          type="text" 
          placeholder="Search showcase..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-input"
        />
      </div>
      
      <div className="showcase-grid">
        {filtered.map(item => (
          <div key={item.id} className="showcase-card" onClick={()=>setSelected(item.id)}>
            <div className="showcase-preview" style={{'--preview-scale': '0.36'} as React.CSSProperties}>
              <iframe src={item.file} title={item.title} sandbox="allow-same-origin allow-scripts" tabIndex={-1} aria-hidden="true" />
              <div className="showcase-overlay"><span>Click to expand →</span></div>
            </div>
            <div className="showcase-info">
              <div className="showcase-tags"><span className="tag tag-system">{item.system}</span><span className="tag tag-skill">{item.skill}</span></div>
              <h3>{item.title}</h3>
              <p>{item.desc}</p>
            </div>
          </div>
        ))}
      </div>
      {selectedItem && (
        <div className="showcase-modal" onClick={()=>setSelected(null)}>
          <div className="modal-inner" onClick={e=>e.stopPropagation()}>
            <div className="modal-header">
              <div><h3>{selectedItem.title}</h3><div className="showcase-tags"><span className="tag tag-system">{selectedItem.system}</span><span className="tag tag-skill">{selectedItem.skill}</span><span className="tag">{selectedItem.direction}</span></div></div>
              <div className="modal-actions">
                <a href={selectedItem.file} target="_blank" rel="noopener noreferrer" className="modal-btn" onClick={e=>e.stopPropagation()}>Open in new tab ↗</a>
                <button className="modal-close" onClick={()=>setSelected(null)}>✕</button>
              </div>
            </div>
            <iframe src={selectedItem.file} title={selectedItem.title} className="modal-iframe" sandbox="allow-same-origin allow-scripts" />
          </div>
        </div>
      )}
    </div>
  );
}

// ──────────────────────────────────────────────────────────────────────────────
// Design Systems Tab
// ──────────────────────────────────────────────────────────────────────────────
// MiniSitePreview — renders a data-driven mini webpage mockup for a design system
// ──────────────────────────────────────────────────────────────────────────────
function MiniSitePreview({ ds }: { ds: typeof openDesignSystems[0] }) {
  const bg = ds.bgColor || '#ffffff';
  const acc = ds.accentColor || '#667788';
  const txt = ds.textColor || '#111111';
  const isDark = ds.tags?.includes('dark');
  const surface = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';
  const muted = isDark ? 'rgba(255,255,255,0.35)' : 'rgba(0,0,0,0.35)';
  const border = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';

  const isBrutalist = ds.style === 'brutalist';
  const isEditorial = ds.style === 'editorial';
  const isLuxury = ds.style === 'luxury';
  const radius = isBrutalist ? '0px' : isLuxury ? '2px' : '6px';
  const fontStyle = isEditorial ? 'Georgia, serif' : isBrutalist ? 'Impact, Arial Black, sans-serif' : 'system-ui, sans-serif';

  return (
    <div className="mini-preview" style={{ background: bg, fontFamily: fontStyle, border: `1px solid ${border}` }}>
      {/* Nav */}
      <div className="mp-nav" style={{ background: surface, borderBottom: `1px solid ${border}` }}>
        <div className="mp-logo" style={{ color: acc, fontWeight: 700, fontSize: 11 }}>{ds.name}</div>
        <div className="mp-nav-links">
          {['Product','Pricing','Docs'].map(l => (
            <div key={l} className="mp-nav-link" style={{ background: muted, borderRadius: radius }} />
          ))}
          <div className="mp-cta" style={{ background: acc, borderRadius: radius }} />
        </div>
      </div>
      {/* Hero */}
      <div className="mp-hero">
        <div className="mp-hero-text">
          <div className="mp-h1" style={{ background: txt, borderRadius: radius, opacity: 0.9 }} />
          <div className="mp-h1 mp-h1-sm" style={{ background: txt, borderRadius: radius, opacity: 0.5, width: '70%' }} />
          <div className="mp-p" style={{ background: muted, borderRadius: radius }} />
          <div className="mp-p" style={{ background: muted, borderRadius: radius, width: '80%' }} />
          <div style={{ display:'flex', gap:6, marginTop:8 }}>
            <div className="mp-btn" style={{ background: acc, borderRadius: radius, border: isBrutalist ? `2px solid ${txt}` : 'none' }} />
            <div className="mp-btn-ghost" style={{ border: `1.5px solid ${acc}`, borderRadius: radius }} />
          </div>
        </div>
        <div className="mp-hero-img" style={{ background: acc, opacity: 0.15, borderRadius: radius, border: `1px solid ${acc}` }}>
          <div style={{ width:'60%', height:6, background: acc, opacity:0.6, borderRadius:2, margin:'auto', marginTop:16 }} />
          <div style={{ width:'80%', height:4, background: acc, opacity:0.3, borderRadius:2, margin:'6px auto 0' }} />
          <div style={{ width:'40%', height:4, background: acc, opacity:0.3, borderRadius:2, margin:'4px auto 0' }} />
        </div>
      </div>
      {/* Feature strip */}
      <div className="mp-features">
        {[0,1,2].map(i => (
          <div key={i} className="mp-feature" style={{ background: surface, borderRadius: radius, border: `1px solid ${border}` }}>
            <div className="mp-feat-icon" style={{ background: acc, borderRadius: isBrutalist ? 0 : '50%', opacity: 0.8 }} />
            <div className="mp-feat-t" style={{ background: txt, borderRadius: 2, opacity: 0.7 }} />
            <div className="mp-feat-p" style={{ background: muted, borderRadius: 2 }} />
            <div className="mp-feat-p" style={{ background: muted, borderRadius: 2, width: '70%' }} />
          </div>
        ))}
      </div>
    </div>
  );
}

// ──────────────────────────────────────────────────────────────────────────────
// SkillPreview — layout skeleton based on skill category
// ──────────────────────────────────────────────────────────────────────────────
const skillPalettes: Record<string, { bg: string; acc: string; txt: string }> = {
  design:      { bg: '#0f0a1e', acc: '#a78bfa', txt: '#e5e0f8' },
  development: { bg: '#0a1628', acc: '#38bdf8', txt: '#e0eeff' },
  content:     { bg: '#1a1209', acc: '#f59e0b', txt: '#fdf3dc' },
  media:       { bg: '#0d1a12', acc: '#34d399', txt: '#d8f5ec' },
  ai:          { bg: '#0d1117', acc: '#f472b6', txt: '#fce7f3' },
  utility:     { bg: '#111827', acc: '#94a3b8', txt: '#e2e8f0' },
};

function SkillPreview({ skill }: { skill: typeof openDesignSkills[0] }) {
  const p = skillPalettes[skill.category] || skillPalettes.utility;
  const bg = p.bg, acc = p.acc, txt = p.txt;
  const muted = 'rgba(255,255,255,0.2)';
  const surface = 'rgba(255,255,255,0.05)';
  const border = 'rgba(255,255,255,0.08)';

  const isMagazine = skill.category === 'content';
  const isDev = skill.category === 'development';
  const isMedia = skill.category === 'media';

  return (
    <div className="mini-preview" style={{ background: bg, fontFamily: isDev ? 'monospace' : 'system-ui, sans-serif', border: `1px solid ${border}` }}>
      <div className="mp-nav" style={{ background: surface, borderBottom: `1px solid ${border}` }}>
        <div className="mp-logo" style={{ color: acc, fontWeight: 700, fontSize: 11 }}>{skill.name}</div>
        <div className="mp-nav-links">
          <div className="mp-nav-link" style={{ background: muted }} />
          <div className="mp-nav-link" style={{ background: muted }} />
          <div className="mp-cta" style={{ background: acc }} />
        </div>
      </div>
      {isMedia ? (
        <div style={{ padding: '10px 10px 6px', display:'flex', flexDirection:'column', gap:6 }}>
          <div style={{ background: acc, opacity:0.2, borderRadius:4, height:60 }} />
          <div style={{ display:'flex', gap:6 }}>
            {[1,2,3].map(i=><div key={i} style={{ flex:1, background:surface, borderRadius:4, height:40, border:`1px solid ${border}` }} />)}
          </div>
        </div>
      ) : isDev ? (
        <div style={{ padding: '8px 10px', display:'flex', flexDirection:'column', gap:4 }}>
          {['const app = build()', '  .with(design)', '  .export(html)'].map((line,i)=>(
            <div key={i} style={{ display:'flex', gap:6, alignItems:'center' }}>
              <div style={{ width:12, height:3, background:acc, opacity:0.4, borderRadius:1 }} />
              <div style={{ flex:1, height:3, background: i===0?acc:muted, opacity:0.6, borderRadius:1 }} />
            </div>
          ))}
          <div style={{ marginTop:4, background:'rgba(255,255,255,0.04)', borderRadius:4, padding:'6px 8px', border:`1px solid ${border}` }}>
            {[80,60,90,50].map((w,i)=><div key={i} style={{ width:`${w}%`, height:3, background:muted, borderRadius:1, marginBottom:i<3?3:0 }} />)}
          </div>
        </div>
      ) : isMagazine ? (
        <div style={{ padding: '8px 10px', display:'flex', flexDirection:'column', gap:5 }}>
          <div style={{ width:'85%', height:7, background:txt, opacity:0.8, borderRadius:2 }} />
          <div style={{ width:'60%', height:5, background:acc, opacity:0.7, borderRadius:2 }} />
          <div style={{ height:1, background:border }} />
          {[90,100,70,85].map((w,i)=><div key={i} style={{ width:`${w}%`, height:3, background:muted, borderRadius:1 }} />)}
        </div>
      ) : (
        <div className="mp-hero" style={{ paddingBottom:6 }}>
          <div className="mp-hero-text">
            <div className="mp-h1" style={{ background:txt, opacity:0.8 }} />
            <div className="mp-p" style={{ background:muted }} />
            <div className="mp-p" style={{ background:muted, width:'80%' }} />
            <div style={{ display:'flex', gap:6, marginTop:6 }}>
              <div className="mp-btn" style={{ background:acc }} />
            </div>
          </div>
          <div className="mp-hero-img" style={{ background:acc, opacity:0.12, border:`1px solid ${acc}` }} />
        </div>
      )}
      <div className="mp-features">
        {[0,1,2].map(i=>(
          <div key={i} className="mp-feature" style={{ background:surface, border:`1px solid ${border}` }}>
            <div className="mp-feat-icon" style={{ background:acc, opacity:0.7 }} />
            <div className="mp-feat-t" style={{ background:txt, opacity:0.6 }} />
            <div className="mp-feat-p" style={{ background:muted }} />
          </div>
        ))}
      </div>
    </div>
  );
}

// ──────────────────────────────────────────────────────────────────────────────
// DirectionPreview — rich mini page with direction's own palette + posture
// ──────────────────────────────────────────────────────────────────────────────
function DirectionPreview({ dir }: { dir: typeof directions[0] }) {
  const { bg, fg, accent } = dir.palette;
  const isEditorial = dir.id === 'editorial-monocle';
  const isBrutalist = dir.id === 'brutalist-experimental';
  const isTech = dir.id === 'tech-utility';
  const font = dir.displayFont.split(',')[0];
  const muted = `${fg}55`;
  const surface = isTech ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';
  const border = isTech ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';
  const radius = isBrutalist ? '0px' : isEditorial ? '2px' : '8px';

  return (
    <div className="mini-preview dir-mini" style={{ background: bg, fontFamily: font + ', system-ui, sans-serif', border: `1px solid ${border}` }}>
      <div className="mp-nav" style={{ background: surface, borderBottom: `1px solid ${border}` }}>
        <div style={{ color: accent, fontWeight: 700, fontSize: 11, letterSpacing: isEditorial?'0.05em':'-0.02em' }}>{dir.subtitle.split('/')[0].trim()}</div>
        <div className="mp-nav-links">
          <div className="mp-nav-link" style={{ background: muted }} />
          <div className="mp-nav-link" style={{ background: muted }} />
          <div className="mp-cta" style={{ background: accent, borderRadius: radius }} />
        </div>
      </div>
      {isEditorial ? (
        <div style={{ padding:'10px 10px 6px' }}>
          <div style={{ width:4, height:16, background:accent, display:'inline-block', marginRight:6, verticalAlign:'middle' }} />
          <div style={{ display:'inline-block', width:'70%', height:8, background:fg, opacity:0.8, verticalAlign:'middle', borderRadius:1 }} />
          <div style={{ marginTop:6 }}>
            {[100,90,85,70].map((w,i)=><div key={i} style={{ width:`${w}%`, height:3, background:muted, borderRadius:1, marginBottom:3 }} />)}
          </div>
          <div style={{ display:'flex', gap:8, marginTop:8 }}>
            {[0,1].map(i=><div key={i} style={{ flex:1, height:40, background:surface, border:`1px solid ${border}`, borderRadius:2 }} />)}
          </div>
        </div>
      ) : isBrutalist ? (
        <div style={{ padding:'8px 10px' }}>
          <div style={{ fontSize:0, borderBottom:`3px solid ${fg}`, paddingBottom:4, marginBottom:6 }}>
            <div style={{ width:'90%', height:10, background:fg }} />
          </div>
          <div style={{ display:'flex', gap:6 }}>
            <div style={{ flex:2, display:'flex', flexDirection:'column', gap:3 }}>
              {[100,90,80].map((w,i)=><div key={i} style={{ width:`${w}%`, height:3, background:fg, opacity:0.7 }} />)}
            </div>
            <div style={{ flex:1, height:40, background:accent, border:`2px solid ${fg}` }} />
          </div>
          <div style={{ marginTop:8, display:'flex', gap:4 }}>
            <div style={{ padding:'4px 10px', background:accent, border:`2px solid ${fg}`, fontSize:0, height:18 }} />
            <div style={{ padding:'4px 10px', border:`2px solid ${fg}`, fontSize:0, height:18 }} />
          </div>
        </div>
      ) : isTech ? (
        <div style={{ padding:'8px 10px', fontFamily:'monospace' }}>
          <div style={{ background:'rgba(255,255,255,0.04)', border:`1px solid ${border}`, borderRadius:4, padding:'6px 8px', marginBottom:6 }}>
            {['$ design generate', '  --system terminal', '  --output ./dist'].map((l,i)=>(
              <div key={i} style={{ display:'flex', gap:4, alignItems:'center', marginBottom:i<2?3:0 }}>
                <div style={{ width: i===0?8:12, height:3, background: i===0?accent:muted, borderRadius:1 }} />
                <div style={{ flex:1, height:3, background:muted, borderRadius:1 }} />
              </div>
            ))}
          </div>
          <div style={{ display:'flex', gap:6 }}>
            {[0,1,2].map(i=><div key={i} style={{ flex:1, height:32, background:surface, border:`1px solid ${border}`, borderRadius:4 }}>
              <div style={{ width:'60%', height:3, background:accent, opacity:0.6, borderRadius:1, margin:'8px auto 3px' }} />
              <div style={{ width:'80%', height:2, background:muted, borderRadius:1, margin:'0 auto' }} />
            </div>)}
          </div>
        </div>
      ) : (
        <div className="mp-hero" style={{ paddingBottom:6 }}>
          <div className="mp-hero-text">
            <div className="mp-h1" style={{ background:fg, opacity:0.85, borderRadius:radius }} />
            <div className="mp-p" style={{ background:muted, borderRadius:radius }} />
            <div className="mp-p" style={{ background:muted, borderRadius:radius, width:'80%' }} />
            <div style={{ display:'flex', gap:6, marginTop:6 }}>
              <div className="mp-btn" style={{ background:accent, borderRadius:radius }} />
              <div className="mp-btn-ghost" style={{ border:`1.5px solid ${accent}`, borderRadius:radius }} />
            </div>
          </div>
          <div className="mp-hero-img" style={{ background:accent, opacity:0.15, borderRadius:radius }} />
        </div>
      )}
      <div className="mp-features">
        {[0,1,2].map(i=>(
          <div key={i} className="mp-feature" style={{ background:surface, border:`1px solid ${border}`, borderRadius:radius }}>
            <div className="mp-feat-icon" style={{ background:accent, opacity:0.75, borderRadius:isBrutalist?0:'50%' }} />
            <div className="mp-feat-t" style={{ background:fg, opacity:0.65 }} />
            <div className="mp-feat-p" style={{ background:muted }} />
          </div>
        ))}
      </div>
    </div>
  );
}

function DesignSystemsTab() {
  const [catFilter, setCatFilter] = useState('all');
  const [search, setSearch] = useState('');
  const cats = [...new Set(openDesignSystems.map(d => d.category))];
  const filtered = openDesignSystems
    .filter(d => catFilter === 'all' || d.category === catFilter)
    .filter(d => !search || d.name.toLowerCase().includes(search.toLowerCase()) || d.description.toLowerCase().includes(search.toLowerCase()));
  return (
    <div className="systems-tab">
      <div className="systems-controls">
        <input className="search-input" placeholder="Search design systems…" value={search} onChange={e=>setSearch(e.target.value)} />
        <div className="cat-filters">
          <button className={`filter-btn ${catFilter==='all'?'active':''}`} onClick={()=>setCatFilter('all')}>All ({openDesignSystems.length})</button>
          {designSystemCategories.map(c => (
            <button key={c.id} className={`filter-btn ${catFilter===c.id?'active':''}`} onClick={()=>setCatFilter(c.id)}>
              {c.icon} {c.name}
            </button>
          ))}
        </div>
      </div>
      <div className="systems-grid">
        {filtered.map(ds => (
          <div key={ds.id} className="ds-card">
            <div className="ds-preview-wrap">
              <MiniSitePreview ds={ds} />
            </div>
            <div className="ds-body">
              <div className="ds-head">
                <span className="ds-name">{ds.name}</span>
                <span className={`ds-style-tag style-${ds.style}`}>{ds.style}</span>
              </div>
              <p className="ds-desc">{ds.description}</p>
              <div className="ds-swatches">
                {[ds.accentColor, ds.bgColor, ds.textColor].map((c,i) => (
                  <div key={i} className="swatch" style={{background:c}} title={c} />
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
      {filtered.length === 0 && <div className="empty-state">No design systems match your search.</div>}
    </div>
  );
}

// ──────────────────────────────────────────────────────────────────────────��───
// Skills Tab
// ──────────────────────────────────────────────────────────────────────────────
function SkillsTab() {
  const [catFilter, setCatFilter] = useState('all');
  const [search, setSearch] = useState('');
  const filtered = openDesignSkills
    .filter(s => catFilter === 'all' || s.category === catFilter)
    .filter(s => !search || s.name.toLowerCase().includes(search.toLowerCase()) || s.description.toLowerCase().includes(search.toLowerCase()));
  const catIcons: Record<string,string> = { design:'🎨', development:'💻', content:'📝', media:'🎬', ai:'🤖', utility:'🛠️' };
  return (
    <div className="skills-tab">
      <div className="systems-controls">
        <input className="search-input" placeholder="Search skills…" value={search} onChange={e=>setSearch(e.target.value)} />
        <div className="cat-filters">
          <button className={`filter-btn ${catFilter==='all'?'active':''}`} onClick={()=>setCatFilter('all')}>All ({openDesignSkills.length})</button>
          {skillCategories.map(c => (
            <button key={c.id} className={`filter-btn ${catFilter===c.id?'active':''}`} onClick={()=>setCatFilter(c.id)}>
              {c.icon} {c.name}
            </button>
          ))}
        </div>
      </div>
      <div className="skills-grid">
        {filtered.map(skill => (
          <div key={skill.id} className="skill-card skill-card-v">
            <div className="skill-preview-wrap">
              <SkillPreview skill={skill} />
            </div>
            <div className="skill-info skill-info-v">
              <div className="skill-head">
                <span className="skill-icon-sm">{catIcons[skill.category]||'🔧'}</span>
                <span className="skill-name">{skill.name}</span>
                <span className={`skill-cat-badge cat-${skill.category}`}>{skill.category}</span>
              </div>
              <p className="skill-desc">{skill.description}</p>
            </div>
          </div>
        ))}
      </div>
      {filtered.length === 0 && <div className="empty-state">No skills match your search.</div>}
    </div>
  );
}

// ──────────────────────────────────────────────────────────────────────────────
// Directions Tab
// ──────────────────────────────────────────────────────────────────────────────
function DirectionsTab() {
  return (
    <div className="directions-tab">
      <p className="directions-intro">Five curated visual directions from Open Design. Each ships a deterministic OKLCH palette, font stack, and layout posture — no model freestyle needed.</p>
      <div className="directions-grid">
        {directions.map(d => (
          <div key={d.id} className="direction-card" style={{'--dir-accent': d.palette.accent, '--dir-bg': d.palette.bg, '--dir-fg': d.palette.fg} as React.CSSProperties}>
            <div className="dir-preview-wrap">
              <DirectionPreview dir={d} />
            </div>
            <div className="dir-body">
              <span className="dir-subtitle">{d.subtitle}</span>
              <h3 className="dir-name">{d.name}</h3>
              <p className="dir-mood">{d.mood}</p>
              <div className="dir-refs">
                {d.refs.map(r => <span key={r} className="dir-ref">{r}</span>)}
              </div>
              <div className="dir-fonts">
                <div><span className="dir-font-label">Display</span><span className="dir-font-val">{d.displayFont.split(',')[0]}</span></div>
                <div><span className="dir-font-label">Body</span><span className="dir-font-val">{d.bodyFont.split(',')[0]}</span></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ──────────────────────────────────────────────────────────────────────────────
// Original Design Styles Tab (renamed from App)
// ──────────────────────────────────────────────────────────────────────────────
function DesignStylesTab() {
  const [activeStyle, setActiveStyle] = useState<string>('swiss');
  const [activeCategory, setActiveCategory] = useState<string>('classic');
  const [copiedColor, setCopiedColor] = useState<string | null>(null);
  const [activeModel, setActiveModel] = useState<'nano_banana_pro' | 'recraft_v4'>('nano_banana_pro');

  const filteredStyles = activeCategory === 'mixed' 
    ? [] 
    : designStyles.filter(s => s.category === activeCategory);

  const currentStyle = designStyles.find(s => s.id === activeStyle);
  const currentMixed = mixedStyles.find(m => m.id === activeStyle);

  const handleCopyColor = (color: string) => {
    navigator.clipboard.writeText(color);
    setCopiedColor(color);
    setTimeout(() => setCopiedColor(null), 1500);
  };

  return (
    <div className="dashboard">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>Design<span>Styles</span></h1>
          <p>30 Design Systems</p>
        </div>

        <nav className="sidebar-nav">
          {categories.map(cat => (
            <div key={cat.id} className="nav-category">
              <button 
                className={`category-header ${activeCategory === cat.id ? 'active' : ''}`}
                onClick={() => {
                  setActiveCategory(cat.id);
                  if (cat.id !== 'mixed') {
                    const firstStyle = designStyles.find(s => s.category === cat.id);
                    if (firstStyle) setActiveStyle(firstStyle.id);
                  } else {
                    setActiveStyle(mixedStyles[0].id);
                  }
                }}
              >
                <span className="cat-icon">{cat.icon}</span>
                <span className="cat-name">{cat.name}</span>
              </button>
              
              {cat.id !== 'mixed' && activeCategory === cat.id && (
                <div className="category-items">
                  {designStyles.filter(s => s.category === cat.id).map(style => (
                    <button
                      key={style.id}
                      className={`style-item ${activeStyle === style.id ? 'active' : ''}`}
                      onClick={() => setActiveStyle(style.id)}
                    >
                      <span className="style-number">{designStyles.indexOf(style) + 1}</span>
                      <span className="style-name">{style.name.split(' / ')[0]}</span>
                    </button>
                  ))}
                </div>
              )}

              {cat.id === 'mixed' && activeCategory === 'mixed' && (
                <div className="category-items">
                  {mixedStyles.map((mixed, idx) => (
                    <button
                      key={mixed.id}
                      className={`style-item mixed-item ${activeStyle === mixed.id ? 'active' : ''}`}
                      onClick={() => setActiveStyle(mixed.id)}
                    >
                      <span className="style-number mixed-num">{idx + 1}</span>
                      <span className="style-name">{mixed.name}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {activeCategory !== 'mixed' && currentStyle && (
          <StyleDisplay 
            style={currentStyle} 
            onCopyColor={handleCopyColor}
            copiedColor={copiedColor}
            activeModel={activeModel}
          />
        )}

        {activeCategory === 'mixed' && currentMixed && (
          <MixedStyleDisplay 
            mixed={currentMixed}
            onCopyColor={handleCopyColor}
            copiedColor={copiedColor}
          />
        )}
      </main>
    </div>
  );
}

function StyleDisplay({ 
  style, 
  onCopyColor, 
  copiedColor,
  activeModel
}: { 
  style: DesignStyle; 
  onCopyColor: (c: string) => void;
  copiedColor: string | null;
  activeModel?: 'nano_banana_pro' | 'recraft_v4';
}) {
  return (
    <div className="style-display">
      <header className="style-header">
        <div className="style-badge">{designStyles.indexOf(style) + 1}</div>
        <div className="style-title-group">
          <h2>{style.name}</h2>
          <p className="style-mood">{style.mood}</p>
        </div>
      </header>

      <div className="style-content">
        <div className="info-panel">
          <section className="info-section">
            <h3>Description</h3>
            <p>{style.description}</p>
          </section>

          <section className="info-section">
            <h3>Color Palette</h3>
            <div className="color-swatches">
              {style.colors.map((color, idx) => (
                <button
                  key={idx}
                  className="color-swatch"
                  style={{ backgroundColor: color }}
                  onClick={() => onCopyColor(color)}
                  title={`${color} - Click to copy`}
                >
                  <span className={`color-code ${copiedColor === color ? 'copied' : ''}`}>
                    {copiedColor === color ? '✓' : color}
                  </span>
                </button>
              ))}
            </div>
          </section>

          <section className="info-section">
            <h3>Typography</h3>
            <div className="font-info">
              <div className="font-row">
                <span className="font-label">Display</span>
                <span className="font-name">{style.fonts.display}</span>
              </div>
              <div className="font-row">
                <span className="font-label">Body</span>
                <span className="font-name">{style.fonts.body}</span>
              </div>
            </div>
          </section>

          <section className="info-section">
            <h3>Key Characteristics</h3>
            <div className="characteristics">
              {style.characteristics.map((char, idx) => (
                <span key={idx} className="characteristic-tag">{char}</span>
              ))}
            </div>
          </section>

          <section className="info-section prompt-section">
            <h3>AI Image Prompt</h3>
            <p className="prompt-hint">Copy this prompt for AI image generators</p>
            <div className="prompt-box">
              <pre>{`Create a webpage in ${style.name} style. ${style.description} 

Use these colors: ${style.colors.join(', ')}
Typography: ${style.fonts.display} for headlines, ${style.fonts.body} for body text.

Key elements: ${style.characteristics.join(', ')}.

The design should feel: ${style.mood}`}</pre>
            </div>
            <button 
              className="copy-prompt-btn"
              onClick={() => {
                const prompt = `Create a webpage in ${style.name} style. ${style.description} 

Use these colors: ${style.colors.join(', ')}
Typography: ${style.fonts.display} for headlines, ${style.fonts.body} for body text.

Key elements: ${style.characteristics.join(', ')}.

The design should feel: ${style.mood}`;
                navigator.clipboard.writeText(prompt);
                alert('Prompt copied to clipboard!');
              }}
            >
              📋 Copy Prompt
            </button>
          </section>
        </div>

        <div className="preview-panel">
          <div className="preview-browser">
            <div className="browser-chrome">
              <div className="browser-dots">
                <span></span><span></span><span></span>
              </div>
              <div className="browser-url">{style.exampleWebsite.toLowerCase().replace(/\s+/g, '-')}.com</div>
            </div>
            <WebsitePreview style={style} activeModel={activeModel} />
          </div>
          <p className="preview-caption">Best for: <strong>{style.exampleWebsite}</strong></p>
        </div>
      </div>
    </div>
  );
}

function MixedStyleDisplay({ 
  mixed, 
  onCopyColor, 
  copiedColor 
}: { 
  mixed: typeof mixedStyles[0]; 
  onCopyColor: (c: string) => void;
  copiedColor: string | null;
}) {
  return (
    <div className="style-display mixed-display">
      <header className="style-header">
        <div className="style-badge mixed-badge">⚗️</div>
        <div className="style-title-group">
          <h2>{mixed.name}</h2>
          <p className="style-mood">Hybrid Style Combination</p>
        </div>
      </header>

      <div className="style-content">
        <div className="info-panel">
          <section className="info-section">
            <h3>Description</h3>
            <p>{mixed.description}</p>
          </section>

          <section className="info-section">
            <h3>Parent Styles</h3>
            <div className="parent-styles">
              {mixed.parentStyles.map((parent, idx) => (
                <span key={idx} className="parent-style-tag">{parent}</span>
              ))}
            </div>
          </section>

          <section className="info-section">
            <h3>Combined Palette</h3>
            <div className="color-swatches">
              {mixed.colors.map((color, idx) => (
                <button
                  key={idx}
                  className="color-swatch"
                  style={{ backgroundColor: color }}
                  onClick={() => onCopyColor(color)}
                  title={`${color} - Click to copy`}
                >
                  <span className={`color-code ${copiedColor === color ? 'copied' : ''}`}>
                    {copiedColor === color ? '✓' : color}
                  </span>
                </button>
              ))}
            </div>
          </section>

          <section className="info-section prompt-section">
            <h3>AI Image Prompt</h3>
            <p className="prompt-hint">Copy this prompt for AI image generators</p>
            <div className="prompt-box">
              <pre>{`Create a webpage combining ${mixed.name}. 

${mixed.description}

Use these colors: ${mixed.colors.join(', ')}

This hybrid style blends: ${mixed.parentStyles.join(' + ')}`}</pre>
            </div>
            <button 
              className="copy-prompt-btn"
              onClick={() => {
                const prompt = `Create a webpage combining ${mixed.name}. 

${mixed.description}

Use these colors: ${mixed.colors.join(', ')}

This hybrid style blends: ${mixed.parentStyles.join(' + ')}`;
                navigator.clipboard.writeText(prompt);
                alert('Prompt copied to clipboard!');
              }}
            >
              📋 Copy Prompt
            </button>
          </section>
        </div>

        <div className="preview-panel">
          <div className="preview-browser">
            <div className="browser-chrome">
              <div className="browser-dots">
                <span></span><span></span><span></span>
              </div>
              <div className="browser-url">{mixed.exampleWebsite.toLowerCase().replace(/\s+/g, '-')}.com</div>
            </div>
            <WebsitePreview mixed={mixed} />
          </div>
          <p className="preview-caption">Best for: <strong>{mixed.exampleWebsite}</strong></p>
        </div>
      </div>
    </div>
  );
}

function WebsitePreview({ 
  style, 
  mixed,
  activeModel = 'nano_banana_pro'
}: { 
  style?: DesignStyle; 
  mixed?: typeof mixedStyles[0];
  activeModel?: 'nano_banana_pro' | 'recraft_v4';
}) {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);
  const minSwipeDistance = 50;
  
  const colors = mixed ? mixed.colors : style!.colors;
  const fonts = style?.fonts || { display: 'Arial', body: 'Arial' };
  const category = style?.category || 'brand';
  const styleId = style?.id || mixed?.id || '';
  
  // Check if mockup image exists
  const mockupImageNano = `/mockups/${styleId}_nano_banana_pro.png`;
  const mockupImageRecraft = `/mockups/${styleId}_recraft_v4.png`;
  
  // Sync slide with activeModel prop
  useEffect(() => {
    setCurrentSlide(activeModel === 'recraft_v4' ? 1 : 0);
  }, [activeModel]);
  
  // Touch handlers for swipe
  const handleTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };
  
  const handleTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };
  
  const handleTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;
    if (isLeftSwipe) {
      setCurrentSlide(prev => Math.min(prev + 1, 1));
    }
    if (isRightSwipe) {
      setCurrentSlide(prev => Math.max(prev - 1, 0));
    }
  };
  
  // Generate different preview layouts based on style characteristics
  const getPreviewLayout = () => {
    const id = style?.id || mixed?.id || '';
    
    // Map each specific style to its own layout
    const layoutMap: Record<string, string> = {
      // Classic styles
      'swiss': 'swiss',
      'modernism': 'modernism',
      'bauhaus': 'bauhaus',
      'midcentury': 'midcentury',
      'minimalism': 'minimalism',
      'editorial': 'editorial',
      // Contemporary
      'flat': 'flat',
      'material': 'material',
      'neumorphism': 'neumorphism',
      'glassmorphism': 'glass',
      'brutalist': 'brutalist',
      'cleanui': 'cleanui',
      // Typography
      'typographic': 'typographic',
      'swisstypography': 'swisstypography',
      'experimental': 'experimental',
      'editorialmax': 'editorialmax',
      // Expressive
      'maximalism': 'maximal',
      'psychedelic': 'psychedelic',
      'surrealism': 'surrealism',
      'collage': 'collage',
      'illustrative': 'illustrative',
      // Tech
      'futurism': 'futurism',
      'cyberpunk': 'cyberpunk',
      'terminal': 'terminal',
      'data': 'data',
      'algorithmic': 'algorithmic',
      // Brand
      'luxury': 'luxury',
      'corporate': 'corporate',
      'playful': 'playful',
      'handcrafted': 'handcrafted',
      'retro': 'retro',
      // Mixed
      'swiss-glass': 'swiss-glass',
      'brutal-cyber': 'brutal-cyber',
      'minimal-luxury': 'minimal-luxury',
      'editorial-max': 'editorial-max',
      'retro-futurism': 'retro-futurism',
      'nature-tech': 'nature-tech'
    };
    
    return layoutMap[id] || 'fullsite';
  };

  const layout = getPreviewLayout();

  // Use the mockup images with carousel for ALL styles that have images generated
  const generatedStyles = ['swiss', 'modernism', 'bauhaus', 'midcentury', 'minimalism', 'editorial', 'flat', 'material', 'neumorphism', 'glassmorphism', 'brutalist', 'cleanui', 'typographic', 'swisstypography', 'experimental', 'editorialmax', 'maximalism', 'psychedelic', 'surrealism', 'collage', 'illustrative', 'futurism', 'cyberpunk', 'terminal', 'data', 'algorithmic', 'luxury', 'corporate', 'playful', 'handcrafted', 'retro', 'swiss-glass', 'brutal-cyber', 'minimal-luxury', 'editorial-max', 'retro-futurism', 'nature-tech'];
  const hasMockup = generatedStyles.includes(styleId) || (mixed ? generatedStyles.includes(mixed.id) : false);
  
  // If we have mockup images, show them - skip the layout-specific HTML
  if (hasMockup) {
    return (
      <div className="preview-fullsite" style={{ 
        '--primary': colors[0],
        '--secondary': colors[1] || colors[0],
        '--accent': colors[2] || colors[0],
        '--dark': colors[3] || '#000',
        '--light': colors[4] || '#fff',
        '--font-display': fonts.display,
        '--font-body': fonts.body,
      } as React.CSSProperties}>
        {/* Swipeable Mockup Carousel */}
        <div className="mockup-carousel" onTouchStart={(e) => handleTouchStart(e)} onTouchMove={(e) => handleTouchMove(e)} onTouchEnd={handleTouchEnd}>
          <div className="carousel-track" style={{ transform: `translateX(${-currentSlide * 100}%)` }}>
            <div className="carousel-slide">
              <img 
                src={mockupImageNano} 
                alt={`${style?.name || 'Style'} - Nano Banana Pro`}
                className="mockup-image"
                draggable={false}
              />
            </div>
            <div className="carousel-slide">
              <img 
                src={mockupImageRecraft} 
                alt={`${style?.name || 'Style'} - Recraft V4`}
                className="mockup-image"
                draggable={false}
              />
            </div>
          </div>
          {/* Swipe Indicators */}
          <div className="swipe-indicators">
            <span className={`indicator ${currentSlide === 0 ? 'active' : ''}`} onClick={() => setCurrentSlide(0)}></span>
            <span className={`indicator ${currentSlide === 1 ? 'active' : ''}`} onClick={() => setCurrentSlide(1)}></span>
          </div>
          
          {/* Swipe Arrows - translucent indicators */}
          <button 
            className={`swipe-arrow swipe-arrow-left ${currentSlide === 0 ? 'hidden' : ''}`}
            onClick={() => setCurrentSlide(prev => Math.max(prev - 1, 0))}
            aria-label="Previous image"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
          </button>
          <button 
            className={`swipe-arrow swipe-arrow-right ${currentSlide === 1 ? 'hidden' : ''}`}
            onClick={() => setCurrentSlide(prev => Math.min(prev + 1, 1))}
            aria-label="Next image"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
          
          {/* Tap hint for mobile */}
          <div className="swipe-hint">Tap to flip</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`website-preview ${layout}`} style={{ 
      '--primary': colors[0],
      '--secondary': colors[1] || colors[0],
      '--accent': colors[2] || colors[0],
      '--dark': colors[3] || '#000',
      '--light': colors[4] || '#fff',
    } as React.CSSProperties}>
      {/* SWISS - Asymmetric grid, red accent */}
      {layout === 'swiss' && (
        <div className="preview-swiss">
          <div className="swiss-grid">
            <div className="swiss-block swiss-red" style={{background: colors[0]}}></div>
            <div className="swiss-block swiss-large">
              <span className="swiss-title">OBJECTIVE</span>
              <span className="swiss-sub">CLARITY</span>
            </div>
            <div className="swiss-block swiss-text">Helvetica</div>
            <div className="swiss-block swiss-img"></div>
          </div>
        </div>
      )}

      {/* MODERNISM - Pure function, no decoration */}
      {layout === 'modernism' && (
        <div className="preview-modernism">
          <div className="mod-hero">
            <div className="mod-line"></div>
            <h1 className="mod-title">FORM</h1>
            <p className="mod-follows">FOLLOWS FUNCTION</p>
            <div className="mod-line"></div>
          </div>
          <div className="mod-blocks">
            <div className="mod-block"></div>
            <div className="mod-block mod-tall"></div>
            <div className="mod-block"></div>
          </div>
        </div>
      )}

      {/* BAUHAUS - Geometric, primary colors */}
      {layout === 'bauhaus' && (
        <div className="preview-bauhaus">
          <div className="bauhaus-circle" style={{background: colors[0]}}></div>
          <div className="bauhaus-triangle"></div>
          <div className="bauhaus-rect" style={{background: colors[1]}}></div>
          <div className="bauhaus-text">BAUHAUS</div>
        </div>
      )}

      {/* MID-CENTURY - Warm, organic curves */}
      {layout === 'midcentury' && (
        <div className="preview-midcentury">
          <div className="mc-shape mc-blob"></div>
          <div className="mc-content">
            <h2 className="mc-title">Organic<br/>Modern</h2>
            <div className="mc-chair"></div>
          </div>
        </div>
      )}

      {/* MINIMALISM - Extreme whitespace */}
      {layout === 'minimalism' && (
        <div className="preview-minimalism">
          <div className="min-content">
            <h1 className="min-title">less</h1>
            <div className="min-divider"></div>
            <p className="min-sub">is more</p>
          </div>
        </div>
      )}

      {/* EDITORIAL - Magazine layout */}
      {layout === 'editorial' && (
        <div className="preview-editorial">
          <div className="ed-mast">Vogue</div>
          <div className="ed-hero">
            <h1 className="ed-title">The Art<br/>of Fashion</h1>
            <div className="ed-sidebar">
              <div className="ed-line"></div>
              <div className="ed-line short"></div>
            </div>
          </div>
        </div>
      )}

      {/* FLAT - No depth, simple shapes */}
      {layout === 'flat' && (
        <div className="preview-flat">
          <div className="flat-nav">
            <span className="flat-logo">☰</span>
            <div className="flat-icons">
              <span className="flat-icon" style={{background: colors[0]}}></span>
              <span className="flat-icon" style={{background: colors[1]}}></span>
              <span className="flat-icon" style={{background: colors[2]}}></span>
            </div>
          </div>
          <div className="flat-cards">
            <div className="flat-card" style={{background: colors[0]}}>
              <span className="flat-symbol">★</span>
            </div>
            <div className="flat-card" style={{background: colors[1]}}>
              <span className="flat-symbol">♥</span>
            </div>
            <div className="flat-card" style={{background: colors[2]}}>
              <span className="flat-symbol">◆</span>
            </div>
          </div>
        </div>
      )}

      {/* MATERIAL - Elevated cards, shadows */}
      {layout === 'material' && (
        <div className="preview-material">
          <div className="mat-fab" style={{background: colors[0]}}>+</div>
          <div className="mat-cards">
            <div className="mat-card mat-elevated">
              <div className="mat-header" style={{background: colors[0]}}></div>
              <div className="mat-body">
                <div className="mat-line"></div>
                <div className="mat-line short"></div>
              </div>
            </div>
            <div className="mat-card">
              <div className="mat-header" style={{background: colors[1]}}></div>
              <div className="mat-body">
                <div className="mat-line"></div>
                <div className="mat-line short"></div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* NEUMORPHISM - Soft shadows */}
      {layout === 'neumorphism' && (
        <div className="preview-neumorphism">
          <div className="neu-container">
            <div className="neu-btn neu-pressed">✓</div>
            <div className="neu-slider">
              <div className="neu-thumb"></div>
            </div>
            <div className="neu-card">
              <div className="neu-avatar"></div>
              <div className="neu-lines">
                <div className="neu-line"></div>
                <div className="neu-line short"></div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* GLASS - Frosted transparency */}
      {layout === 'glass' && (
        <div className="preview-glass">
          <div className="glass-bg-shapes">
            <div className="shape s1" style={{background: colors[0]}}></div>
            <div className="shape s2" style={{background: colors[1]}}></div>
          </div>
          <div className="glass-card">
            <div className="glass-header">
              <div className="avatar"></div>
              <div className="lines">
                <div className="line"></div>
                <div className="line short"></div>
              </div>
            </div>
            <div className="glass-content">
              <div className="g-block"></div>
              <div className="g-block"></div>
            </div>
          </div>
        </div>
      )}

      {/* BRUTALIST - Raw, harsh */}
      {layout === 'brutalist' && (
        <div className="preview-brutalist">
          <div className="brutalist-header" style={{background: colors[0], color: colors[2] || '#fff'}}>!! WARNING !!</div>
          <h1 className="brutalist-title">RAW<br/>DATA</h1>
          <div className="brutalist-blocks">
            <div className="b-block" style={{background: colors[0]}}></div>
            <div className="b-block" style={{background: colors[1]}}></div>
            <div className="b-block" style={{background: colors[2]}}></div>
          </div>
          <div className="brutalist-marquee">
            <span>NO DESIGN IS GOOD DESIGN NO DESIGN IS GOOD DESIGN</span>
          </div>
        </div>
      )}

      {/* CLEAN UI - Apple-like minimal */}
      {layout === 'cleanui' && (
        <div className="preview-cleanui">
          <nav className="clean-nav">
            <span className="clean-logo">Brand</span>
            <div className="clean-links">
              <span>Product</span>
              <span>Features</span>
              <span>Pricing</span>
            </div>
          </nav>
          <div className="clean-hero">
            <h1 className="clean-title">Simple.</h1>
            <p className="clean-sub">Beautifully minimal.</p>
            <button className="clean-btn">Learn more →</button>
          </div>
        </div>
      )}

      {/* TYPOGRAPHIC - Type as hero */}
      {layout === 'typographic' && (
        <div className="preview-typographic">
          <div className="typ-letters">
            <span className="typ-letter" style={{color: colors[0]}}>A</span>
            <span className="typ-letter" style={{color: colors[1]}}>a</span>
            <span className="typ-letter" style={{color: colors[2]}}>!</span>
          </div>
          <div className="typ-text">
            <h1 className="typ-headline">TYPOGRAPHY<br/>IS THE DESIGN</h1>
          </div>
        </div>
      )}

      {/* SWISS TYPOGRAPHY - Grid-based type */}
      {layout === 'swisstypography' && (
        <div className="preview-swisstypography">
          <div className="st-grid">
            <div className="st-item st-red" style={{background: colors[0]}}></div>
            <div className="st-item st-text">
              <span className="st-helv">HELVETICA</span>
            </div>
            <div className="st-item st-large">NEUE</div>
            <div className="st-item st-num">57</div>
          </div>
        </div>
      )}

      {/* EXPERIMENTAL - Broken, expressive */}
      {layout === 'experimental' && (
        <div className="preview-experimental">
          <div className="exp-text exp-rotated" style={{color: colors[0]}}>BROKEN</div>
          <div className="exp-text exp-offset" style={{color: colors[1]}}>GRID</div>
          <div className="exp-shape"></div>
          <div className="exp-text exp-small">experimental</div>
        </div>
      )}

      {/* EDITORIAL MAX - Oversized type */}
      {layout === 'editorialmax' && (
        <div className="preview-editorialmax">
          <h1 className="edmax-title">
            <span className="edmax-line1" style={{color: colors[0]}}>BIG</span>
            <span className="edmax-line2" style={{color: colors[1]}}>TYPE</span>
          </h1>
          <div className="edmax-small">oversized and dramatic</div>
        </div>
      )}

      {/* MAXIMALISM - Bold, chaotic */}
      {layout === 'maximal' && (
        <div className="preview-maximal">
          <div className="max-shapes">
            <div className="m-shape s1" style={{background: colors[0]}}></div>
            <div className="m-shape s2" style={{background: colors[1]}}></div>
            <div className="m-shape s3" style={{background: colors[2]}}></div>
            <div className="m-shape s4" style={{background: colors[3]}}></div>
            <div className="m-shape s5" style={{background: colors[4]}}></div>
          </div>
          <h1 className="max-title">MORE<br/>IS MORE</h1>
        </div>
      )}

      {/* PSYCHEDELIC - Flowing gradients */}
      {layout === 'psychedelic' && (
        <div className="preview-psychedelic">
          <div className="psy-bg"></div>
          <div className="psy-waves">
            <div className="psy-wave" style={{borderColor: colors[0]}}></div>
            <div className="psy-wave" style={{borderColor: colors[1]}}></div>
            <div className="psy-wave" style={{borderColor: colors[2]}}></div>
          </div>
          <h1 className="psy-title">TRIPPY</h1>
        </div>
      )}

      {/* SURREALISM - Dreamlike juxtapositions */}
      {layout === 'surrealism' && (
        <div className="preview-surrealism">
          <div className="surr-moon"></div>
          <div className="surr-eye" style={{borderColor: colors[0]}}></div>
          <div className="surr-cloud" style={{background: colors[1]}}></div>
          <div className="surr-text">DREAM</div>
        </div>
      )}

      {/* COLLAGE - Cut and paste */}
      {layout === 'collage' && (
        <div className="preview-collage">
          <div className="col-piece col-torn" style={{background: colors[0]}}></div>
          <div className="col-piece col-photo"></div>
          <div className="col-piece col-text" style={{background: colors[1]}}>
            <span>COPY</span>
          </div>
          <div className="col-piece col-tape"></div>
        </div>
      )}

      {/* ILLUSTRATIVE - Hand-drawn feel */}
      {layout === 'illustrative' && (
        <div className="preview-illustrative">
          <div className="ill-scene">
            <div className="ill-sun"></div>
            <div className="ill-hill"></div>
            <div className="ill-tree">
              <div className="ill-trunk"></div>
              <div className="ill-leaves"></div>
            </div>
          </div>
          <h2 className="ill-title">Hello World!</h2>
        </div>
      )}

      {/* FUTURISM - Tech, neon */}
      {layout === 'futurism' && (
        <div className="preview-futurism">
          <div className="fut-grid"></div>
          <div className="fut-hud">
            <div className="fut-ring" style={{borderColor: colors[0]}}></div>
            <div className="fut-ring inner" style={{borderColor: colors[1]}}></div>
          </div>
          <div className="fut-text">2077</div>
        </div>
      )}

      {/* CYBERPUNK - Neon, glitch */}
      {layout === 'cyberpunk' && (
        <div className="preview-cyberpunk">
          <div className="cyb-grid"></div>
          <div className="cyb-lines">
            <div className="cyb-line" style={{background: colors[0]}}></div>
            <div className="cyb-line" style={{background: colors[1]}}></div>
          </div>
          <h1 className="cyb-title">
            <span className="cyb-glitch" style={{color: colors[0]}}>NEON</span>
            <span className="cyb-glitch" style={{color: colors[1]}}>CITY</span>
          </h1>
        </div>
      )}

      {/* TERMINAL - AI Command Center */}
      {layout === 'terminal' && (
        <div className="preview-terminal">
          <div className="term-status">
            <span className="term-dot"></span>
            <span>SYSTEM ONLINE</span>
          </div>
          <div className="term-header">
            <span className="term-title">DRISHTI // AI COMMAND CENTER</span>
            <span className="term-build">v2.0.14</span>
          </div>
          <div className="term-readouts">
            <span>Neural Stream: <strong>ACTIVE</strong></span>
            <span>Agent Swarm: <strong>READY</strong></span>
          </div>
          <div className="term-prompt">
            <span className="term-prompt-symbol">{">"}</span>
            <span className="term-prompt-text">Enter command...</span>
            <span className="term-cursor">█</span>
          </div>
          <div className="term-logs">
            <div className="term-log">IDLE — Waiting for signals...</div>
            <div className="term-log">Neural Stream Active</div>
          </div>
        </div>
      )}

      {/* DATA - Charts, infographics */}
      {layout === 'data' && (
        <div className="preview-data">
          <div className="data-chart">
            <div className="data-bar" style={{height: '60%', background: colors[0]}}></div>
            <div className="data-bar" style={{height: '80%', background: colors[1]}}></div>
            <div className="data-bar" style={{height: '45%', background: colors[2]}}></div>
            <div className="data-bar" style={{height: '90%', background: colors[3]}}></div>
          </div>
          <div className="data-pie" style={{background: `conic-gradient(${colors[0]} 0deg 90deg, ${colors[1]} 90deg 180deg, ${colors[2]} 180deg 270deg, ${colors[3]} 270deg)`}}></div>
        </div>
      )}

      {/* ALGORITHMIC - Generative, procedural */}
      {layout === 'algorithmic' && (
        <div className="preview-algorithmic">
          <div className="algo-grid">
            {Array.from({length: 16}).map((_, i) => (
              <div 
                key={i} 
                className="algo-cell"
                style={{
                  background: i % 3 === 0 ? colors[0] : i % 2 === 0 ? colors[1] : colors[2],
                  opacity: 0.3 + (i % 5) * 0.15
                }}
              ></div>
            ))}
          </div>
          <div className="algo-text">GEN-01</div>
        </div>
      )}

      {/* LUXURY - Premium, exclusive */}
      {layout === 'luxury' && (
        <div className="preview-luxury">
          <div className="lux-crest">✦</div>
          <h1 className="lux-title">MAISON</h1>
          <p className="lux-sub">Since 1894</p>
          <div className="lux-line"></div>
        </div>
      )}

      {/* CORPORATE - Safe, professional */}
      {layout === 'corporate' && (
        <div className="preview-corporate">
          <nav className="corp-nav">
            <span className="corp-logo">◆ ACME Corp</span>
            <div className="corp-menu">Solutions | About | Contact</div>
          </nav>
          <div className="corp-hero">
            <h1 className="corp-title">Enterprise Solutions</h1>
            <div className="corp-blocks">
              <div className="corp-block" style={{background: colors[0]}}></div>
              <div className="corp-block" style={{background: colors[1]}}></div>
              <div className="corp-block" style={{background: colors[2]}}></div>
            </div>
          </div>
        </div>
      )}

      {/* PLAYFUL - Friendly, rounded */}
      {layout === 'playful' && (
        <div className="preview-playful">
          <div className="play-shapes">
            <div className="play-shape" style={{background: colors[0]}}></div>
            <div className="play-shape" style={{background: colors[1]}}></div>
            <div className="play-shape" style={{background: colors[2]}}></div>
          </div>
          <h1 className="play-title">Yay!</h1>
          <div className="play-btn" style={{background: colors[0]}}>Start</div>
        </div>
      )}

      {/* HANDCRAFTED - Organic, imperfect */}
      {layout === 'handcrafted' && (
        <div className="preview-handcrafted">
          <div className="hand-stamp">HANDMADE</div>
          <div className="hand-paper">
            <h2 className="hand-title">Artisan</h2>
            <div className="hand-line wavy"></div>
            <div className="hand-line"></div>
          </div>
        </div>
      )}

      {/* RETRO - 70s/80s vibes */}
      {layout === 'retro' && (
        <div className="preview-retro">
          <div className="ret-sun">
            <div className="ret-stripes"></div>
          </div>
          <h1 className="ret-title">COOL</h1>
          <div className="ret-grid">
            <div className="ret-square" style={{background: colors[0]}}></div>
            <div className="ret-square" style={{background: colors[1]}}></div>
            <div className="ret-square" style={{background: colors[2]}}></div>
            <div className="ret-square" style={{background: colors[3]}}></div>
          </div>
        </div>
      )}

      {/* DEFAULT fallback */}
      {layout === 'default' && (
        <div className="preview-default">
          <nav className="preview-nav">
            <span className="logo" style={{color: colors[0]}}>Brand</span>
            <div className="links">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </nav>
          <div className="hero">
            <h1 style={{color: colors[3]}}>Welcome</h1>
            <p style={{color: colors[3]}}>Your tagline here</p>
          </div>
          <div className="cards">
            <div className="card" style={{background: colors[0]}}></div>
            <div className="card" style={{background: colors[1] || colors[0]}}></div>
            <div className="card" style={{background: colors[2] || colors[0]}}></div>
          </div>
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────────
// Root App with 5-tab navigation
// ─────────────────────────────────────────────────────────────────────────────────
const TABS = [
  { id: 'styles', label: 'Design Styles', emoji: '🎨' },
  { id: 'systems', label: 'Design Systems', emoji: '🧩', count: openDesignSystems.length },
  { id: 'skills', label: 'Skills', emoji: '⚡', count: openDesignSkills.length },
  { id: 'directions', label: 'Directions', emoji: '🧭', count: 5 },
  { id: 'showcase', label: 'Showcase', emoji: '🔥', count: allShowcaseItems.length },
];

function App() {
  const [activeTab, setActiveTab] = useState<string>('showcase');
  return (
    <div className="root-app">
      <header className="root-header">
        <div className="root-header-inner">
          <div className="root-logo">OpenDesign<span>Studio</span></div>
          <nav className="root-tabs">
            {TABS.map(t => (
              <button key={t.id} className={`root-tab ${activeTab===t.id?'active':''}`} onClick={()=>setActiveTab(t.id)}>
                <span className="tab-emoji">{t.emoji}</span>
                <span className="tab-label">{t.label}</span>
                {t.count && <span className="tab-count">{t.count}</span>}
              </button>
            ))}
          </nav>
        </div>
      </header>
      <main className="root-main">
        {activeTab === 'styles' && <DesignStylesTab />}
        {activeTab === 'systems' && <DesignSystemsTab />}
        {activeTab === 'skills' && <SkillsTab />}
        {activeTab === 'directions' && <DirectionsTab />}
        {activeTab === 'showcase' && <ShowcaseTab />}
      </main>
    </div>
  );
}

export default App;
