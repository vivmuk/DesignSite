# Visual add-ons — part A (01-13)
# Each entry: id, name, css, html, js, hint

ADDONS_A = [
dict(
id="film-grain", name="Film Grain",
css=r'''
.grain-page{position:relative;min-height:100vh;display:grid;grid-template-columns:1.15fr .85fr;align-items:center;gap:4vw;padding:9vh 6vw;overflow:hidden;background:radial-gradient(120% 90% at 15% 10%,#1b1d2a 0%,#0a0b10 55%,#07080b 100%)}
.grain-page::after{content:"";position:absolute;inset:-50%;z-index:9;pointer-events:none;opacity:.16;mix-blend-mode:normal;
background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.5' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)' opacity='.8'/%3E%3C/svg%3E");
animation:grain 7s steps(8) infinite}
body.grain-off .grain-page::after{opacity:0}
@keyframes grain{0%{transform:translate(0,0)}12%{transform:translate(-2%,-3%)}25%{transform:translate(3%,-2%)}37%{transform:translate(-3%,2%)}50%{transform:translate(2%,3%)}62%{transform:translate(-1%,3%)}75%{transform:translate(3%,1%)}87%{transform:translate(-2%,-1%)}100%{transform:translate(0,0)}}
.stage{position:relative;z-index:2;max-width:560px}
.kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;text-transform:uppercase;color:#ff8a5c;margin-bottom:26px}
.stage h1{font-size:clamp(42px,7vw,88px);line-height:.94;letter-spacing:-.045em;font-weight:650}
.stage h1 em{font-family:Georgia,"Times New Roman",serif;font-weight:400;color:#ffb08a}
.lede{margin:26px 0 34px;color:#a6adbe;font-size:16px;line-height:1.65;max-width:44ch}
.pill{appearance:none;border:1px solid #ffffff26;background:#ffffff10;color:#f2f4f8;border-radius:999px;padding:12px 22px;font:500 13px/1 inherit;cursor:pointer;transition:.2s}
.pill:hover{background:#ffffff1c;border-color:#ffffff40}
.swatch{position:relative;z-index:2;height:62vh;border-radius:26px;background:linear-gradient(150deg,#ff6b35 0%,#7a3cff 52%,#1a2a6b 100%);box-shadow:0 40px 120px -30px #ff6b3566,inset 0 1px 0 #ffffff33}
.swatch::before{content:"";position:absolute;inset:0;border-radius:inherit;background:radial-gradient(90% 60% at 20% 15%,#ffffff40,transparent 60%)}
@media(max-width:820px){.grain-page{grid-template-columns:1fr;padding-top:12vh}.swatch{height:34vh}}
''',
html=r'''
<main class="grain-page">
  <section class="stage">
    <p class="kicker">Atmosphere / 01</p>
    <h1>Noise is<br><em>a material.</em></h1>
    <p class="lede">A 30% overlay of animated fractal noise turns flat gradients into something photographed. Toggle it and watch the surface gain weight.</p>
    <button id="toggle" class="pill">Grain: on</button>
  </section>
  <div class="swatch" aria-hidden="true"></div>
</main>
''',
js=r'''
const btn=document.getElementById('toggle');
btn.addEventListener('click',()=>{
  document.body.classList.toggle('grain-off');
  const off=document.body.classList.contains('grain-off');
  btn.textContent='Grain: '+(off?'off':'on');
});
''',
hint="Click the button — the same gradient, with and without animated fractal grain.",
),
dict(
id="aurora-mesh", name="Aurora Mesh",
css=r'''
.aurora{position:relative;min-height:100vh;display:grid;place-items:center;text-align:center;padding:12vh 6vw;overflow:hidden;background:#06070b}
.aurora .blob{position:absolute;width:52vw;height:52vw;min-width:420px;min-height:420px;border-radius:50%;filter:blur(70px);opacity:.68;mix-blend-mode:screen;animation:drift 22s ease-in-out infinite alternate}
.b1{background:#ff5a1f;top:-18%;left:-8%}
.b2{background:#3b5bff;bottom:-26%;right:-6%;animation-duration:28s;animation-delay:-7s}
.b3{background:#00d4aa;top:22%;right:18%;width:34vw;height:34vw;opacity:.4;animation-duration:19s;animation-delay:-12s}
@keyframes drift{0%{transform:translate3d(0,0,0) scale(1)}50%{transform:translate3d(7vw,5vh,0) scale(1.16)}100%{transform:translate3d(-5vw,-4vh,0) scale(.94)}}
.aurora::after{content:"";position:absolute;inset:0;background:radial-gradient(120% 90% at 50% 50%,transparent 20%,#06070bee 100%)}
.aurora-copy{position:relative;z-index:2;max-width:780px}
.aurora .eyebrow{display:inline-flex;gap:8px;align-items:center;border:1px solid #ffffff22;background:#ffffff0d;border-radius:999px;padding:8px 14px;font:600 10px/1 ui-monospace,monospace;letter-spacing:.2em;text-transform:uppercase;color:#c8cede;margin-bottom:28px}
.aurora .eyebrow i{width:6px;height:6px;border-radius:50%;background:#3ddc84;box-shadow:0 0 12px #3ddc84}
.aurora h1{font-size:clamp(48px,8.4vw,104px);line-height:.92;letter-spacing:-.05em;font-weight:620;text-shadow:0 2px 40px #00000066}
.aurora p{margin:26px auto 0;max-width:52ch;color:#b9c0d0;font-size:16.5px;line-height:1.7}
.aurora .cta{margin-top:36px;display:inline-flex;gap:10px}
.aurora .cta a{color:#0a0b0f;background:#f4f6fa;border-radius:999px;padding:14px 24px;font-size:13.5px;font-weight:650;text-decoration:none}
.aurora .cta a.ghost{background:#ffffff10;color:#eef1f7;border:1px solid #ffffff26}
@media(max-width:700px){.b3{display:none}}
''',
html=r'''
<main class="aurora">
  <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
  <div class="aurora-copy">
    <span class="eyebrow"><i></i>System operational</span>
    <h1>Infrastructure<br>that glows.</h1>
    <p>Three blurred light sources drift behind the headline at different speeds. No images, no video — four divs and one keyframe.</p>
    <div class="cta"><a href="#">Start building</a><a href="#" class="ghost">Read the docs</a></div>
  </div>
</main>
''',
js=r'''/* none — pure CSS */''',
hint="Four blurred radial blobs, 19–28s drift cycles, screen blend. Pure CSS.",
),
dict(
id="dot-matrix", name="Dot Matrix",
css=r'''
.matrix{position:relative;min-height:100vh;padding:11vh 7vw;background:#07080c;overflow:hidden;display:grid;align-content:center}
.matrix::before{content:"";position:absolute;inset:0;
background-image:radial-gradient(#ffffff55 1.8px,transparent 1.95px);background-size:28px 28px;
-webkit-mask-image:radial-gradient(120% 90% at 50% 0%,#000 10%,transparent 72%);
mask-image:radial-gradient(120% 90% at 50% 0%,#000 10%,transparent 72%)}
.matrix::after{content:"";position:absolute;inset:0;background:radial-gradient(64% 52% at 50% 4%,#ff6b3530,transparent 72%)}
.matrix-inner{position:relative;z-index:2;max-width:1120px;margin:0 auto}
.matrix .kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#7f8aa3;text-transform:uppercase;margin-bottom:22px}
.matrix h1{font-size:clamp(44px,6.6vw,84px);line-height:.96;letter-spacing:-.045em;max-width:14ch}
.matrix .row{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:64px}
.matrix .cell{border:1px solid #ffffff14;background:#0b0d13cc;border-radius:16px;padding:22px;backdrop-filter:blur(6px);transition:.25s}
.matrix .cell:hover{border-color:#ff6b3566;transform:translateY(-3px);background:#10131acc}
.matrix .cell b{display:block;font:600 24px/1 ui-monospace,monospace;color:#ff8a5c;margin-bottom:10px}
.matrix .cell span{color:#98a1b5;font-size:13px;line-height:1.6}
@media(max-width:820px){.matrix .row{grid-template-columns:1fr}}
''',
html=r'''
<main class="matrix">
  <div class="matrix-inner">
    <p class="kicker">Atmosphere / 03 · technical grid</p>
    <h1>Precision you can see.</h1>
    <div class="row">
      <div class="cell"><b>24px</b><span>The dot pitch. It matches the 8pt spacing scale, so content sits on the grid.</span></div>
      <div class="cell"><b>72%</b><span>A radial mask fades the field out before it reaches the edges — no hard seam.</span></div>
      <div class="cell"><b>0 KB</b><span>One repeating radial-gradient. No texture image, no canvas, no request.</span></div>
    </div>
  </div>
</main>
''',
js=r'''/* none — pure CSS */''',
hint="One repeating radial-gradient plus a radial mask. Zero image weight.",
),
dict(
id="cursor-spotlight", name="Cursor Spotlight",
css=r'''
.spot{--mx:50%;--my:30%;position:relative;min-height:100vh;padding:11vh 7vw;background:#06070a;overflow:hidden}
.spot::before{content:"";position:absolute;inset:0;pointer-events:none;
background:radial-gradient(620px circle at var(--mx) var(--my),#ff6b3526,transparent 62%);
transition:background .08s linear}
.spot::after{content:"";position:absolute;inset:0;pointer-events:none;
background:radial-gradient(900px circle at var(--mx) var(--my),#4d9fff12,transparent 60%)}
.spot-inner{position:relative;z-index:2;max-width:1080px;margin:0 auto}
.spot .eyebrow{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;text-transform:uppercase;color:#6f7a91;margin-bottom:22px}
.spot h1{font-size:clamp(40px,6vw,76px);line-height:1;letter-spacing:-.04em;max-width:16ch}
.spot p.lede{color:#aab2c4;margin-top:22px;max-width:52ch;line-height:1.7;font-size:16px}
.spot .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:70px}
.spot .card{position:relative;background:#0b0e14b8;border:1px solid #ffffff12;border-radius:18px;padding:26px 22px;overflow:hidden}
.spot .card h3{font-size:16px;margin-bottom:9px}
.spot .card p{color:#8f99ae;font-size:13px;line-height:1.6;margin:0}
.spot .card .ico{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:#ff6b351f;color:#ff9b74;margin-bottom:18px;font-size:15px}
@media(max-width:820px){.spot .cards{grid-template-columns:1fr}.spot::before{background:radial-gradient(420px circle at var(--mx) var(--my),#ff6b3522,transparent 62%)}}
''',
html=r'''
<main class="spot" id="spot">
  <div class="spot-inner">
    <p class="eyebrow">Atmosphere / 04 · pointer-linked light</p>
    <h1>Light that follows attention.</h1>
    <p class="lede">A 620px radial wash tracks your pointer across the section. It is two custom properties and two gradients — and it makes a static page feel responsive to a human.</p>
    <div class="cards">
      <article class="card"><div class="ico">◐</div><h3>One listener</h3><p>A single pointermove handler writes --mx and --my on the section. Nothing else re-renders.</p></article>
      <article class="card"><div class="ico">✳</div><h3>Two temperatures</h3><p>A warm orange core layered over a cool blue bloom keeps the light from looking like a flashlight.</p></article>
      <article class="card"><div class="ico">⌁</div><h3>Touch-safe</h3><p>The light parks at 50% / 30% on coarse pointers, so mobile users see a composed gradient.</p></article>
    </div>
  </div>
</main>
''',
js=r'''
const spot=document.getElementById('spot');
const fine=matchMedia('(pointer:fine)').matches;
if(fine){
  spot.addEventListener('pointermove',e=>{
    const r=spot.getBoundingClientRect();
    spot.style.setProperty('--mx',((e.clientX-r.left)/r.width*100).toFixed(2)+'%');
    spot.style.setProperty('--my',((e.clientY-r.top)/r.height*100).toFixed(2)+'%');
  });
}
''',
hint="Move your cursor — one listener, two radial gradients, zero re-renders.",
),
dict(
id="orbital-aura", name="Orbital Aura",
css=r'''
.orbital{position:relative;min-height:100vh;display:grid;place-items:center;padding:10vh 6vw;background:#05060a;overflow:hidden}
.orbital .stars{position:absolute;inset:0;background-image:radial-gradient(#ffffff24 .7px,transparent .7px);background-size:38px 38px;mask-image:radial-gradient(circle at 50% 50%,#000 10%,transparent 72%)}
.aura-wrap{position:relative;width:min(420px,86vw);isolation:isolate}
.halo{position:absolute;inset:-26%;z-index:-1;border-radius:50%;
background:conic-gradient(from 0deg,#ff6b35,#ff2d78,#7a5cff,#4d9fff,#00d4aa,#ff6b35);
filter:blur(46px);opacity:.8;animation:spin 10s linear infinite}
.halo2{position:absolute;inset:-8%;z-index:-1;border-radius:50%;border:1px solid #ffffff1f;animation:spin 18s linear infinite reverse}
.halo2::after{content:"";position:absolute;top:-4px;left:50%;width:7px;height:7px;border-radius:50%;background:#fff;box-shadow:0 0 16px #fff}
@keyframes spin{to{transform:rotate(360deg)}}
.orb-card{position:relative;border-radius:24px;padding:34px 30px 30px;background:#0a0c12f2;border:1px solid #ffffff1a;box-shadow:0 40px 90px -30px #000,inset 0 1px 0 #ffffff1f;backdrop-filter:blur(8px)}
.orb-card .tag{font:600 10px/1 ui-monospace,monospace;letter-spacing:.2em;color:#ff9b74;text-transform:uppercase}
.orb-card h2{font-size:30px;letter-spacing:-.03em;margin:16px 0 8px}
.orb-card .sub{color:#9aa3b6;font-size:13.5px;line-height:1.65;margin-bottom:26px}
.orb-row{display:flex;align-items:baseline;gap:8px;margin-bottom:24px}
.orb-row b{font:650 46px/1 ui-monospace,monospace;letter-spacing:-.04em}
.orb-row span{color:#7f889d;font-size:13px}
.orb-cta{display:flex;gap:10px}
.orb-cta a{flex:1;text-align:center;text-decoration:none;border-radius:12px;padding:12px;font-size:13px;font-weight:600;background:#f2f4f8;color:#090a0e}
.orb-cta a.ghost{background:#ffffff0d;color:#e7ebf3;border:1px solid #ffffff1f}
''',
html=r'''
<main class="orbital">
  <div class="stars"></div>
  <div class="aura-wrap">
    <div class="halo"></div><div class="halo2"></div>
    <article class="orb-card">
      <p class="tag">Professional · annual</p>
      <h2>Everything, unlocked.</h2>
      <p class="sub">A conic gradient rotates behind the card at 10 seconds per turn, blurred into an aura.</p>
      <div class="orb-row"><b>$24</b><span>/ month, billed yearly</span></div>
      <div class="orb-cta"><a href="#">Choose plan</a><a href="#" class="ghost">Compare</a></div>
    </article>
  </div>
</main>
''',
js=r'''/* none — pure CSS */''',
hint="A rotating conic gradient, blurred to 46px, sits one layer behind the card.",
),
dict(
id="glass-panel", name="Glass Panel",
css=r'''
.glass-scene{position:relative;min-height:100vh;display:grid;place-items:center;padding:10vh 6vw;overflow:hidden;background:#070a10}
.glass-scene .bg{position:absolute;inset:-10%;
background:
radial-gradient(40% 50% at 20% 25%,#ff6b35 0%,transparent 60%),
radial-gradient(45% 55% at 80% 30%,#3b5bff 0%,transparent 62%),
radial-gradient(50% 60% at 55% 85%,#00d4aa 0%,transparent 60%),
#080a10;
filter:blur(50px) saturate(1.2);opacity:.85}
.glass-scene::after{content:"";position:absolute;inset:0;background:#05060acc}
.glass-panel{position:relative;z-index:2;width:min(760px,92vw);border-radius:26px;padding:38px;
background:linear-gradient(155deg,#ffffff1f,#ffffff08 46%,#ffffff12);
border:1px solid #ffffff2b;backdrop-filter:blur(22px) saturate(1.4);-webkit-backdrop-filter:blur(22px) saturate(1.4);
box-shadow:0 40px 100px -24px #000000cc,inset 0 1px 0 #ffffff5c,inset 0 -1px 0 #ffffff12;overflow:hidden}
.glass-panel::before{content:"";position:absolute;inset:0;pointer-events:none;
background:linear-gradient(105deg,transparent 30%,#ffffff26 48%,transparent 62%);transform:translateX(-30%)}
.gp-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:34px}
.gp-logo{font-weight:650;letter-spacing:-.02em}
.gp-logo em{color:#ff9b74;font-style:normal}
.gp-pill{font:500 11px/1 ui-monospace,monospace;color:#dfe4ee;border:1px solid #ffffff2e;background:#ffffff12;border-radius:999px;padding:7px 12px}
.glass-panel h2{font-size:clamp(28px,4.6vw,44px);line-height:1.03;letter-spacing:-.04em;max-width:15ch}
.glass-panel p{color:#c3cad9;margin-top:16px;line-height:1.7;font-size:14.5px;max-width:48ch}
.gp-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:30px}
.gp-cell{background:#ffffff0d;border:1px solid #ffffff1a;border-radius:14px;padding:16px}
.gp-cell b{display:block;font:650 22px/1 ui-monospace,monospace;margin-bottom:6px}
.gp-cell span{color:#aab3c4;font-size:11.5px;line-height:1.5}
@media(max-width:760px){.glass-panel{padding:26px}.gp-grid{grid-template-columns:1fr}}
''',
html=r'''
<main class="glass-scene">
  <div class="bg"></div>
  <section class="glass-panel">
    <div class="gp-top"><span class="gp-logo">prism<em>.</em></span><span class="gp-pill">LIVE PREVIEW</span></div>
    <h2>Frosted, but never foggy.</h2>
    <p>22px of backdrop blur over a three-colour light field, plus a 1px inner highlight along the top edge. The panel keeps text at AA contrast while the background stays saturated.</p>
    <div class="gp-grid">
      <div class="gp-cell"><b>22px</b><span>backdrop blur</span></div>
      <div class="gp-cell"><b>1px</b><span>inset specular edge</span></div>
      <div class="gp-cell"><b>0</b><span>images loaded</span></div>
    </div>
  </section>
</main>
''',
js=r'''/* none — pure CSS */''',
hint="Backdrop blur, a specular inset edge, and a diagonal sheen over a live light field.",
),
dict(
id="gradient-border", name="Animated Gradient Border",
css=r'''
@property --angle{syntax:"<angle>";inherits:false;initial-value:0deg}
.gb-scene{min-height:100vh;display:grid;place-items:center;padding:10vh 6vw;background:#06070b}
.gb-card{position:relative;width:min(520px,92vw);border-radius:22px;padding:1px;border:1px solid transparent;
background:linear-gradient(#0a0c12,#0a0c12) padding-box,
conic-gradient(from var(--angle),#ff6b35,#ff2d78,#7a5cff,#4d9fff,#00d4aa,#ff6b35) border-box;
animation:turn 5s linear infinite}
@supports not (background:linear-gradient(#000,#000) padding-box,conic-gradient(#000,#000) border-box){.gb-card{border-color:#ff6b3566}}
@keyframes turn{to{--angle:360deg}}
.gb-inner{position:relative;border-radius:21px;padding:38px 34px;background:radial-gradient(120% 100% at 20% 0%,#131722,#090b10 70%)}
.gb-inner .badge{display:inline-block;font:600 10px/1 ui-monospace,monospace;letter-spacing:.2em;text-transform:uppercase;color:#ffb08a;margin-bottom:20px}
.gb-inner h2{font-size:clamp(26px,4.4vw,38px);letter-spacing:-.035em;line-height:1.06}
.gb-inner p{color:#a3abbd;font-size:14px;line-height:1.7;margin:14px 0 26px}
.gb-inner form{display:flex;gap:8px;flex-wrap:wrap}
.gb-inner input{flex:1;min-width:180px;background:#ffffff0a;border:1px solid #ffffff1c;color:#eef1f7;border-radius:11px;padding:12px 14px;font:inherit;font-size:13px;outline:none}
.gb-inner input:focus{border-color:#ff8a5c88}
.gb-inner button{border:0;border-radius:11px;padding:12px 18px;background:#ff6b35;color:#120a05;font-weight:700;font-size:13px;cursor:pointer}
''',
html=r'''
<main class="gb-scene">
  <section class="gb-card">
    <div class="gb-inner">
      <span class="badge">Launch list</span>
      <h2>Get the first 500 invites.</h2>
      <p>A conic gradient rotates through a 1px border-box. The card body is an opaque gradient, so the colour can only escape at the edge.</p>
      <form onsubmit="event.preventDefault();this.querySelector('button').textContent='You\'re in ✓'">
        <input type="email" placeholder="you@company.com" required>
        <button type="submit">Request access</button>
      </form>
    </div>
  </section>
</main>
''',
js=r'''/* none — @property drives the angle in CSS */''',
hint="@property animates the conic angle; the border is a 1px transparent box showing through.",
),
dict(
id="tilt-3d", name="3D Tilt Card",
css=r'''
.tilt-scene{min-height:100vh;display:grid;place-items:center;padding:10vh 6vw;background:radial-gradient(90% 70% at 50% 0%,#151a26,#06070a 70%);perspective:1200px}
.tilt-wrap{perspective:1100px}
.tilt-card{position:relative;width:min(360px,86vw);height:470px;border-radius:22px;overflow:hidden;
background:linear-gradient(160deg,#1d2433,#0b0d13 72%);
border:1px solid #2b3446;box-shadow:0 50px 90px -30px #000;
transform-style:preserve-3d;transition:transform .18s ease-out;will-change:transform}
.tilt-card::before{content:"";position:absolute;inset:0;z-index:1;border-radius:inherit;
background:radial-gradient(circle at var(--gx,50%) var(--gy,50%),#ffffff30,transparent 55%)}
.tilt-card::after{content:"";position:absolute;left:0;right:0;bottom:0;height:60%;background:linear-gradient(transparent,#07080b);z-index:1}
.t-layer{position:absolute;z-index:2;transform-style:preserve-3d}
.t-top{top:22px;left:24px;right:24px;display:flex;justify-content:space-between;transform:translateZ(26px)}
.t-tag{font:600 10px/1 ui-monospace,monospace;letter-spacing:.2em;color:#7ee8fa}
.t-no{font:500 10px/1 ui-monospace,monospace;color:#7d879c}
.t-mid{top:44%;left:24px;right:24px;transform:translateZ(58px)}
.t-mid h2{font-size:34px;letter-spacing:-.03em;line-height:1.02}
.t-mid p{color:#9aa4b8;font-size:13px;margin-top:8px;line-height:1.5}
.t-bot{bottom:24px;left:24px;right:24px;transform:translateZ(40px);display:flex;justify-content:space-between;align-items:end}
.t-price{font:650 22px/1 ui-monospace,monospace}
.t-price span{font-size:11px;color:#8c96aa;font-weight:400}
.t-chip{font:600 10px/1 ui-monospace,monospace;letter-spacing:.14em;color:#ffb08a;border:1px solid #ff8a5c44;background:#ff6b3514;padding:7px 10px;border-radius:999px}
.t-hint{margin-top:26px;text-align:center;color:#69738a;font-size:12px}
''',
html=r'''
<main class="tilt-scene">
  <div>
    <div class="tilt-wrap">
      <article class="tilt-card" id="tilt">
        <div class="t-layer t-top"><span class="t-tag">HOLO / 001</span><span class="t-no">EDITION 1 OF 12</span></div>
        <div class="t-layer t-mid"><h2>Glacier Fox</h2><p>Archival pigment print, 60 × 90 cm</p></div>
        <div class="t-layer t-bot"><div class="t-price">€480 <span>incl. VAT</span></div><span class="t-chip">IN STOCK</span></div>
      </article>
    </div>
    <p class="t-hint">Move across the card — three layers move at different depths.</p>
  </div>
</main>
''',
js=r'''
const card=document.getElementById('tilt');
card.parentElement.addEventListener('pointermove',e=>{
  const r=card.getBoundingClientRect();
  const px=(e.clientX-r.left)/r.width, py=(e.clientY-r.top)/r.height;
  card.style.transform='rotateX('+((.5-py)*16).toFixed(2)+'deg) rotateY('+((px-.5)*20).toFixed(2)+'deg)';
  card.style.setProperty('--gx',(px*100).toFixed(1)+'%');
  card.style.setProperty('--gy',(py*100).toFixed(1)+'%');
});
card.parentElement.addEventListener('pointerleave',()=>{card.style.transform='rotateX(0) rotateY(0)'});
''',
hint="Pointer position drives rotation and a moving glare; layers sit at 26/40/58px of depth.",
),
dict(
id="bento-grid", name="Bento Grid",
css=r'''
.bento{min-height:100vh;padding:9vh 6vw;background:#07080c}
.bento-inner{max-width:1120px;margin:0 auto}
.bento-head{display:flex;justify-content:space-between;align-items:end;gap:24px;margin-bottom:34px;flex-wrap:wrap}
.bento-head h1{font-size:clamp(34px,5vw,58px);letter-spacing:-.045em;line-height:.98}
.bento-head p{color:#8f99ae;font-size:14px;max-width:34ch;line-height:1.6;margin:0}
.bento-grid{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:132px;gap:12px}
.tile{position:relative;border-radius:18px;border:1px solid #ffffff12;background:#0c0f16;padding:20px;overflow:hidden;transition:transform .3s cubic-bezier(.2,.7,.2,1),border-color .3s}
.tile:hover{transform:translateY(-4px);border-color:#ffffff2e}
.tile .k{font:600 10px/1 ui-monospace,monospace;letter-spacing:.18em;text-transform:uppercase;color:#6f7a91}
.tile h3{font-size:18px;letter-spacing:-.02em;margin-top:10px}
.tile p{font-size:12px;color:#8f99ae;line-height:1.55;margin-top:6px}
.t1{grid-column:span 2;grid-row:span 2;background:linear-gradient(150deg,#1a2233,#0b0e15 70%)}
.t2{grid-column:span 2}
.t3{grid-column:span 1}
.t4{grid-column:span 1}
.t5{grid-column:span 2}
.t6{grid-column:span 2}
.t1 h3{font-size:26px;max-width:16ch}
.t1 .orb{position:absolute;right:-30px;bottom:-40px;width:190px;height:190px;border-radius:50%;background:conic-gradient(from 40deg,#ff6b35,#7a5cff,#4d9fff,#ff6b35);filter:blur(18px);opacity:.75}
.t2 .bars{display:flex;align-items:end;gap:5px;height:44px;margin-top:12px}
.t2 .bars i{flex:1;background:linear-gradient(#4d9fff,#4d9fff33);border-radius:3px 3px 0 0}
.t3 .big{font:650 30px/1 ui-monospace,monospace;margin-top:14px}
.t4 .avatars{display:flex;margin-top:14px}
.t4 .avatars i{width:26px;height:26px;border-radius:50%;border:2px solid #0c0f16;margin-left:-7px;background:linear-gradient(135deg,#ff6b35,#7a5cff)}
.t4 .avatars i:first-child{margin-left:0}
.t5 .row{display:flex;justify-content:space-between;align-items:center;margin-top:12px;color:#aab3c4;font-size:12px}
.t5 .row b{color:#e8ecf5;font-weight:600}
@media(max-width:900px){.bento-grid{grid-template-columns:repeat(2,1fr);grid-auto-rows:124px}.t1,.t2,.t5,.t6{grid-column:span 2}.t5,.t6{grid-row:span 1}}
''',
html=r'''
<main class="bento">
  <div class="bento-inner">
    <div class="bento-head">
      <h1>Built from<br>unequal parts.</h1>
      <p>A 4-column, 132px-row grid. Tiles claim spans instead of equal widths — the layout reads as a composition, not a table.</p>
    </div>
    <section class="bento-grid">
      <article class="tile t1"><p class="k">Overview</p><div class="orb"></div><h3>Revenue up 38% this quarter.</h3><p>Asymmetric weight tells the eye where to start.</p></article>
      <article class="tile t2"><p class="k">Weekly volume</p><div class="bars"><i style="height:38%"></i><i style="height:62%"></i><i style="height:48%"></i><i style="height:80%"></i><i style="height:66%"></i><i style="height:96%"></i></div></article>
      <article class="tile t3"><p class="k">Active</p><div class="big">12.4k</div></article>
      <article class="tile t4"><p class="k">Team</p><div class="avatars"><i></i><i></i><i></i><i></i></div></article>
      <article class="tile t5"><p class="k">Next invoice</p><div class="row"><span>Acme Industries</span><b>€4,280 · Mar 14</b></div></article>
      <article class="tile t6"><p class="k">Latency</p><div class="row"><span>p95, last 24h</span><b>142 ms</b></div></article>
    </section>
  </div>
</main>
''',
js=r'''/* none — pure CSS grid */''',
hint="Column AND row spans on a 4-column grid. Hover lifts each tile by 4px.",
),
dict(
id="inset-neumorph", name="Inset Neumorph",
css=r'''
.neu{min-height:100vh;display:grid;place-items:center;padding:10vh 6vw;background:#15171c}
.panel{width:min(680px,94vw);border-radius:26px;padding:34px;background:#171a20;
box-shadow:18px 18px 40px #0a0b0e, -16px -16px 36px #242830;border:1px solid #ffffff08}
.panel h2{font-size:24px;letter-spacing:-.03em;margin-bottom:6px}
.panel .sub{color:#7f8899;font-size:13px;margin-bottom:28px}
.neu-row{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:26px}
.nbtn{appearance:none;border:0;border-radius:16px;background:#1a1d24;color:#c9d0dd;padding:22px 10px;font:inherit;font-size:12.5px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:10px;
box-shadow:8px 8px 18px #0b0c0f,-6px -6px 16px #24282f;transition:.16s}
.nbtn span{font-size:18px;color:#ff9b74}
.nbtn:hover{color:#fff}
.nbtn:active,.nbtn.on{box-shadow:inset 7px 7px 15px #0b0c0f,inset -6px -6px 14px #262b33;color:#ffb08a}
.nslide{height:14px;border-radius:999px;background:#15181d;box-shadow:inset 4px 4px 9px #0b0c0f,inset -4px -4px 9px #232730;position:relative;margin:6px 0 30px;cursor:pointer}
.nslide i{position:absolute;top:-6px;left:38%;width:26px;height:26px;border-radius:50%;background:#1d2128;box-shadow:5px 5px 11px #0b0c0f,-4px -4px 10px #2a2f38;border:1px solid #343a45}
.panel .meta{display:flex;justify-content:space-between;color:#6d7686;font-size:11.5px;font-family:ui-monospace,monospace}
''',
html=r'''
<main class="neu">
  <section class="panel">
    <h2>Studio controls</h2>
    <p class="sub">Every surface is the same colour. Depth comes only from paired light and shadow.</p>
    <div class="neu-row">
      <button class="nbtn on"><span>◐</span>Dim room</button>
      <button class="nbtn"><span>✦</span>Soft focus</button>
      <button class="nbtn"><span>⌁</span>Low latency</button>
    </div>
    <div class="nslide" role="slider" aria-label="Intensity"><i></i></div>
    <div class="meta"><span>INTENSITY 38</span><span>ROOM 2 · DESK</span></div>
  </section>
</main>
''',
js=r'''
document.querySelectorAll('.nbtn').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('.nbtn').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
}));
''',
hint="Same fill everywhere; pressed states invert the shadow pair. Click the buttons.",
),
dict(
id="marquee-band", name="Marquee Band",
css=r'''
.mq{min-height:100vh;display:flex;flex-direction:column;justify-content:center;gap:26px;padding:8vh 0;background:#08090d;overflow:hidden}
.mq-head{text-align:center;padding:0 6vw;margin-bottom:10px}
.mq-head p{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#ff8a5c;text-transform:uppercase;margin-bottom:16px}
.mq-head h1{font-size:clamp(32px,5vw,58px);letter-spacing:-.045em}
.band{position:relative;overflow:hidden;border-top:1px solid #ffffff12;border-bottom:1px solid #ffffff12;padding:18px 0;
-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.track{display:flex;width:max-content;gap:0;animation:slide 26s linear infinite;will-change:transform}
.band.rev .track{animation-direction:reverse;animation-duration:32s}
.band:hover .track{animation-play-state:paused}
.track span{display:inline-flex;align-items:center;gap:26px;padding:0 26px;font-size:clamp(22px,3.4vw,40px);letter-spacing:-.03em;white-space:nowrap;color:#e8ecf4}
.track span i{font-style:normal;color:#ff6b35;font-size:.55em}
.band.rev .track span{color:transparent;-webkit-text-stroke:1px #8a94a8;font-family:Georgia,serif}
.band.rev .track span i{-webkit-text-stroke:0;color:#4d9fff}
@keyframes slide{to{transform:translateX(-50%)}}
.mq-foot{text-align:center;color:#6d7686;font-size:12px;padding:0 6vw}
''',
html=r'''
<main class="mq">
  <div class="mq-head"><p>Motion / 11</p><h1>Say it until it sticks.</h1></div>
  <div class="band">
    <div class="track">
      <span>DESIGN SYSTEMS <i>✦</i> ART DIRECTION <i>✦</i> MOTION <i>✦</i> CODE <i>✦</i></span>
      <span>DESIGN SYSTEMS <i>✦</i> ART DIRECTION <i>✦</i> MOTION <i>✦</i> CODE <i>✦</i></span>
    </div>
  </div>
  <div class="band rev">
    <div class="track">
      <span>Amsterdam — Berlin — Lisbon — Tokyo — <i>◇</i> — Amsterdam — Berlin — Lisbon — Tokyo — <i>◇</i> —</span>
      <span>Amsterdam — Berlin — Lisbon — Tokyo — <i>◇</i> — Amsterdam — Berlin — Lisbon — Tokyo — <i>◇</i> —</span>
    </div>
  </div>
  <p class="mq-foot">Hover either band to pause. The track is duplicated once and translated −50%.</p>
</main>
''',
js=r'''/* none — pure CSS, hover pauses */''',
hint="Two duplicated tracks, opposite directions, edge masks. Hover pauses.",
),
dict(
id="split-text-reveal", name="Split-Text Reveal",
css=r'''
.split-scene{min-height:100vh;display:grid;place-items:center;padding:10vh 7vw;background:radial-gradient(80% 70% at 50% 10%,#12151f,#06070a 70%);text-align:center}
.split-copy{max-width:900px}
.split-scene .kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#ff8a5c;text-transform:uppercase;margin-bottom:26px}
.split-scene h1{font-size:clamp(40px,7.4vw,88px);line-height:.98;letter-spacing:-.05em;font-weight:640}
.word{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .06em}
.word > span{display:inline-block;transform:translateY(110%) rotate(4deg);opacity:0;animation:rise .9s cubic-bezier(.16,1,.3,1) forwards;animation-delay:calc(var(--i) * 90ms)}
@keyframes rise{to{transform:translateY(0) rotate(0);opacity:1}}
.split-scene p{color:#a3abbd;font-size:16px;line-height:1.7;max-width:54ch;margin:30px auto 34px;opacity:0;animation:fade .8s .75s forwards}
@keyframes fade{to{opacity:1}}
.replay{border:1px solid #ffffff26;background:#ffffff0d;color:#eef1f7;border-radius:999px;padding:12px 20px;font:500 13px/1 inherit;cursor:pointer}
.replay:hover{background:#ffffff18}
@media(prefers-reduced-motion:reduce){.word>span,.split-scene p{animation:none;transform:none;opacity:1}}
''',
html=r'''
<main class="split-scene">
  <div class="split-copy">
    <p class="kicker">Motion / 12 · staggered type</p>
    <h1 id="headline">Every word arrives on its own beat.</h1>
    <p>Each word is wrapped in an overflow-hidden span, then lifted from below with a 90ms stagger. Cheap, legible, and it survives a refresh.</p>
    <button class="replay" id="replay">↻ Replay</button>
  </div>
</main>
''',
js=r'''
const h=document.getElementById('headline');
const original=h.textContent;
function build(){
  h.innerHTML='';
  original.split(' ').forEach((w,i)=>{
    const outer=document.createElement('span');outer.className='word';
    const inner=document.createElement('span');inner.textContent=w;
    inner.style.setProperty('--i',i);
    inner.style.animation='none';
    outer.appendChild(inner);h.appendChild(outer);
    h.appendChild(document.createTextNode(' '));
  });
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    h.querySelectorAll('.word>span').forEach(s=>{s.style.animation='';});
  }));
}
build();
document.getElementById('replay').addEventListener('click',build);
''',
hint="Words are split at runtime and lifted with a 90ms stagger. Hit replay.",
),
dict(
id="scroll-parallax", name="Scroll Parallax",
css=r'''
html{scroll-behavior:smooth}
.px{position:relative;height:220vh;background:linear-gradient(#0a1020,#07080c 40%,#0c0a12)}
.px-sticky{position:sticky;top:0;height:100vh;overflow:hidden;display:grid;place-items:center}
.layer{position:absolute;inset:-12%;will-change:transform}
.l1{background:radial-gradient(50% 40% at 50% 68%,#ff6b3533,transparent 70%)}
.l2{background:radial-gradient(42% 34% at 62% 46%,#7a5cff38,transparent 70%)}
.l3{background-image:radial-gradient(#ffffff30 1px,transparent 1px);background-size:34px 34px;mask-image:radial-gradient(60% 55% at 50% 50%,#000,transparent 75%)}
.l4{display:grid;place-items:center}
.px-copy{position:relative;z-index:4;text-align:center;max-width:820px;padding:0 6vw}
.px-copy .kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#ff9b74;text-transform:uppercase;margin-bottom:22px}
.px-copy h1{font-size:clamp(40px,7vw,84px);line-height:.96;letter-spacing:-.05em;text-shadow:0 10px 60px #000}
.px-copy p{color:#aab3c6;margin-top:22px;line-height:1.7;font-size:15.5px}
.px-copy .depth{margin-top:26px;display:inline-block;font:500 11px/1 ui-monospace,monospace;color:#7f8aa0;border:1px solid #ffffff1a;padding:9px 14px;border-radius:999px}
.px-hint{position:absolute;bottom:26px;left:50%;transform:translateX(-50%);color:#5f6a80;font-size:11px;font-family:ui-monospace,monospace;letter-spacing:.1em}
''',
html=r'''
<main class="px">
  <div class="px-sticky">
    <div class="layer l1" data-speed=".18"></div>
    <div class="layer l2" data-speed="-.12"></div>
    <div class="layer l3" data-speed=".3"></div>
    <div class="layer l4"><div class="px-copy">
      <p class="kicker">Motion / 13 · depth on scroll</p>
      <h1>Three planes,<br>one scroll.</h1>
      <p>Each layer translates at its own rate — +0.18, −0.12 and +0.30 — inside a sticky viewport. The eye reads depth even though everything is flat.</p>
      <span class="depth" id="depth">scroll to change depth</span>
    </div></div>
    <span class="px-hint">SCROLL ↓</span>
  </div>
</main>
''',
js=r'''
const layers=[...document.querySelectorAll('.layer')];
const depth=document.getElementById('depth');
let ticking=false;
function update(){
  const y=window.scrollY;
  layers.forEach(l=>{l.style.transform='translate3d(0,'+(y*parseFloat(l.dataset.speed)).toFixed(1)+'px,0)';});
  depth.textContent='depth '+Math.round(y)+'px';
  ticking=false;
}
addEventListener('scroll',()=>{if(!ticking){requestAnimationFrame(update);ticking=true;}},{passive:true});
update();
''',
hint="Scroll inside the frame — three layers move at +0.18, −0.12 and +0.30.",
),
]
