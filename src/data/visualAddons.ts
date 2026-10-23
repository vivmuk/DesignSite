/**
 * Visual add-ons — the layer that turns a correct page into a designed one.
 *
 * 25 drop-in effects, each with: a live demo, a copy-paste snippet, and an
 * agent prompt. These are style-agnostic: they layer on top of any of the
 * 150 Styles DB directions rather than replacing them.
 */

export type AddonCategory = 'atmosphere' | 'surface' | 'motion' | 'type' | 'interaction';

export interface VisualAddon {
  n: number;
  id: string;
  name: string;
  category: AddonCategory;
  tagline: string;
  what: string;
  why: string;
  surface: string[];
  intensity: 'subtle' | 'medium' | 'bold';
  worksWith: string[];
  snippet: string;
  prompt: string;
  demo: string;
}

export const addonCategories: { id: AddonCategory; label: string; emoji: string; color: string; blurb: string }[] = [
  { id: 'atmosphere', label: 'Atmosphere', emoji: '🌫️', color: '#7fb2ff', blurb: 'Light, grain and texture behind the content.' },
  { id: 'surface', label: 'Surface & Depth', emoji: '🧊', color: '#4dd0e1', blurb: 'Panels, borders and cards that have physical weight.' },
  { id: 'motion', label: 'Motion', emoji: '🎞️', color: '#ff9f43', blurb: 'Entrances, scroll links and pointer physics.' },
  { id: 'type', label: 'Type & Texture', emoji: '🔠', color: '#c084fc', blurb: 'Treatments applied to headlines, images and print rhythm.' },
  { id: 'interaction', label: 'Chrome & Interaction', emoji: '🖱️', color: '#3ddc84', blurb: 'Cursor, nav, progress and feedback at the edges.' },
];

const D = (id: string) => `/addons/${id}.html`;

export const visualAddons: VisualAddon[] = [
  {
    n: 1,
    id: 'film-grain',
    name: 'Film Grain',
    category: 'atmosphere',
    tagline: 'Animated fractal noise that makes flat gradients feel photographed.',
    what: 'A fixed overlay of SVG feTurbulence at 18–30% opacity, blended in overlay mode, jittering through 8 positions every 7 seconds.',
    why: 'Digital gradients band and read as “CSS”. A grain layer adds micro-variation the eye interprets as material, and it hides banding for free.',
    surface: ['Page background', 'Hero', 'Imagery'],
    intensity: 'subtle',
    worksWith: ['dark-tech', 'luxe-brand', 'cultural', 'expressive', 'immersive-3d'],
    snippet: `<div class="grain" aria-hidden="true"></div>

<style>
.grain{
  position:fixed; inset:-50%; z-index:9999; pointer-events:none;
  opacity:.14; mix-blend-mode:normal;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.5' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)' opacity='.8'/%3E%3C/svg%3E");
  animation:grain 7s steps(8) infinite;
}
@keyframes grain{
  0%{transform:translate(0,0)} 25%{transform:translate(3%,-2%)}
  50%{transform:translate(2%,3%)} 75%{transform:translate(-3%,1%)}
  100%{transform:translate(0,0)}
}
@media (prefers-reduced-motion: reduce){ .grain{animation:none} }
</style>`,
    prompt: 'Add a film-grain layer to this page: one fixed, pointer-events:none div at inset:-50% with an inline SVG feTurbulence noise background, mix-blend-mode:overlay, opacity between .14 and .22. Animate it through 8 stepped positions over ~7s using steps() so it flickers like film rather than drifting. Disable the animation under prefers-reduced-motion. Do not put the layer inside a transformed ancestor — position:fixed breaks. Verify text contrast is unchanged.',
    demo: D('film-grain'),
  },
  {
    n: 2,
    id: 'aurora-mesh',
    name: 'Aurora Mesh',
    category: 'atmosphere',
    tagline: 'Drifting blurred blobs that turn a dark hero into a light source.',
    what: 'Three or four oversized radial blobs in screen blend mode, 19–28 second independent drift cycles, plus a vignette to keep edges dark.',
    why: 'It gives a page atmosphere without an image request, and because the motion is slow and non-repeating it reads as ambience rather than animation.',
    surface: ['Hero', 'Page background', 'CTA bands'],
    intensity: 'medium',
    worksWith: ['dark-tech', 'immersive-3d', 'contemporary', 'expressive', 'data-pro'],
    snippet: `<section class="aurora">
  <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
  <div class="aurora-content">…your hero…</div>
</section>

<style>
.aurora{position:relative;overflow:hidden;background:#06070b;isolation:isolate}
.aurora .blob{
  position:absolute;width:52vw;height:52vw;min-width:420px;min-height:420px;
  border-radius:50%;filter:blur(70px);opacity:.7;mix-blend-mode:screen;
  animation:drift 22s ease-in-out infinite alternate;
}
.b1{background:#ff5a1f;top:-18%;left:-8%}
.b2{background:#3b5bff;bottom:-26%;right:-6%;animation-duration:28s;animation-delay:-7s}
.b3{background:#00d4aa;top:22%;right:18%;width:34vw;height:34vw;opacity:.4;animation-duration:19s}
.aurora::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(120% 90% at 50% 50%,transparent 20%,#06070bee 100%)}
.aurora-content{position:relative;z-index:2}
@keyframes drift{
  0%{transform:translate3d(0,0,0) scale(1)}
  50%{transform:translate3d(7vw,5vh,0) scale(1.16)}
  100%{transform:translate3d(-5vw,-4vh,0) scale(.94)}
}
@media (prefers-reduced-motion: reduce){ .blob{animation:none} }
</style>`,
    prompt: 'Build an aurora mesh background behind the hero: 3–4 absolutely positioned blobs, each a solid brand colour, border-radius:50%, filter:blur(60–80px), mix-blend-mode:screen, on a near-black base. Give each an independent 19–28s ease-in-out alternate drift of translate and scale. Add a radial vignette overlay so edges stay dark and text keeps AA contrast. Content sits at z-index 2, blobs at 1, vignette at 3 but pointer-events:none. Freeze all animation under prefers-reduced-motion.',
    demo: D('aurora-mesh'),
  },
  {
    n: 3,
    id: 'dot-matrix',
    name: 'Dot Matrix',
    category: 'atmosphere',
    tagline: 'A technical dot field that fades out before it reaches the edges.',
    what: 'One repeating radial-gradient at a 24px pitch, softened by a radial CSS mask so there is no hard seam anywhere.',
    why: 'It adds structure to empty space and signals engineering precision, at zero image weight and zero runtime cost.',
    surface: ['Page background', 'Hero', 'Feature sections'],
    intensity: 'subtle',
    worksWith: ['data-pro', 'dark-tech', 'component-kit', 'contemporary', 'classic'],
    snippet: `<style>
.dotfield{position:relative;background:#07080c;overflow:hidden}
.dotfield::before{
  content:""; position:absolute; inset:0; pointer-events:none;
  background-image:radial-gradient(#ffffff2e 1px,transparent 1px);
  background-size:24px 24px;
  -webkit-mask-image:radial-gradient(120% 90% at 50% 0%,#000 10%,transparent 72%);
          mask-image:radial-gradient(120% 90% at 50% 0%,#000 10%,transparent 72%);
}
.dotfield > *{position:relative;z-index:1}
</style>`,
    prompt: 'Add a dot-matrix backdrop to this section: a ::before layer with repeating radial-gradient dots (1px dot, 24px pitch) in rgba(255,255,255,.18), masked by a radial gradient so the field fades to nothing before the section edges. Keep it pointer-events:none and place content above it with its own stacking context. Match the pitch to the existing 8pt spacing scale. Do not use an image.',
    demo: D('dot-matrix'),
  },
  {
    n: 4,
    id: 'cursor-spotlight',
    name: 'Cursor Spotlight',
    category: 'atmosphere',
    tagline: 'A warm pool of light that follows the pointer across a section.',
    what: 'Two radial gradients positioned at --mx/--my, updated by one pointermove listener; a 620px warm core over a 900px cool bloom.',
    why: 'It makes a static page feel responsive to a human presence, and it directs attention without adding visual clutter when the pointer is still.',
    surface: ['Hero', 'Feature sections', 'Pricing'],
    intensity: 'medium',
    worksWith: ['dark-tech', 'immersive-3d', 'luxe-brand', 'expressive', 'component-kit'],
    snippet: `<section class="spot" id="spot">
  …content…
</section>

<style>
.spot{--mx:50%;--my:30%;position:relative;overflow:hidden;background:#06070a}
.spot::before,.spot::after{content:"";position:absolute;inset:0;pointer-events:none}
.spot::before{background:radial-gradient(620px circle at var(--mx) var(--my),#ff6b3526,transparent 62%)}
.spot::after{background:radial-gradient(900px circle at var(--mx) var(--my),#4d9fff12,transparent 60%)}
.spot > *{position:relative;z-index:1}
</style>
<script>
const s = document.getElementById('spot');
if (matchMedia('(pointer:fine)').matches) {
  s.addEventListener('pointermove', e => {
    const r = s.getBoundingClientRect();
    s.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100).toFixed(2) + '%');
    s.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100).toFixed(2) + '%');
  }, { passive: true });
}
</script>`,
    prompt: 'Add a pointer spotlight to the hero: two absolutely positioned pseudo-elements painting radial gradients at CSS variables --mx/--my (warm 620px core, cool 900px bloom, low alpha). One passive pointermove listener converts client coordinates to percentages and writes the variables on the section — never read layout inside the handler beyond one cached rect. Only enable on (pointer:fine); park the light at 50%/30% for touch. Keep content above the light.',
    demo: D('cursor-spotlight'),
  },
  {
    n: 5,
    id: 'orbital-aura',
    name: 'Orbital Aura',
    category: 'atmosphere',
    tagline: 'A conic gradient rotating behind a card, blurred into a halo.',
    what: 'A blurred conic wheel one layer behind the card at 10s per rotation, plus a thin counter-rotating orbit with a single bright node.',
    why: 'It gives a still object implied energy and a premium, “product shot” quality without video or WebGL.',
    surface: ['Pricing card', 'Product card', 'Modal'],
    intensity: 'bold',
    worksWith: ['luxe-brand', 'dark-tech', 'immersive-3d', 'expressive'],
    snippet: `<div class="aura-wrap">
  <div class="halo"></div><div class="orbit"></div>
  <article class="card">…</article>
</div>

<style>
.aura-wrap{position:relative;isolation:isolate}
.halo{position:absolute;inset:-26%;z-index:-1;border-radius:50%;
  background:conic-gradient(from 0deg,#ff6b35,#ff2d78,#7a5cff,#4d9fff,#00d4aa,#ff6b35);
  filter:blur(46px);opacity:.8;animation:spin 10s linear infinite}
.orbit{position:absolute;inset:-8%;z-index:-1;border-radius:50%;
  border:1px solid #ffffff1f;animation:spin 18s linear infinite reverse}
.orbit::after{content:"";position:absolute;top:-4px;left:50%;width:7px;height:7px;
  border-radius:50%;background:#fff;box-shadow:0 0 16px #fff}
@keyframes spin{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion: reduce){ .halo,.orbit{animation:none} }
</style>`,
    prompt: 'Add an orbital aura to the featured pricing card: a blurred conic-gradient disc positioned behind the card at inset:-26%, filter:blur(46px), rotating once every 10s, and a 1px orbit ring with one bright node counter-rotating every 18s. Both sit at z-index:-1 inside an isolated wrapper so they never cover the card. Keep the card surface opaque enough for AA text contrast. Stop both rotations under prefers-reduced-motion.',
    demo: D('orbital-aura'),
  },
  {
    n: 6,
    id: 'glass-panel',
    name: 'Glass Panel',
    category: 'surface',
    tagline: 'Frosted glass with a specular edge, over a live light field.',
    what: '22px backdrop blur with saturation, a 1px inset top highlight, a diagonal sheen, and a saturated multi-radial background doing the work.',
    why: 'Glass only works when there is something worth blurring. Pair it with colour and light, otherwise it reads as grey fog.',
    surface: ['Cards', 'Nav', 'Modals', 'Overlays'],
    intensity: 'medium',
    worksWith: ['dark-tech', 'immersive-3d', 'contemporary', 'luxe-brand', 'data-pro'],
    snippet: `<div class="glass">
  …content…
</div>

<style>
.glass{
  position:relative; border-radius:26px; padding:38px; overflow:hidden;
  background:linear-gradient(155deg,#ffffff1f,#ffffff08 46%,#ffffff12);
  border:1px solid #ffffff2b;
  backdrop-filter:blur(22px) saturate(1.4);
  -webkit-backdrop-filter:blur(22px) saturate(1.4);
  box-shadow:0 40px 100px -24px #000c, inset 0 1px 0 #ffffff5c, inset 0 -1px 0 #ffffff12;
}
.glass::before{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(105deg,transparent 30%,#ffffff26 48%,transparent 62%)}
</style>

<!-- put it over saturated light, or blur has nothing to show -->
<div class="lightfield" aria-hidden="true"></div>`,
    prompt: 'Convert this panel to glass: 22px backdrop-filter blur plus 1.4 saturation, a translucent white gradient fill, a 1px border with a brighter inset top edge, and a diagonal sheen pseudo-element. Place it over a saturated radial light field — a glass panel over flat grey is illegible mush. Ensure body text still meets AA against the blurred backdrop by keeping the fill tinted, not transparent. Provide an @supports fallback with a solid surface when backdrop-filter is unavailable.',
    demo: D('glass-panel'),
  },
  {
    n: 7,
    id: 'gradient-border',
    name: 'Animated Gradient Border',
    category: 'surface',
    tagline: 'A one-pixel conic rainbow orbiting a card, powered by @property.',
    what: 'A transparent 1px border-box filled by a conic gradient whose angle is a registered @property, animated to 360deg over 5s.',
    why: 'It draws the eye to the one card you want clicked, and because it is only 1px it stays premium rather than carnival.',
    surface: ['CTA card', 'Pricing', 'Form', 'Featured item'],
    intensity: 'medium',
    worksWith: ['dark-tech', 'immersive-3d', 'luxe-brand', 'contemporary', 'expressive'],
    snippet: `<style>
@property --angle { syntax:"<angle>"; inherits:false; initial-value:0deg }

.gb{
  border:1px solid transparent; border-radius:22px; padding:1px;
  background:
    linear-gradient(#0a0c12,#0a0c12) padding-box,
    conic-gradient(from var(--angle),#ff6b35,#ff2d78,#7a5cff,#4d9fff,#00d4aa,#ff6b35) border-box;
  animation:turn 5s linear infinite;
}
@keyframes turn{ to{ --angle:360deg } }

@supports not (background:linear-gradient(#000,#000) padding-box,
               conic-gradient(#000,#000) border-box){
  .gb{ border-color:#ff6b3566 }
}
@media (prefers-reduced-motion: reduce){ .gb{animation:none} }
</style>`,
    prompt: 'Give the featured card an animated gradient border: register @property --angle as an <angle>, paint a transparent 1px border with a conic gradient in border-box clipped to the padding box, and animate the angle to 360deg over 5s linear. The card body must be an opaque gradient so the colour escapes only at the edge. Add an @supports fallback to a static border and freeze the animation under prefers-reduced-motion.',
    demo: D('gradient-border'),
  },
  {
    n: 8,
    id: 'tilt-3d',
    name: '3D Tilt Card',
    category: 'surface',
    tagline: 'Pointer-driven rotation with a glare and three layers of real depth.',
    what: 'Max ±16° rotateX and ±20° rotateY from pointer position, a moving radial glare, and content layers at 26/40/58px translateZ.',
    why: 'Parallax inside a single card creates depth the eye believes, and the tilt makes a static object feel inspectable.',
    surface: ['Product cards', 'Portfolio', 'Collectibles'],
    intensity: 'medium',
    worksWith: ['immersive-3d', 'luxe-brand', 'expressive', 'dark-tech'],
    snippet: `<div class="tilt-wrap">
  <article class="tilt" id="tilt">
    <div class="layer top">…</div>
    <div class="layer mid">…</div>
    <div class="layer bot">…</div>
  </article>
</div>

<style>
.tilt-wrap{perspective:1100px}
.tilt{position:relative;transform-style:preserve-3d;transition:transform .18s ease-out;
  border-radius:22px;overflow:hidden;background:linear-gradient(160deg,#1d2433,#0b0d13 72%);
  border:1px solid #2b3446}
.tilt::before{content:"";position:absolute;inset:0;z-index:1;
  background:radial-gradient(circle at var(--gx,50%) var(--gy,50%),#ffffff30,transparent 55%)}
.layer{position:absolute;z-index:2;transform-style:preserve-3d}
.top{inset:22px 24px auto;transform:translateZ(26px)}
.mid{top:44%;left:24px;right:24px;transform:translateZ(58px)}
.bot{bottom:24px;left:24px;right:24px;transform:translateZ(40px)}
@media (prefers-reduced-motion: reduce){ .tilt{transition:none} }
</style>
<script>
const card = document.getElementById('tilt');
card.parentElement.addEventListener('pointermove', e => {
  const r = card.getBoundingClientRect();
  const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
  card.style.transform = \`rotateX(\${(.5-py)*16}deg) rotateY(\${(px-.5)*20}deg)\`;
  card.style.setProperty('--gx', px*100+'%');
  card.style.setProperty('--gy', py*100+'%');
});
card.parentElement.addEventListener('pointerleave', () => card.style.transform = 'rotateX(0) rotateY(0)');
</script>`,
    prompt: 'Make the product card tilt in 3D: perspective on the wrapper, preserve-3d on the card, rotateX within ±16° and rotateY within ±20° from the pointer, with a 180ms ease-out return. Add a radial glare that follows the pointer via --gx/--gy, and place the eyebrow/body/footer layers at increasing translateZ (26/40/58px) so depth is visible. Do not tilt on coarse pointers; keep the click target flat and readable.',
    demo: D('tilt-3d'),
  },
  {
    n: 9,
    id: 'bento-grid',
    name: 'Bento Grid',
    category: 'surface',
    tagline: 'Asymmetric tiles that give unequal content equal dignity.',
    what: 'A 4-column, fixed-row grid where tiles claim column and row spans; one hero tile, supporting stats, and a 2-up footer.',
    why: 'Equal-width card grids flatten hierarchy. Spans let the layout say which fact matters before anyone reads a word.',
    surface: ['Features', 'Dashboards', 'About', 'Stats'],
    intensity: 'subtle',
    worksWith: ['contemporary', 'data-pro', 'component-kit', 'dark-tech', 'classic'],
    snippet: `<section class="bento">
  <article class="tile hero">…</article>
  <article class="tile wide">…</article>
  <article class="tile">…</article>
  <article class="tile">…</article>
</section>

<style>
.bento{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:132px;gap:12px}
.tile{position:relative;border-radius:18px;border:1px solid #ffffff12;background:#0c0f16;
  padding:20px;overflow:hidden;transition:transform .3s cubic-bezier(.2,.7,.2,1)}
.tile:hover{transform:translateY(-4px)}
.hero{grid-column:span 2;grid-row:span 2}
.wide{grid-column:span 2}
@media (max-width:900px){
  .bento{grid-template-columns:repeat(2,1fr);grid-auto-rows:124px}
  .hero,.wide{grid-column:span 2}
}
</style>`,
    prompt: 'Rework this feature grid into a bento layout: 4 columns on desktop, 132px implicit rows, and explicit column/row spans so one tile is 2×2, two are 2×1, and two are 1×1. On tablet collapse to 2 columns with the large tiles spanning both. Every tile keeps 20px padding, an 18px radius, and a 4px hover lift. Do not let a tile’s content overflow its span — truncate supporting copy rather than shrink type below 12px.',
    demo: D('bento-grid'),
  },
  {
    n: 10,
    id: 'inset-neumorph',
    name: 'Inset Neumorph',
    category: 'surface',
    tagline: 'One surface colour, two shadow pairs, and depth you can press.',
    what: 'A single fill tone across panel and controls; raised elements pair a dark offset shadow with a light one, pressed states invert both to inset.',
    why: 'It makes physical controls legible without borders, and the pressed inversion gives tactile feedback that flat buttons lack.',
    surface: ['Controls', 'Settings', 'Audio / hardware UI'],
    intensity: 'medium',
    worksWith: ['component-kit', 'contemporary', 'data-pro', 'immersive-3d'],
    snippet: `<style>
:root{ --neu:#171a20; --neu-dark:#0b0c0f; --neu-light:#242830; }

.neu-panel{
  background:var(--neu); border-radius:26px; padding:34px;
  border:1px solid #ffffff08;
  box-shadow:18px 18px 40px var(--neu-dark), -16px -16px 36px var(--neu-light);
}
.neu-btn{
  background:var(--neu); color:#c9d0dd; border:0; border-radius:16px; padding:22px 10px;
  box-shadow:8px 8px 18px var(--neu-dark), -6px -6px 16px var(--neu-light);
  transition:.16s;
}
.neu-btn:active, .neu-btn[aria-pressed="true"]{
  box-shadow:inset 7px 7px 15px var(--neu-dark), inset -6px -6px 14px var(--neu-light);
}
</style>`,
    prompt: 'Restyle this settings panel in inset neumorph: define --neu, --neu-dark and --neu-light once, use the same fill on panel and controls, and build every raised surface from a paired outer shadow (dark below-right, light above-left). Pressed/selected states invert both shadows to inset. No borders except a 1px near-transparent edge. Keep focus-visible outlines visible — neumorph routinely destroys focus affordance.',
    demo: D('inset-neumorph'),
  },
  {
    n: 11,
    id: 'marquee-band',
    name: 'Marquee Band',
    category: 'motion',
    tagline: 'A ribbon of type that never ends and pauses when you look.',
    what: 'A duplicated track translated −50%, edge-masked to transparent, two bands running opposite directions; hover pauses either one.',
    why: 'It fills a band with rhythm without demanding reading, and the duplication trick means no JS and no visible loop seam.',
    surface: ['Between sections', 'Client lists', 'Announcements'],
    intensity: 'medium',
    worksWith: ['expressive', 'luxe-brand', 'cultural', 'contemporary', 'scrollcraft'],
    snippet: `<div class="band">
  <div class="track">
    <span>DESIGN SYSTEMS ✦ ART DIRECTION ✦ MOTION ✦ CODE ✦</span>
    <span aria-hidden="true">DESIGN SYSTEMS ✦ ART DIRECTION ✦ MOTION ✦ CODE ✦</span>
  </div>
</div>

<style>
.band{overflow:hidden;border-block:1px solid #ffffff12;padding:18px 0;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);
          mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.track{display:flex;width:max-content;animation:slide 26s linear infinite;will-change:transform}
.band:hover .track{animation-play-state:paused}
.track span{white-space:nowrap;padding:0 26px;font-size:clamp(22px,3.4vw,40px);letter-spacing:-.03em}
@keyframes slide{to{transform:translateX(-50%)}}
@media (prefers-reduced-motion: reduce){ .track{animation:none} }
</style>`,
    prompt: 'Add a marquee band between two sections: duplicate one track exactly, translate it -50% over ~26s linear infinite, and mask both edges to transparent with a linear gradient. Pause on hover and under prefers-reduced-motion. Mark the duplicate aria-hidden so screen readers hear the phrase once. If the content is shorter than the viewport, repeat the phrase enough times before duplicating.',
    demo: D('marquee-band'),
  },
  {
    n: 12,
    id: 'split-text-reveal',
    name: 'Split-Text Reveal',
    category: 'motion',
    tagline: 'Words lifted from below, one beat at a time.',
    what: 'Headline text split into word spans at runtime, each inside an overflow-hidden wrapper, rising with a 90ms stagger.',
    why: 'Staggered type reads as composed rather than animated, and word-level masking keeps descenders from clipping if you pad the wrapper.',
    surface: ['Hero headline', 'Section headings'],
    intensity: 'medium',
    worksWith: ['expressive', 'luxe-brand', 'contemporary', 'scrollcraft', 'cultural'],
    snippet: `<h1 class="split">Every word arrives on its own beat.</h1>

<style>
.split .word{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .06em}
.split .word > span{display:inline-block;transform:translateY(110%) rotate(4deg);
  animation:rise .9s cubic-bezier(.16,1,.3,1) forwards;animation-delay:calc(var(--i) * 90ms)}
@keyframes rise{to{transform:translateY(0) rotate(0)}}
@media (prefers-reduced-motion: reduce){
  .split .word > span{animation:none;transform:none}
}
</style>
<script>
document.querySelectorAll('.split').forEach(h => {
  const words = h.textContent.trim().split(/\\s+/);
  h.textContent = '';
  words.forEach((w, i) => {
    const outer = document.createElement('span'); outer.className = 'word';
    const inner = document.createElement('span'); inner.textContent = w;
    inner.style.setProperty('--i', i);
    outer.appendChild(inner); h.appendChild(outer);
    h.appendChild(document.createTextNode(' '));
  });
});
</script>`,
    prompt: 'Animate the hero headline word by word: split text into word spans wrapped in overflow-hidden containers, lift each from translateY(110%) with a 90ms stagger and an ease-out expo curve. Keep a trailing space between words so the line still wraps naturally, and pad the wrapper horizontally so italic/descender glyphs are not clipped. Skip the animation entirely under prefers-reduced-motion. Never split mid-word.',
    demo: D('split-text-reveal'),
  },
  {
    n: 13,
    id: 'scroll-parallax',
    name: 'Scroll Parallax',
    category: 'motion',
    tagline: 'Three flat planes, three speeds, one sticky viewport.',
    what: 'A 220vh section with a sticky 100vh stage; three layers translate at +0.18, −0.12 and +0.30 of scroll, updated in a rAF callback.',
    why: 'Opposing speeds create depth that a single background image cannot, and the sticky stage keeps the composition framed the whole way.',
    surface: ['Hero', 'Story sections', 'Product reveals'],
    intensity: 'bold',
    worksWith: ['scrollcraft', 'immersive-3d', 'expressive', 'luxe-brand'],
    snippet: `<section class="px">
  <div class="px-stage">
    <div class="layer" data-speed=".18"></div>
    <div class="layer" data-speed="-.12"></div>
    <div class="layer" data-speed=".30"></div>
    <div class="px-copy">…</div>
  </div>
</section>

<style>
.px{position:relative;height:220vh}
.px-stage{position:sticky;top:0;height:100vh;overflow:hidden;display:grid;place-items:center}
.layer{position:absolute;inset:-12%;will-change:transform}
.px-copy{position:relative;z-index:2}
@media (prefers-reduced-motion: reduce){ .layer{transform:none !important} }
</style>
<script>
const layers = [...document.querySelectorAll('.layer')];
let ticking = false;
function update(){
  const y = scrollY;
  layers.forEach(l => l.style.transform = \`translate3d(0,\${y * parseFloat(l.dataset.speed)}px,0)\`);
  ticking = false;
}
addEventListener('scroll', () => {
  if (!ticking) { requestAnimationFrame(update); ticking = true; }
}, { passive: true });
</script>`,
    prompt: 'Build a parallax hero: a tall section (200–240vh) containing a sticky 100vh stage, with 2–3 absolutely positioned layers translated at different signed rates of scroll (e.g. +0.18, −0.12, +0.30). Do all writes inside a requestAnimationFrame guarded by a ticking flag; listen passively. Use translate3d and will-change:transform. Negative rates must not expose the stage edges — inset layers by at least 12%. Disable all movement under prefers-reduced-motion.',
    demo: D('scroll-parallax'),
  },
  {
    n: 14,
    id: 'magnetic-button',
    name: 'Magnetic Button',
    category: 'motion',
    tagline: 'A control that leans toward the pointer without moving its hit area.',
    what: 'Within a padded halo, translate the button up to 9px toward the cursor with a 250ms spring-style curve; release returns it to zero.',
    why: 'It adds tactility and intent to the primary action, and because only the visual translates, the click target stays exactly where the user expects.',
    surface: ['Primary CTA', 'Nav action', 'Footer'],
    intensity: 'bold',
    worksWith: ['expressive', 'luxe-brand', 'immersive-3d', 'contemporary'],
    snippet: `<div class="mag-zone">
  <button class="mag">Start a project <span class="arr">→</span></button>
</div>

<style>
.mag-zone{display:inline-block;padding:70px}
.mag{display:inline-flex;align-items:center;gap:12px;border:0;border-radius:999px;
  padding:20px 34px;background:#f2f4f8;color:#090a0e;font-weight:650;cursor:pointer;
  transition:transform .25s cubic-bezier(.2,.8,.2,1);will-change:transform}
.mag .arr{transition:transform .25s cubic-bezier(.2,.8,.2,1)}
.mag:hover .arr{transform:translateX(4px)}
@media (prefers-reduced-motion: reduce){ .mag{transition:none;transform:none !important} }
</style>
<script>
const btn = document.querySelector('.mag'), zone = btn.parentElement;
const strength = .22, max = 9;
zone.addEventListener('pointermove', e => {
  const r = btn.getBoundingClientRect();
  const dx = Math.max(-max, Math.min(max, (e.clientX - (r.left + r.width/2)) * strength));
  const dy = Math.max(-max, Math.min(max, (e.clientY - (r.top + r.height/2)) * strength));
  btn.style.transform = \`translate(\${dx}px,\${dy}px)\`;
});
zone.addEventListener('pointerleave', () => btn.style.transform = 'translate(0,0)');
</script>`,
    prompt: 'Add a magnetic effect to the primary CTA: listen for pointermove on a padded halo around the button, compute the offset from the button centre, clamp it to 9px, and translate the button with a 250ms spring-ish curve. Keep the hit area stationary — transform the visual only. Reset on pointerleave. Disable on coarse pointers and under prefers-reduced-motion. Ensure focus-visible styling is not removed.',
    demo: D('magnetic-button'),
  },
  {
    n: 15,
    id: 'count-up-stats',
    name: 'Count-Up Stats',
    category: 'motion',
    tagline: 'Numbers that earn their final value as you arrive.',
    what: 'IntersectionObserver triggers a 1.5s easeOutQuart count to the target, with decimals and a superscript suffix; tabular numerals prevent width jitter.',
    why: 'It pulls the eye to proof points at exactly the moment they enter the viewport, and tabular alignment keeps the layout from twitching.',
    surface: ['Stats bands', 'Dashboards', 'Case studies'],
    intensity: 'subtle',
    worksWith: ['data-pro', 'contemporary', 'component-kit', 'classic', 'dark-tech'],
    snippet: `<div class="stat"><span class="num" data-to="12.4" data-dec="1" data-suffix="k">0</span><span>Teams shipping</span></div>

<style>
.num{font-variant-numeric:tabular-nums}
.num sup{font-size:.42em;position:relative;top:-.7em;color:var(--accent,#ff8a5c)}
</style>
<script>
const run = el => {
  const to = parseFloat(el.dataset.to), dec = +(el.dataset.dec || 0), suf = el.dataset.suffix || '';
  const t0 = performance.now(), dur = 1500;
  const tick = t => {
    const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 4);
    el.innerHTML = (to * e).toFixed(dec) + (suf ? '<sup>' + suf + '</sup>' : '');
    if (p < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
};
const io = new IntersectionObserver((es, o) => {
  es.forEach(e => { if (e.isIntersecting) { run(e.target); o.unobserve(e.target); } });
}, { threshold: .4 });
document.querySelectorAll('.num').forEach(n => io.observe(n));
</script>`,
    prompt: 'Animate the stats band on entry: each number counts from 0 to its data-to value over 1.5s with an easeOutQuart curve, preserving decimals and a superscript suffix. Trigger once with IntersectionObserver at 40% visibility, then unobserve. Use font-variant-numeric: tabular-nums so digits do not shift width. Under prefers-reduced-motion, render the final value immediately. The final text must be the real number for copy/paste and screen readers.',
    demo: D('count-up-stats'),
  },
  {
    n: 16,
    id: 'duotone-image',
    name: 'Duotone Image',
    category: 'type',
    tagline: 'One photograph, two inks, and a hover that decodes it.',
    what: 'Grayscale base, a colour layer in mix-blend-mode:color, a warm screen wash at 28%, and a hover that fades both to reveal the original.',
    why: 'It unifies mismatched photography into a brand palette without editing each asset, and the hover reward makes the section interactive.',
    surface: ['Hero imagery', 'Editorial', 'Team / culture'],
    intensity: 'medium',
    worksWith: ['classic', 'cultural', 'luxe-brand', 'expressive', 'contemporary'],
    snippet: `<figure class="duo">
  <img src="/your-image.jpg" alt="…">
  <span class="wash" aria-hidden="true"></span>
  <span class="lift" aria-hidden="true"></span>
</figure>

<style>
.duo{position:relative;overflow:hidden;border-radius:22px}
.duo img{display:block;width:100%;height:100%;object-fit:cover;
  filter:grayscale(1) contrast(1.08);transition:filter .5s}
.duo .wash,.duo .lift{position:absolute;inset:0;transition:opacity .5s}
.duo .wash{background:#0b2a4a;mix-blend-mode:color}
.duo .lift{background:linear-gradient(150deg,#ff6b35,#ff2d78);mix-blend-mode:screen;opacity:.28}
.duo:hover .wash,.duo:hover .lift{opacity:0}
.duo:hover img{filter:grayscale(.15) contrast(1.02)}
</style>`,
    prompt: 'Apply a duotone treatment to the photography: grayscale the image, add a solid colour layer in mix-blend-mode:color, then a warm gradient layer in screen at ~28%. On hover, fade both layers and reduce the grayscale so the source image returns. Keep the wrapper overflow-hidden with the same radius as the image. Never put text directly on the duotone without a scrim — midtones can fail contrast.',
    demo: D('duotone-image'),
  },
  {
    n: 17,
    id: 'halftone-overlay',
    name: 'Halftone Overlay',
    category: 'type',
    tagline: 'A printable dot screen that fades at the edges and scales live.',
    what: 'A 7px radial-gradient dot grid in multiply mode over artwork, masked to a soft oval, with a slider that changes the pitch from 4 to 14px.',
    why: 'It gives digital imagery print provenance, and variable pitch lets one treatment serve both a 30px thumbnail and a full-bleed hero.',
    surface: ['Hero imagery', 'Album / poster art', 'Editorial'],
    intensity: 'bold',
    worksWith: ['cultural', 'expressive', 'classic', 'luxe-brand'],
    snippet: `<figure class="half">
  <img src="/your-art.jpg" alt="…">
  <span class="dots" aria-hidden="true"></span>
</figure>

<style>
.half{position:relative;overflow:hidden}
.half .dots{
  position:absolute;inset:0;pointer-events:none;
  background-image:radial-gradient(#ff6b35 1.6px,transparent 1.7px);
  background-size:7px 7px;
  mix-blend-mode:multiply;opacity:.72;
  -webkit-mask-image:radial-gradient(60% 60% at 50% 50%,#000 8%,transparent 76%);
          mask-image:radial-gradient(60% 60% at 50% 50%,#000 8%,transparent 76%);
}
</style>`,
    prompt: 'Lay a halftone screen over the hero artwork: a repeating radial-gradient dot field (1.6px dots, 7px pitch) in a brand ink colour, mix-blend-mode:multiply, masked by a radial gradient so the screen dissolves at the edges. The image beneath stays grayscale or high-contrast so the dots read. On light imagery switch to screen blend and a darker ink. Expose the pitch as a CSS variable so the same component scales.',
    demo: D('halftone-overlay'),
  },
  {
    n: 18,
    id: 'outline-type',
    name: 'Outline Type',
    category: 'type',
    tagline: 'Hollow strokes that fill on hover and turn type into structure.',
    what: 'Display type with transparent fill and a 2px text-stroke; hover swaps fill and stroke and nudges the line 14px.',
    why: 'It builds poster-level hierarchy with no image, and the fill/stroke inversion gives an interaction that feels like ink being pressed.',
    surface: ['Hero', 'Section dividers', 'Posters'],
    intensity: 'bold',
    worksWith: ['classic', 'expressive', 'cultural', 'luxe-brand'],
    snippet: `<h1 class="ot">
  <span class="line">Outline</span>
  <span class="line solid">becomes</span>
  <span class="line">structure</span>
</h1>

<style>
.ot{font-size:clamp(64px,15vw,210px);line-height:.8;letter-spacing:-.06em;
  font-weight:800;text-transform:uppercase;user-select:none}
.ot .line{display:block;white-space:nowrap;color:transparent;
  -webkit-text-stroke:2px #14120f;transition:.35s cubic-bezier(.2,.8,.2,1)}
.ot .line:hover{color:#c94020;-webkit-text-stroke-color:#c94020;transform:translateX(14px)}
.ot .solid{color:#14120f;-webkit-text-stroke:0}
.ot .solid:hover{color:transparent;-webkit-text-stroke:2px #14120f;transform:translateX(-14px)}
@media (prefers-reduced-motion: reduce){ .ot .line{transition:none} }
</style>`,
    prompt: 'Set the hero headline as outline type: display-size uppercase, transparent fill, 2px -webkit-text-stroke in ink. Alternate solid and outline lines, and on hover invert each line (fill ↔ stroke) with a small horizontal nudge. Keep a solid fallback colour for browsers without text-stroke. The words must remain selectable and readable by screen readers — never replace them with SVG paths.',
    demo: D('outline-type'),
  },
  {
    n: 19,
    id: 'text-shimmer',
    name: 'Text Shimmer',
    category: 'type',
    tagline: 'A four-stop gradient clipped to the glyphs, sweeping forever.',
    what: 'A 220%-wide linear gradient with a warm and cool highlight, clipped to text, animated across 5.5s; static position under reduced motion.',
    why: 'It draws the eye to one headline and signals a premium surface — foil, not neon — provided it is used once per page.',
    surface: ['One hero headline', 'Logo lockup', 'Price'],
    intensity: 'medium',
    worksWith: ['dark-tech', 'luxe-brand', 'immersive-3d', 'expressive'],
    snippet: `<h1 class="shimmer">Attention is a moving target.</h1>

<style>
.shimmer{
  background:linear-gradient(100deg,#6f7788 18%,#fff 38%,#ffb08a 48%,#7fb2ff 58%,#6f7788 78%);
  background-size:220% 100%;
  -webkit-background-clip:text; background-clip:text; color:transparent;
  animation:sweep 5.5s linear infinite;
}
@keyframes sweep{
  0%{background-position:120% 0}
  100%{background-position:-120% 0}
}
@media (prefers-reduced-motion: reduce){
  .shimmer{animation:none;background-position:50% 0}
}
</style>`,
    prompt: 'Apply a shimmer to the single most important headline: a 4-stop gradient 220% wide, clipped to the text with background-clip:text and transparent fill, swept from 120% to -120% every 5.5s. Include a mid-tone base so the text is readable at every frame of the sweep. Use it once per page. Under prefers-reduced-motion, freeze at 50% and keep the gradient static.',
    demo: D('text-shimmer'),
  },
  {
    n: 20,
    id: 'editorial-dropcap',
    name: 'Editorial Drop Cap',
    category: 'type',
    tagline: 'Print rhythm: drop cap, small-caps opening, justified measure.',
    what: 'A 4.9em floated first letter in the brand accent, a small-caps first line, two columns with a 34px gutter, and hairline rules.',
    why: 'It gives long-form content a designed opening instead of a wall of body copy, and the typographic details do the work without imagery.',
    surface: ['Articles', 'Docs intros', 'About page'],
    intensity: 'subtle',
    worksWith: ['classic', 'cultural', 'luxe-brand', 'contemporary'],
    snippet: `<article class="editorial">
  <p class="stand">On texture, rhythm, and the details nobody screenshots.</p>
  <div class="body">
    <p>The first thing a reader feels is not the headline. It is the measure…</p>
    <p>Typography is the only material a website is actually made of…</p>
  </div>
</article>

<style>
.editorial .body{column-count:2;column-gap:34px;font-family:Georgia,serif;
  font-size:15.5px;line-height:1.72}
.editorial .body p{margin:0 0 14px;text-align:justify;hyphens:auto}
.editorial .body p:first-child::first-letter{
  float:left;font-size:4.9em;line-height:.82;padding:.06em .1em 0 0;color:#c94020}
.editorial .body p:first-child::first-line{
  font-variant:small-caps;letter-spacing:.02em}
@media (max-width:700px){ .editorial .body{column-count:1} }
</style>`,
    prompt: 'Give the article an editorial opening: a 4.9em floated drop cap in the accent colour, a small-caps first line, a justified two-column body with a 34px gutter and hyphens:auto, collapsing to one column under 700px. Add a short italic standfirst and hairline rules above and below the block. Keep the measure between 60 and 75 characters per column; do not justify text without hyphenation.',
    demo: D('editorial-dropcap'),
  },
  {
    n: 21,
    id: 'custom-cursor',
    name: 'Custom Cursor',
    category: 'interaction',
    tagline: 'A precise dot and a lagging ring that knows what is clickable.',
    what: 'A 6px dot follows the pointer exactly; a 34px ring lerps at 0.16 and expands to 58px over links and buttons. Hidden entirely on touch.',
    why: 'It makes a site feel authored at the first mouse movement, and the ring’s expansion is a second, continuous affordance cue.',
    surface: ['Whole site', 'Portfolio', 'Campaign pages'],
    intensity: 'bold',
    worksWith: ['expressive', 'luxe-brand', 'immersive-3d', 'cultural'],
    snippet: `<div class="cursor-ring" aria-hidden="true"></div>
<div class="cursor-dot" aria-hidden="true"></div>

<style>
@media (pointer:fine){
  body{cursor:none}
  a,button{cursor:none}
  .cursor-dot,.cursor-ring{position:fixed;top:0;left:0;border-radius:50%;
    pointer-events:none;z-index:9999;translate:-50% -50%}
  .cursor-dot{width:6px;height:6px;background:#ff8a5c}
  .cursor-ring{width:34px;height:34px;border:1px solid #ffffff66;
    transition:width .2s,height .2s,background .2s,border-color .2s}
  .cursor-ring.hot{width:58px;height:58px;background:#ff6b3522;border-color:#ff8a5c99}
}
</style>
<script>
if (matchMedia('(pointer:fine)').matches) {
  const dot = document.querySelector('.cursor-dot');
  const ring = document.querySelector('.cursor-ring');
  let mx = innerWidth/2, my = innerHeight/2, rx = mx, ry = my;
  addEventListener('pointermove', e => {
    mx = e.clientX; my = e.clientY;
    dot.style.left = mx + 'px'; dot.style.top = my + 'px';
    ring.classList.toggle('hot', !!e.target.closest('a,button,[role="button"]'));
  });
  (function loop(){
    rx += (mx - rx) * .16; ry += (my - ry) * .16;
    ring.style.left = rx + 'px'; ring.style.top = ry + 'px';
    requestAnimationFrame(loop);
  })();
}
</script>`,
    prompt: 'Add a custom cursor: a small solid dot that tracks the pointer exactly, and a larger outlined ring that lerps toward it at ~0.16 per frame and expands on hover over links/buttons. Hide the native cursor only under (pointer:fine). The elements must be position:fixed, pointer-events:none, and high z-index, with aria-hidden. Restore the native cursor for keyboard and touch users, and never trap or obscure the focus ring.',
    demo: D('custom-cursor'),
  },
  {
    n: 22,
    id: 'scroll-progress',
    name: 'Scroll Progress Rail',
    category: 'interaction',
    tagline: 'A 3px gradient fill and a chapter list that knows where you are.',
    what: 'A fixed top rail scaled by scroll fraction, plus a right-hand chapter index that highlights the section currently in view.',
    why: 'Wayfinding is the cheapest retention tool on a long page, and it makes an article feel finite and finishable.',
    surface: ['Long articles', 'Docs', 'Case studies'],
    intensity: 'subtle',
    worksWith: ['classic', 'data-pro', 'scrollcraft', 'contemporary', 'dark-tech'],
    snippet: `<div class="progress"><i id="progress-fill"></i></div>

<style>
.progress{position:fixed;top:0;left:0;right:0;height:3px;background:#ffffff0d;z-index:100}
.progress i{display:block;height:100%;width:100%;transform:scaleX(0);
  transform-origin:0 50%;
  background:linear-gradient(90deg,#ff6b35,#ff2d78,#7a5cff,#4d9fff);
  box-shadow:0 0 18px #ff6b3588}
@media (prefers-reduced-motion: reduce){ .progress i{transition:none} }
</style>
<script>
const fill = document.getElementById('progress-fill');
let ticking = false;
function upd(){
  const max = document.documentElement.scrollHeight - innerHeight;
  fill.style.transform = 'scaleX(' + (max > 0 ? scrollY / max : 0) + ')';
  ticking = false;
}
addEventListener('scroll', () => {
  if (!ticking) { requestAnimationFrame(upd); ticking = true; }
}, { passive: true });
upd();
</script>`,
    prompt: 'Add scroll wayfinding: a 3px fixed rail at the top, filled with a brand gradient via transform:scaleX(scrollY / (scrollHeight - innerHeight)) inside a rAF-guarded passive scroll listener. Add a right-side chapter list that highlights the section whose top has crossed 45% of the viewport, and make each entry scroll smoothly to its section. Hide the chapter list under 700px. The rail must not cover focus outlines or the skip link.',
    demo: D('scroll-progress'),
  },
  {
    n: 23,
    id: 'condensing-nav',
    name: 'Condensing Nav',
    category: 'interaction',
    tagline: 'Generous at rest, compact and blurred once you move.',
    what: 'A transparent 26px-padded header that collapses to 12px with a blurred translucent backdrop and a hairline after 40px of scroll.',
    why: 'It preserves the calm of a spacious opening while keeping navigation usable and legible over content.',
    surface: ['Site header', 'Docs', 'Marketing pages'],
    intensity: 'subtle',
    worksWith: ['contemporary', 'classic', 'component-kit', 'data-pro'],
    snippet: `<header class="sitenav" id="sitenav">
  <a class="logo" href="/">north<span>.</span>studio</a>
  <nav>…</nav>
</header>

<style>
.sitenav{position:fixed;top:0;left:0;right:0;z-index:50;
  display:flex;align-items:center;justify-content:space-between;
  padding:26px 6vw;background:transparent;border-bottom:1px solid transparent;
  transition:padding .35s cubic-bezier(.2,.8,.2,1),background .35s,
             border-color .35s,backdrop-filter .35s}
.sitenav.small{padding:12px 6vw;background:#080a10d9;
  border-bottom-color:#ffffff12;backdrop-filter:blur(16px)}
.sitenav .logo{font-weight:700;letter-spacing:-.03em;transition:font-size .35s}
.sitenav.small .logo{font-size:15px}
@media (prefers-reduced-motion: reduce){ .sitenav{transition:none} }
</style>
<script>
const nav = document.getElementById('sitenav');
addEventListener('scroll', () => nav.classList.toggle('small', scrollY > 40), { passive: true });
</script>`,
    prompt: 'Make the header condense on scroll: full padding and a transparent background at the top, then after ~40px reduce vertical padding by ~14px, add a translucent dark background, 16px backdrop blur and a 1px bottom hairline. Transition padding, background, border and backdrop-filter over 350ms. Toggle a single class from a passive scroll listener. Keep the nav height stable enough that the hero does not jump, and respect prefers-reduced-motion.',
    demo: D('condensing-nav'),
  },
  {
    n: 24,
    id: 'card-spotlight',
    name: 'Card Spotlight',
    category: 'interaction',
    tagline: 'Every card carries a light that follows your pointer.',
    what: 'Per-card --mx/--my from pointermove, painting a 260px radial fill and a matching 1px border glow via mask compositing.',
    why: 'It creates a sense of inspection across a grid without making every card animate at once, and the border glow reads as material thickness.',
    surface: ['Feature grids', 'Pricing', 'Integrations'],
    intensity: 'medium',
    worksWith: ['dark-tech', 'component-kit', 'data-pro', 'immersive-3d', 'contemporary'],
    snippet: `<article class="spot-card">
  <div class="icon">◈</div><h3>Vector export</h3><p>…</p>
</article>

<style>
.spot-card{--mx:50%;--my:0%;position:relative;border-radius:18px;padding:26px;
  background:#0b0d13;border:1px solid #ffffff12;overflow:hidden;
  transition:transform .25s,border-color .25s}
.spot-card::before{content:"";position:absolute;inset:0;opacity:0;transition:opacity .25s;
  background:radial-gradient(260px circle at var(--mx) var(--my),#ff6b3526,transparent 65%)}
.spot-card::after{content:"";position:absolute;inset:-1px;border-radius:inherit;padding:1px;
  opacity:0;transition:opacity .25s;
  background:radial-gradient(220px circle at var(--mx) var(--my),#ff8a5c99,transparent 70%);
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
.spot-card:hover{transform:translateY(-3px)}
.spot-card:hover::before,.spot-card:hover::after{opacity:1}
.spot-card > *{position:relative;z-index:1}
</style>
<script>
document.querySelectorAll('.spot-card').forEach(card => {
  card.addEventListener('pointermove', e => {
    const r = card.getBoundingClientRect();
    card.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
    card.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
  });
});
</script>`,
    prompt: 'Add a pointer-tracked spotlight to every card in the grid: on pointermove write --mx/--my as percentages, then paint a 260px radial warm fill and a matching 1px border glow using mask-composite:exclude. Lift the card 3px on hover. Content must sit above the light. On coarse pointers, replace the chase with a static top-edge highlight. One listener per card, no layout reads beyond the cached rect.',
    demo: D('card-spotlight'),
  },
  {
    n: 25,
    id: 'success-burst',
    name: 'Success Burst',
    category: 'interaction',
    tagline: 'Twenty-six particles and a colour change: a win you can feel.',
    what: 'On click, particles leave the button at randomised angles with gravity and rotation, while the button turns green and swaps to a Saved state.',
    why: 'Micro-celebrations confirm that an action landed, reduce repeat submissions, and cost almost nothing in code or performance.',
    surface: ['Save / submit', 'Checkout', 'Onboarding'],
    intensity: 'medium',
    worksWith: ['component-kit', 'expressive', 'contemporary', 'data-pro'],
    snippet: `<div class="burst-wrap" id="wrap">
  <button class="save" id="save">Save changes</button>
  <div class="particles" id="particles"></div>
</div>

<style>
.burst-wrap{position:relative;display:inline-block}
.save{border:0;border-radius:999px;padding:17px 30px;background:#ff6b35;color:#160a04;
  font-weight:700;cursor:pointer;transition:.25s}
.save.done{background:#3ddc84;color:#04220f}
.particles{position:absolute;inset:0;pointer-events:none;z-index:3}
.p{position:absolute;left:50%;top:50%;width:7px;height:7px;border-radius:2px;opacity:0;
  animation:fly .95s cubic-bezier(.12,.7,.2,1) forwards}
@keyframes fly{
  0%{opacity:1;transform:translate(-50%,-50%) rotate(0) scale(1)}
  70%{opacity:1}
  100%{opacity:0;transform:translate(calc(-50% + var(--x)),calc(-50% + var(--y)))
       rotate(var(--r)) scale(.4)}
}
@media (prefers-reduced-motion: reduce){ .p{display:none} }
</style>
<script>
const btn = document.getElementById('save'), field = document.getElementById('particles');
const colors = ['#ff6b35','#ff2d78','#7a5cff','#4d9fff','#3ddc84','#ffd166'];
btn.addEventListener('click', () => {
  if (btn.classList.contains('done')) return;
  btn.classList.add('done'); btn.textContent = '✓ Saved';
  for (let i = 0; i < 26; i++) {
    const p = document.createElement('i'); p.className = 'p';
    const a = Math.random() * Math.PI * 2, d = 60 + Math.random() * 110;
    p.style.setProperty('--x', Math.cos(a) * d + 'px');
    p.style.setProperty('--y', Math.sin(a) * d + 30 + 'px');
    p.style.setProperty('--r', Math.round(Math.random() * 540 - 270) + 'deg');
    p.style.background = colors[i % colors.length];
    p.style.animationDelay = (Math.random() * .08).toFixed(2) + 's';
    field.appendChild(p);
    setTimeout(() => p.remove(), 1200);
  }
});
</script>`,
    prompt: 'Add a success micro-celebration to the save button: on a successful save, spawn ~26 small particles at the button centre with randomised angle, distance, rotation and a 0–80ms delay, animate them out over 950ms with gravity, then remove them from the DOM. At the same time flip the button to a green Saved state and disable repeat submits. Skip particles entirely under prefers-reduced-motion. Announce the result through an aria-live region, not just colour.',
    demo: D('success-burst'),
  },
];

export const addonsByCategory = (cat: AddonCategory | 'all') =>
  cat === 'all' ? visualAddons : visualAddons.filter(a => a.category === cat);

/** Styles DB categories → the add-ons that suit them. */
export const addonsForStyleCategory = (styleCategory: string): VisualAddon[] => {
  const picks = visualAddons.filter(a => a.worksWith.includes(styleCategory));
  return (picks.length ? picks : visualAddons).slice(0, 6);
};
