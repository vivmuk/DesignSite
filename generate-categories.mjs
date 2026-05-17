#!/usr/bin/env node
/**
 * Generate category-level showcase pages (the missing ones that the TS parser skipped).
 * These are the category pages: developer, fintech, gaming, media, productivity, etc.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.join(__dirname, 'public', 'showcase');

const category_systems = {
  "developer": { name: "Developer Tools", emoji: "🛠️", bg: "#0a1628", acc: "#38bdf8", desc: "Tools and platforms that empower developers to build, ship, and iterate faster. Dark interfaces, code-centric layouts, and monospace precision." },
  "fintech": { name: "Fintech & Crypto", emoji: "💳", bg: "#0a2540", acc: "#00d4aa", desc: "Financial platforms and cryptocurrency exchanges. Trust indicators, data-dense dashboards, and institutional clarity." },
  "gaming": { name: "Gaming & Fun", emoji: "🎮", bg: "#1a0a2e", acc: "#a855f7", desc: "Playful, immersive, and visually adventurous. Bright colors, dynamic layouts, and interactive motivation." },
  "media": { name: "Media & Consumer", emoji: "📱", bg: "#ffffff", acc: "#ff385c", desc: "Consumer brands and media platforms. Photography-driven, elegant, and emotionally resonant interfaces." },
  "productivity": { name: "Productivity & SaaS", emoji: "⚡", bg: "#fafafa", acc: "#533afd", desc: "SaaS dashboards and productivity tools. Clean, efficient interfaces focused on workflows and clarity." },
};

const category_skills = {
  "ai": { name: "AI & Generation", emoji: "🤖", bg: "#0d1117", acc: "#f472b6", desc: "Artificial intelligence and generation skills. Neural interfaces, prompt engineering, and AI-powered creation tools." },
  "content": { name: "Content & Documents", emoji: "📝", bg: "#1a1209", acc: "#f59e0b", desc: "Document creation, editing, and publishing. Rich text, formatting, and content management workflows." },
  "design": { name: "Design & Visual", emoji: "🎨", bg: "#0f0a1e", acc: "#a78bfa", desc: "Visual design, layout, and creative tools. Color theory, composition, and design system implementation." },
  "development": { name: "Development & Code", emoji: "💻", bg: "#0a1628", acc: "#38bdf8", desc: "Code generation, frontend development, and programming tools. Syntax highlighting and developer experience." },
  "media": { name: "Media & Video", emoji: "🎬", bg: "#0d1a12", acc: "#34d399", desc: "Video, audio, and multimedia creation. Frames, effects, and cinematic production tools." },
  "utility": { name: "Utility & Tools", emoji: "🛠️", bg: "#111827", acc: "#94a3b8", desc: "Practical tools and utilities. Screenshot capture, diagrams, and workflow automation." },
};

function categorySystemHtml(id, data) {
  const { name, emoji, bg, acc, desc } = data;
  const isDark = !['#ffffff', '#fafafa', '#f5f5f7'].includes(bg);
  const fg = isDark ? '#ffffff' : '#111111';
  const surface = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)';
  const border = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';
  const navBg = isDark ? 'rgba(0,0,0,0.6)' : 'rgba(255,255,255,0.8)';
  const btnText = isDark ? '#000' : '#fff';

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${name} — Design System Category</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { font-family: 'Inter', system-ui, sans-serif; background: ${bg}; color: ${fg}; line-height: 1.6; -webkit-font-smoothing: antialiased; }
    a { color: ${acc}; text-decoration: none; }
    a:hover { opacity: 0.8; }
  </style>
</head>
<body>
  <nav style="position:sticky;top:0;z-index:100;background:${navBg};backdrop-filter:blur(20px);border-bottom:1px solid ${border};padding:0 24px">
    <div style="max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:60px">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:24px">${emoji}</span>
        <span style="font-weight:700;font-size:18px">${name}</span>
      </div>
      <div style="display:flex;gap:24px;align-items:center">
        <a href="#" style="color:${fg};font-size:14px;opacity:0.7">Systems</a>
        <a href="#" style="color:${fg};font-size:14px;opacity:0.7">Skills</a>
        <a href="#" style="color:${fg};font-size:14px;opacity:0.7">Directions</a>
        <a href="#" style="background:${acc};color:${btnText};padding:8px 20px;border-radius:8px;font-size:14px;font-weight:500">Explore</a>
      </div>
    </div>
  </nav>

  <section style="padding:120px 24px 80px;text-align:center;position:relative;overflow:hidden">
    <div style="position:absolute;top:-200px;left:50%;transform:translateX(-50%);width:600px;height:600px;background:radial-gradient(circle,${acc}20 0%,transparent 70%);pointer-events:none"></div>
    <div style="max-width:800px;margin:0 auto;position:relative">
      <div style="font-size:64px;margin-bottom:24px">${emoji}</div>
      <div style="display:inline-block;background:${surface};padding:6px 16px;border-radius:20px;font-size:13px;color:${acc};margin-bottom:20px">Design System Category</div>
      <h1 style="font-size:clamp(36px,6vw,64px);font-weight:800;line-height:1.05;margin:0 0 24px;letter-spacing:-0.03em">${name}</h1>
      <p style="font-size:18px;color:${isDark?'rgba(255,255,255,0.6)':'rgba(0,0,0,0.55)'};line-height:1.7;margin:0 auto 40px;max-width:600px">${desc}</p>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
        <a href="#" style="background:${acc};color:${btnText};padding:12px 28px;border-radius:8px;font-size:15px;font-weight:600;box-shadow:0 0 30px ${acc}44">Browse Systems</a>
        <a href="#" style="background:${surface};color:${fg};padding:12px 28px;border-radius:8px;font-size:15px;font-weight:500;border:1px solid ${border}">View Skills</a>
      </div>
    </div>
  </section>

  <section style="padding:60px 24px">
    <div style="max-width:1200px;margin:0 auto">
      <h2 style="font-size:28px;font-weight:700;margin:0 0 40px;text-align:center">Featured Systems</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px">
        ${['Alpha System','Beta Platform','Gamma Interface','Delta Dashboard','Epsilon Tools','Zeta Engine'].map(n => `
        <div style="background:${surface};border:1px solid ${border};border-radius:12px;padding:24px;cursor:default;transition:transform 0.2s">
          <h3 style="font-size:16px;font-weight:600;margin:0 0 8px">${n}</h3>
          <p style="font-size:14px;opacity:0.6;line-height:1.5;margin:0">Explore ${n.toLowerCase()} within the ${name.toLowerCase()} category</p>
        </div>`).join('')}
      </div>
    </div>
  </section>

  <section style="padding:60px 24px;background:${acc};text-align:center">
    <div style="max-width:600px;margin:0 auto">
      <h2 style="font-size:32px;font-weight:700;margin:0 0 16px;color:${btnText}">Start Exploring</h2>
      <p style="opacity:0.8;margin:0 0 28px;color:${btnText}">Discover all ${name.toLowerCase()} design systems and skills.</p>
      <a href="#" style="display:inline-block;background:${btnText};color:${acc};padding:14px 32px;border-radius:8px;font-weight:600;font-size:15px;text-decoration:none">Browse All →</a>
    </div>
  </section>

  <footer style="padding:32px 24px;text-align:center;opacity:0.4;font-size:13px">© 2026 Open Design Studio · ${name} Category</footer>
</body>
</html>`;
}

function categorySkillHtml(id, data) {
  const { name, emoji, bg, acc, desc } = data;

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${name} — Skill Category</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { font-family: 'Inter', system-ui, sans-serif; background: ${bg}; color: #e0e0e0; line-height: 1.6; -webkit-font-smoothing: antialiased; }
    a { color: ${acc}; text-decoration: none; }
    a:hover { opacity: 0.8; }
  </style>
</head>
<body>
  <nav style="position:sticky;top:0;z-index:100;background:rgba(0,0,0,0.6);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.1);padding:0 24px">
    <div style="max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:60px">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:24px">${emoji}</span>
        <span style="font-weight:700;font-size:16px;color:#e0e0e0">${name}</span>
      </div>
      <div style="display:flex;gap:24px;align-items:center">
        <a href="#" style="color:#e0e0e0;font-size:14px;opacity:0.7">Overview</a>
        <a href="#" style="color:#e0e0e0;font-size:14px;opacity:0.7">Skills</a>
        <a href="#" style="color:#e0e0e0;font-size:14px;opacity:0.7">API</a>
        <a href="#" style="background:${acc};color:#000;padding:6px 16px;border-radius:6px;font-size:13px;font-weight:600">Try Free</a>
      </div>
    </div>
  </nav>

  <section style="padding:100px 24px 80px;text-align:center;position:relative;overflow:hidden">
    <div style="position:absolute;top:-200px;left:50%;transform:translateX(-50%);width:600px;height:600px;background:radial-gradient(circle,${acc}15 0%,transparent 70%);pointer-events:none"></div>
    <div style="max-width:800px;margin:0 auto;position:relative">
      <div style="font-size:64px;margin-bottom:20px">${emoji}</div>
      <div style="display:inline-block;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);padding:6px 16px;border-radius:20px;font-size:13px;color:${acc};margin-bottom:24px">Open Design Skills</div>
      <h1 style="font-size:clamp(32px,5vw,52px);font-weight:700;line-height:1.1;margin:0 0 20px;letter-spacing:-0.02em">${name}</h1>
      <p style="font-size:17px;color:rgba(255,255,255,0.6);line-height:1.7;margin:0 auto 36px;max-width:560px">${desc}</p>
      <div style="display:flex;gap:12px;justify-content:center">
        <a href="#" style="background:${acc};color:#000;padding:12px 28px;border-radius:8px;font-size:14px;font-weight:600;box-shadow:0 0 20px ${acc}44">Explore Skills</a>
        <a href="#" style="background:rgba(255,255,255,0.05);color:#e0e0e0;padding:12px 28px;border-radius:8px;font-size:14px;font-weight:500;border:1px solid rgba(255,255,255,0.1)">Documentation</a>
      </div>
    </div>
  </section>

  <section style="padding:40px 24px 60px">
    <div style="max-width:1200px;margin:0 auto">
      <h2 style="font-size:28px;font-weight:700;margin:0 0 32px;text-align:center">Skills in This Category</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px">
        ${['Quick Generate','High Quality','Iterate & Refine','System Aware'].map((title,i) => `
        <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:24px;cursor:default;transition:transform 0.2s">
          <div style="font-size:24px;margin-bottom:12px">${['⚡','🎯','🔄','📐'][i]}</div>
          <h3 style="font-size:16px;font-weight:600;margin:0 0 8px">${title}</h3>
          <p style="font-size:14px;opacity:0.65;line-height:1.5;margin:0">${name.toLowerCase()} skills for professional output.</p>
        </div>`).join('')}
      </div>
    </div>
  </section>

  <section style="padding:60px 24px;text-align:center;background:rgba(255,255,255,0.05);border-top:1px solid rgba(255,255,255,0.1)">
    <div style="max-width:600px;margin:0 auto">
      <h2 style="font-size:32px;font-weight:700;margin:0 0 16px">Start Building</h2>
      <p style="opacity:0.7;margin:0 0 28px">Open Design ${name} — free to try, powerful in production.</p>
      <a href="#" style="display:inline-block;background:${acc};color:#000;padding:14px 32px;border-radius:8px;font-weight:600;font-size:15px">Get Started Free →</a>
    </div>
  </section>

  <footer style="padding:32px 24px;text-align:center;opacity:0.4;font-size:13px">© 2026 Open Design Studio · ${name} Skills</footer>
</body>
</html>`;
}

// Generate and write files
let count = 0;
for (const [id, data] of Object.entries(category_systems)) {
  const html = categorySystemHtml(id, data);
  const fp = path.join(OUT_DIR, 'systems', `${id}.html`);
  fs.writeFileSync(fp, html, 'utf-8');
  console.log(`✅ systems/${id}.html`);
  count++;
}

for (const [id, data] of Object.entries(category_skills)) {
  const html = categorySkillHtml(id, data);
  const fp = path.join(OUT_DIR, 'skills', `${id}.html`);
  fs.writeFileSync(fp, html, 'utf-8');
  console.log(`✅ skills/${id}.html`);
  count++;
}

// Verify no remaining JSX stubs
import { execSync } from 'child_process';
let stubs = 0;
for (const subdir of ['systems', 'skills', 'directions']) {
  const full = path.join(OUT_DIR, subdir);
  for (const f of fs.readdirSync(full)) {
    if (!f.endsWith('.html')) continue;
    const fp = path.join(full, f);
    const content = fs.readFileSync(fp, 'utf-8');
    if (!content.startsWith('<!DOCTYPE html>')) {
      console.log(`⚠️ STILL A STUB: ${subdir}/${f}`);
      stubs++;
    }
  }
}
console.log(`\n✅ Generated ${count} category pages`);
console.log(`   Remaining JSX stubs: ${stubs}`);