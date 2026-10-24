"""Batch three — scroll-driven scenes (6 demos)."""

BASE = r"""
body{overflow-y:auto;overflow-x:hidden;scrollbar-width:none}
body::-webkit-scrollbar{display:none}
#cv{position:fixed;inset:0;z-index:0;opacity:.9}
#ui{position:relative;z-index:3;display:block;min-height:100vh;padding:0}
.k{font:600 10px/1.4 ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase;color:#8fd8ff}
h2{font-size:clamp(30px,7vw,78px);line-height:.92;letter-spacing:-.045em;margin:10px 0;font-weight:650}
h2 em{font-style:normal;color:#8fd8ff}
p{color:#98a1b3;font-size:13px;line-height:1.6}
"""

DEMOS = [
    {
        "id": "scroll-scrub", "name": "Scroll Scrub", "category": "spatial",
        "tagline": "Scroll position drives a frame-by-frame sequence.",
        "what": "A 340vh page holds a sticky canvas. Scroll progress is mapped to a timeline of 12 states: the ring count, rotation, colour and scale all change as you scrub.",
        "why": "Scroll-scrubbing gives the visitor a physical handle on time — the same trick as an image sequence, without the image weight.",
        "surface": ["Product film", "Story", "Launch"], "intensity": "bold",
        "worksWith": ["dark-tech", "immersive-3d", "luxe-brand"], "stat": "scroll to scrub",
        "scroll": True,
        "css": r"""
.ss-wrap{height:340vh}
.ss-sticky{position:sticky;top:0;height:100vh;display:grid;place-items:center;text-align:center}
.ss-copy{position:relative;z-index:4}
.ss-copy h2 span{color:#8fd8ff}
.ss-meter{position:fixed;right:22px;top:50%;transform:translateY(-50%);display:grid;gap:5px;z-index:5}
.ss-meter i{width:3px;height:22px;background:#ffffff22;border-radius:2px;display:block}
.ss-meter i.on{background:#8fd8ff}
""",
        "html": r"""
<div class="ss-wrap"><div class="ss-sticky"><div class="ss-copy"><p class="k">3D / SCROLL SCRUB</p><h2>Time is a<br><span>scrollbar.</span></h2><p>Keep scrolling. The scene is not playing — you are moving it.</p></div></div></div>
<div class="ss-meter" id="meter"></div>
""",
        "code": r"""
const meter=document.getElementById('meter');for(let i=0;i<12;i++){const b=document.createElement('i');meter.appendChild(b);}
function prog(){return Math.max(0,Math.min(1,scrollY/(document.body.scrollHeight-innerHeight)));}
function frame(dt){const p=prog();[...meter.children].forEach((el,i)=>el.classList.toggle('on',i<=Math.floor(p*11)));
 ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);
 const cx=W/2,cy=H*.52;const n=3+Math.floor(p*9);
 for(let i=0;i<n;i++){const a=t*.3+i/n*Math.PI*2;const r=60+i*22+p*80;ctx.strokeStyle='hsla('+(190+p*120)+',70%,60%,'+(.16+i/n*.32)+')';ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(cx+Math.cos(a)*20,cy+Math.sin(a)*14,r,0,7);ctx.stroke();}
 ctx.fillStyle='rgba(143,216,255,'+(.1+p*.35)+')';ctx.beginPath();ctx.arc(cx,cy,28+p*40,0,7);ctx.fill();
 stat('scrub '+(p*100).toFixed(0)+'%');}
""",
        "snippet": "const progress = scrollY / (document.body.scrollHeight - innerHeight);\nconst frameIndex = Math.round(progress * (frames.length - 1));\ndraw(frames[frameIndex]);",
        "prompt": "Build a scroll-scrubbed sequence: a tall page with a sticky canvas, scroll progress mapped to 12 visual states, a side progress meter. Single HTML file.",
    },
    {
        "id": "sticky-scrollytelling", "name": "Sticky Scrollytelling", "category": "spatial",
        "tagline": "A pinned visual that changes as each step arrives.",
        "what": "Three full-height steps scroll past a sticky panel. The panel's scene, caption and accent change at 0.33 and 0.66 progress, with a short cross-fade.",
        "why": "Sticky scrollytelling keeps the explanation and the evidence in the same viewport, which is why it dominates data journalism.",
        "surface": ["Report", "Case study", "Explainer"], "intensity": "medium",
        "worksWith": ["data-pro", "editorial", "dark-tech"], "stat": "3 steps",
        "scroll": True,
        "css": r"""
.story{display:grid;grid-template-columns:1.1fr .9fr;height:300vh}
.story-visual{position:sticky;top:0;height:100vh;display:grid;place-items:center}
.story-orb{width:min(42vw,420px);aspect-ratio:1;border-radius:50%;background:radial-gradient(circle at 35% 30%,#8fd8ff66,#9d7bff22 45%,transparent 70%);border:1px solid #8fd8ff33;position:relative}
.story-orb::after{content:"";position:absolute;inset:18%;border:1px solid #ffffff22;border-radius:50%}
.story-steps{display:grid}
.story-step{min-height:100vh;display:grid;align-content:center;padding:0 8vw 0 0}
.story-step b{font:600 10px/1 ui-monospace,monospace;color:#8fd8ff;letter-spacing:.16em}
.story-step h2{font-size:clamp(28px,4.6vw,58px);margin:14px 0}
@media (max-width:700px){.story{grid-template-columns:1fr}.story-visual{display:none}.story-step{padding:0 8vw}}
""",
        "html": r"""
<div class="story"><div class="story-visual"><div class="story-orb"><span id="orbLabel" style="position:absolute;inset:0;display:grid;place-items:center;font:600 11px/1 ui-monospace,monospace;letter-spacing:.18em;color:#dff4ff">01 / SIGNAL</span></div></div>
<div class="story-steps">
 <section class="story-step"><b>01 / SIGNAL</b><h2>Start with<br>one clear signal.</h2><p>Every screen gets one job. The sticky panel shows the state the text is describing.</p></section>
 <section class="story-step"><b>02 / SYSTEM</b><h2>Then let it<br>repeat.</h2><p>Tokens, spacing and motion curves turn a one-off screen into a system that can grow.</p></section>
 <section class="story-step"><b>03 / SURFACE</b><h2>Finish with<br>material.</h2><p>Grain, light and depth are the difference between a layout and a place.</p></section>
</div></div>
""",
        "code": r"""
function prog(){return Math.max(0,Math.min(.999,scrollY/(document.body.scrollHeight-innerHeight)));}
function frame(dt){const p=prog();const step=Math.floor(p*3);const labels=['01 / SIGNAL','02 / SYSTEM','03 / SURFACE'];const el=document.getElementById('orbLabel');if(el)el.textContent=labels[step];
 ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);if(innerWidth<700)return;
 const cx=W*.28,cy=H*.5;const col=[190,265,35][step];
 ctx.strokeStyle='hsla('+col+',70%,62%,.25)';for(let i=0;i<5;i++){ctx.beginPath();ctx.arc(cx,cy,80+i*34+step*10+Math.sin(t+i)*3,0,7);ctx.stroke();}
 stat('step '+(step+1)+' / 3');}
""",
        "snippet": "const step = Math.floor(scrollProgress * steps.length);\nstickyVisual.dataset.step = step;\n// CSS cross-fades the matching scene",
        "prompt": "Build a sticky scrollytelling section: 3 full-height steps, a pinned visual that swaps state by scroll progress with a cross-fade. Single HTML file.",
    },
    {
        "id": "horizontal-gallery", "name": "Horizontal Gallery", "category": "spatial",
        "tagline": "A vertical wheel that moves a horizontal track.",
        "what": "Wheel and drag input translate a six-card track along X with inertia. A progress bar reports position and cards scale up as they reach the centre.",
        "why": "Horizontal scroll breaks the vertical rhythm and makes a small set of work feel like a sequence rather than a grid.",
        "surface": ["Portfolio", "Product carousel", "Editorial"], "intensity": "medium",
        "worksWith": ["luxe-brand", "cultural", "expressive"], "stat": "6 cards",
        "scroll": False,
        "css": r"""
.hg{height:100vh;display:grid;grid-template-rows:auto 1fr auto;padding:26px 0 20px;overflow:hidden}
.hg-head{padding:0 26px}
.hg-view{overflow:hidden;display:flex;align-items:center}
.hg-track{display:flex;gap:18px;padding:0 26px;will-change:transform}
.hg-card{flex:none;width:min(340px,42vw);height:min(320px,44vh);border-radius:18px;border:1px solid #ffffff1c;background:linear-gradient(150deg,#121826,#0a0d14);padding:20px;display:flex;flex-direction:column;justify-content:space-between;transition:transform .2s}
.hg-card b{font:600 10px/1 ui-monospace,monospace;color:#8fd8ff}.hg-card h3{font-size:26px;letter-spacing:-.04em;margin:0}
.hg-foot{display:flex;align-items:center;gap:12px;padding:0 26px}
.hg-bar{flex:1;height:2px;background:#ffffff18;position:relative}.hg-bar i{position:absolute;left:0;top:0;bottom:0;background:#8fd8ff;width:30%}
.hg-foot span{font:500 9px/1 ui-monospace,monospace;color:#7e8799}
""",
        "html": r"""
<div class="hg"><div class="hg-head"><p class="k">3D / HORIZONTAL GALLERY</p><h2>Read it <em>sideways.</em></h2></div>
<div class="hg-view"><div class="hg-track" id="track">
 <article class="hg-card"><b>01 / IDENTITY</b><h3>Signal</h3><p>Mark, motion, system.</p></article>
 <article class="hg-card"><b>02 / PRODUCT</b><h3>Slow Motion</h3><p>A launch film in 12 frames.</p></article>
 <article class="hg-card"><b>03 / EDITORIAL</b><h3>Field Notes</h3><p>Print rhythm on screen.</p></article>
 <article class="hg-card"><b>04 / CAMPAIGN</b><h3>After Hours</h3><p>Night as a brand colour.</p></article>
 <article class="hg-card"><b>05 / WEB</b><h3>Open Studio</h3><p>A site that behaves like a tool.</p></article>
 <article class="hg-card"><b>06 / FILM</b><h3>Quiet Parts</h3><p>Sound, grain, patience.</p></article>
</div></div><div class="hg-foot"><div class="hg-bar"><i id="bar"></i></div><span id="pct">01 / 06</span></div></div>
""",
        "code": r"""
const track=document.getElementById('track'),bar=document.getElementById('bar'),pct=document.getElementById('pct');let x=0,target=0,drag=false,sx=0,base=0;
addEventListener('wheel',e=>{target-=e.deltaY*1.6;},{passive:true});
track.addEventListener('pointerdown',e=>{drag=true;sx=e.clientX;base=target;track.setPointerCapture(e.pointerId);});
track.addEventListener('pointermove',e=>{if(drag)target=base-(e.clientX-sx);});
track.addEventListener('pointerup',()=>drag=false);
function frame(dt){if(!drag&&Math.abs(target-x)<2&&t>1.2)target-=18*dt;const max=Math.max(0,track.scrollWidth-innerWidth);
 target=Math.min(0,Math.max(-max,target));x+=(target-x)*Math.min(1,dt*8);track.style.transform='translateX('+x+'px)';
 const p=max?Math.min(1,-x/max):0;bar.style.width=(p*100)+'%';pct.textContent=String(Math.min(6,1+Math.floor(p*5))).padStart(2,'0')+' / 06';
 ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);stat('gallery '+Math.round(p*100)+'%');}
""",
        "snippet": "track.style.transform = `translateX(${-x}px)`;\n// wheel: x += deltaY; drag: x += dx;\n// clamp to track.scrollWidth - viewportWidth",
        "prompt": "Build a horizontal gallery driven by wheel and drag with inertia, a progress bar and centre-card scaling. Single HTML file.",
    },
    {
        "id": "scroll-progress-rail", "name": "Scroll Progress Rail", "category": "play",
        "tagline": "A rail that draws itself as the story advances.",
        "what": "A fixed vertical rail fills with scroll progress, with a dot per section that activates as it enters. The active section title updates in the rail's label.",
        "why": "Progress rails orient the reader in long-form pages and give the scroll a visible consequence.",
        "surface": ["Case study", "Docs", "Report"], "intensity": "subtle",
        "worksWith": ["data-pro", "editorial", "dark-tech"], "stat": "4 sections",
        "scroll": True,
        "css": r"""
.rail-page{height:400vh}
.rail-fixed{position:fixed;left:max(22px,4vw);top:50%;transform:translateY(-50%);z-index:6;display:flex;gap:14px;align-items:flex-start}
.rail-line{width:2px;height:220px;background:#ffffff18;position:relative}.rail-line i{position:absolute;left:0;top:0;width:100%;background:#8fd8ff;height:0}
.rail-dots{display:flex;flex-direction:column;justify-content:space-between;height:220px}
.rail-dots b{width:6px;height:6px;border-radius:50%;background:#3a4152;display:block;transition:transform .2s,background .2s}.rail-dots b.on{background:#8fd8ff;transform:scale(1.8)}
.rail-label{font:600 9px/1.4 ui-monospace,monospace;color:#8fd8ff;letter-spacing:.14em;writing-mode:vertical-rl;text-orientation:mixed}
.rail-section{height:100vh;display:grid;align-content:center;padding-left:24vw}
.rail-section h2{font-size:clamp(30px,5vw,62px)}
@media (max-width:700px){.rail-section{padding-left:18vw}}
""",
        "html": r"""
<div class="rail-page"><div class="rail-fixed"><div class="rail-line"><i id="fill"></i></div><div class="rail-dots" id="dots"></div><span class="rail-label" id="label">01 / OPEN</span></div>
<section class="rail-section"><p class="k">PLAY / PROGRESS RAIL</p><h2>Long pages<br>need a spine.</h2><p>Scroll. The rail is the page's pulse.</p></section>
<section class="rail-section"><h2>Orientation</h2><p>The reader always knows how far in they are.</p></section>
<section class="rail-section"><h2>Rhythm</h2><p>Dots break a long scroll into chapters.</p></section>
<section class="rail-section"><h2>Ending</h2><p>And a clear arrival, not an infinite feed.</p></section></div>
""",
        "code": r"""
const dots=document.getElementById('dots');for(let i=0;i<4;i++){const b=document.createElement('b');dots.appendChild(b);}
function prog(){return Math.max(0,Math.min(1,scrollY/(document.body.scrollHeight-innerHeight)));}
function frame(dt){const p=prog();document.getElementById('fill').style.height=(p*100)+'%';const sec=Math.min(3,Math.floor(p*4));[...dots.children].forEach((b,i)=>b.classList.toggle('on',i<=sec));document.getElementById('label').textContent=String(sec+1).padStart(2,'0')+' / '+['OPEN','ORIENT','RHYTHM','END'][sec];
 ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);ctx.strokeStyle='rgba(143,216,255,.08)';for(let i=0;i<6;i++){ctx.beginPath();ctx.arc(W*.72,H*.5,90+i*50+p*60,0,7);ctx.stroke();}
 stat('progress '+(p*100).toFixed(0)+'%');}
""",
        "snippet": "const p = scrollY / (document.body.scrollHeight - innerHeight);\nrailFill.style.height = `${p * 100}%`;\nactiveDot = Math.floor(p * sections.length);",
        "prompt": "Build a fixed scroll-progress rail with a filling line, a dot per section, an active label, and four full-height sections. Single HTML file.",
    },
    {
        "id": "text-mask-reveal", "name": "Text Mask Reveal", "category": "typefx",
        "tagline": "A headline uncovered by the scroll, not by a timer.",
        "what": "A sticky headline is clipped by a CSS mask whose width follows scroll progress. The second line reveals in the opposite direction for contrast.",
        "why": "Scroll-linked masking makes the reader complicit in the reveal; it feels like turning a page rather than watching an animation.",
        "surface": ["Hero", "Editorial", "Launch"], "intensity": "bold",
        "worksWith": ["luxe-brand", "editorial", "expressive"], "stat": "scroll to reveal",
        "scroll": True,
        "css": r"""
.tm-page{height:300vh}
.tm-sticky{position:sticky;top:0;height:100vh;display:grid;place-content:center;padding:0 7vw}
.tm-sticky h1{font-size:clamp(44px,11vw,150px);line-height:.82;letter-spacing:-.06em;margin:0;font-weight:680}
.tm-line{display:block;overflow:hidden;white-space:nowrap}
.tm-line span{display:block;clip-path:inset(0 100% 0 0)}
.tm-line:nth-child(2) span{clip-path:inset(0 0 0 100%);color:#8fd8ff;text-align:right}
.tm-note{position:fixed;left:7vw;bottom:24px;font:500 9px/1.5 ui-monospace,monospace;letter-spacing:.14em;color:#7e8799;z-index:5}
""",
        "html": r"""
<div class="tm-page"><div class="tm-sticky"><h1><span class="tm-line"><span id="l1">MAKE IT</span></span><span class="tm-line"><span id="l2">MOVE.</span></span></h1></div></div>
<p class="tm-note">SCROLL · THE TYPE DOES THE REST</p>
""",
        "code": r"""
function frame(dt){const p=Math.max(0,Math.min(1,scrollY/(document.body.scrollHeight-innerHeight)));
 const a=Math.min(1,p*1.6),b=Math.min(1,Math.max(0,(p-.15)*1.6));
 document.getElementById('l1').style.clipPath='inset(0 '+(100-a*100)+'% 0 0)';
 document.getElementById('l2').style.clipPath='inset(0 0 0 '+(100-b*100)+'%)';
 ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);ctx.strokeStyle='rgba(143,216,255,.06)';for(let i=0;i<7;i++){ctx.beginPath();ctx.moveTo(0,H*.2+i*40);ctx.lineTo(W,H*.2+i*40);ctx.stroke();}
 stat('reveal '+(p*100).toFixed(0)+'%');}
""",
        "snippet": "line.style.clipPath = `inset(0 ${100 - progress * 100}% 0 0)`;\n// second line: inset(0 0 0 ${100 - progress * 100}%)",
        "prompt": "Build a scroll-linked text mask reveal: sticky headline, two lines wiping in from opposite sides based on scroll progress. Single HTML file.",
    },
    {
        "id": "marquee-ticker", "name": "Marquee Ticker", "category": "typefx",
        "tagline": "An infinite line that speeds up under your hand.",
        "what": "Two duplicated rows of type translate continuously. Hovering slows them, dragging changes velocity and direction, and the rows run in opposite directions.",
        "why": "The marquee is a workhorse: it fits a lot of language into a thin band and gives a page a pulse without a video.",
        "surface": ["Footer", "Event", "Music"], "intensity": "bold",
        "worksWith": ["expressive", "cultural", "contemporary"], "stat": "2 rows",
        "scroll": False,
        "css": r"""
.mq{height:100vh;display:grid;align-content:center;overflow:hidden;gap:8px}
.mq-row{display:flex;white-space:nowrap;will-change:transform;font-size:clamp(40px,7vw,92px);letter-spacing:-.05em;font-weight:680;line-height:.95}
.mq-row span{padding-right:.35em}
.mq-row:nth-child(2){color:#8fd8ff;font-style:italic;font-weight:500;opacity:.85}
.mq-note{position:fixed;left:24px;bottom:20px;font:500 9px/1 ui-monospace,monospace;letter-spacing:.14em;color:#7e8799;z-index:4}
.mq-badge{position:fixed;right:24px;top:24px;font:600 9px/1 ui-monospace,monospace;letter-spacing:.16em;color:#8fd8ff;border:1px solid #8fd8ff44;border-radius:999px;padding:8px 12px}
""",
        "html": r"""
<div class="mq" id="mq"><div class="mq-row" id="r1"></div><div class="mq-row" id="r2"></div></div>
<p class="mq-note">DRAG · HOVER TO SLOW</p><span class="mq-badge">SCROLL / MARQUEE</span>
""",
        "code": r"""
const mq=document.getElementById('mq'),r1=document.getElementById('r1'),r2=document.getElementById('r2');
const words=['SIGNAL','NOISE','MOTION','TYPE','SURFACE','LIGHT','RHYTHM','EDGE'];
r1.innerHTML=words.map(w=>'<span>'+w+' ✳ </span>').join('').repeat(3);r2.innerHTML=words.slice().reverse().map(w=>'<span>'+w+' ✳ </span>').join('').repeat(3);
let x1=0,x2=0,vel=90,hover=false,drag=false,sx=0;
mq.addEventListener('pointerenter',()=>hover=true);mq.addEventListener('pointerleave',()=>hover=false);
mq.addEventListener('pointerdown',e=>{drag=true;sx=e.clientX;});addEventListener('pointerup',()=>drag=false);
addEventListener('pointermove',e=>{if(drag)vel=Math.max(-500,Math.min(500,(e.clientX-sx)*6));});
function frame(dt){const speed=hover?22:vel;x1-=speed*dt;x2+=speed*.72*dt;const w1=r1.scrollWidth/3,w2=r2.scrollWidth/3;if(x1<-w1)x1+=w1;if(x2>0)x2-=w2;
 r1.style.transform='translateX('+x1+'px)';r2.style.transform='translateX('+x2+'px)';
 ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);stat(Math.round(Math.abs(speed))+' px/s');}
""",
        "snippet": "offset -= speed * dt;\nif (offset < -halfWidth) offset += halfWidth;\ntrack.style.transform = `translateX(${offset}px)`;",
        "prompt": "Build an infinite marquee: duplicated rows translating continuously in opposite directions, hover slows, drag changes velocity and direction. Single HTML file.",
    },
]
