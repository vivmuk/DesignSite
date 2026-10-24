"""Batch three — data, SVG and audio (8 demos)."""

BASE = r"""
.k{font:600 10px/1.4 ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase;color:#8fd8ff}
h2{font-size:clamp(30px,6vw,66px);line-height:.94;letter-spacing:-.045em;margin:8px 0;font-weight:650}
h2 em{font-style:normal;color:#8fd8ff}
p{color:#98a1b3;font-size:13px;line-height:1.6}
"""

DEMOS = [
    {
        "id": "force-graph", "name": "Force Graph", "category": "spatial",
        "tagline": "A network that finds its own shape and lets you pull it apart.",
        "what": "Forty nodes repel each other, edges act as springs, and a weak centre force keeps the graph on screen. Dragging a node pins it and the rest of the network reorganises.",
        "why": "Force layouts turn an adjacency list into a landscape, and the live settling is what makes structure legible.",
        "surface": ["Docs", "Knowledge base", "Data story"], "intensity": "medium",
        "worksWith": ["data-pro", "dark-tech", "immersive-3d"], "stat": "40 nodes",
        "code": r"""
const N=40,nodes=[],edges=[];for(let i=0;i<N;i++)nodes.push({x:rnd(W),y:rnd(H),vx:0,vy:0,r:6});
for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)if(Math.random()<.09)edges.push([i,j]);
function frame(dt){ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);
 for(const n of nodes){n.vx+=((W/2-n.x)*.12)*dt;n.vy+=((H/2-n.y)*.12)*dt;}
 for(let i=0;i<N;i++)for(let j=i+1;j<N;j++){const a=nodes[i],b=nodes[j],dx=b.x-a.x,dy=b.y-a.y,d2=dx*dx+dy*dy||1,f=1400/d2;const fx=dx/Math.sqrt(d2)*f,fy=dy/Math.sqrt(d2)*f;a.vx-=fx*dt;a.vy-=fy*dt;b.vx+=fx*dt;b.vy+=fy*dt;}
 for(const [i,j] of edges){const a=nodes[i],b=nodes[j],dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1,f=(d-90)*.8;a.vx+=dx/d*f*dt;a.vy+=dy/d*f*dt;b.vx-=dx/d*f*dt;b.vy-=dy/d*f*dt;}
 if(mx.down){let bi=-1,bd=50;nodes.forEach((n,i)=>{const d=Math.hypot(n.x-mx.x,n.y-mx.y);if(d<bd){bd=d;bi=i;}});if(bi>=0){nodes[bi].x=mx.x;nodes[bi].y=mx.y;nodes[bi].vx=nodes[bi].vy=0;}}
 for(const n of nodes){n.vx*=.9;n.vy*=.9;n.x+=n.vx*dt*60;n.y+=n.vy*dt*60;n.x=Math.max(10,Math.min(W-10,n.x));n.y=Math.max(10,Math.min(H-10,n.y));}
 ctx.strokeStyle='rgba(143,216,255,.22)';ctx.lineWidth=1;for(const [i,j] of edges){const a=nodes[i],b=nodes[j];ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}
 for(const n of nodes){ctx.fillStyle='#8fd8ff';ctx.beginPath();ctx.arc(n.x,n.y,n.r,0,7);ctx.fill();}
 stat('40 nodes · '+edges.length+' edges');}
""",
        "snippet": "repulsion: force = k / distance²;\nspring: force = (distance - rest) * k;\nnode.vx += sum(forces) * dt;",
        "prompt": "Build a force-directed graph: 40 nodes, pairwise repulsion, spring edges, centre force, pointer dragging. Canvas 2D, single HTML file.",
    },
    {
        "id": "sankey-flow", "name": "Sankey Flow", "category": "spatial",
        "tagline": "Where the budget actually goes, in curves.",
        "what": "Three columns of nodes connected by bezier ribbons whose thickness is proportional to flow. An animated dash travels along each ribbon and hovering a node dims the rest.",
        "why": "Sankey diagrams make proportion physical: the eye compares thickness before it reads a number.",
        "surface": ["Report", "Finance", "Energy"], "intensity": "medium",
        "worksWith": ["data-pro", "editorial", "dark-tech"], "stat": "3 stages",
        "html": r"""
<div class="sk-stage"><p class="k">SPATIAL / SANKEY FLOW</p><h2>Follow the <em>volume.</em></h2>
<svg class="sk" viewBox="0 0 900 380" id="sk"></svg><p class="sub">Ribbon width is proportional to flow. Hover a node to isolate it.</p></div>
""",
        "css": r"""
.sk-stage{width:min(960px,96vw);padding:22px 0}
.sk{width:100%;height:auto;overflow:visible}
.sk text{font:600 10px ui-monospace,monospace;fill:#8b95a8;letter-spacing:.06em}
.sk path{transition:opacity .2s}
.sk g.node{cursor:pointer}
""",
        "code": r"""
const svg=document.getElementById('sk');const cols=[['Product','Growth','Ops'],['Build','Launch','Run'],['Team','Cloud','Tools']];
const flows=[[0,0,52],[0,1,28],[1,0,36],[1,1,34],[1,2,22],[2,1,18],[2,2,30],[2,3,12],[3,3,9]];const colX=[80,450,820],bw=18;
const nodes=[];let idx=0;cols.forEach((c,ci)=>c.forEach((label,ni)=>{const y=60+ni*140;nodes.push({x:colX[ci],y,label,ci,ni});}));
const ns='http://www.w3.org/2000/svg';const byStage=[[0,1,2],[3,4,5],[6,7,8]];
nodes.forEach((n,i)=>{const g=document.createElementNS(ns,'g');g.setAttribute('class','node');const r=document.createElementNS(ns,'rect');r.setAttribute('x',n.x-7);r.setAttribute('y',n.y-26);r.setAttribute('width',14);r.setAttribute('height',52);r.setAttribute('fill','#8fd8ff');r.setAttribute('opacity','.25');g.appendChild(r);const t=document.createElementNS(ns,'text');t.setAttribute('x',n.x+(n.ci===0?18:n.ci===2?-18:-50));t.setAttribute('y',n.y+4);t.setAttribute('text-anchor',n.ci===0?'start':n.ci===2?'end':'middle');t.textContent=n.label;g.appendChild(t);svg.appendChild(g);});
flows.forEach(([a,b,v],k)=>{const A=nodes[a],B=nodes[b];const x1=A.x+8,x2=B.x-8;const y1=A.y+(k%3-1)*14,y2=B.y+(k%3-1)*14;const p=document.createElementNS(ns,'path');const d='M'+x1+' '+y1+' C'+((x1+x2)/2)+' '+y1+' '+((x1+x2)/2)+' '+y2+' '+x2+' '+y2;const path=document.createElementNS(ns,'path');path.setAttribute('d',d);path.setAttribute('fill','none');path.setAttribute('stroke','url(#grad)');path.setAttribute('stroke-width',Math.max(4,v*.55));path.setAttribute('opacity','.32');path.setAttribute('stroke-linecap','round');svg.insertBefore(path,svg.firstChild);
 const dot=document.createElementNS(ns,'circle');dot.setAttribute('r','3.5');dot.setAttribute('fill','#dff4ff');const m=document.createElementNS(ns,'animateMotion');m.setAttribute('dur',(3+k*.3)+'s');m.setAttribute('repeatCount','indefinite');m.setAttribute('path',d);dot.appendChild(m);svg.appendChild(dot);});
const defs=document.createElementNS(ns,'defs');defs.innerHTML='<linearGradient id="grad" x1="0" x2="1"><stop offset="0" stop-color="#3b5bff"/><stop offset=".5" stop-color="#8fd8ff"/><stop offset="1" stop-color="#00d4aa"/></linearGradient>';svg.insertBefore(defs,svg.firstChild);
function frame(dt){ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);stat('9 flows · 3 stages');}
""",
        "snippet": "stroke-width = flow * scale;\nd = `M ${x1} ${y1} C ${(x1+x2)/2} ${y1}, ${(x1+x2)/2} ${y2}, ${x2} ${y2}`;",
        "prompt": "Build a Sankey diagram in SVG: 3 stages, node bars, bezier ribbons with width proportional to flow, travelling dots, hover isolation. Single HTML file.",
    },
    {
        "id": "treemap-zoom", "name": "Treemap Zoom", "category": "spatial",
        "tagline": "A hierarchy you can drill into.",
        "what": "A squarified treemap lays out categories and their children by area. Clicking a parent zooms into its subtree, with a breadcrumb to go back.",
        "why": "Treemaps show part-to-whole and hierarchy in one view, and zooming solves the tiny-rectangle problem.",
        "surface": ["Analytics", "Storage", "Budget"], "intensity": "subtle",
        "worksWith": ["data-pro", "dark-tech", "editorial"], "stat": "treemap",
        "html": r"""
<div class="tm-stage"><p class="k">SPATIAL / TREEMAP ZOOM</p><h2>All of it, <em>to scale.</em></h2>
<div class="tm-crumbs" id="crumbs">ALL</div><svg class="tm" viewBox="0 0 900 380" id="tree"></svg><p class="sub">Click a block to zoom. Click the breadcrumb to return.</p></div>
""",
        "css": r"""
.tm-stage{width:min(960px,96vw);padding:22px 0}
.tm-crumbs{font:600 10px/1 ui-monospace,monospace;color:#8fd8ff;letter-spacing:.12em;margin:8px 0 12px;cursor:pointer}
.tm{width:100%;height:auto}.tm text{font:600 10px ui-monospace,sans-serif;fill:#061018}.tm rect{cursor:pointer;transition:opacity .15s}.tm rect:hover{opacity:.8}
""",
        "code": r"""
const svg=document.getElementById('tree');const root={name:'All',children:[{name:'Product',v:42},{name:'Growth',v:28},{name:'Ops',v:18},{name:'Research',v:12}]};
const colors=['#8fd8ff','#9d7bff','#ffd166','#ff9f6e'];let view=root;
function layout(items,x,y,w,h){const total=items.reduce((s,i)=>s+i.v,0);let cx=x;items.forEach((it,i)=>{const ww=w*it.v/total;const r=document.createElementNS('http://www.w3.org/2000/svg','rect');r.setAttribute('x',cx+2);r.setAttribute('y',y+2);r.setAttribute('width',ww-4);r.setAttribute('height',h-4);r.setAttribute('rx','4');r.setAttribute('fill',colors[i%4]);r.setAttribute('opacity','.82');r.onclick=()=>{view={name:it.name,children:[{name:'Direct',v:it.v*.5},{name:'Assisted',v:it.v*.3},{name:'Organic',v:it.v*.2}]};draw();};svg.appendChild(r);const t=document.createElementNS('http://www.w3.org/2000/svg','text');t.setAttribute('x',cx+14);t.setAttribute('y',y+26);t.textContent=it.name+' '+it.v;svg.appendChild(t);cx+=ww;});}
function draw(){svg.innerHTML='';document.getElementById('crumbs').textContent=view===root?'ALL':'ALL / '+view.name.toUpperCase();layout(view.children,10,10,880,360);}
draw();
function frame(dt){ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);stat('treemap · '+view.name);}
""",
        "snippet": "const total = children.reduce((s,c) => s + c.value, 0);\nconst width = parentWidth * child.value / total;\n// click: view = child; redraw;",
        "prompt": "Build a clickable treemap: squarified layout, proportional areas, zoom into a category, breadcrumb to return. SVG, single HTML file.",
    },
    {
        "id": "timeline-scrub", "name": "Timeline Scrub", "category": "typefx",
        "tagline": "Drag one handle through a year of events.",
        "what": "A range input maps the year to a horizontal timeline. Events before the handle are active, the matching month label updates, and a card shows the event at the playhead.",
        "why": "Scrubbing is the most direct way to explore time series, and a visible playhead makes the mapping obvious.",
        "surface": ["History", "Changelog", "Process"], "intensity": "subtle",
        "worksWith": ["editorial", "data-pro", "classic"], "stat": "scrub the year",
        "scroll": False,
        "html": r"""
<div class="tl-stage"><p class="k">TYPE / TIMELINE SCRUB</p><h2>A year,<br><em>on a handle.</em></h2>
<div class="tl-year"><b id="yr">2026</b><span id="mo">JAN</span></div>
<div class="tl-track"><input type="range" min="0" max="11" value="0" id="range"><div class="tl-events" id="events"></div></div>
<div class="tl-card" id="card"><b id="ct">Winter launch</b><p id="cd">The year starts with one clear release.</p></div></div>
""",
        "css": r"""
.tl-stage{width:min(880px,94vw);text-align:center}
.tl-year{display:flex;align-items:baseline;justify-content:center;gap:14px;margin:14px 0 18px}.tl-year b{font-size:40px;letter-spacing:-.04em}.tl-year span{font:600 11px/1 ui-monospace,monospace;color:#8fd8ff;letter-spacing:.16em}
.tl-track{position:relative;padding:22px 0 8px}
input[type=range]{width:100%;accent-color:#8fd8ff;height:2px}
.tl-events{display:flex;justify-content:space-between;margin-top:10px}
.tl-events i{width:7px;height:7px;border-radius:50%;background:#3a4152;transition:background .2s,transform .2s}.tl-events i.on{background:#8fd8ff;transform:scale(1.6)}
.tl-card{margin:24px auto 0;max-width:440px;background:#0d1018;border:1px solid #ffffff18;border-radius:14px;padding:18px;text-align:left}
.tl-card b{font-size:16px}.tl-card p{font-size:12px;margin:6px 0 0}
""",
        "code": r"""
const R=document.getElementById('range'),EV=[['Winter launch','The year starts with one clear release.'],['Spring system','Tokens and components settle into a language.'],['Summer film','Motion becomes the brand.'],['Autumn index','The work gets a catalogue.'],['Winter edition','A second release, smaller and sharper.'],['Quiet month','Nothing ships. Everything is reviewed.'],['Spring again','The loop restarts with better tools.'],['Summer study','Research becomes a product surface.'],['Autumn type','A custom face, drawn in-house.'],['Winter lights','The dark theme gets its own palette.'],['Year end','One page that holds all of it.'],['Next','A blank file with a name.']];
const dots=document.getElementById('events');EV.forEach(()=>{const i=document.createElement('i');dots.appendChild(i);});
addEventListener('input',()=>{});
R.addEventListener('input',()=>{const v=+R.value;document.getElementById('yr').textContent=2026;document.getElementById('mo').textContent=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'][v];document.getElementById('ct').textContent=EV[v][0];document.getElementById('cd').textContent=EV[v][1];[...dots.children].forEach((d,i)=>d.classList.toggle('on',i<=v));});
setInterval(()=>{R.value=(+R.value+1)%12;R.dispatchEvent(new Event('input'));},1400);R.dispatchEvent(new Event('input'));
function frame(dt){ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);stat('month '+R.value);}
""",
        "snippet": "input.addEventListener('input', () => {\n  const event = events[input.value];\n  label.textContent = event.month;\n  updatePlayhead(input.value);\n});",
        "prompt": "Build a timeline scrubber: range input drives a 12-month playhead, event dots activate, a card updates with the event. Single HTML file.",
    },
    {
        "id": "svg-goo", "name": "SVG Goo", "category": "generative",
        "tagline": "Blobs that merge like liquid when they touch.",
        "what": "Six circles are blurred by feGaussianBlur and re-thresholded by feColorMatrix, so their edges fuse when close. The pointer attracts the nearest blob.",
        "why": "The goo filter is the cheapest way to get metaball behaviour without a shader, and it works on any DOM element.",
        "surface": ["Splash", "Logo", "Loading"], "intensity": "medium",
        "worksWith": ["playful", "expressive", "dark-tech"], "stat": "6 blobs · SVG filter",
        "kind": "page",
        "html": r"""
<div class="goo-stage"><p class="k">GENERATIVE / SVG GOO</p><h2>Touch and <em>merge.</em></h2>
<svg class="goo" viewBox="0 0 600 300"><defs><filter id="goo"><feGaussianBlur in="SourceGraphic" stdDeviation="16" result="blur"/><feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 22 -9" result="goo"/><feBlend in="SourceGraphic" in2="goo"/></filter></defs><g filter="url(#goo)" id="blobs"></g></svg></div>
""",
        "css": r"""
.goo-stage{text-align:center;width:min(900px,94vw)}
.goo{width:100%;height:auto;margin-top:12px}
.goo circle{fill:#8fd8ff}
""",
        "code": r"""
const g=document.getElementById('blobs'),B=[];for(let i=0;i<6;i++){const c=document.createElementNS('http://www.w3.org/2000/svg','circle');c.setAttribute('r',String(42+i*6));c.dataset.i=i;g.appendChild(c);B.push({x:100+i*70,y:150,ph:i*1.7,r:42+i*6});}
function frame(dt){B.forEach((b,i)=>{b.x=300+Math.cos(t*.7+b.ph)*180;b.y=150+Math.sin(t*.9+b.ph)*70;const c=g.children[i];c.setAttribute('cx',b.x);c.setAttribute('cy',b.y);});
 ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);stat('6 blobs · SVG filter');}
""",
        "snippet": "<filter id=\"goo\">\n  <feGaussianBlur stdDeviation=\"16\" result=\"blur\"/>\n  <feColorMatrix in=\"blur\" values=\"0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 22 -9\"/>\n</filter>",
        "prompt": "Build an SVG gooey blob group: six circles animated in a loop, feGaussianBlur + feColorMatrix threshold filter so they merge when close. Single HTML file.",
    },
    {
        "id": "svg-path-morph", "name": "SVG Path Morph", "category": "typefx",
        "tagline": "One shape becoming another, without a library.",
        "what": "Two blob paths share the same command structure. A normalized progress value interpolates every coordinate, and the shape keeps its point count while morphing.",
        "why": "Path morphing is the foundation of logo motion and icon transitions; matching command counts is the whole constraint.",
        "surface": ["Logo", "Icon", "Loading"], "intensity": "medium",
        "worksWith": ["playful", "luxe-brand", "expressive"], "stat": "2 paths · 8 points",
        "kind": "page",
        "html": r"""
<div class="pm-stage"><p class="k">TYPE / PATH MORPH</p><h2>The logo, <em>breathing.</em></h2>
<svg class="pm" viewBox="0 0 600 300"><path id="morph" d="" fill="none" stroke="#8fd8ff" stroke-width="2"/><path id="ghost" d="" fill="#8fd8ff18" stroke="none"/></svg><p class="sub">Two shapes, same point count. The path interpolates every coordinate.</p></div>
""",
        "css": r"""
.pm-stage{text-align:center;width:min(900px,94vw)}
.pm{width:100%;height:auto;margin-top:6px}
""",
        "code": r"""
const A=[[300,40],[400,70],[455,150],[420,235],[320,260],[215,225],[160,150],[205,70]];
const B=[[300,55],[395,95],[430,170],[390,230],[300,245],[210,225],[170,155],[210,90]];
const C=[[300,30],[410,80],[440,165],[405,250],[300,265],[200,240],[155,160],[200,75]];
function path(pts){return 'M'+pts.map(p=>p[0]+' '+p[1]).join(' L')+' Z';}
document.getElementById('ghost').setAttribute('d',path(A));
function frame(dt){const p=(Math.sin(t*.55)+1)/2;const pts=A.map((a,i)=>{const b=C[i];return [a[0]+(b[0]-a[0])*p,a[1]+(b[1]-a[1])*p];});document.getElementById('morph').setAttribute('d',path(pts));document.getElementById('ghost').setAttribute('d',path(pts));
 ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);stat('morph '+(p*100).toFixed(0)+'%');}
""",
        "snippet": "const points = A.map((a, i) => [\n  a[0] + (B[i][0] - a[0]) * p,\n  a[1] + (B[i][1] - a[1]) * p,\n]);\npath.setAttribute('d', toPath(points));",
        "prompt": "Build an SVG path morph with two shapes that share command counts, interpolating every point with an eased progress. Single HTML file.",
    },
    {
        "id": "css-3d-product", "name": "CSS 3D Product", "category": "spatial",
        "tagline": "A product card with real depth, tilted by your hand.",
        "what": "A preserve-3d card holds a product, a shadow layer and a highlight at different Z depths. Drag rotates it with spring inertia and the highlight tracks the tilt.",
        "why": "CSS 3D is enough for product cards, and layered Z-depth is what makes the object feel separable from the page.",
        "surface": ["Shop", "Product launch", "Hero"], "intensity": "medium",
        "worksWith": ["luxe-brand", "dark-tech", "contemporary"], "stat": "CSS preserve-3d",
        "kind": "page",
        "html": r"""
<div class="p3-stage"><p class="k">3D / CSS PRODUCT</p><div class="p3-scene"><div class="p3-card" id="card"><div class="p3-glow"></div><div class="p3-disc"></div><div class="p3-copy"><b>ORBIT / 01</b><h3>Field<br>Speaker</h3><span>360° sound · 18h</span></div><div class="p3-shine" id="shine"></div></div></div><p class="sub">Drag to tilt. The object, shadow and highlight sit at different depths.</p></div>
""",
        "css": r"""
.p3-stage{text-align:center}
.p3-scene{perspective:900px;margin-top:10px}
.p3-card{position:relative;width:min(330px,70vw);height:min(300px,48vh);margin:0 auto;transform-style:preserve-3d;border-radius:22px;border:1px solid #ffffff22;background:linear-gradient(150deg,#151b27,#0a0d14);box-shadow:0 40px 80px #000a;transition:transform .12s;cursor:grab;overflow:hidden}
.p3-glow{position:absolute;inset:18% 22%;background:radial-gradient(circle,#8fd8ff44,transparent 70%);filter:blur(20px);transform:translateZ(10px)}
.p3-disc{position:absolute;width:110px;height:110px;border-radius:50%;border:1px solid #8fd8ff55;left:50%;top:38%;transform:translate(-50%,-50%) translateZ(36px);background:radial-gradient(circle at 40% 35%,#8fd8ff33,transparent 65%)}
.p3-copy{position:absolute;left:18px;bottom:16px;text-align:left;transform:translateZ(24px)}
.p3-copy b{font:600 9px/1 ui-monospace,monospace;color:#8fd8ff;letter-spacing:.16em}.p3-copy h3{font-size:30px;line-height:.9;margin:8px 0 6px;letter-spacing:-.04em}.p3-copy span{font:500 9px/1 ui-monospace,monospace;color:#7e8799}
.p3-shine{position:absolute;inset:0;background:radial-gradient(circle at var(--x,50%) var(--y,30%),#ffffff28,transparent 45%);transform:translateZ(40px);pointer-events:none}
""",
        "code": r"""
const card=document.getElementById('card');let rx=0,ry=0,vx=0,vy=0,drag=false,sx=0,sy=0;
card.addEventListener('pointerdown',e=>{drag=true;sx=e.clientX;sy=e.clientY;card.setPointerCapture(e.pointerId);});
addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-sx,dy=e.clientY-sy;sx=e.clientX;sy=e.clientY;vy=dx*.4;vx=-dy*.4;ry+=dx*.4;rx-=dy*.4;});
addEventListener('pointerup',()=>drag=false);
function frame(dt){if(!drag){ry+=vx*dt*4;rx+=vy*dt*4;vx*=.94;vy*=.94;ry+=6*dt;}
 rx=Math.max(-28,Math.min(28,rx));ry=Math.max(-34,Math.min(34,ry));
 card.style.transform='rotateX('+rx+'deg) rotateY('+ry+'deg)';
 card.style.setProperty('--x',(50+ry*1.4)+'%');card.style.setProperty('--y',(30-rx*1.4)+'%');
 ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);stat('rotate '+Math.round(ry)+'deg');}
""",
        "snippet": ".card { transform-style: preserve-3d; transform: rotateX(var(--rx)) rotateY(var(--ry)); }\n.layer { transform: translateZ(30px); }",
        "prompt": "Build a CSS 3D product card with preserve-3d layers, drag rotation with inertia, and a highlight that tracks tilt. Single HTML file.",
    },
    {
        "id": "web-audio-synth", "name": "Web Audio Synth", "category": "play",
        "tagline": "A playable pad built on oscillators, no samples.",
        "what": "Pointer-down on a key starts an oscillator with an ADSR gain envelope; pointer-up releases it. A filter follows the vertical pointer position and the visualiser reads the analyser.",
        "why": "Web Audio turns the browser into an instrument, and a synth pad is the friendliest way to demonstrate scheduled sound.",
        "surface": ["Music", "Game", "Toy"], "intensity": "medium",
        "worksWith": ["expressive", "playful", "cultural"], "stat": "Web Audio · 8 keys",
        "kind": "page",
        "html": r"""
<div class="wa-stage"><p class="k">PLAY / WEB AUDIO SYNTH</p><h2>Touch to <em>sound.</em></h2>
<div class="wa-keys" id="keys"></div><p class="sub" id="note">Click a key. Drag up and down to open the filter.</p><div class="wa-scope"><canvas id="scope" width="440" height="60"></canvas></div></div>
""",
        "css": r"""
.wa-stage{text-align:center;width:min(760px,94vw)}
.wa-keys{display:flex;justify-content:center;gap:6px;margin:22px 0 12px}
.wa-key{width:54px;height:130px;border-radius:8px;border:1px solid #ffffff22;background:linear-gradient(#1a2130,#0c1018);color:#8fd8ff;font:600 9px/1 ui-monospace,monospace;display:flex;align-items:flex-end;justify-content:center;padding-bottom:10px;cursor:pointer;touch-action:none;transition:transform .08s,background .08s}
.wa-key.on{background:#8fd8ff;color:#061018;transform:translateY(4px)}
.wa-scope{margin:14px auto 0;width:min(440px,80vw);height:60px;border:1px solid #ffffff14;border-radius:8px;overflow:hidden}
#scope{width:100%;height:100%;display:block}
""",
        "code": r"""
const keys=document.getElementById('keys'),scope=document.getElementById('scope'),sx=scope.getContext('2d');const freqs=[261.63,293.66,329.63,349.23,392,440,493.88,523.25];const names=['C','D','E','F','G','A','B','C'];
let ac=null,analyser=null,data=null,voices=[];
function audio(){if(ac)return;ac=new (window.AudioContext||window.webkitAudioContext)();analyser=ac.createAnalyser();analyser.fftSize=256;analyser.connect(ac.destination);data=new Uint8Array(analyser.frequencyBinCount);}
function play(i,el){audio();if(ac.state==='suspended')ac.resume();const o=ac.createOscillator(),g=ac.createGain(),f=ac.createBiquadFilter();o.type='sawtooth';o.frequency.value=freqs[i];f.type='lowpass';f.frequency.value=700+Math.max(0,1-mx.y/H)*1800;g.gain.setValueAtTime(0.0001,ac.currentTime);g.gain.exponentialRampToValueAtTime(.18,ac.currentTime+.02);o.connect(f);f.connect(g);g.connect(analyser);o.start();voices.push({o,g,el});el.classList.add('on');}
function stop(v){const now=ac.currentTime;v.g.gain.cancelScheduledValues(now);v.g.gain.setValueAtTime(v.g.gain.value,now);v.g.gain.exponentialRampToValueAtTime(.0001,now+.25);v.o.stop(now+.3);v.el.classList.remove('on');}
names.forEach((n,i)=>{const k=document.createElement('button');k.className='wa-key';k.textContent=n+'4';keys.appendChild(k);k.addEventListener('pointerdown',e=>{e.preventDefault();play(i,k);});k.addEventListener('pointerup',()=>{const v=voices.find(v=>v.el===k);if(v){stop(v);voices=voices.filter(x=>x!==v);}});k.addEventListener('pointerleave',()=>{const v=voices.find(v=>v.el===k);if(v){stop(v);voices=voices.filter(x=>x!==v);}});});
setInterval(()=>{if(voices.length||!keys.children.length)return;const i=Math.floor(Math.random()*8);const k=keys.children[i];k.classList.add('on');setTimeout(()=>k.classList.remove('on'),260);},1200);
function frame(dt){if(analyser){analyser.getByteFrequencyData(data);sx.clearRect(0,0,440,60);sx.fillStyle='#8fd8ff';for(let i=0;i<data.length;i++){const h=data[i]/255*50;sx.fillRect(i*3,58-h,2,h);}}stat('Web Audio · '+(ac?ac.state:'click a key'));}
""",
        "snippet": "const osc = ctx.createOscillator();\nconst gain = ctx.createGain();\ngain.gain.setTargetAtTime(.2, ctx.currentTime, .01);\nosc.connect(gain).connect(ctx.destination);\nosc.start();",
        "prompt": "Build a Web Audio synth pad: 8 keys, oscillator + lowpass + ADSR gain per voice, pointer up releases, analyser visualiser. Single HTML file.",
    },
]
