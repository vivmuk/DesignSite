#!/usr/bin/env node
/**
 * Generate fully-rendered showcase HTML pages for every design system, skill, and direction.
 * Each page is a standalone HTML file that visually demonstrates the style's aesthetic.
 * Reads data from src/data/*.ts and writes to public/showcase/{systems,skills,directions}/*.html
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.join(__dirname, 'public', 'showcase');

// ── Parse TS data files ──────────────────────────────────────────────────────
function parseTsArray(filePath, exportName) {
  const content = fs.readFileSync(filePath, 'utf-8');
  // Extract the array portion between [ and ]; 
  const match = content.match(/export\s+const\s+\w+\s*:\s*\w+\[\]\s*=\s*\[([\s\S]*?)\];/);
  if (!match) { console.error(`Could not parse ${filePath}`); process.exit(1); }
  // Parse each object literal
  const objs = [];
  let depth = 0, start = -1;
  const src = match[1];
  for (let i = 0; i < src.length; i++) {
    if (src[i] === '{') { if (depth === 0) start = i; depth++; }
    if (src[i] === '}') { depth--; if (depth === 0 && start >= 0) { 
      try { objs.push(eval('(' + src.slice(start, i+1) + ')')); } catch(e) {}
      start = -1; 
    }}
  }
  return objs;
}

const systems = parseTsArray(path.join(__dirname, 'src/data/openDesignSystems.ts'), 'openDesignSystems');
const skills = parseTsArray(path.join(__dirname, 'src/data/openDesignSkills.ts'), 'openDesignSkills');

// Directions are defined inline in App.tsx — extract them manually
const directions = [
  { id: 'editorial-monocle', name: 'Editorial Monocle', subtitle: 'Monocle / FT Magazine', mood: 'Print-magazine feel. Generous whitespace, large serif headlines, restrained palette of neutral paper + ink + a single brand-justified accent.', refs: ['Monocle', 'Financial Times Weekend', 'NYT Magazine'], displayFont: 'Iowan Old Style, Charter, Georgia, serif', bodyFont: 'System-UI, sans-serif', palette: { bg: '#faf9f7', surface: '#fff', fg: '#1a1510', accent: '#c94020' } },
  { id: 'modern-minimal', name: 'Modern Minimal', subtitle: 'Linear / Vercel', mood: 'Quiet, precise, software-native. System fonts, crisp neutral foundations.', refs: ['Linear', 'Vercel', 'Notion 2024', 'Stripe Docs'], displayFont: '-apple-system, SF Pro Display, system-ui, sans-serif', bodyFont: '-apple-system, SF Pro Text, system-ui, sans-serif', palette: { bg: '#fafafa', surface: '#fff', fg: '#111', accent: '#5566ff' } },
  { id: 'warm-soft', name: 'Warm Soft', subtitle: 'Calm / Loom / Duolingo', mood: 'Approachable, rounded, warm neutrals. Friendly but not childish.', refs: ['Calm', 'Loom', 'Duolingo'], displayFont: 'Plus Jakarta Sans, system-ui, sans-serif', bodyFont: 'system-ui, sans-serif', palette: { bg: '#fdf8f2', surface: '#fff9f2', fg: '#1c1612', accent: '#e07c3c' } },
  { id: 'tech-utility', name: 'Tech Utility', subtitle: 'Terminal / GitHub / Warp', mood: 'Monospace-heavy, data-dense, dark backgrounds. For power users.', refs: ['GitHub', 'Warp Terminal', 'Raycast'], displayFont: 'JetBrains Mono, SF Mono, monospace', bodyFont: 'system-ui, sans-serif', palette: { bg: '#0d0d0d', surface: '#141414', fg: '#e4e4e4', accent: '#3dd68c' } },
  { id: 'brutalist-experimental', name: 'Brutalist Experimental', subtitle: 'Raw / Conflicted / Confrontational', mood: 'Raw HTML feel, heavy borders, oversized type, high contrast, broken grids.', refs: ['brutalistwebsites.com', 'Bloomberg'], displayFont: 'Impact, Arial Black, sans-serif', bodyFont: 'system-ui, sans-serif', palette: { bg: '#fafaf0', surface: '#fff', fg: '#0a0a0a', accent: '#ffe500' } },
];

// Design style data (from designStyles.ts)
const designStyles = parseTsArray(path.join(__dirname, 'src/data/designStyles.ts'), 'designStyles');

// ── Style-aware HTML generators ──────────────────────────────────────────────

const placeholdCo = (w, h) => `https://placehold.co/${w}x${h}/eee/999?text=+`;

function systemHtml(ds) {
  const { id, name, category, description, accentColor, bgColor, textColor, primaryFont, style, tags } = ds;
  const isDark = tags?.includes('dark');
  const fg = textColor || '#111111';
  const bg = bgColor || '#ffffff';
  const acc = accentColor || '#667788';
  const font = primaryFont || 'system-ui';
  const surfaceAlpha = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)';
  const muteAlpha = isDark ? 'rgba(255,255,255,0.5)' : 'rgba(0,0,0,0.45)';
  const borderAlpha = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';
  const radius = style==='brutalist' ? '0' : style==='luxury' ? '2px' : style==='playful' ? '16px' : '8px';
  const fontStack = style==='editorial' ? 'Georgia, serif' : style==='brutalist' ? 'Impact, Arial Black, sans-serif' : font === 'system-ui' ? 'system-ui, -apple-system, sans-serif' : font;
  const categoryLabel = { productivity:'Productivity & SaaS', developer:'Developer Tools', fintech:'Fintech & Crypto', media:'Media & Consumer', creative:'Creative & Design', enterprise:'Enterprise', luxury:'Luxury & Automotive', gaming:'Gaming & Fun', editorial:'Editorial', modern:'Modern & Trendy' }[category] || category;
  
  // Generate different layout variations based on style
  const layouts = {
    minimal: 'nav+hero+features+testimonials+cta',
    bold: 'nav+split-hero+cards+stats+cta',
    playful: 'nav+colorful-hero+fun-cards+ricing+cta',
    elegant: 'nav+cinematic-hero+gallery+details+cta',
    technical: 'nav+code-hero+integrations+pricing+cta',
    editorial: 'nav+mag-hero+article+sidebar+cta',
    luxury: 'nav+premium-hero+showcase+heritage+cta',
    brutalist: 'nav+raw-hero+blocks+manifesto+cta',
  };
  const layout = layouts[style] || layouts.minimal;

  const nav = `
  <nav style="position:sticky;top:0;z-index:100;background:${isDark?'rgba(0,0,0,0.85)':'rgba(255,255,255,0.85)'};backdrop-filter:blur(20px);border-bottom:1px solid ${borderAlpha};padding:0 24px">
    <div style="max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:64px">
      <div style="font-weight:700;font-size:18px;letter-spacing:-0.02em;color:${fg}">${name}</div>
      <div style="display:flex;gap:32px;align-items:center">
        <a href="#" style="color:${muteAlpha};font-size:14px;text-decoration:none;font-weight:500">Product</a>
        <a href="#" style="color:${muteAlpha};font-size:14px;text-decoration:none;font-weight:500">Solutions</a>
        <a href="#" style="color:${muteAlpha};font-size:14px;text-decoration:none;font-weight:500">Docs</a>
        <a href="#" style="color:${muteAlpha};font-size:14px;text-decoration:none;font-weight:500">Pricing</a>
        <a href="#" style="background:${acc};color:${isDark?'#000':'#fff'};padding:8px 20px;border-radius:${radius};font-size:14px;font-weight:500;text-decoration:none">Get Started</a>
      </div>
    </div>
  </nav>`;

  const heroSection = style === 'brutalist' ? `
  <section style="padding:80px 24px;background:${bg};border-bottom:4px solid ${fg};position:relative;overflow:hidden">
    <div style="position:absolute;top:-40px;right:-40px;font-size:300px;font-weight:900;color:${acc};opacity:0.08;line-height:1">${name.toUpperCase()}</div>
    <div style="max-width:1200px;margin:0 auto;position:relative">
      <div style="display:inline-block;background:${acc};color:${fg};padding:4px 12px;font-weight:900;font-size:11px;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:16px;border:${radius==='0'?'none':'4px solid '+fg}">${categoryLabel}</div>
      <h1 style="font-size:clamp(36px,6vw,72px);font-weight:900;line-height:0.95;margin:0 0 24px;color:${fg};text-transform:uppercase;letter-spacing:-0.03em">${name}<br/>Redefined.</h1>
      <p style="font-size:18px;max-width:600px;margin:0 0 32px;color:${muteAlpha};line-height:1.6">${description}</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap">
        <a href="#" style="background:${fg};color:${bg};padding:14px 32px;font-weight:900;font-size:14px;text-decoration:none;text-transform:uppercase;border:4px solid ${fg}">Start Now →</a>
        <a href="#" style="background:transparent;color:${fg};padding:14px 32px;font-weight:900;font-size:14px;text-decoration:none;text-transform:uppercase;border:4px solid ${fg}">Read Docs</a>
      </div>
    </div>
  </section>` : style === 'luxury' ? `
  <section style="padding:140px 24px 120px;background:${bg};text-align:center;position:relative">
    <div style="max-width:900px;margin:0 auto">
      <div style="font-size:11px;text-transform:uppercase;letter-spacing:0.3em;color:${acc};margin-bottom:24px">${categoryLabel}</div>
      <h1 style="font-size:clamp(32px,5vw,64px);font-weight:300;letter-spacing:0.04em;line-height:1.1;margin:0 0 24px;color:${fg}">${name}</h1>
      <div style="width:60px;height:1px;background:${acc};margin:0 auto 24px"></div>
      <p style="font-size:18px;color:${muteAlpha};line-height:1.7;max-width:540px;margin:0 auto 48px">${description}</p>
      <a href="#" style="color:${acc};font-size:13px;text-transform:uppercase;letter-spacing:0.2em;text-decoration:none;border-bottom:1px solid ${acc}">Discover →</a>
    </div>
  </section>` : style === 'editorial' ? `
  <section style="padding:80px 24px;background:${bg};position:relative">
    <div style="max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center">
      <div>
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:0.2em;color:${acc};margin-bottom:20px">${categoryLabel}</div>
        <h1 style="font-size:clamp(36px,5vw,56px);font-weight:700;line-height:1.1;margin:0 0 20px;color:${fg};font-family:${fontStack}">${name}</h1>
        <p style="font-size:17px;color:${muteAlpha};line-height:1.7;margin:0 0 32px">${description}</p>
        <a href="#" style="color:${acc};text-decoration:none;font-weight:600;font-size:15px">Read article →</a>
      </div>
      <div style="background:${surfaceAlpha};aspect-ratio:4/3;border-radius:${radius};position:relative;overflow:hidden">
        <div style="position:absolute;bottom:20px;left:20px;right:20px;font-size:12px;text-transform:uppercase;letter-spacing:0.1em;color:${muteAlpha}">${name} — Visual Preview</div>
        <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;color:${muteAlpha}">
          <div style="font-size:48px;font-weight:200;color:${acc};opacity:0.4;line-height:1">${name.charAt(0)}</div>
        </div>
      </div>
    </div>
  </section>` : `
  <section style="padding:100px 24px 80px;background:${bg};text-align:center">
    <div style="max-width:800px;margin:0 auto">
      <div style="display:inline-block;background:${surfaceAlpha};padding:6px 16px;border-radius:20px;font-size:13px;color:${muteAlpha};margin-bottom:24px">${categoryLabel}</div>
      <h1 style="font-size:clamp(36px,5vw,56px);font-weight:${style==='bold'?'800':'600'};line-height:1.1;margin:0 0 20px;color:${fg};letter-spacing:-0.02em;font-family:${fontStack}">${name}</h1>
      <p style="font-size:18px;color:${muteAlpha};line-height:1.6;margin:0 auto 40px;max-width:600px">${description}</p>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
        <a href="#" style="background:${acc};color:${isDark?'#000':'#fff'};padding:12px 28px;border-radius:${radius};font-size:15px;font-weight:500;text-decoration:none;box-shadow:${style==='playful'?'4px 4px 0 '+fg:'0 4px 14px '+acc+'44'}">Get Started</a>
        <a href="#" style="background:transparent;color:${fg};padding:12px 28px;border-radius:${radius};font-size:15px;font-weight:500;text-decoration:none;border:1.5px solid ${borderAlpha}">Learn More</a>
      </div>
    </div>
  </section>`;

  const features = `
  <section style="padding:80px 24px;background:${isDark?'#0a0a0a':bg}">
    <div style="max-width:1200px;margin:0 auto">
      <div style="text-align:center;margin-bottom:48px">
        <h2 style="font-size:32px;font-weight:700;color:${fg};margin:0 0 12px;letter-spacing:-0.02em">Why ${name}?</h2>
        <p style="color:${muteAlpha};font-size:16px;margin:0">Built for teams that demand excellence.</p>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px">
        ${['Lightning Fast','Rock Solid','Beautifully Crafted'].map((title,i) => `
        <div style="background:${surfaceAlpha};border:1px solid ${borderAlpha};border-radius:${radius};padding:28px;transition:transform 0.2s">
          <div style="width:40px;height:40px;background:${acc};border-radius:${style==='brutalist'?'0':'50%'};margin-bottom:16px;display:flex;align-items:center;justify-content:center;color:${isDark?'#000':'#fff'};font-weight:700;font-size:18px">${['⚡','🛡️','✨'][i]}</div>
          <h3 style="font-size:17px;font-weight:600;color:${fg};margin:0 0 8px">${title}</h3>
          <p style="font-size:14px;color:${muteAlpha};line-height:1.6;margin:0">${['Unmatched performance that scales.','Enterprise-grade reliability at every level.','Every detail meticulously designed.'][i]}</p>
        </div>`).join('')}
      </div>
    </div>
  </section>`;

  const stats = `
  <section style="padding:60px 24px;background:${acc};color:${isDark?'#000':'#fff'}">
    <div style="max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:24px;text-align:center">
      ${[['99.9%','Uptime'],['10ms','Avg Response'],['50K+','Teams Use It'],['4.9★','Rating']].map(([val,label]) => `
      <div>
        <div style="font-size:36px;font-weight:${style==='bold'?'900':'700'};letter-spacing:-0.02em">${val}</div>
        <div style="font-size:14px;opacity:0.8;margin-top:4px">${label}</div>
      </div>`).join('')}
    </div>
  </section>`;

  const cta = `
  <section style="padding:80px 24px;background:${isDark?'#060606':bg};text-align:center">
    <div style="max-width:600px;margin:0 auto">
      <h2 style="font-size:36px;font-weight:700;color:${fg};margin:0 0 16px;letter-spacing:-0.02em">Ready to get started?</h2>
      <p style="color:${muteAlpha};font-size:16px;margin:0 0 32px;line-height:1.6">Join thousands of teams building with ${name}.</p>
      <div style="display:flex;gap:12px;justify-content:center">
        <a href="#" style="background:${acc};color:${isDark?'#000':'#fff'};padding:14px 32px;border-radius:${radius};font-weight:600;text-decoration:none;font-size:15px">Start Free →</a>
        <a href="#" style="color:${fg};padding:14px 32px;border-radius:${radius};font-weight:500;text-decoration:none;border:1.5px solid ${borderAlpha};font-size:15px">Contact Sales</a>
      </div>
    </div>
  </section>`;

  const footer = `
  <footer style="padding:40px 24px;background:${isDark?'#000':fg};color:${isDark?'rgba(255,255,255,0.5)':'rgba(255,255,255,0.7)'};font-size:13px">
    <div style="max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px">
      <div>© 2026 ${name}. ${style==='brutalist'?'NO RIGHTS RESERVED.':'All rights reserved.'}</div>
      <div style="display:flex;gap:24px">${['Privacy','Terms','Status','Blog'].map(l => `<a href="#" style="color:inherit;text-decoration:none">${l}</a>`).join('')}</div>
    </div>
  </footer>`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${name} — Design System Showcase</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { font-family: ${fontStack}; background: ${bg}; color: ${fg}; line-height: 1.6; -webkit-font-smoothing: antialiased; }
    a:hover { opacity: 0.8; }
  </style>
</head>
<body>
  ${nav}
  ${heroSection}
  ${features}
  ${stats}
  ${cta}
  ${footer}
</body>
</html>`;
}

function skillHtml(skill) {
  const { id, name, category, description } = skill;
  // Category-specific color palettes
  const palettes = {
    design: { bg:'#0f0a1e', acc:'#a78bfa', txt:'#e5e0f8', surface:'rgba(167,139,250,0.08)', border:'rgba(167,139,250,0.15)', cat:'🎨 Design & Visual' },
    development: { bg:'#0a1628', acc:'#38bdf8', txt:'#e0eeff', surface:'rgba(56,189,248,0.08)', border:'rgba(56,189,248,0.15)', cat:'💻 Development' },
    content: { bg:'#1a1209', acc:'#f59e0b', txt:'#fdf3dc', surface:'rgba(245,158,11,0.08)', border:'rgba(245,158,11,0.15)', cat:'📝 Content & Documents' },
    media: { bg:'#0d1a12', acc:'#34d399', txt:'#d8f5ec', surface:'rgba(52,211,153,0.08)', border:'rgba(52,211,153,0.15)', cat:'🎬 Media & Video' },
    ai: { bg:'#0d1117', acc:'#f472b6', txt:'#fce7f3', surface:'rgba(244,114,182,0.08)', border:'rgba(244,114,182,0.15)', cat:'🤖 AI & Generation' },
    utility: { bg:'#111827', acc:'#94a3b8', txt:'#e2e8f0', surface:'rgba(148,163,184,0.08)', border:'rgba(148,163,184,0.15)', cat:'🛠️ Utility & Tools' },
  };
  const p = palettes[category] || palettes.utility;
  const isDev = category === 'development';
  const fontStack = isDev ? "'JetBrains Mono', 'SF Mono', 'Fira Code', monospace" : "'Inter', system-ui, sans-serif";

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${name} — Skill Showcase</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { font-family: ${fontStack}; background: ${p.bg}; color: ${p.txt}; line-height: 1.6; -webkit-font-smoothing: antialiased; }
    a { color: ${p.acc}; text-decoration: none; }
    a:hover { opacity: 0.8; }
    .glow { box-shadow: 0 0 30px ${p.acc}33; }
    .card-hover:hover { transform: translateY(-2px); box-shadow: 0 8px 30px ${p.acc}22; }
  </style>
</head>
<body>
  <!-- Nav -->
  <nav style="position:sticky;top:0;z-index:100;background:rgba(0,0,0,0.6);backdrop-filter:blur(20px);border-bottom:1px solid ${p.border};padding:0 24px">
    <div style="max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:60px">
      <div style="display:flex;align-items:center;gap:8px">
        <div style="width:28px;height:28px;background:${p.acc};border-radius:6px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;color:${p.bg}">${name.charAt(0)}</div>
        <span style="font-weight:600;font-size:16px;color:${p.txt}">${name}</span>
      </div>
      <div style="display:flex;gap:24px;align-items:center">
        <a href="#" style="color:${p.txt};font-size:14px;opacity:0.7">Docs</a>
        <a href="#" style="color:${p.txt};font-size:14px;opacity:0.7">Examples</a>
        <a href="#" style="color:${p.txt};font-size:14px;opacity:0.7">API</a>
        <a href="#" style="background:${p.acc};color:${p.bg};padding:6px 16px;border-radius:6px;font-size:13px;font-weight:600">Try Free</a>
      </div>
    </div>
  </nav>

  <!-- Hero -->
  <section style="padding:80px 24px 60px;text-align:center;position:relative;overflow:hidden">
    <div style="position:absolute;top:0;left:50%;transform:translateX(-50%);width:600px;height:600px;background:radial-gradient(circle,${p.acc}15 0%,transparent 70%);pointer-events:none"></div>
    <div style="max-width:800px;margin:0 auto;position:relative">
      <div style="display:inline-block;background:${p.surface};border:1px solid ${p.border};padding:6px 16px;border-radius:20px;font-size:13px;color:${p.acc};margin-bottom:24px">${p.cat}</div>
      <h1 style="font-size:clamp(32px,5vw,52px);font-weight:700;line-height:1.1;margin:0 0 20px;letter-spacing:-0.02em">${name}</h1>
      <p style="font-size:17px;color:${p.txt};opacity:0.7;line-height:1.7;margin:0 auto 36px;max-width:560px">${description}</p>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
        <a href="#" style="background:${p.acc};color:${p.bg};padding:12px 28px;border-radius:8px;font-size:14px;font-weight:600;box-shadow:0 0 20px ${p.acc}44">Get Started</a>
        <a href="#" style="background:${p.surface};color:${p.txt};padding:12px 28px;border-radius:8px;font-size:14px;font-weight:500;border:1px solid ${p.border}">View Documentation</a>
      </div>
    </div>
  </section>

  <!-- Code/Preview Block -->
  <section style="padding:40px 24px 60px">
    <div style="max-width:900px;margin:0 auto">
      <div style="background:${p.surface};border:1px solid ${p.border};border-radius:12px;overflow:hidden;glow">
        <div style="padding:12px 16px;border-bottom:1px solid ${p.border};display:flex;align-items:center;gap:8px">
          <div style="width:12px;height:12px;border-radius:50%;background:#ff5f57"></div>
          <div style="width:12px;height:12px;border-radius:50%;background:#febc2e"></div>
          <div style="width:12px;height:12px;border-radius:50%;background:#28c840"></div>
          <span style="margin-left:auto;font-size:12px;opacity:0.5">example.${isDev?'ts':'html'}</span>
        </div>
        <pre style="padding:20px;font-family:${fontStack};font-size:13px;line-height:1.7;overflow-x:auto;color:${p.txt};opacity:0.9"><code>${isDev ? `import { ${name.replace(/[^a-zA-Z]/g,'')} } from '@opendesign/${id}';

const result = await ${name.replace(/[^a-zA-Z]/g,'')}.generate({
  input: "Your creative brief",
  style: "modern",
  quality: "high"
});

console.log(result.output);
// → ✨ Generated ${category} output` : `&lt;div class="${id}-container"&gt;
  &lt;h1 class="${id}-title"&gt;${name}&lt;/h1&gt;
  &lt;p class="${id}-description"&gt;
    ${description}
  &lt;/p&gt;
&lt;/div&gt;`}</code></pre>
      </div>
    </div>
  </section>

  <!-- Feature Grid -->
  <section style="padding:40px 24px 80px">
    <div style="max-width:1200px;margin:0 auto">
      <h2 style="font-size:28px;font-weight:700;margin:0 0 32px;text-align:center">Capabilities</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px">
        ${[
          {icon:'⚡',title:'Lightning Fast',desc:'Instant generation with optimized pipelines.'},
          {icon:'🎯',title:'Pixel Perfect',desc:'Every output crafted to professional standards.'},
          {icon:'🔄',title:'Iterative Refinement',desc:'Refine results until they match your vision.'},
          {icon:'📐',title:'Design System Aware',desc:'Works within your existing design language.'},
          {icon:'🌐',title:'Open Standards',desc:'Built on open protocols and standards.'},
          {icon:'🔧',title:'Highly Configurable',desc:'Customize every parameter for your needs.'},
        ].map(f => `
        <div class="card-hover" style="background:${p.surface};border:1px solid ${p.border};border-radius:10px;padding:24px;transition:all 0.2s;cursor:default">
          <div style="font-size:24px;margin-bottom:12px">${f.icon}</div>
          <h3 style="font-size:16px;font-weight:600;margin:0 0 8px">${f.title}</h3>
          <p style="font-size:14px;opacity:0.65;line-height:1.5;margin:0">${f.desc}</p>
        </div>`).join('')}
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section style="padding:60px 24px;text-align:center;background:${p.surface};border-top:1px solid ${p.border}">
    <div style="max-width:600px;margin:0 auto">
      <h2 style="font-size:32px;font-weight:700;margin:0 0 16px">Start Building</h2>
      <p style="opacity:0.7;margin:0 0 28px">Open Design ${name} — free to try, powerful in production.</p>
      <a href="#" style="display:inline-block;background:${p.acc};color:${p.bg};padding:14px 32px;border-radius:8px;font-weight:600;font-size:15px">Get Started Free →</a>
    </div>
  </section>

  <!-- Footer -->
  <footer style="padding:32px 24px;text-align:center;opacity:0.4;font-size:13px">
    © 2026 Open Design Studio · ${name} Skill Showcase
  </footer>
</body>
</html>`;
}

function directionHtml(dir) {
  const { id, name, subtitle, mood, refs, displayFont, bodyFont, palette } = dir;
  const isDark = palette.bg === '#0d0d0d' || palette.bg === '#0a0a0f';
  const fontStack = displayFont || 'system-ui, sans-serif';

  const refLinks = (refs||[]).map(r => `<a href="#" style="color:${palette.accent};text-decoration:none;font-size:13px;border:1px solid ${palette.accent}33;padding:4px 10px;border-radius:4px">${r}</a>`).join(' ');

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${name} — Design Direction</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { font-family: ${displayFont}, ${bodyFont}; background: ${palette.bg}; color: ${palette.fg}; line-height: 1.6; -webkit-font-smoothing: antialiased; }
  </style>
</head>
<body>
  <!-- Navigation -->
  <nav style="position:sticky;top:0;z-index:100;background:${isDark?'rgba(13,13,13,0.85)':'rgba(255,255,255,0.85)'};backdrop-filter:blur(20px);border-bottom:1px solid ${isDark?'rgba(255,255,255,0.08)':'rgba(0,0,0,0.08)'};padding:0 24px">
    <div style="max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:56px">
      <div style="font-weight:700;font-size:16px;letter-spacing:-0.02em">${name}</div>
      <div style="display:flex;gap:24px;align-items:center">
        <a href="#" style="color:inherit;opacity:0.6;font-size:14px;text-decoration:none">Overview</a>
        <a href="#" style="color:inherit;opacity:0.6;font-size:14px;text-decoration:none">Principles</a>
        <a href="#" style="color:inherit;opacity:0.6;font-size:14px;text-decoration:none">Examples</a>
        <a href="#" style="background:${palette.accent};color:${isDark?'#000':'#fff'};padding:6px 18px;border-radius:6px;font-size:13px;font-weight:500;text-decoration:none">Use Direction</a>
      </div>
    </div>
  </nav>

  <!-- Hero -->
  <section style="padding:120px 24px 100px;text-align:center;position:relative;overflow:hidden">
    <div style="position:absolute;top:-200px;left:50%;transform:translateX(-50%);width:800px;height:800px;background:radial-gradient(circle,${palette.accent}20 0%,transparent 60%);pointer-events:none"></div>
    <div style="max-width:900px;margin:0 auto;position:relative">
      <div style="font-size:12px;text-transform:uppercase;letter-spacing:0.3em;color:${palette.accent};margin-bottom:24px">${subtitle}</div>
      <h1 style="font-size:clamp(40px,7vw,80px);font-weight:900;line-height:0.95;margin:0 0 32px;letter-spacing:-0.03em">${name}</h1>
      <p style="font-size:20px;color:${isDark?'rgba(255,255,255,0.6)':'rgba(0,0,0,0.55)'};line-height:1.7;max-width:680px;margin:0 auto 40px">${mood}</p>
      <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">${refLinks}</div>
    </div>
  </section>

  <!-- Showcase Grid -->
  <section style="padding:60px 24px">
    <div style="max-width:1200px;margin:0 auto">
      <h2 style="font-size:28px;font-weight:700;margin:0 0 40px;text-align:center">Design Language</h2>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">
        <!-- Color Palette -->
        <div style="background:${palette.surface};border:1px solid ${isDark?'rgba(255,255,255,0.08)':'rgba(0,0,0,0.08)'};border-radius:12px;padding:32px">
          <h3 style="font-size:14px;text-transform:uppercase;letter-spacing:0.15em;margin:0 0 20px;opacity:0.5">Color Palette</h3>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            ${Object.entries(palette).map(([key, color]) => `
            <div style="text-align:center">
              <div style="width:60px;height:60px;background:${color};border-radius:8px;border:2px solid ${isDark?'rgba(255,255,255,0.1)':'rgba(0,0,0,0.1)'}"></div>
              <div style="font-size:11px;margin-top:6px;opacity:0.6">${key}</div>
              <div style="font-size:10px;opacity:0.4">${color}</div>
            </div>`).join('')}
          </div>
        </div>
        <!-- Typography -->
        <div style="background:${palette.surface};border:1px solid ${isDark?'rgba(255,255,255,0.08)':'rgba(0,0,0,0.08)'};border-radius:12px;padding:32px">
          <h3 style="font-size:14px;text-transform:uppercase;letter-spacing:0.15em;margin:0 0 20px;opacity:0.5">Typography</h3>
          <div style="margin-bottom:20px">
            <div style="font-family:${displayFont};font-size:48px;font-weight:700;line-height:1.1;margin-bottom:4px">Aa</div>
            <div style="font-size:12px;opacity:0.5">${displayFont}</div>
          </div>
          <div>
            <div style="font-family:${bodyFont};font-size:16px;line-height:1.6;opacity:0.7">The quick brown fox jumps over the lazy dog. 0123456789</div>
            <div style="font-size:12px;opacity:0.5;margin-top:4px">${bodyFont}</div>
          </div>
        </div>
        <!-- UI Components -->
        <div style="background:${palette.surface};border:1px solid ${isDark?'rgba(255,255,255,0.08)':'rgba(0,0,0,0.08)'};border-radius:12px;padding:32px;grid-column:1/-1">
          <h3 style="font-size:14px;text-transform:uppercase;letter-spacing:0.15em;margin:0 0 24px;opacity:0.5">UI Components</h3>
          <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center">
            <button style="background:${palette.accent};color:${isDark?'#000':'#fff'};padding:12px 24px;border:none;border-radius:6px;font-size:14px;font-weight:600;cursor:pointer;font-family:${displayFont}">Primary Button</button>
            <button style="background:transparent;color:${palette.fg};padding:12px 24px;border:1.5px solid ${isDark?'rgba(255,255,255,0.2)':'rgba(0,0,0,0.2)'};border-radius:6px;font-size:14px;font-weight:500;cursor:pointer;font-family:${bodyFont}">Secondary</button>
            <div style="background:${isDark?'rgba(255,255,255,0.06)':'rgba(0,0,0,0.04)'};padding:10px 16px;border-radius:8px;font-size:14px">${isDark?'🌙 Dark Mode':'☀️ Light Mode'}</div>
            <input placeholder="Search this style..." style="background:${isDark?'rgba(255,255,255,0.08)':'rgba(0,0,0,0.04)'};border:1px solid ${isDark?'rgba(255,255,255,0.12)':'rgba(0,0,0,0.12)'};padding:10px 16px;border-radius:8px;font-size:14px;color:${palette.fg};width:200px;outline:none;font-family:${bodyFont}">
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Principles -->
  <section style="padding:60px 24px;background:${isDark?'#000':palette.bg}">
    <div style="max-width:1200px;margin:0 auto;text-align:center">
      <h2 style="font-size:28px;font-weight:700;margin:0 0 40px">Key Principles</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px;text-align:left">
        ${['Visual Clarity','Consistent Rhythm','Purposeful Space','Adaptive Layout','Expressive Detail'].map((title,i) => `
        <div style="background:${isDark?'rgba(255,255,255,0.03)':'rgba(0,0,0,0.02)'};padding:24px;border-radius:10px;border:1px solid ${isDark?'rgba(255,255,255,0.06)':'rgba(0,0,0,0.06)'}">
          <div style="font-size:28px;margin-bottom:8px">${['👁️','🎵','📐','🌊','✨'][i]}</div>
          <h3 style="font-size:16px;font-weight:600;margin:0 0 8px">${title}</h3>
          <p style="font-size:14px;opacity:0.6;line-height:1.5;margin:0">Core design principles that define the ${name} direction and ensure visual coherence.</p>
        </div>`).join('')}
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section style="padding:80px 24px;text-align:center;background:${palette.accent}">
    <div style="max-width:600px;margin:0 auto">
      <h2 style="font-size:36px;font-weight:800;margin:0 0 16px;color:${isDark?'#000':'#fff'}">Apply This Direction</h2>
      <p style="opacity:0.8;margin:0 0 28px;color:${isDark?'#000':'#fff'}">Use ${name} in your next project.</p>
      <a href="#" style="display:inline-block;background:${isDark?'#000':'#fff'};color:${palette.accent};padding:14px 32px;border-radius:8px;font-weight:600;font-size:15px;text-decoration:none">Explore →</a>
    </div>
  </section>

  <!-- Footer -->
  <footer style="padding:32px 24px;text-align:center;opacity:0.4;font-size:13px;color:${palette.fg}">
    © 2026 Open Design Studio · ${name} Direction
  </footer>
</body>
</html>`;
}

// ── Generate all files ──────────────────────────────────────────────────────

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

let count = 0;
const dirs = ['systems', 'skills', 'directions'];
dirs.forEach(d => ensureDir(path.join(OUT_DIR, d)));

// Systems
for (const ds of systems) {
  const html = systemHtml(ds);
  const fp = path.join(OUT_DIR, 'systems', `${ds.id}.html`);
  fs.writeFileSync(fp, html, 'utf-8');
  count++;
}

// Skills
for (const skill of skills) {
  const html = skillHtml(skill);
  const fp = path.join(OUT_DIR, 'skills', `${skill.id}.html`);
  fs.writeFileSync(fp, html, 'utf-8');
  count++;
}

// Directions
for (const dir of directions) {
  const html = directionHtml(dir);
  const fp = path.join(OUT_DIR, 'directions', `${dir.id}.html`);
  fs.writeFileSync(fp, html, 'utf-8');
  count++;
}

console.log(`✅ Generated ${count} showcase pages`);
console.log(`   Systems: ${systems.length}`);
console.log(`   Skills: ${skills.length}`);
console.log(`   Directions: ${directions.length}`);