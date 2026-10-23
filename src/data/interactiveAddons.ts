/**
 * Interactive elements — 25 working playgrounds.
 *
 * Where the visual add-ons finish a page, these are the parts a visitor can
 * touch: generative canvases, pointer physics, 3D, type experiments and
 * reveal mechanics. Every demo is a single self-contained HTML file.
 */
import type { VisualAddon } from './visualAddons';

const D = (id: string) => `/interactive/${id}.html`;

export const interactiveCategories: {
  id: VisualAddon['category'];
  label: string;
  emoji: string;
  color: string;
  blurb: string;
}[] = [
  { id: 'generative', label: 'Generative Art', emoji: '🌀', color: '#ff8a5c', blurb: 'Algorithms that draw something new every time.' },
  { id: 'pointer', label: 'Pointer & Physics', emoji: '🧲', color: '#7fb2ff', blurb: 'The cursor as a force: attract, drag, fling.' },
  { id: 'spatial', label: '3D & Depth', emoji: '🧊', color: '#c084fc', blurb: 'Objects and scenes with real perspective.' },
  { id: 'typefx', label: 'Type & Image', emoji: '🔤', color: '#3ddc84', blurb: 'Particles, glyphs, dither and distortion.' },
  { id: 'play', label: 'Play & Reveal', emoji: '🎛️', color: '#ffd166', blurb: 'Sound, celebration, comparison and lightbox.' },
];

export const interactiveAddons: VisualAddon[] = [
  {
    n: 1,
    id: 'voronoi-mosaic',
    name: 'Voronoi Mosaic',
    category: 'generative',
    group: 'interactive',
    tagline: 'Cells that grow, split and heal around your pointer.',
    what: 'Around 40 seed points tessellated every frame by clipping a bounding box against the perpendicular bisector of every other seed. Drag a seed and its whole neighbourhood redraws.',
    why: 'Voronoi is the geometry of proximity — territories that belong to their nearest point. Because the map is derived, not drawn, every drag produces a different but always-valid composition.',
    surface: ['Hero', 'Campaign microsite', 'Studio homepage'],
    intensity: 'bold',
    worksWith: ['dark-tech', 'immersive-3d', 'expressive', 'cultural', 'contemporary'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
let pts = Array.from({length: 40}, () => [Math.random()*innerWidth, Math.random()*innerHeight]);
const clip = (poly, ax, ay, nx, ny) => {
  const out = [];
  for (let i = 0; i < poly.length; i++) {
    const p = poly[i], q = poly[(i+1) % poly.length];
    const dp = (p[0]-ax)*nx + (p[1]-ay)*ny;
    const dq = (q[0]-ax)*nx + (q[1]-ay)*ny;
    if (dp <= 0) out.push(p);
    if (dp * dq < 0) {
      const t = dp / (dp - dq);
      out.push([p[0] + (q[0]-p[0])*t, p[1] + (q[1]-p[1])*t]);
    }
  }
  return out;
};
function cell(s) {
  let poly = [[0,0],[innerWidth,0],[innerWidth,innerHeight],[0,innerHeight]];
  for (const o of pts) {
    if (o === s) continue;
    poly = clip(poly, (s[0]+o[0])/2, (s[1]+o[1])/2, o[0]-s[0], o[1]-s[1]);
    if (poly.length < 3) return [];
  }
  return poly;
}
function draw() {
  x.clearRect(0, 0, innerWidth, innerHeight);
  for (const s of pts) {
    const p = cell(s); if (!p.length) continue;
    x.beginPath(); p.forEach((q, i) => i ? x.lineTo(q[0], q[1]) : x.moveTo(q[0], q[1]));
    x.closePath();
    x.fillStyle = 'hsl(' + ((s[0]/innerWidth)*80 + 190) + ' 60% 24%)';
    x.fill(); x.strokeStyle = '#07080c'; x.stroke();
  }
  requestAnimationFrame(draw);
}
addEventListener('pointermove', e => { pts[0] = [e.clientX, e.clientY]; });
draw();
</script>`,
    prompt: 'Build a full-screen Voronoi mosaic on canvas: ~40 seeds, and every frame rebuild each cell by starting with the viewport rectangle and clipping it against the perpendicular bisector of every other seed. Fill cells by hue derived from position, stroke the seams in the page background colour, and let the pointer drag the nearest seed. Keep it under 60 cells so the O(n²) clipping stays smooth, and cap devicePixelRatio at 2.',
    demo: D('voronoi-mosaic'),
  },
  {
    n: 2,
    id: 'flow-field',
    name: 'Particle Flow Field',
    category: 'generative',
    group: 'interactive',
    tagline: 'A thousand particles steered by a field you can stir.',
    what: '1,200 particles read an angle from summed sine waves at their position, move one step along it, and draw a line from their previous point. A translucent fill each frame turns motion into long ink trails.',
    why: 'Flow fields produce complexity no designer could place by hand, yet the rules fit in ten lines. The pointer adds a radial force, so the piece becomes a toy rather than a screensaver.',
    surface: ['Hero background', 'Album / launch page', 'Interactive about page'],
    intensity: 'medium',
    worksWith: ['dark-tech', 'expressive', 'immersive-3d', 'cultural'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
const pts = Array.from({length: 1200}, () => ({x: Math.random()*innerWidth, y: Math.random()*innerHeight, px: 0, py: 0}));
const m = {x: -1e4, y: -1e4}; let t = 0;
addEventListener('pointermove', e => { m.x = e.clientX; m.y = e.clientY; });
function frame() {
  t += 0.008;
  x.fillStyle = 'rgba(5,6,10,.06)'; x.fillRect(0, 0, innerWidth, innerHeight);
  for (const p of pts) {
    p.px = p.x; p.py = p.y;
    const a = Math.sin(p.x*.0016 + t) + Math.cos(p.y*.0014 - t);
    p.x += Math.cos(a*1.7) * 1.1; p.y += Math.sin(a*1.7) * 1.1;
    const dx = p.x-m.x, dy = p.y-m.y, d = Math.hypot(dx,dy);
    if (d < 160 && d > 1) { p.x += dx/d*(160-d)*.04; p.y += dy/d*(160-d)*.04; }
    if (p.x < 0 || p.x > innerWidth || p.y < 0 || p.y > innerHeight) {
      p.x = Math.random()*innerWidth; p.y = Math.random()*innerHeight; p.px = p.x; p.py = p.y;
    }
    x.strokeStyle = 'hsla(205,75%,62%,.3)';
    x.beginPath(); x.moveTo(p.px, p.py); x.lineTo(p.x, p.y); x.stroke();
  }
  requestAnimationFrame(frame);
}
frame();
</script>`,
    prompt: 'Create a flow-field hero: 1,000–1,500 particles, each steered by an angle built from 2–3 sine/cosine terms of its own x/y, advanced a pixel or two per frame and stroked from the previous position. Fade the canvas with a low-alpha background fill instead of clearing, so trails accumulate. Add a pointer repulsion within ~160px. Respawn particles at the edges so the field never empties.',
    demo: D('flow-field'),
  },
  {
    n: 3,
    id: 'generative-poster',
    name: 'Generative Poster Studio',
    category: 'generative',
    group: 'interactive',
    tagline: 'A print studio in a canvas — generated, not templated.',
    what: 'A seeded random generator picks one of four layout systems, applies a fixed palette, sets real headline typography and exports a 900×1200 PNG. The same seed always reproduces the same poster.',
    why: 'Seeded randomness is repeatable, so a visitor can generate until something resonates and still share the exact result. It also gives a brand a way to produce endless campaign variants without a designer in the loop.',
    surface: ['Campaign page', 'Studio / portfolio', 'Event microsite'],
    intensity: 'bold',
    worksWith: ['cultural', 'expressive', 'luxe-brand', 'contemporary', 'classic'],
    snippet: `<canvas id="c" width="900" height="1200"></canvas>
<button id="gen">Generate</button>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
const mulberry = s => () => {
  s |= 0; s = s + 0x6D2B79F5 | 0;
  let t = Math.imul(s ^ s >>> 15, 1 | s);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
  return ((t ^ t >>> 14) >>> 0) / 4294967296;
};
function poster(seed) {
  const r = mulberry(seed);
  x.fillStyle = '#f4f0e6'; x.fillRect(0, 0, 900, 1200);
  x.fillStyle = '#14120f';
  const cols = 4 + Math.floor(r()*3), rows = 6 + Math.floor(r()*3);
  for (let i = 0; i < cols*rows; i++) {
    if (r() < .55) continue;
    const w = 900/cols, h = 620/rows;
    x.fillStyle = r() > .78 ? '#ff5a1f' : '#14120f';
    x.fillRect((i%cols)*w + 8, 80 + Math.floor(i/cols)*h + 8, w-16, h-16);
  }
  x.fillStyle = '#14120f';
  x.font = '800 128px system-ui'; x.fillText('FORM', 60, 900);
  x.font = '500 20px ui-monospace'; x.fillText('EDITION ' + String(seed).padStart(3,'0') + ' / 250', 62, 1080);
}
document.getElementById('gen').onclick = () => poster(Math.floor(Math.random()*999));
poster(7);
</script>`,
    prompt: 'Build a generative poster tool on a 900×1200 canvas. Use a seeded PRNG (mulberry32) so a seed reproduces the exact poster. Offer 3–4 layout systems (concentric rings, modular grid, overlapping discs, rotated bars), a fixed 4-colour palette, real headline typography and an edition number. Add Generate and Download PNG buttons. Keep the safe margins consistent and the type aligned to a baseline grid.',
    demo: D('generative-poster'),
  },
  {
    n: 4,
    id: 'waveform-grid',
    name: 'Waveform Grid',
    category: 'generative',
    group: 'interactive',
    tagline: 'A field of lines that bends around your hand.',
    what: '48 horizontal lines are sampled every 8px and displaced by two travelling sine waves. A Gaussian falloff around the pointer adds a local ripple, and lines near the cursor brighten.',
    why: 'It gives a page a sense of material — like a surface being disturbed — while staying legible behind text. The interaction is legible immediately, with no instructions needed.',
    surface: ['Hero', 'Section divider', 'Data / sound brand'],
    intensity: 'subtle',
    worksWith: ['dark-tech', 'data-pro', 'contemporary', 'immersive-3d'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
let m = {x: -1e4, y: -1e4}, t = 0;
addEventListener('pointermove', e => { m = {x: e.clientX, y: e.clientY}; });
function frame() {
  t += .012;
  x.fillStyle = '#06070b'; x.fillRect(0, 0, innerWidth, innerHeight);
  const gap = innerHeight / 49;
  for (let l = 0; l < 48; l++) {
    const y0 = gap * (l + 1);
    const near = Math.max(0, 1 - Math.abs(y0 - m.y) / 260);
    x.beginPath();
    for (let px = 0; px <= innerWidth; px += 8) {
      const w = Math.sin(px*.014 + t + l*.22)*46 + Math.sin(px*.0066 - t*.7)*22;
      const pull = Math.exp(-Math.pow((px - m.x)/160, 2)) * near * Math.sin(t*4 + px*.01) * 54;
      const y = y0 + w + pull;
      px ? x.lineTo(px, y) : x.moveTo(px, y);
    }
    x.strokeStyle = near > .15 ? 'rgba(127,178,255,.9)' : 'rgba(120,132,156,.28)';
    x.lineWidth = near > .15 ? 1.6 : 1; x.stroke();
  }
  requestAnimationFrame(frame);
}
frame();
</script>`,
    prompt: 'Draw a full-bleed waveform field: 40–60 horizontal lines sampled every 6–10px, each displaced by two sine waves of different frequency and speed. Add a Gaussian falloff around the pointer that injects a local ripple and brightens nearby lines. Keep the base stroke low-contrast so text can sit on top, and never clear fully — repaint the background each frame.',
    demo: D('waveform-grid'),
  },
  {
    n: 5,
    id: 'pixel-studio',
    name: 'Pixel Studio',
    category: 'generative',
    group: 'interactive',
    tagline: 'A 32×20 canvas you can paint with one drag.',
    what: 'A CSS grid of 640 cells with pointer capture so a single drag paints continuously. Six palette colours plus an eraser, a random seed and a clear button; the painted-pixel count updates live.',
    why: 'Constraint is the point: a tiny grid makes anyone an artist in ten seconds, and the output looks intentional at any scale. It is also a gentle way to let visitors leave a mark on a campaign page.',
    surface: ['Campaign / event page', 'Playful 404', 'Studio easter egg'],
    intensity: 'medium',
    worksWith: ['expressive', 'cultural', 'component-kit', 'contemporary'],
    snippet: `<div id="grid" style="display:grid;grid-template-columns:repeat(32,1fr);width:640px;aspect-ratio:32/20"></div>
<script>
const g = document.getElementById('grid'), cols = 32, rows = 20;
let colour = '#ff5a1f', painting = false;
for (let i = 0; i < cols*rows; i++) {
  const d = document.createElement('div');
  d.style.cssText = 'background:transparent;border:1px solid #ffffff08';
  g.appendChild(d);
}
g.addEventListener('pointerdown', e => {
  painting = true; g.setPointerCapture(e.pointerId);
  if (e.target !== g) e.target.style.background = colour;
});
g.addEventListener('pointermove', e => {
  if (!painting) return;
  const el = document.elementFromPoint(e.clientX, e.clientY);
  if (el && el.parentElement === g) el.style.background = colour;
});
addEventListener('pointerup', () => painting = false);
</script>`,
    prompt: 'Make a pixel-art toy: a 32×20 CSS grid, 8×8px cells, pointer capture on pointerdown so one drag paints continuously, six brand colours plus an eraser and clear. Track the painted-cell count and show it in a monospace HUD. The grid should be responsive but keep square cells; use elementFromPoint during the drag to find the cell under the pointer.',
    demo: D('pixel-studio'),
  },
  {
    n: 6,
    id: 'fluid-trail',
    name: 'Fluid Trail',
    category: 'pointer',
    group: 'interactive',
    tagline: 'Ink that follows the speed of your hand.',
    what: 'Every pointermove pushes a point carrying velocity and a hue derived from speed. Points are stroked from their previous position with additive blending and fade over roughly a second, so fast gestures bloom and slow ones draw tight lines.',
    why: 'It converts an invisible input (cursor movement) into a visible material. Because the colour comes from velocity, the effect teaches its own interaction without a label.',
    surface: ['Hero', 'Launch / event page', 'Creative portfolio'],
    intensity: 'bold',
    worksWith: ['expressive', 'immersive-3d', 'dark-tech', 'cultural'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
let pts = [], last = {x: innerWidth/2, y: innerHeight/2};
addEventListener('pointermove', e => {
  const vx = e.clientX - last.x, vy = e.clientY - last.y;
  const speed = Math.min(24, Math.hypot(vx, vy));
  pts.push({x: e.clientX, y: e.clientY, vx, vy, life: 1, hue: (210 + speed*7) % 360});
  last = {x: e.clientX, y: e.clientY};
  if (pts.length > 500) pts.shift();
});
function frame() {
  x.fillStyle = 'rgba(5,6,10,.10)'; x.fillRect(0, 0, innerWidth, innerHeight);
  x.globalCompositeOperation = 'lighter';
  for (const p of pts) {
    p.life *= .94; p.x += p.vx*.06; p.y += p.vy*.06;
    if (p.life < .02) continue;
    x.strokeStyle = 'hsla(' + p.hue + ',85%,62%,' + p.life*.5 + ')';
    x.lineWidth = 1 + 10*p.life;
    x.beginPath(); x.moveTo(p.x, p.y); x.lineTo(p.x - p.vx*.5, p.y - p.vy*.5);
    x.stroke();
  }
  x.globalCompositeOperation = 'source-over';
  pts = pts.filter(p => p.life > .02);
  requestAnimationFrame(frame);
}
frame();
</script>`,
    prompt: 'Add a velocity-reactive ink trail to the hero: on each pointermove push a point with the delta as velocity and a hue mapped from speed; stroke from the previous position with lineWidth scaled by remaining life and globalCompositeOperation lighter. Fade with a low-alpha fill rather than clearing. Cap the point array at ~500 and hide the native cursor inside the canvas area.',
    demo: D('fluid-trail'),
  },
  {
    n: 7,
    id: 'magnetic-dots',
    name: 'Magnetic Dots',
    category: 'pointer',
    group: 'interactive',
    tagline: 'A grid that leans toward the cursor and springs back.',
    what: 'Every dot stores a home position and a displaced position. Within a radius, a force pulls it toward the pointer; outside, a spring returns it home with damping. Nearby dots also draw a line back to their anchor.',
    why: 'Spring return is what makes it feel physical rather than scripted. The grid gives the eye a reference so the deformation is obvious even at small amplitudes.',
    surface: ['Hero', 'Footer', 'Interactive brand page'],
    intensity: 'medium',
    worksWith: ['dark-tech', 'data-pro', 'component-kit', 'contemporary'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
let m = {x: -1e4, y: -1e4}, dots = [];
addEventListener('pointermove', e => { m = {x: e.clientX, y: e.clientY}; });
function build() {
  dots = [];
  for (let y = 22; y < innerHeight; y += 44)
    for (let px = 22; px < innerWidth; px += 44)
      dots.push({hx: px, hy: y, x: px, y: y, vx: 0, vy: 0});
}
build(); addEventListener('resize', build);
function frame() {
  x.fillStyle = '#07080c'; x.fillRect(0, 0, innerWidth, innerHeight);
  for (const d of dots) {
    const dx = m.x-d.x, dy = m.y-d.y, dist = Math.hypot(dx, dy);
    let tx = d.hx, ty = d.hy;
    if (dist < 190 && dist > 1) {
      const f = (1 - dist/190) * 30;
      tx = d.x + dx/dist*f; ty = d.y + dy/dist*f;
    }
    d.vx += (tx-d.x)*.14; d.vy += (ty-d.y)*.14;
    d.vx *= .86; d.vy *= .86; d.x += d.vx; d.y += d.vy;
    const hot = Math.max(0, 1 - Math.hypot(m.x-d.x, m.y-d.y)/150);
    x.fillStyle = hot > .05
      ? 'rgba(255,' + (138 + hot*80) + ',' + (92 + hot*60) + ',' + (.5 + hot*.5) + ')'
      : 'rgba(160,172,196,.32)';
    x.beginPath(); x.arc(d.x, d.y, 1.4 + hot*1.8, 0, 7); x.fill();
  }
  requestAnimationFrame(frame);
}
frame();
</script>`,
    prompt: 'Build a magnetic dot grid: dots on a 44px pitch, each with a home position, velocity and spring return. Within ~190px of the pointer apply a radial force; always pull back toward home with damping (vx += (home-x)*0.14, vx *= 0.86). Draw anchor lines for the most displaced dots and brighten dots near the cursor. Rebuild on resize.',
    demo: D('magnetic-dots'),
  },
  {
    n: 8,
    id: 'gravity-sandbox',
    name: 'Gravity Sandbox',
    category: 'pointer',
    group: 'interactive',
    tagline: 'Fling balls. Change gravity mid-flight.',
    what: 'Balls integrate velocity with a gravity slider, bounce off the four walls with an energy multiplier, and leave short motion trails. Dragging and releasing on empty space spawns a ball whose velocity is your gesture.',
    why: 'Direct manipulation plus a live physical parameter is instantly understandable. It also demonstrates a real skill: making motion feel weighted, not linear.',
    surface: ['Playful landing page', 'Physics / dev tool', 'Event microsite'],
    intensity: 'medium',
    worksWith: ['expressive', 'dark-tech', 'component-kit', 'data-pro'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
const balls = Array.from({length: 16}, () => ({
  x: Math.random()*innerWidth, y: Math.random()*innerHeight*.5,
  r: 6 + Math.random()*16, vx: (Math.random()-.5)*6, vy: 0,
  h: ['#ff5a1f','#ffd166','#3ddc84','#7fb2ff'][0|Math.random()*4]
}));
let gravity = .6, bounce = .72;
function frame() {
  x.fillStyle = 'rgba(6,7,11,.22)'; x.fillRect(0, 0, innerWidth, innerHeight);
  for (const b of balls) {
    b.vy += gravity; b.x += b.vx; b.y += b.vy;
    if (b.x < b.r) { b.x = b.r; b.vx = Math.abs(b.vx)*bounce; }
    if (b.x > innerWidth-b.r) { b.x = innerWidth-b.r; b.vx = -Math.abs(b.vx)*bounce; }
    if (b.y > innerHeight-b.r) { b.y = innerHeight-b.r; b.vy = -Math.abs(b.vy)*bounce; }
    x.fillStyle = b.h; x.beginPath(); x.arc(b.x, b.y, b.r, 0, 7); x.fill();
  }
  requestAnimationFrame(frame);
}
frame();
</script>`,
    prompt: 'Build a gravity sandbox: 12–20 balls with position, velocity, radius and colour; integrate gravity, bounce off all four walls with a restitution multiplier, and leave short trails with a low-alpha repaint. Add sliders for gravity and bounce, a button to add eight balls, and drag-to-fling spawning on empty space. Clamp velocity so nothing tunnels through a wall.',
    demo: D('gravity-sandbox'),
  },
  {
    n: 9,
    id: 'liquid-blob',
    name: 'Liquid Blob',
    category: 'pointer',
    group: 'interactive',
    tagline: 'Three bodies that merge, split and chase the pointer.',
    what: 'Three divs with radial gradients follow the pointer with different offsets and easing, filtered through an SVG goo (blur + high-contrast alpha) so overlaps fuse into one liquid mass.',
    why: 'The goo filter is the whole trick: blur the group, crush the alpha, then blend the original on top. It costs no WebGL and works in every modern browser.',
    surface: ['Hero', 'CTA band', 'Product launch'],
    intensity: 'bold',
    worksWith: ['expressive', 'luxe-brand', 'immersive-3d', 'contemporary'],
    snippet: `<div id="stage" style="filter:url(#goo)">
  <div class="b"></div><div class="b"></div><div class="b"></div>
</div>
<svg width="0" height="0"><defs><filter id="goo">
  <feGaussianBlur in="SourceGraphic" stdDeviation="18" result="b"/>
  <feColorMatrix in="b" mode="matrix"
    values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 24 -10" result="g"/>
  <feBlend in="SourceGraphic" in2="g"/>
</filter></defs></svg>
<style>
.b{position:absolute;width:180px;height:180px;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#ffb08a,#ff5a1f 60%,#8a2a00);mix-blend-mode:screen}
</style>
<script>
const blobs = [...document.querySelectorAll('.b')].map((el, i) => ({el, x: innerWidth/2, y: innerHeight/2, i}));
const m = {x: innerWidth/2, y: innerHeight/2};
addEventListener('pointermove', e => { m.x = e.clientX; m.y = e.clientY; });
function frame(t) {
  blobs.forEach((b, i) => {
    const tx = m.x + Math.cos(t*.0007 + i*2.1)*80;
    const ty = m.y + Math.sin(t*.0009 + i*1.3)*60;
    b.x += (tx-b.x)*.05; b.y += (ty-b.y)*.05;
    b.el.style.transform = 'translate(' + (b.x-90) + 'px,' + (b.y-90) + 'px)';
  });
  requestAnimationFrame(frame);
}
frame();
</script>`,
    prompt: 'Create a gooey pointer follower: 3–4 absolutely positioned gradient circles inside a container with filter:url(#goo), where the filter is feGaussianBlur stdDeviation 18 + feColorMatrix alpha 24 -10 + feBlend. Each blob eases toward the pointer with a different orbit offset, so they overlap and separate. Use mix-blend-mode:screen and keep the group pointer-events:none.',
    demo: D('liquid-blob'),
  },
  {
    n: 10,
    id: 'image-lens',
    name: 'Image Lens',
    category: 'pointer',
    group: 'interactive',
    tagline: 'A magnifier that makes a still image feel inspectable.',
    what: 'A circular canvas follows the pointer and draws a zoomed crop of an offscreen scene (or an uploaded image), with crosshairs and a live magnification readout.',
    why: 'The lens gives people a reason to move across an image instead of scrolling past it — the classic detail-reveal mechanic for product and editorial photography.',
    surface: ['Product page', 'Editorial feature', 'Campaign imagery'],
    intensity: 'subtle',
    worksWith: ['luxe-brand', 'classic', 'cultural', 'contemporary'],
    snippet: `<canvas id="scene"></canvas>
<div id="lens" style="position:fixed;width:220px;height:220px;border-radius:50%;
  overflow:hidden;pointer-events:none;transform:translate(-50%,-50%)">
  <canvas id="zoom" width="440" height="440"></canvas>
</div>
<script>
const scene = document.getElementById('scene'), sctx = scene.getContext('2d');
const lens = document.getElementById('lens'), zctx = document.getElementById('zoom').getContext('2d');
const img = new Image(); img.src = '/your-image.jpg';
let zoom = 2.4, size = 220;
img.onload = () => sctx.drawImage(img, 0, 0, innerWidth, innerHeight);
addEventListener('pointermove', e => {
  lens.style.left = e.clientX + 'px'; lens.style.top = e.clientY + 'px';
  const sw = size/zoom, sh = size/zoom;
  zctx.drawImage(img,
    e.clientX/innerWidth*img.width - sw/2, e.clientY/innerHeight*img.height - sh/2,
    sw, sh, 0, 0, 440, 440);
});
</script>`,
    prompt: 'Add an image magnifier: a fixed circular div containing a 2× canvas that follows the pointer, drawing a cropped region of the source image scaled to fill. Zoom and lens size are sliders. Hide the native cursor over the image area, add a thin ring and crosshairs, and ignore pointer events on the lens. Make sure the crop maths uses the displayed image dimensions, not the natural ones.',
    demo: D('image-lens'),
  },
  {
    n: 11,
    id: 'carousel-3d',
    name: '3D Carousel',
    category: 'spatial',
    group: 'interactive',
    tagline: 'A ring of cards you can throw with your hand.',
    what: 'Eight absolutely positioned cards on a CSS 3D ring (rotateY(i×45°) translateZ(430px)). Dragging changes the ring angle, release adds inertia, and arrows snap one card at a time.',
    why: 'It gives a set of equal items — planets, projects, products — physical order. The perspective supplies depth cues that a flat slider cannot.',
    surface: ['Portfolio', 'Product collection', 'Editorial series'],
    intensity: 'bold',
    worksWith: ['immersive-3d', 'luxe-brand', 'expressive', 'contemporary'],
    snippet: `<div class="stage" style="perspective:1300px">
  <div id="ring" style="position:relative;width:260px;height:360px;
    transform-style:preserve-3d;transition:transform .1s linear"></div>
</div>
<script>
const ring = document.getElementById('ring'), n = 8, step = 360/n;
for (let i = 0; i < n; i++) {
  const c = document.createElement('div');
  c.style.cssText = 'position:absolute;inset:0;border-radius:16px;background:#151a28;' +
    'border:1px solid #ffffff26;transform:rotateY(' + (i*step) + 'deg) translateZ(430px)';
  c.textContent = '0' + (i+1);
  ring.appendChild(c);
}
let angle = 0, target = 0, down = false, sx = 0, sa = 0;
addEventListener('pointerdown', e => { down = true; sx = e.clientX; sa = target; });
addEventListener('pointermove', e => { if (down) target = sa + (e.clientX-sx)*.32; });
addEventListener('pointerup', () => down = false);
(function loop() {
  angle += (target-angle)*.09;
  ring.style.transform = 'rotateY(' + angle + 'deg)';
  requestAnimationFrame(loop);
})();
</script>`,
    prompt: 'Build a draggable 3D card ring: 8 cards positioned with rotateY(i * 45deg) translateZ(430px) inside a preserve-3d container with perspective ~1300px. Pointer drag changes the ring angle, release adds inertia, and prev/next buttons snap by one step. Keep the active card index in a HUD. Disable text selection while dragging and make the whole thing work with touch.',
    demo: D('carousel-3d'),
  },
  {
    n: 12,
    id: 'dot-globe',
    name: 'Dot Globe',
    category: 'spatial',
    group: 'interactive',
    tagline: 'A planet made of points, spun by your finger.',
    what: '2,200 points distributed on a sphere via the golden-angle spiral, rotated by yaw/pitch, projected orthographically and shaded by depth. Drag spins it with inertia.',
    why: 'Dots make a globe read as data rather than decoration, and the projection keeps it light enough to run in a hero without WebGL.',
    surface: ['Global / network brand', 'Hero', 'Contact page'],
    intensity: 'medium',
    worksWith: ['dark-tech', 'data-pro', 'immersive-3d', 'contemporary'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
const pts = [], N = 2200, ga = Math.PI*(3-Math.sqrt(5));
for (let i = 0; i < N; i++) {
  const y = 1 - i/(N-1)*2, r = Math.sqrt(1-y*y), th = ga*i;
  pts.push({x: Math.cos(th)*r, y, z: Math.sin(th)*r});
}
let yaw = .4, pitch = -.15, drag = false, lx = 0, ly = 0;
addEventListener('pointerdown', e => { drag = true; lx = e.clientX; ly = e.clientY; });
addEventListener('pointermove', e => {
  if (!drag) return;
  yaw += (e.clientX-lx)*.006; pitch += (e.clientY-ly)*.006;
  lx = e.clientX; ly = e.clientY;
});
addEventListener('pointerup', () => drag = false);
function frame() {
  x.fillStyle = 'rgba(4,5,10,.35)'; x.fillRect(0, 0, innerWidth, innerHeight);
  const cx = innerWidth/2, cy = innerHeight/2, R = Math.min(innerWidth, innerHeight)*.34;
  const cyw = Math.cos(yaw), syw = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
  for (const p of pts) {
    const rx = p.x*cyw - p.z*syw, rz = p.x*syw + p.z*cyw;
    const ry = p.y*cp - rz*sp, z = p.y*sp + rz*cp;
    if (z < -.15) continue;
    const d = (z+1)/2, s = .7 + d*1.9;
    x.fillStyle = 'rgba(' + (120+d*80) + ',' + (170+d*60) + ',255,' + (.06+Math.pow(d,3)*.85) + ')';
    x.fillRect(cx + rx*R - s/2, cy + ry*R - s/2, s, s);
  }
  requestAnimationFrame(frame);
}
frame();
</script>`,
    prompt: 'Build a dot-matrix globe: distribute ~2,200 points on a unit sphere with the golden-angle spiral, rotate by yaw/pitch from pointer drag, project orthographically, and skip points with z < -0.15. Size and alpha each point by depth, add a soft radial glow behind the sphere, and apply inertia on release. No three.js — plain 2D canvas.',
    demo: D('dot-globe'),
  },
  {
    n: 13,
    id: 'scroll-gallery',
    name: 'Scroll 3D Gallery',
    category: 'spatial',
    group: 'interactive',
    tagline: 'The page scroll becomes the carousel.',
    what: 'A sticky stage holds a 3D ring of seven panels; scroll progress maps to ring rotation with easing. Pointer drag adds a manual offset, and a progress bar tracks the page.',
    why: 'Scroll is the one gesture every visitor already performs. Binding it to spatial movement makes a long page feel like a single continuous object.',
    surface: ['Case study', 'Lookbook', 'Product story'],
    intensity: 'bold',
    worksWith: ['immersive-3d', 'luxe-brand', 'cultural', 'expressive'],
    snippet: `<div style="height:360vh"><div style="position:sticky;top:0;height:100vh;
  display:grid;place-items:center;perspective:1400px">
  <div id="ring" style="position:relative;width:280px;height:380px;
    transform-style:preserve-3d"></div></div></div>
<script>
const ring = document.getElementById('ring'), n = 7, step = 360/n;
for (let i = 0; i < n; i++) {
  const c = document.createElement('div');
  c.style.cssText = 'position:absolute;inset:0;border-radius:14px;background:#151a28;' +
    'border:1px solid #ffffff26;transform:rotateY(' + (i*step) + 'deg) translateZ(460px)';
  ring.appendChild(c);
}
let offset = 0;
function frame() {
  const max = document.body.scrollHeight - innerHeight;
  const p = max > 0 ? scrollY/max : 0;
  offset += (p*(n-1)*step - offset)*.08;
  ring.style.transform = 'rotateY(' + offset + 'deg)';
  requestAnimationFrame(frame);
}
frame();
</script>`,
    prompt: 'Build a scroll-driven 3D gallery: a 360vh page with a sticky 100vh stage and a preserve-3d ring of 7 panels. Map scroll progress to rotateY from 0 to (n-1) * (360/n), eased toward the target each frame. Add a fixed top progress bar, a card counter, and a pointer-drag offset so users can also throw the ring. Respect prefers-reduced-motion by jumping instead of easing.',
    demo: D('scroll-gallery'),
  },
  {
    n: 14,
    id: 'voxel-terrain',
    name: 'Voxel Terrain',
    category: 'spatial',
    group: 'interactive',
    tagline: 'An isometric landscape you can push hills into.',
    what: 'A 16×16 heightmap rendered as isometric cubes with shaded top and side faces, painter-sorted back to front. Dragging raises the cells under the pointer; rotate and regenerate rebuild the silhouette.',
    why: 'Height plus light is enough for the eye to read terrain. Because the terrain is a grid, interacting with it feels like sculpting rather than drawing.',
    surface: ['Hero', 'Data / simulation brand', 'Playful product page'],
    intensity: 'medium',
    worksWith: ['immersive-3d', 'data-pro', 'dark-tech', 'expressive'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
const N = 16, grid = [];
for (let i = 0; i < N; i++) grid[i] = Array.from({length: N}, (_, j) =>
  .5 + Math.sin(i*.7)*.22 + Math.cos(j*.55)*.2);
function frame() {
  x.fillStyle = '#04060a'; x.fillRect(0, 0, innerWidth, innerHeight);
  const tw = Math.min(innerWidth/(N*1.7), 26), th = tw*.55;
  const ox = innerWidth/2, oy = innerHeight*.16;
  const cubes = [];
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++)
    cubes.push({i, j, h: grid[i][j], d: i+j});
  cubes.sort((a, b) => a.d - b.d);
  for (const {i, j, h} of cubes) {
    const px = ox + (i-j)*tw/2, py = oy + (i+j)*th/2 - h*40;
    const depth = h*24;
    x.fillStyle = 'rgba(20,60,52,.95)';
    x.beginPath(); x.moveTo(px, py); x.lineTo(px-tw*.43, py+th/2);
    x.lineTo(px-tw*.43, py+th/2+depth); x.lineTo(px, py+depth); x.fill();
    x.fillStyle = 'rgba(12,40,36,.95)';
    x.beginPath(); x.moveTo(px, py); x.lineTo(px+tw*.43, py+th/2);
    x.lineTo(px+tw*.43, py+th/2+depth); x.lineTo(px, py+depth); x.fill();
    x.fillStyle = 'rgb(' + (40+h*80) + ',' + (120+h*110) + ',' + (90+h*90) + ')';
    x.beginPath(); x.moveTo(px, py); x.lineTo(px+tw*.43, py+th/2);
    x.lineTo(px, py+th); x.lineTo(px-tw*.43, py+th/2); x.fill();
  }
  requestAnimationFrame(frame);
}
frame();
</script>`,
    prompt: 'Render an interactive voxel terrain: a 16×16 heightmap, isometric projection (x-y for horizontal, x+y for depth), cubes drawn as three shaded faces and painter-sorted by x+y. Convert pointer position back to grid coordinates and raise the 3×3 neighbourhood on drag. Add rotate-90° and regenerate buttons, and normalize heights so the silhouette stays inside the viewport.',
    demo: D('voxel-terrain'),
  },
  {
    n: 15,
    id: 'parallax-scene',
    name: 'Parallax Scene',
    category: 'spatial',
    group: 'interactive',
    tagline: 'A landscape with six planes of depth.',
    what: 'A CSS-built night scene split into sky, stars, moon, two mountain ranges, fog, trees and foreground. Each layer translates by its own depth factor and the whole world tilts a few degrees with the pointer.',
    why: 'Depth is communicated by differential movement, not by 3D models. It turns a flat hero into a place, at almost no payload.',
    surface: ['Hero', 'Campaign landing', 'Story opening'],
    intensity: 'medium',
    worksWith: ['immersive-3d', 'cultural', 'luxe-brand', 'expressive'],
    snippet: `<div id="scene" style="position:fixed;inset:0;overflow:hidden;perspective:1200px">
  <div id="world" style="position:absolute;inset:0;transform-style:preserve-3d">
    <div class="layer" data-z=".1"></div>
    <div class="layer" data-z=".3"></div>
    <div class="layer" data-z=".6"></div>
    <div class="layer" data-z="1"></div>
  </div>
</div>
<script>
const world = document.getElementById('world');
const layers = [...document.querySelectorAll('.layer')];
let tx = 0, ty = 0, cx = 0, cy = 0;
addEventListener('pointermove', e => {
  tx = e.clientX/innerWidth - .5;
  ty = e.clientY/innerHeight - .5;
});
(function frame() {
  cx += (tx-cx)*.06; cy += (ty-cy)*.06;
  world.style.transform = 'rotateX(' + (-cy*5) + 'deg) rotateY(' + (cx*7) + 'deg)';
  layers.forEach(l => {
    const z = +l.dataset.z;
    l.style.transform = 'translate3d(' + (cx*z*30) + 'px,' + (cy*z*22) + 'px,0)';
  });
  requestAnimationFrame(frame);
})();
</script>`,
    prompt: 'Build a layered parallax scene with pure CSS gradients and masks — sky, stars, moon, far mountains, fog, trees, foreground — inside a preserve-3d world. On pointermove tilt the world 4–7 degrees and translate each layer by its data-z factor (0.1 to 1.3). Ease toward the pointer, add a depth slider that scales all offsets, and keep every layer pointer-events:none.',
    demo: D('parallax-scene'),
  },
  {
    n: 16,
    id: 'text-particles',
    name: 'Text to Particles',
    category: 'typefx',
    group: 'interactive',
    tagline: 'Your headline, rebuilt out of 5,000 points.',
    what: 'The text is rendered offscreen at display size, scanned for opaque pixels, and each sample becomes a particle that eases to its target. The pointer repels nearby particles; Explode scatters them and they reassemble.',
    why: 'It makes typography physical. Because the text is re-sampled on every edit, the effect works for any word — including a visitor’s own.',
    surface: ['Hero', 'Event / launch page', 'Studio intro'],
    intensity: 'bold',
    worksWith: ['expressive', 'dark-tech', 'immersive-3d', 'cultural'],
    snippet: `<canvas id="c"></canvas>
<input id="txt" value="FORM">
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
let parts = [];
function sample(text) {
  const off = document.createElement('canvas');
  off.width = innerWidth; off.height = innerHeight;
  const o = off.getContext('2d'), size = Math.min(innerWidth/(text.length*.62), innerHeight*.42);
  o.fillStyle = '#fff'; o.textAlign = 'center'; o.textBaseline = 'middle';
  o.font = '900 ' + size + 'px system-ui'; o.fillText(text, innerWidth/2, innerHeight/2);
  const data = o.getImageData(0, 0, off.width, off.height).data;
  parts = [];
  for (let y = 0; y < innerHeight; y += 4)
    for (let px = 0; px < innerWidth; px += 4)
      if (data[(y*innerWidth+px)*4+3] > 128) parts.push({x: px, y, tx: px, ty: y, vx: 0, vy: 0});
}
sample('FORM');
document.getElementById('txt').oninput = e => sample(e.target.value.toUpperCase() || 'FORM');
(function frame() {
  x.fillStyle = 'rgba(5,6,10,.2)'; x.fillRect(0, 0, innerWidth, innerHeight);
  x.globalCompositeOperation = 'lighter';
  for (const p of parts) {
    p.vx += (p.tx-p.x)*.028; p.vy += (p.ty-p.y)*.028;
    p.vx *= .9; p.vy *= .9; p.x += p.vx; p.y += p.vy;
    x.fillStyle = 'rgba(127,178,255,.55)';
    x.fillRect(p.x, p.y, 1.6, 1.6);
  }
  x.globalCompositeOperation = 'source-over';
  requestAnimationFrame(frame);
})();
</script>`,
    prompt: 'Turn a headline into particles: render the text to an offscreen canvas at ~40% of the viewport height, scan every 4th pixel, and create particles at every opaque sample. Ease each particle toward its target with damping; on pointermove repel particles within ~90px. Re-sample on input so visitors can type their own word. Add an Explode button that applies random velocities, and fade the frame instead of clearing.',
    demo: D('text-particles'),
  },
  {
    n: 17,
    id: 'kinetic-type',
    name: 'Kinetic Type Lab',
    category: 'typefx',
    group: 'interactive',
    tagline: 'Letters that bend toward your hand.',
    what: 'Each letter is its own span. A sine wave moves it vertically while pointer proximity adds rotation, scale and lift. Wave amplitude, speed and tracking are live sliders; clicking cycles the word.',
    why: 'It proves typography can respond without leaving the typeface. Per-letter transforms are cheap, accessible (the text is still real text) and easy to art-direct.',
    surface: ['Hero', 'Section opener', 'Event identity'],
    intensity: 'medium',
    worksWith: ['expressive', 'cultural', 'contemporary', 'luxe-brand'],
    snippet: `<div id="word" style="display:flex;font:900 15vw/.8 system-ui;justify-content:center"></div>
<script>
const word = document.getElementById('word');
let letters = [...'MOTION'].map(ch => {
  const s = document.createElement('span');
  s.textContent = ch; s.style.display = 'inline-block';
  word.appendChild(s); return s;
});
let m = {x: -1e4, y: -1e4}, t = 0;
addEventListener('pointermove', e => m = {x: e.clientX, y: e.clientY});
(function frame() {
  t += .016;
  letters.forEach((el, i) => {
    const r = el.getBoundingClientRect();
    const l = r.left + r.width/2, top = r.top + r.height/2;
    const near = Math.max(0, 1 - Math.hypot(m.x-l, m.y-top)/360);
    const wave = Math.sin(t*8 + i*.55)*26;
    el.style.transform = 'translateY(' + (wave + near*12) + 'px)'
      + ' rotate(' + ((m.x > l ? -1 : 1)*near*near*26) + 'deg)'
      + ' scale(' + (1 + near*.18) + ')';
  });
  requestAnimationFrame(frame);
})();
</script>`,
    prompt: 'Build a kinetic type hero: split the word into per-letter spans (keep them as real text for screen readers), then each frame apply translateY from a travelling sine, plus rotation and scale proportional to pointer proximity. Add sliders for wave amplitude, speed and letter spacing, and cycle through 4–5 words on click. Use clamp() for type size and disable transforms under prefers-reduced-motion.',
    demo: D('kinetic-type'),
  },
  {
    n: 18,
    id: 'dither-lab',
    name: 'Dither Lab',
    category: 'typefx',
    group: 'interactive',
    tagline: 'One-bit image processing, live.',
    what: 'The scene (or an uploaded image) is downsampled to a block grid, compared against an 8×8 Bayer matrix with a threshold the pointer shifts, and redrawn in two colours at full size.',
    why: 'Dithering is the visual signature of early print and low-bit screens. Applied to a modern photograph it reads as deliberate, and it compresses beautifully because the output is genuinely two-tone.',
    surface: ['Editorial imagery', 'Campaign artwork', 'Music / zine'],
    intensity: 'bold',
    worksWith: ['cultural', 'expressive', 'dark-tech', 'classic'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
const BAYER = [[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],
  [12,44,4,36,14,46,6,38],[60,28,52,20,62,30,54,22],
  [3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],
  [15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]];
function dither(img, block, threshold) {
  const cols = Math.round(innerWidth/block), rows = Math.round(innerHeight/block);
  const off = document.createElement('canvas');
  off.width = cols; off.height = rows;
  off.getContext('2d').drawImage(img, 0, 0, cols, rows);
  const data = off.getContext('2d').getImageData(0, 0, cols, rows).data;
  c.width = cols; c.height = rows;
  c.style.width = innerWidth + 'px'; c.style.height = innerHeight + 'px';
  const out = x.createImageData(cols, rows);
  for (let i = 0; i < cols*rows; i++) {
    const lum = (data[i*4]*.299 + data[i*4+1]*.587 + data[i*4+2]*.114)/255;
    const bias = (BAYER[(i/cols|0)%8][i%cols%8]/64 - .5)*.5;
    const on = lum + bias > threshold;
    const v = on ? 255 : 0;
    out.data[i*4] = v; out.data[i*4+1] = on ? 90 : 8;
    out.data[i*4+2] = on ? 40 : 14; out.data[i*4+3] = 255;
  }
  x.putImageData(out, 0, 0);
}
</script>`,
    prompt: 'Build a Bayer-dither lab: downsample the source image to a coarse grid (block size 2–16px), read luminance, compare against an 8×8 ordered Bayer matrix with a threshold the pointer shifts horizontally, and write two-tone pixels back at full size with image-rendering:pixelated. Offer a 2-colour palette, invert, and image upload. Recompute on a rAF throttle, not on every pointer event.',
    demo: D('dither-lab'),
  },
  {
    n: 19,
    id: 'glitch-slicer',
    name: 'Glitch Slicer',
    category: 'typefx',
    group: 'interactive',
    tagline: 'The image tears where your cursor passes.',
    what: 'The source is drawn in horizontal bands; each band gets a noise offset plus a proximity boost near the pointer, with red and cyan overlays. Bands re-randomise continuously.',
    why: 'Glitch reads as signal failure, which is exactly the metaphor for a launch, a hack, or a live feed. Band-slicing gets the look without a shader.',
    surface: ['Launch page', 'Music release', 'Tech editorial'],
    intensity: 'bold',
    worksWith: ['dark-tech', 'expressive', 'cultural', 'immersive-3d'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
const img = new Image(); img.src = '/your-image.jpg';
let m = {y: -1e4}, t = 0;
addEventListener('pointermove', e => m.y = e.clientY);
(function frame() {
  t += .016;
  const slices = 18, sh = innerHeight/slices;
  x.clearRect(0, 0, innerWidth, innerHeight);
  for (let i = 0; i < slices; i++) {
    const y = i*sh;
    const near = Math.max(0, 1 - Math.abs(y - m.y)/(innerHeight*.28));
    const noise = Math.sin(i*12.9898 + t*3)*43758.5453 % 1;
    const shift = (noise*55 + near*120)*Math.sin(t*2 + i);
    x.drawImage(img, 0, y/innerHeight*img.height, img.width, img.height/slices,
      shift, y, innerWidth, sh + 1);
    if (near > .25) {
      x.fillStyle = 'rgba(255,60,80,' + near*.16 + ')';
      x.fillRect(0, y, innerWidth, sh);
    }
  }
  requestAnimationFrame(frame);
})();
</script>`,
    prompt: 'Apply a horizontal glitch slicer to an image: draw it in 12–24 bands, offset each band horizontally by a continuous noise term plus a boost when near the pointer, and overlay red/cyan copies at low alpha. Re-randomise the noise every frame. Keep the base image sharp between glitches so the effect reads as a tear, and freeze it under prefers-reduced-motion.',
    demo: D('glitch-slicer'),
  },
  {
    n: 20,
    id: 'ascii-portrait',
    name: 'ASCII Portrait',
    category: 'typefx',
    group: 'interactive',
    tagline: 'A photograph redrawn as glyphs.',
    what: 'The image is sampled at cell resolution, each luminance is mapped to a character from a density ramp, and the glyph is drawn in the sampled colour at full size. Gamma and cell size are live; uploads are supported.',
    why: 'ASCII is instantly recognisable and unusually honest: every mark is a character, and the portrait still reads. It is also tiny when the source is small.',
    surface: ['Editorial feature', 'Developer brand', 'Album artwork'],
    intensity: 'bold',
    worksWith: ['dark-tech', 'cultural', 'expressive', 'data-pro'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
const RAMP = ' .:-=+*#%@';
function ascii(img, cell) {
  const cols = Math.floor(innerWidth/cell), rows = Math.floor(innerHeight/cell);
  const off = document.createElement('canvas');
  off.width = cols; off.height = rows;
  off.getContext('2d').drawImage(img, 0, 0, cols, rows);
  const d = off.getContext('2d').getImageData(0, 0, cols, rows).data;
  x.fillStyle = '#06070b'; x.fillRect(0, 0, innerWidth, innerHeight);
  x.font = Math.round(cell*1.15) + 'px ui-monospace,monospace';
  x.textAlign = 'center'; x.textBaseline = 'middle';
  for (let y = 0; y < rows; y++) for (let px = 0; px < cols; px++) {
    const i = (y*cols + px)*4;
    const lum = (d[i]*.299 + d[i+1]*.587 + d[i+2]*.114)/255;
    const ch = RAMP[Math.min(RAMP.length-1, Math.floor(lum*RAMP.length))];
    if (ch === ' ') continue;
    x.fillStyle = 'rgba(' + d[i] + ',' + d[i+1] + ',' + d[i+2] + ',.9)';
    x.fillText(ch, px*cell + cell/2, y*cell + cell/2);
  }
}
</script>`,
    prompt: 'Render an image as ASCII art on canvas: downsample to a grid matching the monospace cell size, read luminance, map it through the ramp " .:-=+*#%@", and draw each character in the sampled colour. Add sliders for cell size (5–16px) and gamma, a colour/mono toggle, and image upload. Redraw on a rAF throttle and skip space characters entirely.',
    demo: D('ascii-portrait'),
  },
  {
    n: 21,
    id: 'audio-visualizer',
    name: 'Audio Visualizer',
    category: 'play',
    group: 'interactive',
    tagline: 'A radial spectrum that hears the room.',
    what: 'A WebAudio oscillator feeds an AnalyserNode; 128 bars read the frequency data on a logarithmic index curve and radiate from a ring, with hue mapped to amplitude. Idle mode animates a synthetic wave.',
    why: 'Sound plus a reactive shape is one of the strongest engagement loops on the web. It also works as a brand toy — a tone generator with a face.',
    surface: ['Music / podcast site', 'Launch teaser', 'Event page'],
    intensity: 'medium',
    worksWith: ['expressive', 'dark-tech', 'immersive-3d', 'cultural'],
    snippet: `<canvas id="c"></canvas>
<button id="play">Play tone</button>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
let audio, osc, analyser, data, playing = false;
function start() {
  if (!audio) {
    audio = new AudioContext();
    osc = audio.createOscillator(); analyser = audio.createAnalyser();
    analyser.fftSize = 2048; data = new Uint8Array(analyser.frequencyBinCount);
    const g = audio.createGain(); g.gain.value = .03;
    osc.frequency.value = 220; osc.connect(g); g.connect(analyser);
    analyser.connect(audio.destination); osc.start();
  }
  audio.resume(); playing = !playing;
}
document.getElementById('play').onclick = start;
(function frame() {
  x.fillStyle = 'rgba(4,5,10,.35)'; x.fillRect(0, 0, innerWidth, innerHeight);
  const cx = innerWidth/2, cy = innerHeight/2, R = Math.min(innerWidth, innerHeight)*.19;
  if (analyser && playing) analyser.getByteFrequencyData(data);
  for (let i = 0; i < 128; i++) {
    const v = playing && data ? data[Math.floor(Math.pow(i/128, 1.7)*data.length*.7)]/255 : .1;
    const a = i/128*Math.PI*2, len = 12 + v*Math.min(innerWidth, innerHeight)*.28;
    x.strokeStyle = 'hsla(' + (200+v*120) + ',90%,62%,' + (.25+v*.7) + ')';
    x.lineWidth = 2.2;
    x.beginPath();
    x.moveTo(cx + Math.cos(a)*R, cy + Math.sin(a)*R);
    x.lineTo(cx + Math.cos(a)*(R+len), cy + Math.sin(a)*(R+len));
    x.stroke();
  }
  requestAnimationFrame(frame);
})();
</script>`,
    prompt: 'Build a radial audio visualizer: a user-gesture Play button creates an AudioContext, oscillator and AnalyserNode (fftSize 2048), then 128 bars read frequency bins on a logarithmic curve and radiate from a ring, hue mapped to amplitude. Show an idle synthetic wave when paused. Add frequency, gain and waveform controls. Never autoplay audio before a click.',
    demo: D('audio-visualizer'),
  },
  {
    n: 22,
    id: 'before-after',
    name: 'Before / After Slider',
    category: 'play',
    group: 'interactive',
    tagline: 'One drag to prove the difference.',
    what: 'Two full-bleed versions of the same composition, warm and cool, with the top layer clipped by inset(0 0 0 X%). A transparent range input spans the frame, so drag, touch and arrow keys all work.',
    why: 'Comparison is the most persuasive interaction in a portfolio: the viewer controls the reveal, so the improvement is self-evident rather than claimed.',
    surface: ['Case study', 'Photo / retouch', 'Product upgrade'],
    intensity: 'subtle',
    worksWith: ['classic', 'luxe-brand', 'cultural', 'contemporary'],
    snippet: `<div id="frame" style="position:relative;overflow:hidden">
  <div class="before">…before…</div>
  <div class="after" id="after" style="clip-path:inset(0 0 0 50%)">…after…</div>
  <input id="range" type="range" min="0" max="100" value="50"
    style="position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:ew-resize">
</div>
<script>
const range = document.getElementById('range'), after = document.getElementById('after');
range.addEventListener('input', () => {
  after.style.clipPath = 'inset(0 0 0 ' + range.value + '%)';
  document.getElementById('line').style.left = range.value + '%';
});
</script>`,
    prompt: 'Build a before/after comparison: two absolutely stacked versions of the same composition with identical framing, the top one clipped by inset(0 0 0 N%). A full-area transparent range input drives the clip so mouse, touch and arrow keys all work. Add a 2px divider with a round handle, BEFORE/AFTER labels, and a live percentage. Keep both images the same intrinsic size so alignment never drifts.',
    demo: D('before-after'),
  },
  {
    n: 23,
    id: 'kaleidoscope',
    name: 'Kaleidoscope Painter',
    category: 'play',
    group: 'interactive',
    tagline: 'Every stroke becomes eight.',
    what: 'Pointer strokes are replayed under N rotations and a mirror flip around the canvas centre, drawn with additive blending and a slowly cycling hue. Mirrors and brush width are adjustable.',
    why: 'Symmetry makes even a scribble look composed. The interaction is one gesture, the output is immediately frameable, and the mirror count changes the whole character.',
    surface: ['Playful hero', 'Kids / family brand', 'Event wall'],
    intensity: 'bold',
    worksWith: ['expressive', 'cultural', 'contemporary', 'luxe-brand'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
let down = false, lx = 0, ly = 0, hue = 0, mirrors = 8;
addEventListener('pointerdown', e => { down = true; lx = e.clientX; ly = e.clientY; });
addEventListener('pointerup', () => down = false);
addEventListener('pointermove', e => {
  if (!down) return;
  const cx = innerWidth/2, cy = innerHeight/2, seg = Math.PI*2/mirrors;
  x.globalCompositeOperation = 'lighter'; x.lineCap = 'round';
  for (let i = 0; i < mirrors; i++) for (const flip of [1, -1]) {
    x.save(); x.translate(cx, cy); x.rotate(i*seg); x.scale(flip, 1);
    x.strokeStyle = 'hsla(' + ((hue + i*14) % 360) + ',90%,64%,.5)';
    x.lineWidth = 9;
    x.beginPath(); x.moveTo(lx-cx, ly-cy); x.lineTo(e.clientX-cx, e.clientY-cy); x.stroke();
    x.restore();
  }
  x.globalCompositeOperation = 'source-over';
  lx = e.clientX; ly = e.clientY; hue = (hue + 1.4) % 360;
});
</script>`,
    prompt: 'Build a kaleidoscope painter: on every pointermove draw the segment from the previous point under N rotations (3–16) and a horizontal mirror, all around the canvas centre, with additive blending and a hue that advances per event. Expose mirror count and brush width, add Clear, and keep the drawing full-bleed and touch-friendly. No fade — the artwork should accumulate.',
    demo: D('kaleidoscope'),
  },
  {
    n: 24,
    id: 'confetti-physics',
    name: 'Confetti Physics',
    category: 'play',
    group: 'interactive',
    tagline: 'Click, and the page celebrates.',
    what: 'Rectangular pieces spawn with radial velocity, then fall under gravity with air drag, flutter and 3D spin (scaleY by rotation). Gravity and wind are live sliders; a rain button seeds from the top edge.',
    why: 'It is the cheapest way to make a success state feel earned. Because each piece is a rectangle with its own rotation, it reads as paper rather than particles.',
    surface: ['Checkout success', 'Signup confirmation', 'Launch moment'],
    intensity: 'bold',
    worksWith: ['expressive', 'component-kit', 'cultural', 'contemporary'],
    snippet: `<canvas id="c"></canvas>
<script>
const c = document.getElementById('c'), x = c.getContext('2d');
const bits = [];
const colours = ['#ff5a1f','#ffd166','#3ddc84','#7fb2ff','#c084fc','#f4f0e6'];
function burst(px, py, n) {
  for (let i = 0; i < n; i++) {
    const a = Math.random()*Math.PI*2, s = Math.random()*9;
    bits.push({x: px, y: py, vx: Math.cos(a)*s, vy: Math.sin(a)*s - 4,
      w: 5 + Math.random()*7, h: 8 + Math.random()*10,
      rot: Math.random()*6, vr: (Math.random()-.5)*.3,
      c: colours[0|Math.random()*colours.length]});
  }
}
addEventListener('pointerdown', e => burst(e.clientX, e.clientY, 90));
function frame() {
  x.fillStyle = 'rgba(6,7,11,.2)'; x.fillRect(0, 0, innerWidth, innerHeight);
  for (let i = bits.length-1; i >= 0; i--) {
    const b = bits[i];
    b.vy += .45; b.vx += .01; b.vx *= .995; b.vy *= .995;
    b.x += b.vx; b.y += b.vy; b.rot += b.vr;
    if (b.y > innerHeight + 40) { bits.splice(i, 1); continue; }
    x.save(); x.translate(b.x, b.y); x.rotate(b.rot);
    x.scale(1, Math.cos(b.rot*1.6)*.7 + .3);
    x.fillStyle = b.c; x.fillRect(-b.w/2, -b.h/2, b.w, b.h); x.restore();
  }
  requestAnimationFrame(frame);
}
frame();
</script>`,
    prompt: 'Add a confetti burst on success: 80–120 rectangular pieces spawned at the click or button centre with radial velocity, then integrated with gravity, drag and a flutter term. Give each piece independent rotation and squash on one axis so it reads as paper. Include gravity and wind sliders, a rain-from-top mode, a clear button, and a hard cap of ~900 pieces. Skip it under prefers-reduced-motion and announce success in an aria-live region.',
    demo: D('confetti-physics'),
  },
  {
    n: 25,
    id: 'lightbox-gallery',
    name: 'Lightbox Gallery',
    category: 'play',
    group: 'interactive',
    tagline: 'A gallery that opens without leaving the page.',
    what: 'A full-bleed 3×3 grid of works. Clicking one opens a dialog with the artwork, title and index; arrows move, Esc closes, backdrop click closes, and focus returns to the tile that opened it.',
    why: 'It keeps a portfolio on one page while giving each piece room to breathe. The keyboard and focus handling are what separate a real lightbox from a div overlay.',
    surface: ['Portfolio', 'Lookbook', 'Gallery / archive'],
    intensity: 'subtle',
    worksWith: ['classic', 'luxe-brand', 'cultural', 'contemporary'],
    snippet: `<div id="grid">…nine buttons…</div>
<div id="lb" role="dialog" aria-modal="true" style="display:none">
  <button id="close" aria-label="Close">✕</button>
  <button id="prev" aria-label="Previous">←</button>
  <button id="next" aria-label="Next">→</button>
  <div id="art"></div><h2 id="title"></h2>
</div>
<script>
let items = [{name: 'Salt Flats', art: 'linear-gradient(…)'}, {name: 'Night Swim', art: '…'}], idx = 0, lastTile = null;
function paint() { art.style.background = items[idx].art; title.textContent = items[idx].name; }
function open(i, tile) { idx = i; lastTile = tile; paint(); lb.style.display = 'grid'; close.focus(); }
function closeLB() { lb.style.display = 'none'; lastTile && lastTile.focus(); }
function step(d) { idx = (idx + d + items.length) % items.length; paint(); }
document.addEventListener('keydown', e => {
  if (lb.style.display === 'none') return;
  if (e.key === 'Escape') closeLB();
  if (e.key === 'ArrowRight') step(1);
  if (e.key === 'ArrowLeft') step(-1);
});
</script>`,
    prompt: 'Build an accessible lightbox gallery: a responsive grid of tiles, each a real button with an accessible name. Opening sets a dialog (aria-modal, labelled by the title), moves focus to the close button, locks body scroll and remembers the triggering tile. Support prev/next buttons, ← → keys, Esc and backdrop click, and return focus on close. Preload the adjacent works so navigation feels instant.',
    demo: D('lightbox-gallery'),
  },
];

export const addonsByInteractiveCategory = (cat: VisualAddon['category'] | 'all') =>
  cat === 'all' ? interactiveAddons : interactiveAddons.filter(a => a.category === cat);
