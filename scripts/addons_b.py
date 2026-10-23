# Visual add-ons — part B (14-25)

ADDONS_B = [
dict(
id="magnetic-button", name="Magnetic Button",
css=r'''
.mag-scene{min-height:100vh;display:grid;place-items:center;padding:10vh 6vw;background:radial-gradient(70% 60% at 50% 20%,#141826,#06070a 70%);text-align:center}
.mag-copy{max-width:720px}
.mag-copy .kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#ff8a5c;text-transform:uppercase;margin-bottom:24px}
.mag-copy h1{font-size:clamp(36px,6vw,68px);line-height:.98;letter-spacing:-.05em}
.mag-copy p{color:#9fa8bb;margin:20px auto 44px;max-width:46ch;line-height:1.7;font-size:15px}
.mag-zone{display:inline-block;padding:70px}
.mag{position:relative;display:inline-flex;align-items:center;gap:12px;border:0;cursor:pointer;border-radius:999px;padding:20px 34px;background:#f2f4f8;color:#090a0e;font:650 15px/1 inherit;
transition:transform .25s cubic-bezier(.2,.8,.2,1),box-shadow .25s;box-shadow:0 18px 50px -18px #000000cc;will-change:transform}
.mag .arr{transition:transform .25s cubic-bezier(.2,.8,.2,1);font-size:16px}
.mag:hover .arr{transform:translateX(4px)}
.mag .ring{position:absolute;inset:-14px;border-radius:999px;border:1px solid #ffffff24;pointer-events:none;opacity:.6}
.mag-hint{margin-top:26px;color:#5f6a80;font-size:11px;font-family:ui-monospace,monospace;letter-spacing:.08em}
@media(prefers-reduced-motion:reduce){.mag{transition:none}}
''',
html=r'''
<main class="mag-scene">
  <div class="mag-copy">
    <p class="kicker">Motion / 14 · pointer gravity</p>
    <h1>The button leans<br>toward your cursor.</h1>
    <p>Within a 70px halo the control translates by up to 9px toward the pointer. Release and it springs home. The click target never moves.</p>
    <div class="mag-zone">
      <button class="mag" id="mag"><span>Start a project</span><span class="arr">→</span><span class="ring"></span></button>
    </div>
    <p class="mag-hint">MOVE WITHIN THE HALO</p>
  </div>
</main>
''',
js=r'''
const btn=document.getElementById('mag'), zone=btn.parentElement;
const strength=.22, max=9;
zone.addEventListener('pointermove',e=>{
  const r=btn.getBoundingClientRect();
  const cx=r.left+r.width/2, cy=r.top+r.height/2;
  const dx=Math.max(-max,Math.min(max,(e.clientX-cx)*strength));
  const dy=Math.max(-max,Math.min(max,(e.clientY-cy)*strength));
  btn.style.transform='translate('+dx.toFixed(1)+'px,'+dy.toFixed(1)+'px)';
});
zone.addEventListener('pointerleave',()=>{btn.style.transform='translate(0,0)'});
''',
hint="Move inside the halo — the button follows, then springs back on exit.",
),
dict(
id="count-up-stats", name="Count-Up Stats",
css=r'''
.count-scene{min-height:100vh;display:grid;place-items:center;padding:10vh 6vw;background:#07080c}
.count-inner{max-width:1000px;width:100%}
.count-head{text-align:center;margin-bottom:64px}
.count-head p{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#ff8a5c;text-transform:uppercase;margin-bottom:18px}
.count-head h1{font-size:clamp(32px,4.8vw,52px);letter-spacing:-.045em}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#ffffff12;border:1px solid #ffffff12;border-radius:20px;overflow:hidden}
.stat{background:#0a0c12;padding:38px 28px;text-align:center}
.stat .num{font:650 clamp(38px,6vw,64px)/1 ui-monospace,monospace;letter-spacing:-.05em;font-variant-numeric:tabular-nums;color:#f2f4f8}
.stat .num sup{font-size:.42em;color:#ff8a5c;top:-.7em;position:relative;letter-spacing:0}
.stat .lab{margin-top:12px;color:#8b95a9;font-size:12px;letter-spacing:.08em;text-transform:uppercase;font-family:ui-monospace,monospace}
.count-foot{text-align:center;margin-top:30px}
.count-foot button{border:1px solid #ffffff1f;background:#ffffff0d;color:#dfe4ee;border-radius:999px;padding:10px 18px;font:500 12px/1 inherit;cursor:pointer}
.count-foot button:hover{background:#ffffff18}
@media(max-width:760px){.stats{grid-template-columns:1fr}}
''',
html=r'''
<main class="count-scene">
  <div class="count-inner">
    <div class="count-head"><p>Motion / 15 · data entrance</p><h1>Numbers that land.</h1></div>
    <div class="stats" id="stats">
      <div class="stat"><div class="num" data-to="38" data-suffix="%">0</div><div class="lab">Faster handoff</div></div>
      <div class="stat"><div class="num" data-to="12.4" data-dec="1" data-suffix="k">0</div><div class="lab">Teams shipping</div></div>
      <div class="stat"><div class="num" data-to="4.9" data-dec="1" data-suffix="/5">0</div><div class="lab">Average rating</div></div>
    </div>
    <div class="count-foot"><button id="again">↻ Run again</button></div>
  </div>
</main>
''',
js=r'''
const nums=[...document.querySelectorAll('.num')];
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
function run(){
  if(reduce){nums.forEach(el=>{const suf=el.dataset.suffix||'';el.innerHTML=parseFloat(el.dataset.to).toFixed(+(el.dataset.dec||0))+(suf?'<sup>'+suf+'</sup>':'');});return;}
  nums.forEach(el=>{
    const to=parseFloat(el.dataset.to), dec=+(el.dataset.dec||0), suf=el.dataset.suffix||'';
    const t0=performance.now(), dur=1500;
    function tick(t){
      const p=Math.min(1,(t-t0)/dur), e=1-Math.pow(1-p,4);
      el.innerHTML=(to*e).toFixed(dec)+(suf?'<sup>'+suf+'</sup>':'');
      if(p<1)requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
}
new IntersectionObserver((es,o)=>{es.forEach(e=>{if(e.isIntersecting){run();o.disconnect();}})},{threshold:.4}).observe(document.getElementById('stats'));
document.getElementById('again').addEventListener('click',run);
''',
hint="IntersectionObserver fires once; easeOutQuart over 1.5s. Replay to watch again.",
),
dict(
id="duotone-image", name="Duotone Image",
css=r'''
.duo-scene{min-height:100vh;display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:5vw;padding:8vh 6vw;background:#08090d}
.duo-copy .kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#ff8a5c;text-transform:uppercase;margin-bottom:22px}
.duo-copy h1{font-size:clamp(34px,5vw,58px);line-height:1;letter-spacing:-.045em}
.duo-copy p{color:#a0a9bb;line-height:1.7;font-size:15px;margin-top:20px;max-width:42ch}
.duo-frame{position:relative;border-radius:22px;overflow:hidden;aspect-ratio:4/5;border:1px solid #ffffff16;box-shadow:0 40px 90px -30px #000}
.duo-frame svg{display:block;width:100%;height:100%;filter:grayscale(1) contrast(1.08)}
.duo-frame .wash{position:absolute;inset:0;background:#0b2a4a;mix-blend-mode:color;transition:opacity .5s}
.duo-frame .lift{position:absolute;inset:0;background:linear-gradient(150deg,#ff6b35,#ff2d78);mix-blend-mode:screen;opacity:.28;transition:opacity .5s}
.duo-frame:hover .wash{opacity:0}
.duo-frame:hover .lift{opacity:0}
.duo-frame .tag{position:absolute;left:18px;bottom:16px;z-index:3;font:600 10px/1 ui-monospace,monospace;letter-spacing:.16em;color:#fff;background:#00000066;border:1px solid #ffffff33;padding:8px 11px;border-radius:999px;backdrop-filter:blur(6px)}
.duo-frame .split{position:absolute;inset:0;z-index:2;pointer-events:none}
@media(max-width:860px){.duo-scene{grid-template-columns:1fr}.duo-frame{aspect-ratio:16/11;order:-1}}
''',
html=r'''
<main class="duo-scene">
  <div class="duo-copy">
    <p class="kicker">Texture / 16 · two-ink photography</p>
    <h1>One image.<br>Two inks.</h1>
    <p>Grayscale, a midnight-blue colour layer, then a warm screen wash. Hover to let the original photograph back through.</p>
  </div>
  <figure class="duo-frame">
    <svg viewBox="0 0 600 750" preserveAspectRatio="xMidYMid slice" aria-label="Abstract mountain landscape">
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe6ef"/><stop offset=".62" stop-color="#9fb0c4"/><stop offset="1" stop-color="#5e6d80"/></linearGradient>
        <linearGradient id="mtn" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5d6b7c"/><stop offset="1" stop-color="#1d2633"/></linearGradient>
      </defs>
      <rect width="600" height="750" fill="url(#sky)"/>
      <circle cx="430" cy="190" r="86" fill="#f5f1e6" opacity=".9"/>
      <path d="M0 520 L150 340 L260 470 L360 300 L520 520 L600 440 L600 750 L0 750Z" fill="url(#mtn)"/>
      <path d="M0 610 L120 500 L250 610 L400 470 L600 640 L600 750 L0 750Z" fill="#121a24" opacity=".9"/>
      <rect y="700" width="600" height="50" fill="#0b1119"/>
    </svg>
    <div class="wash"></div><div class="lift"></div>
    <span class="tag">HOVER TO DECODE</span>
  </figure>
</main>
''',
js=r'''/* none — blend modes do the work */''',
hint="Grayscale + colour blend + screen wash. Hover reveals the source image.",
),
dict(
id="halftone-overlay", name="Halftone Overlay",
css=r'''
.half-scene{position:relative;min-height:100vh;display:grid;place-items:center;overflow:hidden;background:#08090d;padding:8vh 6vw}
.half-art{position:absolute;inset:0;display:grid;place-items:center;overflow:hidden}
.half-art svg{width:min(78vh,90vw);height:min(78vh,90vw);filter:grayscale(1) contrast(1.15)}
.half-dots{position:absolute;inset:0;pointer-events:none;
background-image:radial-gradient(#ff6b35 1.6px,transparent 1.7px);
background-size:var(--pitch,7px) var(--pitch,7px);
mix-blend-mode:multiply;opacity:.72;
-webkit-mask-image:radial-gradient(60% 60% at 50% 50%,#000 8%,#0000 76%);
mask-image:radial-gradient(60% 60% at 50% 50%,#000 8%,#0000 76%);
transition:background-size .2s}
.half-copy{position:relative;z-index:3;text-align:center;pointer-events:none}
.half-copy .kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#ff8a5c;text-transform:uppercase;margin-bottom:20px}
.half-copy h1{font-size:clamp(40px,7vw,84px);line-height:.94;letter-spacing:-.05em;text-shadow:0 6px 40px #000}
.half-bar{position:fixed;bottom:22px;left:50%;transform:translateX(-50%);z-index:5;display:flex;align-items:center;gap:12px;background:#0b0d13e6;border:1px solid #ffffff1f;border-radius:999px;padding:9px 16px;font:500 11px/1 ui-monospace,monospace;color:#aab3c4;backdrop-filter:blur(8px)}
.half-bar input{accent-color:#ff6b35}
''',
html=r'''
<main class="half-scene">
  <div class="half-art">
    <svg viewBox="0 0 600 600" aria-label="Abstract face study">
      <defs><radialGradient id="glow" cx=".42" cy=".36" r=".7"><stop offset="0" stop-color="#f7f3e8"/><stop offset="1" stop-color="#6c7787"/></radialGradient></defs>
      <rect width="600" height="600" fill="#0d1118"/>
      <circle cx="300" cy="300" r="235" fill="url(#glow)"/>
      <ellipse cx="300" cy="285" rx="128" ry="160" fill="#d8d2c4"/>
      <path d="M172 300 Q152 150 300 126 Q448 150 428 300 Q420 210 300 196 Q180 210 172 300Z" fill="#1a222e"/>
      <ellipse cx="252" cy="276" rx="17" ry="10" fill="#141a22"/><ellipse cx="348" cy="276" rx="17" ry="10" fill="#141a22"/>
      <path d="M266 344 Q300 372 334 344" stroke="#141a22" stroke-width="9" fill="none" stroke-linecap="round"/>
      <path d="M300 292 L286 332 Q300 340 314 332" stroke="#8d8575" stroke-width="7" fill="none" stroke-linecap="round"/>
      <path d="M120 600 Q180 470 300 462 Q420 470 480 600Z" fill="#232c3a"/>
    </svg>
  </div>
  <div class="half-dots" id="dots"></div>
  <div class="half-copy">
    <p class="kicker">Texture / 17 · print screen</p>
    <h1>Dot gain,<br>on purpose.</h1>
  </div>
  <div class="half-bar"><span>PITCH</span><input id="pitch" type="range" min="4" max="14" value="7"><span id="pv">7px</span></div>
</main>
''',
js=r'''
const dots=document.getElementById('dots'), pitch=document.getElementById('pitch'), pv=document.getElementById('pv');
pitch.addEventListener('input',()=>{dots.style.setProperty('--pitch',pitch.value+'px');pv.textContent=pitch.value+'px';});
''',
hint="Drag the pitch slider — the dot screen is a single masked radial-gradient.",
),
dict(
id="outline-type", name="Outline Type",
css=r'''
.ot-scene{min-height:100vh;display:flex;flex-direction:column;justify-content:center;padding:9vh 7vw;background:#f1efe9;color:#111;overflow:hidden}
.ot-scene .top{display:flex;justify-content:space-between;align-items:center;font:600 10px/1 ui-monospace,monospace;letter-spacing:.18em;text-transform:uppercase;color:#6b675e;margin-bottom:6vh}
.ot-scene .top b{color:#c94020}
.ot-type{font-size:clamp(64px,15vw,210px);line-height:.8;letter-spacing:-.06em;font-weight:800;text-transform:uppercase;user-select:none}
.ot-line{display:block;white-space:nowrap;transition:.35s cubic-bezier(.2,.8,.2,1)}
.ot-line.out{color:transparent;-webkit-text-stroke:2px #14120f;text-stroke:2px #14120f}
.ot-line.out:hover{color:#c94020;-webkit-text-stroke-color:#c94020;transform:translateX(14px)}
.ot-line.solid:hover{color:transparent;-webkit-text-stroke:2px #14120f;transform:translateX(-14px)}
.ot-meta{display:flex;justify-content:space-between;gap:20px;border-top:1px solid #14120f33;padding-top:18px;margin-top:7vh;color:#5d594f;font-size:13px;flex-wrap:wrap}
.ot-meta span{max-width:38ch;line-height:1.6}
@media(prefers-reduced-motion:reduce){.ot-line{transition:none}}
''',
html=r'''
<main class="ot-scene">
  <div class="top"><span>Texture / 18 · type as image</span><span><b>viv</b>design</span></div>
  <div class="ot-type">
    <span class="ot-line out">Outline</span>
    <span class="ot-line solid">becomes</span>
    <span class="ot-line out">structure</span>
  </div>
  <div class="ot-meta">
    <span>Hover each line: hollow strokes fill, solid fills turn to stroke. 2px at any viewport because the unit is relative to the type.</span>
    <span>Used by magazines and record sleeves when there is no photograph worth printing.</span>
  </div>
</main>
''',
js=r'''/* none — pure CSS hover states */''',
hint="Hover the lines — fill and stroke swap in place.",
),
dict(
id="text-shimmer", name="Text Shimmer",
css=r'''
.shim-scene{min-height:100vh;display:grid;place-items:center;padding:10vh 7vw;background:#06070a;text-align:center;overflow:hidden}
.shim-copy{max-width:980px}
.shim-copy .kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#7f8aa3;text-transform:uppercase;margin-bottom:26px}
.shim-copy h1{font-size:clamp(44px,8vw,104px);line-height:.94;letter-spacing:-.055em;font-weight:650;
background:linear-gradient(100deg,#6f7788 18%,#ffffff 38%,#ffb08a 48%,#7fb2ff 58%,#6f7788 78%);
background-size:220% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;
animation:sweep 5.5s linear infinite}
@keyframes sweep{0%{background-position:120% 0}100%{background-position:-120% 0}}
.shim-copy p{color:#98a1b4;font-size:15.5px;line-height:1.7;max-width:52ch;margin:30px auto 0}
.shim-tags{display:flex;gap:8px;justify-content:center;margin-top:34px;flex-wrap:wrap}
.shim-tags span{font:500 11px/1 ui-monospace,monospace;color:#8d97aa;border:1px solid #ffffff17;padding:8px 12px;border-radius:999px}
@media(prefers-reduced-motion:reduce){.shim-copy h1{animation:none;background-position:50% 0}}
''',
html=r'''
<main class="shim-scene">
  <div class="shim-copy">
    <p class="kicker">Texture / 19 · gradient ink</p>
    <h1>Attention is a<br>moving target.</h1>
    <p>A four-stop gradient clipped to the glyphs, swept across 220% of the text width every 5.5 seconds. Static screens read it as foil.</p>
    <div class="shim-tags"><span>background-clip: text</span><span>220% width</span><span>5.5s linear</span></div>
  </div>
</main>
''',
js=r'''/* none — pure CSS */''',
hint="One gradient, clipped to text, sweeping 220% of its own width.",
),
dict(
id="editorial-dropcap", name="Editorial Drop Cap",
css=r'''
.drop-scene{min-height:100vh;display:grid;place-items:center;padding:8vh 6vw;background:#0a0908}
.paper{width:min(820px,94vw);background:#f6f1e7;color:#1c1812;border-radius:6px;padding:clamp(28px,5vw,64px);box-shadow:0 50px 110px -40px #000,inset 0 0 0 1px #ffffff}
.paper .kicker{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #1c181226;padding-bottom:12px;margin-bottom:34px;font:600 9.5px/1 ui-monospace,monospace;letter-spacing:.2em;text-transform:uppercase;color:#8a8171}
.paper .kicker b{color:#c94020}
.paper h1{font-family:Georgia,"Times New Roman",serif;font-weight:400;font-size:clamp(34px,5.6vw,60px);line-height:1.02;letter-spacing:-.025em;margin-bottom:8px}
.paper .stand{font-family:Georgia,serif;font-style:italic;color:#6b6355;font-size:17px;margin-bottom:30px}
.paper .body{column-count:2;column-gap:34px;font-family:Georgia,"Times New Roman",serif;font-size:15.5px;line-height:1.72}
.paper .body p{margin:0 0 14px;text-align:justify;hyphens:auto}
.paper .body p:first-child::first-letter{float:left;font-size:4.9em;line-height:.82;padding:.06em .1em 0 0;color:#c94020;font-weight:400}
.paper .body p:first-child::first-line{font-variant:small-caps;letter-spacing:.02em}
.paper .pull{break-inside:avoid;border-top:1px solid #1c181226;border-bottom:1px solid #1c181226;margin:8px 0 18px;padding:14px 0;font-family:Georgia,serif;font-style:italic;font-size:19px;line-height:1.35;color:#3a332a}
.paper .foot{border-top:1px solid #1c181226;margin-top:30px;padding-top:12px;font:500 10px/1.5 ui-monospace,monospace;letter-spacing:.08em;color:#8a8171;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
@media(max-width:700px){.paper .body{column-count:1}}
''',
html=r'''
<main class="drop-scene">
  <article class="paper">
    <div class="kicker"><span>Field notes · issue 12</span><b>The quiet layer</b></div>
    <h1>What a page remembers after you leave.</h1>
    <p class="stand">On texture, rhythm, and the details nobody screenshots.</p>
    <div class="body">
      <p>The first thing a reader feels is not the headline. It is the measure — how far the eye travels before it is asked to turn. Set that line too long and the page becomes a chore; too short and it stutters. A drop cap buys back the altitude the opening needs.</p>
      <p>Typography is the only material a website is actually made of. Everything else — the photography, the gradients, the motion — is a guest in the house that type built. That is why a single well-set paragraph can carry more authority than a hero section.</p>
      <blockquote class="pull">“Hierarchy is a promise that the page keeps or breaks.”</blockquote>
      <p>Notice the small caps on the first line, the hanging punctuation, the rules that behave like breathing marks. None of these are visible as features. They are visible only as ease.</p>
    </div>
    <div class="foot"><span>vivDesign — Add-on 20</span><span>Georgia · 15.5 / 1.72 · 34px gutter</span></div>
  </article>
</main>
''',
js=r'''/* none — print typography in CSS */''',
hint="Drop cap, small-caps first line, two columns, hairline rules — no JavaScript.",
),
dict(
id="custom-cursor", name="Custom Cursor",
css=r'''
.cursor-scene{min-height:100vh;padding:10vh 7vw;background:#07080c;cursor:none;overflow:hidden}
.cursor-scene a,.cursor-scene button,.cursor-scene .target{cursor:none}
.cursor-scene .kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#ff8a5c;text-transform:uppercase;margin-bottom:22px}
.cursor-scene h1{font-size:clamp(38px,6vw,72px);line-height:.98;letter-spacing:-.05em;max-width:16ch}
.cursor-scene p.lede{color:#a0a9bb;max-width:50ch;line-height:1.7;margin-top:20px;font-size:15px}
.links{display:flex;gap:10px;flex-wrap:wrap;margin-top:44px}
.links a{text-decoration:none;color:#dfe4ee;border:1px solid #ffffff1f;background:#ffffff0a;padding:13px 20px;border-radius:999px;font-size:13px;transition:.2s}
.links a:hover{background:#ff6b351a;border-color:#ff6b3566;color:#ffb08a}
.dot,.ring{position:fixed;top:0;left:0;border-radius:50%;pointer-events:none;z-index:9999;translate:-50% -50%}
.dot{width:6px;height:6px;background:#ff8a5c}
.ring{width:34px;height:34px;border:1px solid #ffffff66;transition:width .2s,height .2s,background .2s,border-color .2s}
.ring.hot{width:58px;height:58px;background:#ff6b3522;border-color:#ff8a5c99}
.cursor-note{position:fixed;right:22px;bottom:20px;font:500 10px/1 ui-monospace,monospace;letter-spacing:.12em;color:#5e687d}
@media(pointer:coarse){.cursor-scene{cursor:auto}.cursor-scene a,.cursor-scene button{cursor:pointer}.dot,.ring{display:none}}
''',
html=r'''
<main class="cursor-scene" id="scene">
  <p class="kicker">Interaction / 21 · pointer identity</p>
  <h1>A cursor with a<br>little gravity.</h1>
  <p class="lede">A 6px dot tracks the pointer exactly; a 34px ring follows on a lerp and swells to 58px over anything clickable. Disabled on touch devices.</p>
  <div class="links">
    <a href="#" class="target">See the work</a>
    <a href="#" class="target">Read the studio notes</a>
    <a href="#" class="target">Start a project</a>
  </div>
  <span class="cursor-note">POINTER: FINE</span>
</main>
<div class="ring" id="ring"></div><div class="dot" id="dot"></div>
''',
js=r'''
if(matchMedia('(pointer:fine)').matches){
  const dot=document.getElementById('dot'), ring=document.getElementById('ring'), scene=document.getElementById('scene');
  let mx=innerWidth/2,my=innerHeight/2,rx=mx,ry=my;
  addEventListener('pointermove',e=>{
    mx=e.clientX;my=e.clientY;
    dot.style.left=mx+'px';dot.style.top=my+'px';
    const t=e.target.closest('a,button,.target');
    ring.classList.toggle('hot',!!t);
  });
  (function loop(){rx+=(mx-rx)*.16;ry+=(my-ry)*.16;ring.style.left=rx+'px';ring.style.top=ry+'px';requestAnimationFrame(loop)})();
  scene.addEventListener('pointerleave',()=>{ring.style.opacity=0;dot.style.opacity=0});
  scene.addEventListener('pointerenter',()=>{ring.style.opacity=1;dot.style.opacity=1});
}
''',
hint="Move the pointer — the dot is exact, the ring lags and expands over links.",
),
dict(
id="scroll-progress", name="Scroll Progress Rail",
css=r'''
.prog-scene{min-height:260vh;background:linear-gradient(#08090d,#0b0d14 40%,#08090d);padding:0 0 20vh}
.prog-bar{position:fixed;top:0;left:0;right:0;height:3px;background:#ffffff0d;z-index:20}
.prog-bar i{display:block;height:100%;width:100%;transform-origin:0 50%;transform:scaleX(0);
background:linear-gradient(90deg,#ff6b35,#ff2d78,#7a5cff,#4d9fff);box-shadow:0 0 18px #ff6b3588}
.rail{position:fixed;right:26px;top:50%;transform:translateY(-50%);z-index:20;display:flex;flex-direction:column;gap:16px;align-items:flex-end}
.rail button{appearance:none;border:0;background:none;display:flex;align-items:center;gap:9px;color:#6b768c;font:500 10px/1 ui-monospace,monospace;letter-spacing:.12em;cursor:pointer;padding:4px 0}
.rail button i{width:18px;height:1px;background:#ffffff33;transition:.25s}
.rail button.on{color:#ffb08a}
.rail button.on i{width:34px;background:#ff8a5c;box-shadow:0 0 10px #ff6b3588}
.prog-copy{padding:18vh 8vw 0;max-width:900px}
.prog-copy .kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#ff8a5c;text-transform:uppercase;margin-bottom:22px}
.prog-copy h1{font-size:clamp(40px,6.4vw,80px);line-height:.97;letter-spacing:-.05em}
.prog-copy p{color:#9fa8bb;line-height:1.75;font-size:15.5px;max-width:54ch;margin-top:24px}
.chapter{margin:26vh 8vw 0;max-width:640px;border-left:1px solid #ffffff14;padding-left:26px}
.chapter .n{font:600 10px/1 ui-monospace,monospace;letter-spacing:.18em;color:#6d7890;margin-bottom:12px}
.chapter h2{font-size:clamp(26px,3.4vw,38px);letter-spacing:-.03em;margin-bottom:10px}
.chapter p{color:#8f99ae;line-height:1.7;font-size:14.5px}
@media(max-width:700px){.rail{display:none}}
''',
html=r'''
<main class="prog-scene" id="prog">
  <div class="prog-bar"><i id="bar"></i></div>
  <nav class="rail">
    <button data-to="0" class="on"><span>Intro</span><i></i></button>
    <button data-to="1"><span>Surface</span><i></i></button>
    <button data-to="2"><span>Motion</span><i></i></button>
    <button data-to="3"><span>End note</span><i></i></button>
  </nav>
  <section class="prog-copy">
    <p class="kicker">Interaction / 22 · wayfinding</p>
    <h1>You always know<br>how far you are.</h1>
    <p>A 3px gradient rail fills from the top edge and a right-hand chapter list tracks the section in view. Both are driven by one scroll listener.</p>
  </section>
  <section class="chapter" id="c1"><p class="n">01 — Surface</p><h2>Progress is reassurance.</h2><p>Long pages lose people at the second fold. A visible measure of remaining distance is the cheapest retention tool on the page.</p></section>
  <section class="chapter" id="c2"><p class="n">02 — Motion</p><h2>The bar should never stutter.</h2><p>Write scroll position in a rAF callback, not inside the event. The rail stays composited on its own layer.</p></section>
  <section class="chapter" id="c3"><p class="n">03 — End note</p><h2>Finish the thought.</h2><p>When the bar is full, the reader is exactly where you asked them to be. That is the whole contract.</p></section>
</main>
''',
js=r'''
const bar=document.getElementById('bar'), chapters=[...document.querySelectorAll('.chapter')], railBtns=[...document.querySelectorAll('.rail button')];
let tick=false;
function upd(){
  const max=document.documentElement.scrollHeight-innerHeight;
  bar.style.transform='scaleX('+(max>0?scrollY/max:0)+')';
  let idx=0;chapters.forEach((c,i)=>{if(c.getBoundingClientRect().top<innerHeight*.45)idx=i+1;});
  railBtns.forEach((b,i)=>b.classList.toggle('on',i===Math.min(idx,3)));
  tick=false;
}
addEventListener('scroll',()=>{if(!tick){requestAnimationFrame(upd);tick=true;}},{passive:true});
railBtns.forEach(b=>b.addEventListener('click',()=>{
  const i=+b.dataset.to;
  (i===0?document.body:chapters[i-1]).scrollIntoView({behavior:'smooth'});
}));
upd();
''',
hint="Scroll — the top rail fills and the chapter list follows the section in view.",
),
dict(
id="condensing-nav", name="Condensing Nav",
css=r'''
.cn-scene{min-height:240vh;background:#07080c}
.cn-nav{position:fixed;top:0;left:0;right:0;z-index:30;display:flex;align-items:center;justify-content:space-between;gap:20px;
padding:26px 6vw;background:#07080c00;border-bottom:1px solid transparent;transition:padding .35s cubic-bezier(.2,.8,.2,1),background .35s,border-color .35s,backdrop-filter .35s}
.cn-nav.small{padding:12px 6vw;background:#080a10d9;border-bottom-color:#ffffff12;backdrop-filter:blur(16px)}
.cn-logo{font-weight:700;letter-spacing:-.03em;font-size:18px;transition:font-size .35s}
.cn-nav.small .cn-logo{font-size:15px}
.cn-logo em{font-style:normal;color:#ff8a5c}
.cn-links{display:flex;gap:26px;align-items:center}
.cn-links a{color:#9aa4b8;text-decoration:none;font-size:13px;transition:color .2s}
.cn-links a:hover{color:#fff}
.cn-cta{background:#f2f4f8;color:#090a0e;border-radius:999px;padding:10px 16px;font-size:12.5px;font-weight:650;text-decoration:none}
.cn-nav.small .cn-cta{padding:8px 14px}
.cn-hero{padding:22vh 7vw 12vh;max-width:1000px}
.cn-hero .kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#ff8a5c;text-transform:uppercase;margin-bottom:24px}
.cn-hero h1{font-size:clamp(44px,7.4vw,92px);line-height:.94;letter-spacing:-.055em}
.cn-hero p{color:#9fa8bb;line-height:1.7;max-width:50ch;margin-top:26px;font-size:16px}
.cn-body{height:140vh;padding:0 7vw;display:grid;place-items:start;color:#3f4759;font:500 11px/1 ui-monospace,monospace;letter-spacing:.14em}
@media(max-width:760px){.cn-links{display:none}}
''',
html=r'''
<main class="cn-scene">
  <header class="cn-nav" id="nav">
    <span class="cn-logo">north<em>.</em>studio</span>
    <nav class="cn-links"><a href="#">Work</a><a href="#">About</a><a href="#">Journal</a></nav>
    <a href="#" class="cn-cta">Book a call</a>
  </header>
  <section class="cn-hero">
    <p class="kicker">Interaction / 23 · persistent chrome</p>
    <h1>Chrome that<br>gets out of the way.</h1>
    <p>At rest the nav is transparent and generous. After 40px it condenses, blurs its backdrop, and draws a hairline. Scroll inside the frame.</p>
  </section>
  <div class="cn-body">SCROLL ↓</div>
</main>
''',
js=r'''
const nav=document.getElementById('nav');
addEventListener('scroll',()=>nav.classList.toggle('small',scrollY>40),{passive:true});
''',
hint="Scroll — the nav loses 14px of padding and gains a blurred backdrop.",
),
dict(
id="card-spotlight", name="Card Spotlight",
css=r'''
.cs-scene{min-height:100vh;padding:8vh 6vw;background:#06070a}
.cs-inner{max-width:1120px;margin:0 auto}
.cs-head{margin-bottom:40px}
.cs-head .kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#ff8a5c;text-transform:uppercase;margin-bottom:18px}
.cs-head h1{font-size:clamp(34px,5.2vw,60px);letter-spacing:-.045em;line-height:1}
.cs-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.cs-card{--mx:50%;--my:0%;position:relative;border-radius:18px;padding:26px;background:#0b0d13;border:1px solid #ffffff12;overflow:hidden;transition:transform .25s,border-color .25s}
.cs-card::before{content:"";position:absolute;inset:0;opacity:0;transition:opacity .25s;
background:radial-gradient(260px circle at var(--mx) var(--my),#ff6b3526,transparent 65%)}
.cs-card::after{content:"";position:absolute;inset:-1px;border-radius:inherit;padding:1px;opacity:0;transition:opacity .25s;
background:radial-gradient(220px circle at var(--mx) var(--my),#ff8a5c99,transparent 70%);
-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
.cs-card:hover{transform:translateY(-3px)}
.cs-card:hover::before,.cs-card:hover::after{opacity:1}
.cs-card .ico{position:relative;width:36px;height:36px;border-radius:10px;display:grid;place-items:center;background:#ffffff0a;border:1px solid #ffffff14;color:#ff9b74;margin-bottom:20px;font-size:15px}
.cs-card h3{position:relative;font-size:17px;letter-spacing:-.02em;margin-bottom:8px}
.cs-card p{position:relative;color:#8f99ae;font-size:13px;line-height:1.6;margin:0}
.cs-card .go{position:relative;display:inline-block;margin-top:18px;font:600 10px/1 ui-monospace,monospace;letter-spacing:.14em;color:#69738a}
.cs-card:hover .go{color:#ffb08a}
@media(max-width:880px){.cs-grid{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.cs-grid{grid-template-columns:1fr}}
''',
html=r'''
<main class="cs-scene">
  <div class="cs-inner">
    <div class="cs-head"><p class="kicker">Interaction / 24 · hover light</p><h1>Each card lights<br>where you point.</h1></div>
    <section class="cs-grid">
      <article class="cs-card"><div class="ico">◈</div><h3>Vector export</h3><p>Pointer position writes two percentages per card. The fill and the border glow share them.</p><span class="go">LEARN MORE →</span></article>
      <article class="cs-card"><div class="ico">⌗</div><h3>Token mapping</h3><p>One radial gradient at 260px; the border uses the same stops through a mask compositing trick.</p><span class="go">LEARN MORE →</span></article>
      <article class="cs-card"><div class="ico">✳</div><h3>Motion budget</h3><p>No layout reads in the move handler — only custom properties. The browser keeps it on the compositor.</p><span class="go">LEARN MORE →</span></article>
      <article class="cs-card"><div class="ico">◐</div><h3>Dark by default</h3><p>The effect is tuned for near-black surfaces, where a 15% warm wash reads as light.</p><span class="go">LEARN MORE →</span></article>
      <article class="cs-card"><div class="ico">◇</div><h3>Touch fallback</h3><p>Without a fine pointer the cards keep a static top-edge highlight instead of chasing.</p><span class="go">LEARN MORE →</span></article>
      <article class="cs-card"><div class="ico">⌁</div><h3>Zero dependencies</h3><p>Fourteen lines of pointer handling. No library, no canvas, no request.</p><span class="go">LEARN MORE →</span></article>
    </section>
  </div>
</main>
''',
js=r'''
document.querySelectorAll('.cs-card').forEach(card=>{
  card.addEventListener('pointermove',e=>{
    const r=card.getBoundingClientRect();
    card.style.setProperty('--mx',((e.clientX-r.left)/r.width*100).toFixed(1)+'%');
    card.style.setProperty('--my',((e.clientY-r.top)/r.height*100).toFixed(1)+'%');
  });
});
''',
hint="Move across the grid — every card carries its own light.",
),
dict(
id="success-burst", name="Success Burst",
css=r'''
.burst-scene{min-height:100vh;display:grid;place-items:center;padding:10vh 6vw;background:radial-gradient(70% 60% at 50% 30%,#12151f,#06070a 70%);text-align:center}
.burst-copy{max-width:620px}
.burst-copy .kicker{font:600 10px/1 ui-monospace,monospace;letter-spacing:.24em;color:#ff8a5c;text-transform:uppercase;margin-bottom:22px}
.burst-copy h1{font-size:clamp(34px,5.6vw,62px);line-height:1;letter-spacing:-.05em}
.burst-copy p{color:#9fa8bb;line-height:1.7;margin:20px auto 38px;max-width:44ch;font-size:15px}
.burst-wrap{position:relative;display:inline-block}
.save{border:0;cursor:pointer;border-radius:999px;padding:17px 30px;background:#ff6b35;color:#160a04;font:700 14px/1 inherit;transition:.25s;box-shadow:0 16px 46px -16px #ff6b35aa;position:relative;z-index:2}
.save:hover{background:#ff8256;transform:translateY(-1px)}
.save.done{background:#3ddc84;color:#04220f;box-shadow:0 16px 46px -16px #3ddc84aa}
.particles{position:absolute;inset:0;pointer-events:none;z-index:3}
.p{position:absolute;left:50%;top:50%;width:7px;height:7px;border-radius:2px;opacity:0;
animation:fly .95s cubic-bezier(.12,.7,.2,1) forwards}
@keyframes fly{
  0%{opacity:1;transform:translate(-50%,-50%) rotate(0) scale(1)}
  70%{opacity:1}
  100%{opacity:0;transform:translate(calc(-50% + var(--x)),calc(-50% + var(--y))) rotate(var(--r)) scale(.4)}
}
.burst-note{margin-top:26px;color:#5f6a80;font:500 10px/1 ui-monospace,monospace;letter-spacing:.14em}
@media(prefers-reduced-motion:reduce){.p{animation:none;display:none}}
''',
html=r'''
<main class="burst-scene">
  <div class="burst-copy">
    <p class="kicker">Interaction / 25 · micro-celebration</p>
    <h1>Small win,<br>made visible.</h1>
    <p>On success, 26 particles leave the button at randomised angles and gravity, while the control itself changes state and colour.</p>
    <div class="burst-wrap" id="wrap">
      <button class="save" id="save">Save changes</button>
      <div class="particles" id="particles"></div>
    </div>
    <p class="burst-note" id="note">CLICK TO COMPLETE</p>
  </div>
</main>
''',
js=r'''
const btn=document.getElementById('save'), wrap=document.getElementById('wrap'), field=document.getElementById('particles'), note=document.getElementById('note');
const colors=['#ff6b35','#ff2d78','#7a5cff','#4d9fff','#3ddc84','#ffd166'];
btn.addEventListener('click',()=>{
  if(btn.classList.contains('done')){btn.classList.remove('done');btn.textContent='Save changes';note.textContent='CLICK TO COMPLETE';return;}
  btn.classList.add('done');btn.textContent='✓ Saved';
  note.textContent='26 PARTICLES · 950MS';
  for(let i=0;i<26;i++){
    const p=document.createElement('i');p.className='p';
    const a=Math.random()*Math.PI*2, d=60+Math.random()*110;
    p.style.setProperty('--x',(Math.cos(a)*d).toFixed(1)+'px');
    p.style.setProperty('--y',(Math.sin(a)*d+30).toFixed(1)+'px');
    p.style.setProperty('--r',(Math.random()*540-270|0)+'deg');
    p.style.background=colors[i%colors.length];
    p.style.animationDelay=(Math.random()*.08).toFixed(2)+'s';
    field.appendChild(p);
    setTimeout(()=>p.remove(),1200);
  }
});
''',
hint="Click save — randomised particles, then the button settles into its success state.",
),
]
