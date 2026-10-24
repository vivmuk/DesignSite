#!/usr/bin/env python3
"""Generate 50 interactive playgrounds + animated GIF thumbnails.

Every demo is a single self-contained HTML file in public/interactive/, built
from one of 15 small canvas engines. The GIF in public/interactive/thumbs/ is a
stylised illustration of the same engine so cards read as motion before the
live demo is opened.
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "interactive"
THUMBS = OUT / "thumbs"
TS_FILE = ROOT / "src" / "data" / "interactiveAddonsExtra.ts"

# --------------------------------------------------------------------------
# Demos: id, name, mode, category, palette, tagline, what, why, surface,
# intensity, worksWith, extra HUD noun
# --------------------------------------------------------------------------
DEMOS = [
    # generative
    ("voronoi-repel", "Voronoi Repulsion Field", "voronoi", "generative", "ember",
     "Cells re-tessellate as your cursor pushes the seeds apart.",
     "180 seeds jitter every frame and flee the pointer within 150px. Each cell is clipped from the viewport by every other seed's bisector, then filled by its own area on a log scale.",
     "Proximity becomes territory: the map is derived from points, so every drag produces a different but always valid composition.",
     ["Hero", "Data-art background", "Studio homepage"], "bold", ["dark-tech", "expressive", "immersive-3d"]),
    ("silk-flow-field", "Silk Flow Field", "flow", "generative", "ice",
     "Nine hundred particles combed by a slow sine field.",
     "Particles read a smooth pseudo-noise vector field, leave a translucent trail, and wrap at the edges. The pointer bends the field around itself.",
     "A flow field turns a random walk into visible structure — the cheapest way to make a page look alive without a library.",
     ["Hero", "Section divider", "Case-study cover"], "medium", ["dark-tech", "contemporary", "luxe-brand"]),
    ("harmonograph-ribbons", "Harmonograph Ribbons", "spiral", "generative", "aurora",
     "Two damped pendulums drawing a single endless ribbon.",
     "A Lissajous curve from four oscillators, stroked with a colour ramp and a slow phase drift so the figure never repeats exactly.",
     "The harmonograph is the original generative art machine — simple maths, an unmistakably analogue result.",
     ["Hero", "Album artwork", "Event poster"], "bold", ["cultural", "expressive", "luxe-brand"]),
    ("contour-drift", "Contour Drift", "terrain", "generative", "mono",
     "Topographic lines that breathe like a slow tide.",
     "Eight contour polylines sampled from summed sines scroll across the canvas; the pointer presses a soft dent into the field.",
     "Contour lines read as landscape at any scale, so one loop covers everything from a hero to a chart backdrop.",
     ["Hero", "Map panel", "Annual report cover"], "subtle", ["data-pro", "dark-tech", "classic"]),
    ("interference-weave", "Interference Weave", "waves", "generative", "acid",
     "Three wave sources pulling a lattice into moiré.",
     "A 44×26 point grid is displaced by radial sine waves from two orbiting sources plus the pointer, then drawn as horizontal and vertical threads.",
     "Interference patterns make complexity from almost no code and stay legible behind text because the density is uniform.",
     ["Hero", "Product backdrop", "Launch page"], "medium", ["dark-tech", "contemporary", "expressive"]),
    ("bloom-metaballs", "Bloom Metaballs", "blobs", "generative", "sunset",
     "Soft blobs that merge, split and follow the cursor.",
     "Twelve radial gradients composite with 'lighter' so overlapping fields read as one surface; the pointer is a thirteenth blob.",
     "Metaballs feel organic because additive light already behaves like wet ink — no mesh, no physics solver.",
     ["Loader", "Hero accent", "Audio companion"], "bold", ["immersive-3d", "expressive", "cultural"]),
    ("orbital-dust", "Orbital Dust", "orbit", "generative", "ice",
     "Two hundred particles orbiting a shared centre of mass.",
     "Each particle carries an angle, radius and direction; radius breathes on a sine, and the pointer pulls the whole cloud off centre.",
     "Orbits are the most readable form of perpetual motion: everything is related, nothing is synchronised.",
     ["Hero", "AI product page", "Splash screen"], "medium", ["dark-tech", "immersive-3d", "contemporary"]),
    ("mirrored-wedges", "Mirrored Wedges", "kaleido", "generative", "candy",
     "One drawn wedge, mirrored into a turning mandala.",
     "Shapes are drawn once inside a wedge, then repeated with rotate and scale(-1,1) across six segments. The pointer shifts the seed angle.",
     "Kaleidoscope symmetry multiplies a tiny drawing into a full composition while keeping the file small.",
     ["Cultural campaign", "Poster", "Hero"], "bold", ["cultural", "expressive", "luxe-brand"]),
    ("crystal-growth", "Crystal Growth", "voronoi", "generative", "aurora",
     "A slow tessellation that looks like frost forming.",
     "Fewer seeds than the repulsion field, drifting very slowly, with cells shaded by area and a bright edge where neighbours meet.",
     "Voronoi at low density reads as material, not diagram — frost, cracked glaze, stained glass.",
     ["Product surface", "Editorial figure", "Background"], "subtle", ["luxe-brand", "cultural", "classic"]),
    ("ember-drift", "Ember Drift", "flow", "generative", "ember",
     "Warm particles rising and curling in a night draft.",
     "Particles advect upward through a curl-ish sine field, cool from white to deep orange as they age, and respawn at the bottom.",
     "Directional flow plus a heat ramp is enough to imply fire without a single sprite.",
     ["Late-night hero", "Music release", "Event page"], "medium", ["dark-tech", "expressive", "cultural"]),
    ("seismograph-grid", "Seismograph Grid", "waves", "generative", "mono",
     "A lattice that records every tremor of the pointer.",
     "Point displacement is the sum of a slow ambient wave and an impulse that decays from the last pointer move.",
     "Recording motion, rather than animating decoration, makes the pointer feel like an instrument.",
     ["Data product", "Instrument UI", "Hero"], "subtle", ["data-pro", "dark-tech", "classic"]),
    ("cell-division", "Cell Division", "blobs", "generative", "acid",
     "Blobs that split when the pointer presses them.",
     "Each blob stores a radius and a target; proximity to the pointer pushes the target up, and a split spawns two smaller children.",
     "Emergent population behaviour from two rules — the demo keeps producing configurations you did not author.",
     ["Biotech hero", "Research site", "Loader"], "bold", ["dark-tech", "contemporary", "immersive-3d"]),
    ("star-nursery", "Star Nursery", "orbit", "generative", "aurora",
     "A dense core with a halo of escaping stars.",
     "Orbital particles gain a small radial velocity each pass, so the cloud slowly evaporates while new particles seed the centre.",
     "Growth and loss in one loop gives a composition that never settles — useful when the page must not look frozen.",
     ["AI hero", "Space product", "Splash"], "medium", ["dark-tech", "immersive-3d", "expressive"]),
    ("topographic-scan", "Topographic Scan", "terrain", "generative", "ice",
     "A terrain section redrawn like a scanning instrument.",
     "Contour bands are filled, not just stroked, and a bright scan line sweeps left to right, lighting the band it crosses.",
     "A scan line gives static geometry a sense of measurement and time.",
     ["Dashboard hero", "Hardware page", "Report cover"], "medium", ["data-pro", "dark-tech", "contemporary"]),
    ("marbled-paper", "Marbled Paper", "flow", "generative", "sunset",
     "Suminagashi ink that curls around your hand.",
     "Dense particles advect through a slow field and leave heavy trails, so the canvas fills like marbled paper instead of a particle stream.",
     "Fluid-looking texture without a fluid solver — just a field, a trail and a palette.",
     ["Editorial cover", "Luxe brand", "Invitation"], "medium", ["luxe-brand", "cultural", "classic"]),

    # pointer & physics
    ("magnetic-ink", "Magnetic Ink", "grid", "pointer", "mono",
     "A dot field that pulls toward the cursor like iron filings.",
     "A lattice of dots offsets toward the pointer with inverse-distance falloff; each dot's stretch and colour encode the force.",
     "The pointer becomes a physical field instead of a hover state — the whole surface responds, not one button.",
     ["Hero", "Contact page", "Portfolio"], "medium", ["dark-tech", "expressive", "contemporary"]),
    ("gravity-wells", "Gravity Wells", "orbit", "pointer", "ember",
     "Particles fall into the cursor and swing back out.",
     "Each particle integrates a softened inverse-square pull toward the pointer, with a velocity clamp and a trail buffer.",
     "A gravity well is the most direct way to make a cursor feel heavy.",
     ["Interactive hero", "Game landing", "Music visual"], "bold", ["immersive-3d", "dark-tech", "expressive"]),
    ("elastic-cursor", "Elastic Cursor", "grid", "pointer", "ice",
     "A grid that stretches around the pointer and snaps back.",
     "Dots keep a home position and a spring-damper offset; the pointer pushes, the spring returns, and line segments connect neighbours.",
     "Elasticity reads as material quality — the page feels made of something rather than painted.",
     ["Product page", "Hero", "Feature panel"], "medium", ["contemporary", "luxe-brand", "dark-tech"]),
    ("particle-fountain", "Particle Fountain", "particles", "pointer", "acid",
     "A fountain you can push, drag and choke.",
     "A pooled emitter spawns particles with random spread, gravity and drag; pointer movement adds lateral force and holding down increases pressure.",
     "A single emitter plus forces is a complete toy — no sprites, no assets, immediate feedback.",
     ["Playful hero", "Event page", "404"], "bold", ["expressive", "cultural", "contemporary"]),
    ("comet-trails", "Comet Trails", "particles", "pointer", "ice",
     "Comets that follow the cursor's history.",
     "The pointer writes into a short position buffer; particles launch along the recent path with a little scatter and leave streaks.",
     "Using the pointer's history instead of its position makes gestures feel authored rather than twitchy.",
     ["Interactive hero", "Music visual", "Portfolio"], "medium", ["dark-tech", "expressive", "immersive-3d"]),
    ("repulsion-dots", "Repulsion Dots", "grid", "pointer", "candy",
     "Dots scatter from the cursor and reassemble.",
     "A dot lattice is pushed by inverse-square repulsion inside a 170px radius; dots ease home when the pointer leaves.",
     "Repulsion is the cleanest proof that an interface is listening.",
     ["Hero", "Nav backdrop", "Form background"], "subtle", ["contemporary", "dark-tech", "expressive"]),
    ("vortex-chamber", "Vortex Chamber", "flow", "pointer", "aurora",
     "A flow field with you at the centre of the storm.",
     "Particles follow a field whose angle is rotated by proximity to the pointer, producing a vortex that follows the hand.",
     "One added term to the field creates a completely different behaviour from the same particle engine.",
     ["AI hero", "Music visual", "Landing"], "bold", ["dark-tech", "immersive-3d", "expressive"]),
    ("ripple-pond", "Ripple Pond", "rings", "pointer", "ice",
     "Every move drops a ring into still water.",
     "Rings spawn on pointer movement with a velocity cap, expand at a fixed rate and fade; overlapping strokes read as interference.",
     "Ripples turn navigation into a surface with memory.",
     ["Hero", "Sound page", "Meditation app"], "subtle", ["cultural", "luxe-brand", "contemporary"]),
    ("drag-constellation", "Drag Constellation", "grid", "pointer", "mono",
     "Drag stars and the network rewires itself.",
     "Points are draggable; edges connect every pair under a distance threshold, and the pointer acts as a temporary node.",
     "A proximity graph makes the structure of a drag legible — you see what moved and what it affected.",
     ["Network product", "Data hero", "About page"], "medium", ["data-pro", "dark-tech", "contemporary"]),
    ("slingshot-orbit", "Slingshot Orbit", "orbit", "pointer", "ember",
     "Fling particles around the cursor and watch them escape.",
     "Orbital particles receive an impulse when the pointer moves fast nearby, then integrate a softened gravity with a trail.",
     "Fling mechanics are satisfying because the input has momentum — the pointer is a hand, not a hotspot.",
     ["Game landing", "Playful hero", "Music visual"], "bold", ["expressive", "immersive-3d", "dark-tech"]),
    ("pressure-field", "Pressure Field", "waves", "pointer", "acid",
     "Press and the lattice bows away from you.",
     "Holding the pointer grows a pressure radius that displaces the grid; release and the displacement decays with an elastic overshoot.",
     "A visible pressure model makes a click feel like contact instead of a state change.",
     ["Hero", "Hardware page", "Interactive chart"], "medium", ["dark-tech", "contemporary", "data-pro"]),
    ("magnetic-filings", "Magnetic Filings", "flow", "pointer", "mono",
     "Filings that align to the cursor's field lines.",
     "Short line segments sample the local field angle and rotate toward the pointer's tangent; brightness tracks alignment.",
     "A field of aligned strokes reads as metal shavings, not particles — a different texture from the same maths.",
     ["Industrial brand", "Hero", "Poster"], "medium", ["classic", "dark-tech", "luxe-brand"]),

    # 3D & depth
    ("isometric-city", "Isometric City", "voxel", "spatial", "ice",
     "A block city where the cursor raises the skyline.",
     "A 14×14 height map is drawn as isometric columns sorted back to front; pointer proximity lifts nearby columns with a smooth falloff.",
     "Isometric projection gives depth without a 3D engine, and height maps are trivial to animate.",
     ["Hero", "Game page", "Studio site"], "medium", ["contemporary", "dark-tech", "immersive-3d"]),
    ("voxel-dunes", "Voxel Dunes", "voxel", "spatial", "sunset",
     "Rolling dunes built from stacked cubes.",
     "Column heights come from summed sines; top faces are lit by height and side faces are shaded, so the surface reads as terrain.",
     "Lighting a voxel field by height is enough to imply material and sun direction.",
     ["Hero", "Travel page", "Album art"], "medium", ["expressive", "cultural", "contemporary"]),
    ("wireframe-torus", "Wireframe Torus", "orbit", "spatial", "aurora",
     "A torus of points, spinning in the cursor's grip.",
     "Points are placed on a torus, rotated on two axes and projected with a simple perspective divide; the pointer steers rotation speed.",
     "A point cloud is the smallest possible 3D renderer and still reads as a solid object in motion.",
     ["AI product", "Crypto hero", "Splash"], "bold", ["dark-tech", "immersive-3d", "contemporary"]),
    ("parallax-starfield", "Parallax Starfield", "starfield", "spatial", "ice",
     "Fly through stars that steer with the pointer.",
     "Stars carry x, y and z; z decreases each frame, points project by 1/z and draw a streak from the previous projection.",
     "Parallax is the cheapest depth cue there is, and it makes a flat canvas feel like a window.",
     ["Hero", "Space product", "Launch"], "medium", ["dark-tech", "immersive-3d", "expressive"]),
    ("cube-stack", "Cube Stack", "voxel", "spatial", "candy",
     "A tower of cubes that leans toward the pointer.",
     "A grid of isometric cubes is offset by a height-dependent sway, so the stack appears to bend toward the cursor.",
     "Asymmetric sway turns a rigid grid into something that looks physically soft.",
     ["Playful product", "Toy brand", "Hero"], "bold", ["expressive", "cultural", "contemporary"]),
    ("tunnel-vision", "Tunnel Vision", "rings", "spatial", "aurora",
     "Concentric frames rushing past the centre.",
     "Rings are spaced on a z axis and projected outward with 1/z; pointer position shifts the vanishing point.",
     "A tunnel is pure camera motion — no objects, just the frame rate of space itself.",
     ["Game page", "Music visual", "Event site"], "bold", ["immersive-3d", "dark-tech", "expressive"]),
    ("floating-glyph-cubes", "Floating Glyph Cubes", "voxel", "spatial", "mono",
     "Letter blocks floating in isometric space.",
     "Each cube carries a character on its top face and bobs on a per-column phase; the pointer lifts a neighbourhood.",
     "Type on a 3D surface is a memorable way to make an identity feel dimensional.",
     ["Studio homepage", "Type foundry", "Campaign"], "medium", ["expressive", "cultural", "luxe-brand"]),
    ("terrain-flyover", "Terrain Flyover", "terrain", "spatial", "ice",
     "A contour landscape scrolling under a fixed camera.",
     "Layered contour bands move at different speeds, producing parallax with no 3D transforms at all.",
     "Parallax from flat layers is robust, cheap and works on every device.",
     ["Hero", "Travel", "Report cover"], "subtle", ["classic", "data-pro", "contemporary"]),

    # type & image
    ("glyph-storm", "Glyph Storm", "type", "typefx", "acid",
     "A wall of letters that scatters from the cursor.",
     "A glyph grid keeps home positions and spring offsets; pointer proximity pushes characters out, and each character periodically scrambles.",
     "Type as particles turns a headline into a playground without losing the letterforms.",
     ["Hero", "Campaign", "404"], "bold", ["expressive", "dark-tech", "cultural"]),
    ("decode-rain", "Decode Rain", "matrix", "typefx", "mono",
     "Columns of glyphs falling and resolving.",
     "Columns carry a y position, speed and a short glyph history; characters near the pointer resolve to readable letters.",
     "The decode metaphor says 'computation' in one glance and is legible at any size.",
     ["AI hero", "Security product", "Splash"], "medium", ["dark-tech", "data-pro", "contemporary"]),
    ("ascii-current", "ASCII Current", "matrix", "typefx", "ice",
     "A photographic gradient rebuilt as moving ASCII.",
     "A character grid samples a moving sine field; density maps to luminance, and the pointer brightens nearby cells.",
     "ASCII is a texture made of type — it scales from a favicon to a full-bleed hero.",
     ["Editorial", "Dev tool", "Terminal brand"], "medium", ["classic", "dark-tech", "data-pro"]),
    ("letter-magnet", "Letter Magnet", "type", "typefx", "sunset",
     "Letters that cling to the cursor and spring back.",
     "Each glyph has a home, a velocity and a magnet target; pointer proximity pulls them, releasing snaps them home with overshoot.",
     "Physical type is memorable in navigation and works as a section transition.",
     ["Nav", "Hero", "Menu"], "bold", ["expressive", "cultural", "contemporary"]),
    ("halftone-breathe", "Halftone Breathe", "grid", "typefx", "mono",
     "A dot screen that inhales under the cursor.",
     "Dot radius is sampled from a radial falloff plus a slow sine, producing a halftone gradient that moves.",
     "Halftone is print language; animating it makes a digital surface feel pressed.",
     ["Editorial hero", "Print brand", "Poster"], "subtle", ["classic", "cultural", "luxe-brand"]),
    ("text-vortex", "Text Vortex", "type", "typefx", "aurora",
     "Words spiralling into a point.",
     "Each word is placed on a spiral with an angular speed that grows toward the centre; pointer position changes the twist.",
     "Type in motion can carry hierarchy: near words read first, far words become texture.",
     ["Manifesto", "Campaign", "Event"], "bold", ["expressive", "dark-tech", "cultural"]),
    ("pixel-sort-live", "Pixel Sort, Live", "matrix", "typefx", "candy",
     "Colour bands stretched into glitch columns.",
     "Columns are sorted by hue every few frames; pointer movement sets the threshold, so the sort sweeps through the field.",
     "Glitch is a texture with attitude, and sorting is a one-line operation with infinite variety.",
     ["Music release", "Fashion", "Editorial"], "bold", ["expressive", "dark-tech", "cultural"]),
    ("word-constellation", "Word Constellation", "type", "typefx", "ice",
     "A sentence connected into a constellation.",
     "Words sit at fixed anchors; lines connect neighbouring words, and the pointer drags the nearest word, stretching the graph.",
     "A constellation makes relationships visible without a chart.",
     ["About page", "Data essay", "Hero"], "medium", ["data-pro", "classic", "contemporary"]),

    # play & reveal
    ("confetti-cannon", "Confetti Cannon", "particles", "play", "candy",
     "A success state that actually celebrates.",
     "Rectangles launch from the pointer or a corner with rotation and drag; gravity and a fade cull the pool.",
     "The end of a flow deserves a physical release — confetti is the cheapest emotional payoff.",
     ["Success state", "Checkout", "Onboarding"], "bold", ["expressive", "cultural", "contemporary"]),
    ("sparkler-trail", "Sparkler Trail", "particles", "play", "sunset",
     "A trail of sparks that burns out behind the pointer.",
     "Emissions are proportional to pointer speed; sparks inherit a little velocity, cool through the palette and fade.",
     "Speed-sensitive emission makes a cursor feel like a physical object.",
     ["Playful hero", "Event", "Music"], "medium", ["expressive", "dark-tech", "cultural"]),
    ("applause-meter", "Applause Meter", "bars", "play", "acid",
     "A crowd's noise drawn as a rising waveform.",
     "Bars are driven by a simulated crowd envelope with random claps; pointer movement adds energy and decays back.",
     "Showing an invisible quantity as a physical wave makes feedback feel immediate.",
     ["Live event", "Audio app", "Feedback"], "medium", ["dark-tech", "expressive", "contemporary"]),
    ("countdown-burst", "Countdown Burst", "rings", "play", "ember",
     "A countdown that ends in a shockwave.",
     "Rings spawn from the centre on each beat, expand and fade; the pointer can drop extra rings anywhere.",
     "Rings are a clock you can feel — perfect for launches and timers.",
     ["Launch", "Sale", "Game"], "bold", ["expressive", "immersive-3d", "dark-tech"]),
    ("scratch-to-reveal", "Scratch to Reveal", "grid", "play", "sunset",
     "Scratch a surface away to uncover the image behind it.",
     "A foil mask is erased around the pointer with a soft brush, revealing the artwork underneath.",
     "Reveal mechanics create participation — the visitor does the work and remembers the result.",
     ["Promo", "Announcement", "Gallery"], "bold", ["cultural", "expressive", "contemporary"]),
    ("slot-machine-glyphs", "Slot Machine Glyphs", "type", "play", "candy",
     "Three reels of characters that snap into a word.",
     "Each reel spins a glyph list at a different speed and eases to a stop; the pointer nudges the reels.",
     "Chance plus resolution is a tiny story — and it makes a static headline feel earned.",
     ["Hero", "Game", "Campaign"], "medium", ["expressive", "cultural", "dark-tech"]),
    ("aurora-curtain", "Aurora Curtain", "aurora", "play", "aurora",
     "A curtain of light that follows the pointer.",
     "Vertical ribbons advect through a slow field with additive colour and a vertical gradient; pointer proximity lifts the curtain.",
     "Additive light and soft edges are the whole vocabulary of an aurora — no 3D required.",
     ["Night hero", "Music", "Immersive page"], "bold", ["dark-tech", "immersive-3d", "expressive"]),
]

PALETTES = {
    "ember": ["#2a0b06", "#7a2214", "#ff6a2b", "#ffb15c", "#ffe6c2"],
    "ice": ["#050b16", "#0d2740", "#1f6fa8", "#7fc8f8", "#e6f7ff"],
    "aurora": ["#04120f", "#0b3b34", "#16a085", "#4dffd2", "#c8fff2"],
    "acid": ["#0d0f05", "#26350a", "#76b900", "#d4ff3f", "#f4ffd0"],
    "mono": ["#08080a", "#1c1d22", "#4a4d57", "#a9adba", "#f2f3f7"],
    "sunset": ["#1a0714", "#4a0f3a", "#c0266b", "#ff8a5c", "#ffe3b0"],
    "candy": ["#120a1c", "#3a1250", "#a12bb8", "#ff5c8a", "#ffd1e6"],
}

# --------------------------------------------------------------------------
# Canvas engines (plain JS, no libraries)
# --------------------------------------------------------------------------
from interactive_engines import ENGINES, VARIANTS

PARAMS = {
    "voronoi": {"N": {True: 190, False: 150}},
    "grid": {"STEP": {True: 30, False: 22}},
    "particles": {"SPEED": {True: 260, False: 140}, "GRAV": {True: 240, False: 120}},
    "type": {"STEP": {True: 34, False: 28}, "FONT": {True: "600 18px ui-monospace, monospace", False: "600 15px ui-monospace, monospace"}, "CHARS": {True: "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", False: "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"}},
    "matrix": {"FS": {True: 18, False: 15}},
    "voxel": {"GRID": {True: 14, False: 12}},
    "starfield": {"SPEED": {True: 320, False: 180}},
}

# --------------------------------------------------------------------------
# HTML writer
# --------------------------------------------------------------------------
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="__TAGLINE__">
<title>__NAME__ — Interactive</title>
<style>
*,*::before,*::after{box-sizing:border-box}
html,body{margin:0;min-height:100%;background:__BG__}
body{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;color:#eef1f7;overflow:hidden;-webkit-font-smoothing:antialiased}
canvas{display:block;position:fixed;inset:0;touch-action:none;cursor:crosshair}
.hud{position:fixed;top:16px;left:16px;z-index:5;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#939caf;backdrop-filter:blur(8px)}
.hud b{color:__ACCENT__;font-weight:600}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hint{position:fixed;left:16px;bottom:14px;margin:0;z-index:5;font:500 10px/1 ui-monospace,monospace;letter-spacing:.14em;color:#7e8799;text-transform:uppercase}
.pause{position:fixed;right:16px;bottom:12px;z-index:5;background:#0b0d13cc;border:1px solid #ffffff22;color:#cfd6e2;border-radius:999px;padding:8px 12px;font:600 10px/1 ui-monospace,monospace;letter-spacing:.1em;cursor:pointer}
.pause:focus-visible{outline:2px solid __ACCENT__;outline-offset:2px}
@media (prefers-reduced-motion:reduce){.hint{display:none}}
</style>
</head>
<body>
<canvas id="cv" aria-label="__NAME__ interactive canvas"></canvas>
<div class="hud"><span class="t">__KICKER__ · __NAME__</span><b id="stat">ready</b> · <b id="fps">60</b> fps</div>
<p class="hint">MOVE · DRAG · SPACE TO PAUSE</p>
<button class="pause" id="pause" type="button" aria-pressed="false">PAUSE</button>
<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
const P=__PALETTE__,TAU=Math.PI*2;
let W=0,H=0,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
fit();addEventListener('resize',fit);
const mx={x:-1e4,y:-1e4,down:false};
addEventListener('pointermove',e=>{mx.x=e.clientX;mx.y=e.clientY;},{passive:true});
addEventListener('pointerdown',e=>{mx.down=true;mx.x=e.clientX;mx.y=e.clientY;});
addEventListener('pointerup',()=>mx.down=false);
addEventListener('pointerleave',()=>{mx.x=-1e4;mx.y=-1e4;});
const rnd=(a=1,b=0)=>b+Math.random()*(a-b);
const statEl=document.getElementById('stat'),fpsEl=document.getElementById('fps');
let statText='ready';const stat=v=>{statText=v};
let t=0,paused=false,last=performance.now(),acc=0,frames=0;
const pauseBtn=document.getElementById('pause');
function setPaused(v){paused=v;pauseBtn.textContent=paused?'PLAY':'PAUSE';pauseBtn.setAttribute('aria-pressed',String(paused));}
pauseBtn.addEventListener('click',()=>setPaused(!paused));
addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();setPaused(!paused);}});
__ENGINE__
function loop(now){const dt=Math.min(.05,(now-last)/1000);last=now;
 if(!paused){t+=dt;frame(dt);}
 acc+=dt;frames++;if(acc>.5){statEl.textContent=statText;fpsEl.textContent=Math.round(frames/acc);frames=0;acc=0;}
 requestAnimationFrame(loop);}
if(matchMedia('(prefers-reduced-motion: reduce)').matches){frame(0);statEl.textContent=statText;setPaused(true);}
requestAnimationFrame(loop);
</script>
</body>
</html>
"""


def build_html(demo) -> str:
    did, name, mode, cat, pal, tagline, what, why, surface, intensity, works = demo
    params = PARAMS.get(mode, {})
    js = ENGINES[mode]
    bold = intensity == "bold"
    for key, variants in params.items():
        js = js.replace(f"__{key}__", str(variants[bold]))
    palette = PALETTES[pal]
    kicker = {"generative": "GENERATIVE", "pointer": "POINTER", "spatial": "3D / DEPTH",
              "typefx": "TYPE / IMAGE", "play": "PLAY / REVEAL"}[cat]
    return (HTML.replace("__ENGINE__", js).replace("__V__", VARIANTS.get(did, ""))
            .replace("__NAME__", name).replace("__TAGLINE__", tagline)
            .replace("__KICKER__", kicker).replace("__BG__", palette[0])
            .replace("__ACCENT__", palette[3])
            .replace("__PALETTE__", json.dumps(palette)))


# --------------------------------------------------------------------------
# GIF thumbnails
# --------------------------------------------------------------------------
THUMB_W, THUMB_H, FRAMES = 320, 200, 18


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def gif_frame(mode, pal, f, rng):
    W, H = THUMB_W, THUMB_H
    img = Image.new("RGB", (W, H), rgb(pal[0]))
    d = ImageDraw.Draw(img, "RGBA")
    t = f / FRAMES * math.tau * 1.8
    mid = (W // 2, H // 2)
    if mode == "voronoi" or mode == "crystal":
        seeds = [(rng.random() * W, rng.random() * H) for _ in range(34)]
        # nearest-seed cells
        gw, gh = 80, 50
        small = Image.new("RGB", (gw, gh))
        px = small.load()
        for yy in range(gh):
            for xx in range(gw):
                bx, by = xx / gw * W, yy / gh * H
                best, bi = 1e18, 0
                for i, s in enumerate(seeds):
                    dd = (bx - s[0]) ** 2 + (by - s[1]) ** 2
                    if dd < best:
                        best, bi = dd, i
                px[xx, yy] = rgb(pal[1 + (bi % (len(pal) - 1))])
        img = small.resize((W, H), Image.Resampling.NEAREST)
    elif mode == "flow":
        for i in range(280):
            x, y = rng.random() * W, rng.random() * H
            for k in range(3):
                a = math.sin(x * .03 + t) * 1.8 + math.cos(y * .024 - t * .7) * 1.4
                nx, ny = x + math.cos(a) * 7, y + math.sin(a) * 7
                d.line([(x, y), (nx, ny)], fill=rgb(pal[2 + i % 2]) + (140,), width=1)
                x, y = nx, ny
    elif mode == "waves":
        for yy in range(10, H, 14):
            pts = []
            for xx in range(0, W + 8, 8):
                w = math.sin(xx * .05 + t * 2) * 5 + math.sin(yy * .04 - t) * 4
                pts.append((xx, yy + w))
            d.line(pts, fill=rgb(pal[2]) + (120,), width=1)
        for xx in range(10, W, 14):
            pts = []
            for yy in range(0, H + 8, 8):
                w = math.cos(yy * .05 - t * 2) * 5
                pts.append((xx + w, yy))
            d.line(pts, fill=rgb(pal[3]) + (80,), width=1)
    elif mode == "blobs":
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for i in range(7):
            x = W / 2 + math.cos(t + i * 1.7) * (40 + i * 8)
            y = H / 2 + math.sin(t * .8 + i * 2.1) * (20 + i * 5)
            r = 34 + 10 * math.sin(t + i)
            ld.ellipse([x - r, y - r, x + r, y + r], fill=rgb(pal[2 + i % 2]) + (110,))
        layer = layer.filter(ImageFilter.GaussianBlur(14))
        img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
        d = ImageDraw.Draw(img, "RGBA")
    elif mode == "grid":
        for y in range(14, H, 16):
            for x in range(14, W, 16):
                dx, dy = x - W / 2 - math.cos(t) * 60, y - H / 2 - math.sin(t) * 30
                dd = max(1, math.hypot(dx, dy))
                k = max(0, 1 - dd / 150) ** 2 * 10
                px, py = x + dx / dd * k, y + dy / dd * k
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=rgb(pal[2 + (int(dd) % 2)]) + (200,))
    elif mode == "orbit":
        for i in range(120):
            a = t * (.4 + i % 3 * .12) + i
            r = 30 + (i * 7) % 90
            x = W / 2 + math.cos(a) * r
            y = H / 2 + math.sin(a) * r * .62
            d.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=rgb(pal[2 + i % 2]) + (200,))
            d.line([mid, (x, y)], fill=rgb(pal[2]) + (22,), width=1)
    elif mode == "particles":
        for i in range(150):
            life = (f / FRAMES + i * .13) % 1
            ang = i * 2.399 + t
            r = life * 110
            x = W / 2 + math.cos(ang) * r
            y = H - 10 - (1 - life) * 150 + math.sin(ang) * 20
            d.ellipse([x - 1.6, y - 1.6, x + 1.6, y + 1.6], fill=rgb(pal[1 + i % 3]) + (int(220 * (1 - life)),))
    elif mode == "type" or mode == "matrix":
        chars = "ABCDEFGHIJKLM0123456789#*+"
        step = 18 if mode == "type" else 14
        for yy in range(step, H, step):
            for xx in range(step, W, step):
                jitter = math.sin(t + xx * .03 + yy * .02) * 4
                col = pal[2 + (xx // step + yy // step) % 2]
                d.text((xx + jitter, yy), chars[(xx + yy + f) % len(chars)], fill=rgb(col) + (190,))
    elif mode == "voxel":
        size = 16
        for gy in range(7):
            for gx in range(10):
                bx = 70 + (gx - gy) * size
                by = 50 + (gx + gy) * size * .5
                h = 10 + (math.sin(gx * .6 + t) + math.cos(gy * .5 - t)) * 8
                top = [(bx, by - h - size * .5), (bx + size, by - h), (bx, by - h + size * .5), (bx - size, by - h)]
                d.polygon(top, fill=rgb(pal[3]))
                d.polygon([(bx - size, by - h), (bx, by - h + size * .5), (bx, by), (bx - size, by + size * .5)], fill=rgb(pal[1]))
                d.polygon([(bx + size, by - h), (bx, by - h + size * .5), (bx, by), (bx + size, by + size * .5)], fill=rgb(pal[2]))
    elif mode == "terrain":
        for l in range(7):
            y0 = 30 + l * 24
            pts = [(x, y0 + math.sin(x * .04 + t + l) * 8 + math.cos(x * .09 - t) * 4) for x in range(0, W + 8, 8)]
            d.line(pts, fill=rgb(pal[1 + l % 3]) + (170,), width=1 + (l % 2))
    elif mode == "rings":
        for i in range(6):
            r = ((f / FRAMES) * 180 + i * 30) % 210
            a = int(200 * (1 - r / 210))
            d.ellipse([mid[0] - r, mid[1] - r * .62, mid[0] + r, mid[1] + r * .62], outline=rgb(pal[2 + i % 2]) + (a,), width=2)
    elif mode == "spiral":
        pts = []
        for i in range(280):
            a = i / 280 * math.tau * 3 + t
            r = i / 280 * 110
            pts.append((W / 2 + math.cos(a) * r, H / 2 + math.sin(a * 1.02) * r * .7))
        d.line(pts, fill=rgb(pal[3]) + (200,), width=2)
    elif mode == "kaleido":
        for s in range(6):
            for i in range(4):
                a = t + s * math.tau / 6 + i
                x = W / 2 + math.cos(a) * (35 + i * 14)
                y = H / 2 + math.sin(a) * (20 + i * 8)
                d.ellipse([x - 12, y - 5, x + 12, y + 5], fill=rgb(pal[2 + i % 2]) + (170,))
    elif mode == "starfield":
        for i in range(90):
            a = i * 2.399
            z = (i * 7 + f * 6) % 100
            r = z / 100 * 150
            x, y = W / 2 + math.cos(a) * r, H / 2 + math.sin(a) * r
            d.line([(W / 2 + math.cos(a) * (r - 6), H / 2 + math.sin(a) * (r - 6)), (x, y)], fill=rgb(pal[3]) + (180,), width=1)
    else:
        d.ellipse([60, 40, W - 60, H - 40], outline=rgb(pal[3]), width=2)

    # a soft pointer light so every thumb reads as interactive
    px, py = W * (.5 + .3 * math.cos(t * .8)), H * (.5 + .28 * math.sin(t))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([px - 26, py - 26, px + 26, py + 26], fill=rgb(pal[4]) + (55,))
    glow = glow.filter(ImageFilter.GaussianBlur(12))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    return img


def write_gif(path: Path, mode: str, pal_name: str):
    pal = PALETTES[pal_name]
    rng = random.Random(hash(path.stem) & 0xffff)
    frames = [gif_frame(mode, pal, f, rng) for f in range(FRAMES)]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=85, loop=0,
                   optimize=True, disposal=2)


# --------------------------------------------------------------------------
# TypeScript entries
# --------------------------------------------------------------------------
SNIPPET = {
    "voronoi": "const voronoi = (S) => S.map(s => S.reduce((poly, o) => o === s ? poly :\n  clip(poly, (s.x + o.x) / 2, (s.y + o.y) / 2, o.x - s.x, o.y - s.y),\n  [[0, 0], [W, 0], [W, H], [0, H]]));",
    "flow": "p.x += Math.cos(field(p)) * 80 * dt;\np.y += Math.sin(field(p)) * 80 * dt;\nctx.strokeStyle = palette[1 + (p.h * 3 | 0)];\nctx.lineTo(p.x, p.y); ctx.stroke();",
    "orbit": "p.a += p.s * dt;\nconst x = cx + Math.cos(p.a) * p.r, y = cy + Math.sin(p.a) * p.r * .68;\nctx.fillStyle = palette[2 + (p.r / R | 0)];\nctx.fillRect(x, y, 2, 2);",
    "waves": "const w = Math.sin(d1 * .03 - t * 2) * 10 + Math.sin(dm * .05 - t * 3) * 14;\np.y = baseY + w;",
    "blobs": "ctx.globalCompositeOperation = 'lighter';\nconst g = ctx.createRadialGradient(x, y, 0, x, y, r);\ng.addColorStop(0, c + 'cc'); g.addColorStop(1, c + '00');\nctx.fillStyle = g; ctx.arc(x, y, r, 0, TAU); ctx.fill();",
    "grid": "const dx = mx.x - d.x, dy = mx.y - d.y, dist = Math.hypot(dx, dy) || 1;\nconst k = Math.max(0, 1 - dist / 190) ** 2 * 46;\nd.ox += (dx / dist * k - d.ox) * .2;\nd.oy += (dy / dist * k - d.oy) * .2;",
    "particles": "p.vy += gravity * dt; p.x += p.vx * dt; p.y += p.vy * dt;\np.life -= dt * .5;\nctx.globalAlpha = p.life; ctx.arc(p.x, p.y, p.r, 0, TAU); ctx.fill();",
    "type": "g.vx += ((tx / dist) * k - g.vx * 14) * dt;\ng.vy += ((ty / dist) * k - g.vy * 14) * dt;\ng.vx += (g.hx - g.x) * 22 * dt;\ng.x += g.vx * dt; g.y += g.vy * dt;",
    "matrix": "col.y += col.speed * dt;\nfor (let i = 0; i < col.chars.length; i++) {\n  ctx.globalAlpha = 1 - i / col.chars.length;\n  ctx.fillText(col.chars[i], col.x, col.y - i * size);\n}",
    "voxel": "const h = height(x, y, t) * size;\nd.polygon(topFace(bx, by, h), palette[2]);\nd.polygon(leftFace(bx, by, h), palette[1]);\nd.polygon(rightFace(bx, by, h), palette[3]);",
    "terrain": "ctx.beginPath();\nfor (let x = 0; x <= W; x += 8) {\n  const y = base + Math.sin(x * sp + t) * amp + Math.cos(x * sp * 2.3 - t * .4) * amp * .4;\n  x ? ctx.lineTo(x, y) : ctx.moveTo(x, y);\n}\nctx.stroke();",
    "rings": "r.r += r.v * dt; r.a -= dt * .55;\nctx.globalAlpha = r.a;\nctx.arc(r.x, r.y, r.r, 0, TAU); ctx.stroke();",
    "spiral": "const p = {\n  x: cx + Math.sin(t * .73) * W * .28 + Math.sin(t * 1.91) * W * .09,\n  y: cy + Math.cos(t * .61) * H * .30 + Math.cos(t * 2.23) * H * .08,\n};\ntrail.push(p);",
    "kaleido": "for (let s = 0; s < 6; s++) {\n  ctx.save(); ctx.rotate(s * TAU / 6 + t * .06);\n  if (s % 2) ctx.scale(1, -1);\n  drawWedge(t); ctx.restore();\n}",
    "starfield": "s.z -= speed * dt;\nconst k = 420 / s.z, x = cx + s.x * k, y = cy + s.y * k;\nctx.moveTo(px, py); ctx.lineTo(x, y); ctx.stroke();",
    "bars": "for (let i = 0; i < N; i++) {\n  h[i] += (energy * level(t, i) - h[i]) * dt * 12;\n  ctx.fillRect(i * bw, H - h[i] * H, bw * .62, h[i] * H);\n}",
    "aurora": "for (let i = 0; i < 64; i++) {\n  const x = i / 63 * W + Math.sin(t * .5 + i * .27) * 36;\n  const g = ctx.createLinearGradient(x, 0, x, H);\n  g.addColorStop(0, c1 + '00'); g.addColorStop(.4, c2 + '66');\n  ctx.strokeStyle = g; ctx.stroke();\n}",
}

TECH = {
    "voronoi": "Voronoi cells clipped from the viewport by every other seed's perpendicular bisector; cell area from the shoelace formula drives the fill.",
    "flow": "particles advected by a smooth sine/cosine vector field with translucent trail clearing.",
    "orbit": "polar particles (angle, radius, direction) integrated per frame and projected with a 0.68 y-scale.",
    "waves": "a point lattice displaced by radial sine waves from moving sources plus the pointer.",
    "blobs": "additive radial gradients composited with globalCompositeOperation='lighter' so overlaps read as one surface.",
    "grid": "a dot lattice with spring-damped inverse-distance repulsion from the pointer.",
    "particles": "a pooled emitter with gravity, drag and alpha-based life culling.",
    "type": "glyph sprites with home positions, spring return and pointer repulsion, plus periodic character scrambling.",
    "matrix": "columns of glyphs with per-column speed, trailing alpha and pointer-boosted fall.",
    "voxel": "an isometric height map drawn as sorted cube columns with three shaded faces.",
    "terrain": "stacked contour polylines sampled from summed sines, with a pointer dent.",
    "rings": "expanding stroked circles spawned on pointer movement, fading by alpha.",
    "spiral": "a persistent point trail along a slowly drifting Lissajous curve.",
    "kaleido": "one wedge drawn five times, rotated and mirrored across six segments.",
    "starfield": "3D stars projected with 1/z, drawing streaks between the previous and current projection.",
    "bars": "an envelope per bar eased toward a summed-sine level, with pointer hold adding energy.",
    "aurora": "64 vertical gradient ribbons advected by sine waves and composited with 'lighter'.",
}


def ts_entries():
    rows = []
    for i, demo in enumerate(DEMOS, start=26):
        did, name, mode, cat, pal, tagline, what, why, surface, intensity, works = demo
        rows.append({
            "n": i, "id": did, "name": name, "category": cat, "group": "interactive",
            "tagline": tagline, "what": what, "why": why,
            "surface": surface, "intensity": intensity, "worksWith": works,
            "snippet": SNIPPET[mode],
            "prompt": (f"You are building “{name}”. GOAL: {what} TECHNIQUE: {TECH[mode]} "
                       "CONSTRAINTS: one self-contained HTML file, no build step, pointer and keyboard paths, "
                       "pause when off-screen, render a still under prefers-reduced-motion."),
            "demo": f"/interactive/{did}.html",
            "thumb": f"/interactive/thumbs/{did}.gif",
        })
    body = ",\n".join("  " + json.dumps(r, ensure_ascii=False) for r in rows)
    return ("/**\n * Interactive elements — batch two (26–75).\n *\n * Generated by scripts/generate_interactive_50.py: fifteen canvas engines,\n * fifty parameterised playgrounds, one animated GIF thumb each.\n */\n"
            "import type { VisualAddon } from './visualAddons';\n\n"
            "export const interactiveAddonsExtra: VisualAddon[] = [\n" + body + ",\n];\n")


# Existing 25: id -> mode, so every interactive card gets a GIF thumb.
EXISTING_MODES = {
    "voronoi-mosaic": ("voronoi", "ember"), "flow-field": ("flow", "ice"),
    "audio-visualizer": ("waves", "candy"), "confetti-physics": ("particles", "candy"),
    "dot-globe": ("orbit", "ice"), "fluid-trail": ("flow", "aurora"),
    "generative-poster": ("waves", "mono"), "glitch-slicer": ("matrix", "candy"),
    "gravity-sandbox": ("blobs", "ember"), "image-lens": ("rings", "ice"),
    "kaleidoscope": ("kaleido", "aurora"), "kinetic-type": ("type", "acid"),
    "lightbox-gallery": ("grid", "mono"), "liquid-blob": ("blobs", "aurora"),
    "magnetic-dots": ("grid", "ice"), "parallax-scene": ("terrain", "sunset"),
    "pixel-studio": ("voxel", "candy"), "scroll-gallery": ("grid", "sunset"),
    "text-particles": ("type", "ice"), "voxel-terrain": ("voxel", "ice"),
    "waveform-grid": ("waves", "aurora"), "dither-lab": ("matrix", "mono"),
    "carousel-3d": ("orbit", "candy"), "before-after": ("grid", "sunset"),
    "ascii-portrait": ("matrix", "acid"),
}


def main():
    import sys
    html_only = "--html-only" in sys.argv
    THUMBS.mkdir(parents=True, exist_ok=True)
    for demo in DEMOS:
        did = demo[0]
        (OUT / f"{did}.html").write_text(build_html(demo))
        if not html_only:
            write_gif(THUMBS / f"{did}.gif", demo[2], demo[4])
        print("wrote", did)
    if not html_only:
        for did, (mode, pal) in EXISTING_MODES.items():
            write_gif(THUMBS / f"{did}.gif", mode, pal)
            print("thumb", did)
    TS_FILE.write_text(ts_entries())
    print("demos:", len(DEMOS), "html-only" if html_only else "with generated thumbs")


if __name__ == "__main__":
    main()
