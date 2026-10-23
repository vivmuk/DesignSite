# Interactive visuals — part A (01-09)
# Full-bleed, pointer-driven pieces. Each is a working playground, not a mock.

ADDONS_A = [
dict(
id="voronoi-mosaic", name="Voronoi Mosaic",
css=r'''
body{overflow:hidden;background:#07080c}
#cv{position:fixed;inset:0;display:block;touch-action:none;cursor:crosshair}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud b{color:#ff8a5c;font-weight:600}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:12px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:9px 14px;backdrop-filter:blur(10px)}
.panel button{background:#171b24;border:1px solid #2a3040;color:#cdd4e1;border-radius:999px;padding:7px 12px;
font:500 11px/1 ui-monospace,monospace;cursor:pointer}
.panel button:hover{border-color:#ff8a5c;color:#fff}
''',
html=r'''
<canvas id="cv"></canvas>
<div class="hud"><span class="t">INTERACTIVE 01 · VORONOI MOSAIC</span>cells <b id="cells">0</b> · <b id="fps">60</b> fps · drag a seed</div>
<div class="panel"><button id="add">+ 12 seeds</button><button id="reset">Reset</button></div>
''',
js=r'''
const cv=document.getElementById('cv'), ctx=cv.getContext('2d');
let W=0,H=0,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
fit();addEventListener('resize',fit);
const mouse={x:-9999,y:-9999,down:false},drag={i:-1};
let sites=[];
function seed(n){
  sites=[];
  for(let i=0;i<n;i++)sites.push({x:Math.random()*W,y:Math.random()*H,vx:0,vy:0,h:Math.random()*360});
}
seed(110);
function clip(poly,ax,ay,nx,ny){
  const out=[];
  for(let i=0;i<poly.length;i++){
    const p=poly[i],q=poly[(i+1)%poly.length];
    const dp=(p[0]-ax)*nx+(p[1]-ay)*ny, dq=(q[0]-ax)*nx+(q[1]-ay)*ny;
    if(dp<=0)out.push(p);
    if(dp*dq<0){const t=dp/(dp-dq);out.push([p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t]);}
  }
  return out;
}
function cell(s){
  let poly=[[0,0],[W,0],[W,H],[0,H]];
  for(const o of sites){
    if(o===s)continue;
    const nx=o.x-s.x, ny=o.y-s.y;
    const mx=(s.x+o.x)/2, my=(s.y+o.y)/2;
    poly=clip(poly,mx,my,nx,ny);
    if(poly.length<3)break;
  }
  return poly;
}
function area(p){let a=0;for(let i=0;i<p.length;i++){const q=p[i],r=p[(i+1)%p.length];a+=q[0]*r[1]-r[0]*q[1];}return Math.abs(a)/2;}
cv.addEventListener('pointerdown',e=>{
  mouse.down=true;
  let best=-1,bd=26;
  sites.forEach((s,i)=>{const d=Math.hypot(s.x-e.clientX,s.y-e.clientY);if(d<bd){bd=d;best=i}});
  if(best>=0)drag.i=best;
  else {sites.push({x:e.clientX,y:e.clientY,h:Math.random()*360,vx:0,vy:0});}
});
addEventListener('pointerup',()=>{mouse.down=false;drag.i=-1});
addEventListener('pointermove',e=>{
  mouse.x=e.clientX;mouse.y=e.clientY;
  if(drag.i>=0){sites[drag.i].x=e.clientX;sites[drag.i].y=e.clientY;}
});
addEventListener('pointerleave',()=>{mouse.x=-9999});
document.getElementById('add').onclick=()=>{for(let i=0;i<12;i++)sites.push({x:Math.random()*W,y:Math.random()*H,h:Math.random()*360,vx:0,vy:0})};
document.getElementById('reset').onclick=()=>seed(110);
let last=performance.now(),fps=60;
function frame(t){
  const dt=Math.min((t-last)/1000,.05);last=t;fps+=(1/Math.max(dt,.001)-fps)*.05;
  ctx.fillStyle='#07080c';ctx.fillRect(0,0,W,H);
  for(const s of sites){
    if(Math.random()<.02){s.vx+=(Math.random()-.5)*6;s.vy+=(Math.random()-.5)*6;}
    s.vx*=.94;s.vy*=.94;s.x+=s.vx*.2;s.y+=s.vy*.2;
    const dx=s.x-mouse.x,dy=s.y-mouse.y,d=Math.hypot(dx,dy);
    if(d<150&&d>1){s.x+=dx/d*(150-d)*.03;s.y+=dy/d*(150-d)*.03;}
    s.x=Math.max(0,Math.min(W,s.x));s.y=Math.max(0,Math.min(H,s.y));
  }
  const PAL=['#ff5a1f','#c084fc','#3ddc84','#7fb2ff','#ffd166','#ff5c8a'];
  const drawn=[];
  for(const s of sites){
    const poly=cell(s);
    if(poly.length<3)continue;
    let cx=0,cy=0;for(const p of poly){cx+=p[0];cy+=p[1]}
    cx/=poly.length;cy/=poly.length;
    const a=area(poly);
    drawn.push({s,poly,a,cx,cy,r:Math.sqrt(a/Math.PI)});
  }
  const cols=[];
  drawn.forEach((c,i)=>{
    const used=new Set();
    for(let j=0;j<i;j++){
      const d=Math.hypot(c.cx-drawn[j].cx,c.cy-drawn[j].cy);
      if(d<(c.r+drawn[j].r)*1.5)used.add(cols[j]);
    }
    let k=0;while(k<PAL.length&&used.has(PAL[k]))k++;
    cols[i]=PAL[k%PAL.length];
  });
  drawn.forEach((c,i)=>{
    const poly=c.poly;
    ctx.beginPath();poly.forEach((p,j)=>j?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();
    ctx.fillStyle=cols[i];ctx.fill();
    ctx.fillStyle='rgba(0,0,0,'+(0.02+(i%3)*0.025).toFixed(3)+')';ctx.fill();
    ctx.strokeStyle='#07080c';ctx.lineWidth=1.4;ctx.stroke();
    const dr=Math.max(1.5,Math.min(3.4,c.r/22));
    ctx.beginPath();ctx.arc(c.s.x,c.s.y,dr+1.4,0,Math.PI*2);ctx.fillStyle='#07080c';ctx.fill();
    ctx.beginPath();ctx.arc(c.s.x,c.s.y,dr,0,Math.PI*2);ctx.fillStyle='#fff';ctx.fill();
  });
  const n=drawn.length;
  document.getElementById('cells').textContent=n;
  document.getElementById('fps').textContent=fps|0;
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Move to repel the seeds, drag one, or click empty space to add a cell.",
),
dict(
id="flow-field", name="Particle Flow Field",
css=r'''
body{overflow:hidden;background:#05060a}
#cv{position:fixed;inset:0;touch-action:none;cursor:crosshair}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:16px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:10px 18px;backdrop-filter:blur(10px)}
.panel label{display:flex;align-items:center;gap:8px;color:#8b95a8;font:500 10px/1 ui-monospace,monospace;letter-spacing:.08em}
.panel input{width:96px;accent-color:#ff6b35}
.panel button{background:#171b24;border:1px solid #2a3040;color:#cdd4e1;border-radius:999px;padding:7px 12px;
font:500 11px/1 ui-monospace,monospace;cursor:pointer}
.panel button:hover{border-color:#ff8a5c;color:#fff}
.hint{position:fixed;right:18px;bottom:22px;color:#3f4759;font:500 9px/1 ui-monospace,monospace;letter-spacing:.16em}
@media(max-width:700px){.panel{flex-wrap:wrap;justify-content:center;width:calc(100vw - 32px);border-radius:16px}}
''',
html=r'''
<canvas id="cv"></canvas>
<div class="hud"><span class="t">INTERACTIVE 02 · FLOW FIELD</span>particles <b id="n">3800</b> · <b id="fps">60</b> fps</div>
<div class="panel">
  <label>SPEED <input id="speed" type="range" min="20" max="220" value="90"></label>
  <label>CURL <input id="curl" type="range" min="0" max="300" value="150"></label>
  <button id="clear">Clear</button>
</div>
<span class="hint">MOVE TO STIR</span>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);ctx.fillStyle='#05060a';ctx.fillRect(0,0,W,H);}
fit();addEventListener('resize',fit);
const N=3800, pts=[];
document.getElementById('n').textContent=N;
for(let i=0;i<N;i++)pts.push({x:Math.random()*W,y:Math.random()*H,px:0,py:0,h:Math.random()*60+180});
const mouse={x:-9999,y:-9999};
addEventListener('pointermove',e=>{mouse.x=e.clientX;mouse.y=e.clientY});
addEventListener('pointerleave',()=>{mouse.x=-9999});
const speedEl=document.getElementById('speed'),curlEl=document.getElementById('curl');
let t=0,last=0,fps=60;
function tick(now){
  const dt=Math.min((now-last)/1000,.05);last=now;t+=dt;
  fps+=(1/Math.max(dt,.001)-fps)*.05;
  ctx.fillStyle='rgba(5,6,10,.026)';ctx.fillRect(0,0,W,H);
  const speed=+speedEl.value/100, curl=+curlEl.value/1000;
  ctx.lineWidth=2.2;
  for(const p of pts){
    p.px=p.x;p.py=p.y;
    const a=Math.sin(p.x*curl+t*.7)+Math.cos(p.y*curl*.9-t*.5)+Math.sin((p.x+p.y)*curl*.5);
    p.x+=Math.cos(a*1.6)*speed; p.y+=Math.sin(a*1.6)*speed;
    const dx=p.x-mouse.x,dy=p.y-mouse.y,d=Math.hypot(dx,dy);
    if(d<170&&d>1){p.x+=dx/d*(170-d)*.03;p.y+=dy/d*(170-d)*.03;}
    if(p.x<-20||p.x>W+20||p.y<-20||p.y>H+20||Math.random()<.0009){
      p.x=Math.random()*W;p.y=Math.random()*H;p.px=p.x;p.py=p.y;
    }
    ctx.strokeStyle='hsla('+(p.h+a*26)+',82%,70%,.78)';
    ctx.beginPath();ctx.moveTo(p.px,p.py);ctx.lineTo(p.x,p.y);ctx.stroke();
  }
  document.getElementById('fps').textContent=fps|0;
}
function frame(now){tick(now);requestAnimationFrame(frame)}
for(let k=1;k<=90;k++){last=k*16.7;tick(last)}
last=performance.now();
requestAnimationFrame(frame);
document.getElementById('clear').onclick=()=>{ctx.fillStyle='#05060a';ctx.fillRect(0,0,W,H)};
''',
hint="Move the pointer to stir the field; pull SPEED and CURL while it runs.",
),
dict(
id="generative-poster", name="Generative Poster Studio",
css=r'''
body{overflow:hidden;background:#0b0b0e}
.stage{position:fixed;inset:0;display:grid;place-items:center;padding:52px 20px 112px}
.poster{width:min(66vh,88vw);aspect-ratio:3/4;background:#f4f0e6;border-radius:4px;box-shadow:0 40px 100px -30px #000;
position:relative;overflow:hidden}
#cv{width:100%;height:100%;display:block}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:10px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:9px 12px;backdrop-filter:blur(10px)}
.panel button{background:#171b24;border:1px solid #2a3040;color:#cdd4e1;border-radius:999px;padding:8px 14px;
font:500 11px/1 ui-monospace,monospace;cursor:pointer}
.panel button:hover{border-color:#ff8a5c;color:#fff}
.panel button.primary{background:#f2f4f8;color:#0a0a0e;border-color:#f2f4f8;font-weight:700}
''',
html=r'''
<div class="stage"><div class="poster"><canvas id="cv" width="900" height="1200"></canvas></div></div>
<div class="hud"><span class="t">INTERACTIVE 03 · POSTER STUDIO</span>seed <b id="seed">000</b> · click the poster for a variation</div>
<div class="panel"><button class="primary" id="gen">Generate</button><button id="download">Download PNG</button></div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
const P={bg:'#f4f0e6',ink:'#14120f',a:'#ff5a1f',b:'#2b3cff',c:'#00a884'};
let seed=Math.floor(Math.random()*999);
function rng(s){return function(){s|=0;s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function draw(){
  const r=rng(seed+7);
  ctx.fillStyle=P.bg;ctx.fillRect(0,0,900,1200);
  const variant=Math.floor(r()*4);
  const accents=[P.a,P.b,P.c];
  ctx.save();
  if(variant===0){
    ctx.fillStyle=P.ink;ctx.fillRect(60,60,780,4);
    for(let i=0;i<7;i++){ctx.beginPath();ctx.arc(450,470,60+i*54+r()*20,0,Math.PI*2);ctx.strokeStyle=i%3===0?P.a:'#14120f33';ctx.lineWidth=i%3===0?22:2;ctx.stroke();}
    ctx.fillStyle=P.ink;ctx.font='800 150px system-ui,sans-serif';ctx.textAlign='center';ctx.fillText('FORM',450,930);
    ctx.fillStyle=P.a;ctx.fillText(String(seed).padStart(3,'0'),450,1070);
  }else if(variant===1){
    const cols=5,rows=7,gw=780/cols,gh=900/rows;
    for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){
      const v=r();
      if(v>.42){
        ctx.fillStyle=v>.8?accents[Math.floor(r()*3)]:P.ink;
        const pad=6;ctx.beginPath();ctx.roundRect(60+x*gw+pad,60+y*gh+pad,gw-pad*2,gh-pad*2,v>.9?999:0);ctx.fill();
      }
    }
    ctx.fillStyle=P.ink;ctx.font='700 44px system-ui,sans-serif';ctx.textAlign='left';ctx.fillText('GENERATIVE / '+String(seed).padStart(3,'0'),60,1050);
    ctx.fillStyle='#14120f88';ctx.font='500 18px ui-monospace,monospace';ctx.fillText('SYSTEMS · TYPE · COLOUR',60,1090);
  }else if(variant===2){
    ctx.fillStyle=accents[0];ctx.fillRect(0,0,900,700);
    for(let i=0;i<26;i++){
      ctx.beginPath();ctx.arc(r()*900,r()*700,20+r()*90,0,Math.PI*2);
      ctx.fillStyle=i%2?'#f4f0e6':'#14120f';ctx.globalAlpha=.9;ctx.fill();
    }
    ctx.globalAlpha=1;ctx.fillStyle=P.ink;ctx.font='800 120px system-ui,sans-serif';ctx.fillText('MORE',60,900);ctx.fillText('IS MORE',60,1020);
    ctx.fillStyle=accents[1];ctx.font='600 24px ui-monospace,monospace';ctx.fillText('EDITION '+String(seed).padStart(3,'0')+' / 250',62,1080);
  }else{
    for(let i=0;i<16;i++){
      ctx.save();ctx.translate(450,560);ctx.rotate(r()*Math.PI);
      ctx.fillStyle=i%3===0?accents[0]:(i%3===1?P.ink:accents[1]);
      ctx.fillRect(-360+(r()*140),-8,720,16);ctx.restore();
    }
    ctx.fillStyle=P.bg;ctx.beginPath();ctx.arc(450,560,190,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=P.ink;ctx.font='800 190px system-ui,sans-serif';ctx.textAlign='center';ctx.fillText('24',450,630);
    ctx.fillStyle=P.ink;ctx.font='700 32px system-ui,sans-serif';ctx.fillText('A STUDY IN ROTATION',450,1100);
  }
  ctx.restore();
  ctx.fillStyle='#14120f';ctx.font='500 16px ui-monospace,monospace';ctx.textAlign='left';
  ctx.fillText('VIV/POSTER PRESS · 2026',60,1150);
  document.getElementById('seed').textContent=String(seed).padStart(3,'0');
}
function generate(){seed=Math.floor(Math.random()*999);draw()}
document.getElementById('gen').onclick=generate;
document.getElementById('download').onclick=()=>{const a=document.createElement('a');a.download='poster-'+seed+'.png';a.href=cv.toDataURL('image/png');a.click()};
cv.addEventListener('click',generate);
draw();
''',
hint="Hit Generate, or click the poster. Download gives you the 900×1200 PNG.",
),
dict(
id="waveform-grid", name="Waveform Grid",
css=r'''
body{overflow:hidden;background:#06070b}
#cv{position:fixed;inset:0;touch-action:none}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:16px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:10px 18px;backdrop-filter:blur(10px)}
.panel label{display:flex;align-items:center;gap:8px;color:#8b95a8;font:500 10px/1 ui-monospace,monospace;letter-spacing:.08em}
.panel input{width:100px;accent-color:#7fb2ff}
''',
html=r'''
<canvas id="cv"></canvas>
<div class="hud"><span class="t">INTERACTIVE 04 · WAVEFORM GRID</span>lines <b id="n">48</b> · <b id="fps">60</b> fps</div>
<div class="panel">
  <label>AMPLITUDE <input id="amp" type="range" min="0" max="100" value="46"></label>
  <label>FREQUENCY <input id="freq" type="range" min="4" max="40" value="14"></label>
</div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
fit();addEventListener('resize',fit);
const mouse={x:-9999,y:-9999};
addEventListener('pointermove',e=>{mouse.x=e.clientX;mouse.y=e.clientY});
addEventListener('pointerleave',()=>{mouse.x=-9999});
const amp=document.getElementById('amp'),freq=document.getElementById('freq');
let t=0,last=performance.now(),fps=60;
function frame(now){
  const dt=Math.min((now-last)/1000,.05);last=now;t+=dt;
  fps+=(1/Math.max(dt,.001)-fps)*.05;
  ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);
  const lines=48, gap=H/(lines+1), A=+amp.value/100, F=+freq.value*.001;
  for(let l=0;l<lines;l++){
    const y0=gap*(l+1);
    const near=mouse.y<0?0:Math.max(0,1-Math.abs(y0-mouse.y)/260);
    ctx.beginPath();
    for(let x=-20;x<=W+20;x+=8){
      const wave=Math.sin(x*F+t*1.1+l*.22)*A*46 + Math.sin(x*F*.47-t*.7)*A*22;
      const dy=mouse.x<0?0:Math.exp(-Math.pow((x-mouse.x)/160,2))*near*Math.sin(t*4+x*.01)*54;
      const y=y0+wave+dy;
      x===-20?ctx.moveTo(x,y):ctx.lineTo(x,y);
    }
    const hot=near>.15;
    ctx.strokeStyle=hot?'rgba(160,200,255,1)':'rgba(150,165,192,.62)';
    ctx.lineWidth=hot?1.9:1.35;
    ctx.stroke();
  }
  ctx.fillStyle='rgba(255,138,92,.9)';
  if(mouse.x>=0){ctx.beginPath();ctx.arc(mouse.x,mouse.y,2.4,0,Math.PI*2);ctx.fill();}
  document.getElementById('fps').textContent=fps|0;
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Move the pointer through the lines; the field bends around it.",
),
dict(
id="pixel-studio", name="Pixel Studio",
css=r'''
body{overflow:hidden;background:#0a0b10}
.stage{position:fixed;inset:0;display:grid;place-items:center;padding:44px 20px 100px}
.grid{display:grid;grid-template-columns:repeat(32,1fr);aspect-ratio:32/20;width:min(92vw,1100px);
border:1px solid #ffffff1a;background:#0d0f16;box-shadow:0 30px 90px -30px #000;touch-action:none}
.cell{background:transparent;border-right:1px solid #ffffff05;border-bottom:1px solid #ffffff05;cursor:crosshair}
.cell:hover{outline:1px solid #ffffff44;outline-offset:-1px}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:12px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:9px 13px;backdrop-filter:blur(10px);flex-wrap:wrap;justify-content:center}
.sw{width:24px;height:24px;border-radius:6px;border:1px solid #ffffff26;cursor:pointer;padding:0}
.sw.on{outline:2px solid #fff;outline-offset:2px}
.panel button{background:#171b24;border:1px solid #2a3040;color:#cdd4e1;border-radius:999px;padding:7px 11px;
font:500 10px/1 ui-monospace,monospace;cursor:pointer}
.panel button:hover{border-color:#ff8a5c;color:#fff}
''',
html=r'''
<div class="stage"><div class="grid" id="grid" aria-label="32 by 20 pixel canvas"></div></div>
<div class="hud"><span class="t">INTERACTIVE 05 · PIXEL STUDIO</span>32 × 20 · <b id="count">0</b> px painted</div>
<div class="panel" id="palette">
  <button class="sw on" data-c="#ff5a1f" style="background:#ff5a1f" aria-label="Orange"></button>
  <button class="sw" data-c="#ffd166" style="background:#ffd166" aria-label="Yellow"></button>
  <button class="sw" data-c="#3ddc84" style="background:#3ddc84" aria-label="Green"></button>
  <button class="sw" data-c="#7fb2ff" style="background:#7fb2ff" aria-label="Blue"></button>
  <button class="sw" data-c="#c084fc" style="background:#c084fc" aria-label="Purple"></button>
  <button class="sw" data-c="#f4f0e6" style="background:#f4f0e6" aria-label="Cream"></button>
  <button class="sw" data-c="erase" style="background:#15171f" aria-label="Eraser">⌫</button>
  <button id="random">Random</button><button id="clear">Clear</button>
</div>
''',
js=r'''
const grid=document.getElementById('grid');
const cols=32,rows=20;let color='#ff5a1f',painting=false;
const cells=[];
for(let i=0;i<cols*rows;i++){
  const d=document.createElement('div');d.className='cell';d.dataset.on='0';
  grid.appendChild(d);cells.push(d);
}
function paint(c){c.style.background=color==='erase'?'transparent':color;c.dataset.on=color==='erase'?'0':'1';count()}
function count(){document.getElementById('count').textContent=cells.filter(c=>c.dataset.on==='1').length}
grid.addEventListener('pointerdown',e=>{painting=true;if(e.target.classList.contains('cell'))paint(e.target);grid.setPointerCapture(e.pointerId)});
grid.addEventListener('pointermove',e=>{
  if(!painting)return;
  const el=document.elementFromPoint(e.clientX,e.clientY);
  if(el&&el.classList.contains('cell'))paint(el);
});
addEventListener('pointerup',()=>painting=false);
document.querySelectorAll('.sw').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('.sw').forEach(x=>x.classList.remove('on'));b.classList.add('on');color=b.dataset.c;
}));
document.getElementById('clear').onclick=()=>cells.forEach(c=>{c.style.background='transparent';c.dataset.on='0'});count();
document.getElementById('random').onclick=()=>{
  const pal=['#ff5a1f','#ffd166','#3ddc84','#7fb2ff','#c084fc','#f4f0e6'];
  cells.forEach(c=>{if(Math.random()<.3){c.style.background=pal[Math.floor(Math.random()*pal.length)];c.dataset.on='1'}});count();
};
count();
''',
hint="Drag to paint. Pick a colour or the eraser; Random seeds a pattern.",
),
dict(
id="fluid-trail", name="Fluid Trail",
css=r'''
body{overflow:hidden;background:#05060a;cursor:none}
#cv{position:fixed;inset:0;touch-action:none}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:16px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:10px 18px;backdrop-filter:blur(10px)}
.panel label{display:flex;align-items:center;gap:8px;color:#8b95a8;font:500 10px/1 ui-monospace,monospace;letter-spacing:.08em}
.panel input{width:100px;accent-color:#ff6b35}
.panel button{background:#171b24;border:1px solid #2a3040;color:#cdd4e1;border-radius:999px;padding:7px 11px;
font:500 10px/1 ui-monospace,monospace;cursor:pointer}
#dot{position:fixed;width:8px;height:8px;border-radius:50%;background:#fff;pointer-events:none;z-index:20;translate:-50% -50%;mix-blend-mode:screen;box-shadow:0 0 18px #fff}
''',
html=r'''
<canvas id="cv"></canvas>
<div id="dot"></div>
<div class="hud"><span class="t">INTERACTIVE 06 · FLUID TRAIL</span>points <b id="n">0</b> · move fast for colour</div>
<div class="panel">
  <label>DECAY <input id="decay" type="range" min="2" max="40" value="12"></label>
  <label>WIDTH <input id="width" type="range" min="2" max="40" value="12"></label>
  <button id="clear">Clear</button>
</div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d'),dot=document.getElementById('dot');
let W,H,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
fit();addEventListener('resize',fit);
let pts=[],last={x:W/2,y:H/2};
addEventListener('pointermove',e=>{
  const vx=e.clientX-last.x,vy=e.clientY-last.y,speed=Math.min(24,Math.hypot(vx,vy));
  pts.push({x:e.clientX,y:e.clientY,vx,vy,l:1,h:(210+speed*7)%360});
  last={x:e.clientX,y:e.clientY};
  dot.style.left=e.clientX+'px';dot.style.top=e.clientY+'px';
  if(pts.length>500)pts.shift();
});
const decay=document.getElementById('decay'),width=document.getElementById('width');
function frame(){
  const d=+decay.value/1000,w=+width.value;
  ctx.fillStyle='rgba(5,6,10,'+d+')';ctx.fillRect(0,0,W,H);
  ctx.globalCompositeOperation='lighter';
  for(const p of pts){
    p.l*=.94;p.x+=p.vx*.06;p.y+=p.vy*.06;
    if(p.l<.02)continue;
    const sp=Math.hypot(p.vx,p.vy);
    ctx.strokeStyle='hsla('+p.h+',85%,62%,'+(p.l*.5)+')';
    ctx.lineWidth=Math.max(1,w*(p.l));
    ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p.x-p.vx*.5,p.y-p.vy*.5);ctx.stroke();
    ctx.fillStyle='hsla('+p.h+',90%,70%,'+(p.l*.25)+')';
    ctx.beginPath();ctx.arc(p.x,p.y,w*p.l*.5,0,Math.PI*2);ctx.fill();
  }
  ctx.globalCompositeOperation='source-over';
  pts=pts.filter(p=>p.l>.02);
  document.getElementById('n').textContent=pts.length;
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
document.getElementById('clear').onclick=()=>{pts=[];ctx.fillStyle='#05060a';ctx.fillRect(0,0,W,H)};
''',
hint="Move slowly for tight ink, fast for wide colour. Two sliders change the body.",
),
dict(
id="magnetic-dots", name="Magnetic Dots",
css=r'''
body{overflow:hidden;background:#07080c}
#cv{position:fixed;inset:0;touch-action:none}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:16px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:10px 18px;backdrop-filter:blur(10px)}
.panel label{display:flex;align-items:center;gap:8px;color:#8b95a8;font:500 10px/1 ui-monospace,monospace;letter-spacing:.08em}
.panel input{width:100px;accent-color:#ff6b35}
.panel button{background:#171b24;border:1px solid #2a3040;color:#cdd4e1;border-radius:999px;padding:7px 11px;
font:500 10px/1 ui-monospace,monospace;cursor:pointer}
''',
html=r'''
<canvas id="cv"></canvas>
<div class="hud"><span class="t">INTERACTIVE 07 · MAGNETIC DOTS</span>grid <b id="g">44px</b> · <b id="fps">60</b> fps</div>
<div class="panel">
  <label>RADIUS <input id="radius" type="range" min="60" max="320" value="190"></label>
  <label>FORCE <input id="force" type="range" min="0" max="100" value="62"></label>
  <button id="repel">Repel / Attract</button>
</div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
fit();addEventListener('resize',fit);
const mouse={x:-9999,y:-9999};let sign=1;
addEventListener('pointermove',e=>{mouse.x=e.clientX;mouse.y=e.clientY});
addEventListener('pointerleave',()=>{mouse.x=-9999});
const radius=document.getElementById('radius'),force=document.getElementById('force');
document.getElementById('repel').onclick=()=>{sign*=-1};
let dots=[],gap=44;
function build(){
  dots=[];gap=innerWidth<640?34:44;
  for(let y=gap/2;y<H;y+=gap)for(let x=gap/2;x<W;x+=gap){
    dots.push({hx:x,hy:y,x,y,vx:0,vy:0});
  }
  document.getElementById('g').textContent=gap+'px';
}
build();addEventListener('resize',build);
let last=performance.now(),fps=60;
function frame(now){
  const dt=Math.min((now-last)/1000,.032);last=now;fps+=(1/Math.max(dt,.001)-fps)*.05;
  ctx.fillStyle='#07080c';ctx.fillRect(0,0,W,H);
  const R=+radius.value, F=+force.value/100;
  for(const d of dots){
    const dx=mouse.x-d.x,dy=mouse.y-d.y,dist=Math.hypot(dx,dy);
    let tx=d.hx,ty=d.hy;
    if(dist<R&&dist>1){
      const pull=(1-dist/R)*F*46*sign;
      tx=d.x+dx/dist*pull;ty=d.y+dy/dist*pull;
    }
    d.vx+=(tx-d.x)*.14;d.vy+=(ty-d.y)*.14;
    d.vx*=.86;d.vy*=.86;d.x+=d.vx;d.y+=d.vy;
  }
  for(const d of dots){
    const dist=Math.hypot(mouse.x-d.x,mouse.y-d.y);
    const hot=Math.max(0,1-dist/(R*.8));
    if(hot>.05){
      ctx.strokeStyle='rgba(255,138,92,'+(hot*.16)+')';ctx.lineWidth=1;
      ctx.beginPath();ctx.moveTo(d.hx,d.hy);ctx.lineTo(d.x,d.y);ctx.stroke();
    }
    ctx.fillStyle=hot>.05?'rgba(255,'+(138+hot*80)+','+(92+hot*60)+','+(0.5+hot*.5)+')':'rgba(160,172,196,.32)';
    ctx.beginPath();ctx.arc(d.x,d.y,1.4+hot*1.8,0,Math.PI*2);ctx.fill();
  }
  document.getElementById('fps').textContent=fps|0;
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Move through the grid. Repel switches polarity; pull the radius wide.",
),
dict(
id="gravity-sandbox", name="Gravity Sandbox",
css=r'''
body{overflow:hidden;background:#06070b}
#cv{position:fixed;inset:0;touch-action:none;cursor:crosshair}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:14px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:10px 16px;backdrop-filter:blur(10px);flex-wrap:wrap;justify-content:center}
.panel label{display:flex;align-items:center;gap:8px;color:#8b95a8;font:500 10px/1 ui-monospace,monospace;letter-spacing:.08em}
.panel input{width:90px;accent-color:#ff6b35}
.panel button{background:#171b24;border:1px solid #2a3040;color:#cdd4e1;border-radius:999px;padding:7px 11px;
font:500 10px/1 ui-monospace,monospace;cursor:pointer}
''',
html=r'''
<canvas id="cv"></canvas>
<div class="hud"><span class="t">INTERACTIVE 08 · GRAVITY SANDBOX</span>balls <b id="n">0</b> · drag empty space to fling</div>
<div class="panel">
  <label>GRAVITY <input id="grav" type="range" min="0" max="160" value="60"></label>
  <label>BOUNCE <input id="bounce" type="range" min="20" max="95" value="72"></label>
  <button id="add">+ 8 balls</button><button id="clear">Clear</button>
</div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
fit();addEventListener('resize',fit);
const balls=[];
const colors=['#ff5a1f','#ffd166','#3ddc84','#7fb2ff','#c084fc','#f4f0e6'];
function add(n){
  for(let i=0;i<n;i++){
    const r=6+Math.random()*16;
    balls.push({x:Math.random()*W,y:Math.random()*H*.5,r,vx:(Math.random()-.5)*6,vy:Math.random()*2,h:colors[Math.floor(Math.random()*colors.length)],trail:[]});
  }
  document.getElementById('n').textContent=balls.length;
}
add(16);
let drag=null,lastP=null;
cv.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY,t:performance.now()};lastP={x:e.clientX,y:e.clientY}});
cv.addEventListener('pointermove',e=>{
  if(!lastP)return;
  const vx=e.clientX-lastP.x,vy=e.clientY-lastP.y;
  lastP={x:e.clientX,y:e.clientY};
  drag.vx=vx;drag.vy=vy;
});
addEventListener('pointerup',()=>{
  if(drag&&Math.hypot(drag.vx||0,drag.vy||0)>2){
    balls.push({x:drag.x,y:drag.y,r:13,vx:(drag.vx||0)*.7,vy:(drag.vy||0)*.7,h:colors[Math.floor(Math.random()*colors.length)],trail:[]});
    document.getElementById('n').textContent=balls.length;
  }
  drag=null;lastP=null;
});
const grav=document.getElementById('grav'),bounce=document.getElementById('bounce');
document.getElementById('clear').onclick=()=>{balls.length=0;document.getElementById('n').textContent=0};
document.getElementById('add').onclick=()=>add(8);
function frame(){
  ctx.fillStyle='rgba(6,7,11,.22)';ctx.fillRect(0,0,W,H);
  const g=+grav.value/100, e=+bounce.value/100;
  for(const b of balls){
    b.vy+=g;b.x+=b.vx;b.y+=b.vy;
    if(b.x<b.r){b.x=b.r;b.vx=Math.abs(b.vx)*e}
    if(b.x>W-b.r){b.x=W-b.r;b.vx=-Math.abs(b.vx)*e}
    if(b.y>H-b.r){b.y=H-b.r;b.vy=-Math.abs(b.vy)*e;b.vx*=.99}
    if(b.y<b.r){b.y=b.r;b.vy=Math.abs(b.vy)*e}
    b.trail.push([b.x,b.y]);if(b.trail.length>14)b.trail.shift();
    ctx.fillStyle=b.h+'18';
    for(let i=0;i<b.trail.length;i++){ctx.beginPath();ctx.arc(b.trail[i][0],b.trail[i][1],b.r*(i/b.trail.length)*.7,0,Math.PI*2);ctx.fill()}
    ctx.fillStyle=b.h;ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#ffffff26';ctx.beginPath();ctx.arc(b.x-b.r*.3,b.y-b.r*.3,b.r*.28,0,Math.PI*2);ctx.fill();
  }
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Drag across empty space and release to fling a ball. Add eight more any time.",
),
dict(
id="liquid-blob", name="Liquid Blob",
css=r'''
body{overflow:hidden;background:radial-gradient(80% 70% at 50% 30%,#141826,#06070a 70%)}
.stage{position:fixed;inset:0;filter:url(#goo)}
.blob{position:absolute;border-radius:50%;will-change:transform;
background:radial-gradient(circle at 35% 30%,#ffb08a,#ff5a1f 55%,#9b2f00);mix-blend-mode:screen}
.b2{background:radial-gradient(circle at 35% 30%,#9db8ff,#5a6bff 55%,#1a2380)}
.b3{background:radial-gradient(circle at 35% 30%,#8affd4,#00a884 55%,#00553f)}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:16px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:10px 18px;backdrop-filter:blur(10px)}
.panel label{display:flex;align-items:center;gap:8px;color:#8b95a8;font:500 10px/1 ui-monospace,monospace;letter-spacing:.08em}
.panel input{width:100px;accent-color:#ff6b35}
.panel button{background:#171b24;border:1px solid #2a3040;color:#cdd4e1;border-radius:999px;padding:7px 11px;
font:500 10px/1 ui-monospace,monospace;cursor:pointer}
.panel button:hover{border-color:#ff8a5c;color:#fff}
svg.defs{position:absolute;width:0;height:0}
''',
html=r'''
<main class="stage" id="stage"></main>
<svg class="defs" aria-hidden="true"><defs><filter id="goo"><feGaussianBlur in="SourceGraphic" stdDeviation="18" result="b"/><feColorMatrix in="b" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 24 -10" result="g"/><feBlend in="SourceGraphic" in2="g"/></filter></defs></svg>
<div class="hud"><span class="t">INTERACTIVE 09 · LIQUID BLOB</span>3 bodies · move to pull</div>
<div class="panel">
  <label>VISCOSITY <input id="visc" type="range" min="4" max="40" value="18"></label>
  <label>SIZE <input id="size" type="range" min="60" max="240" value="130"></label>
  <button id="burst">Burst</button>
</div>
''',
js=r'''
const stage=document.getElementById('stage');
const mouse={x:innerWidth/2,y:innerHeight/2,tx:innerWidth/2,ty:innerHeight/2};
addEventListener('pointermove',e=>{mouse.tx=e.clientX;mouse.ty=e.clientY});
addEventListener('touchmove',e=>{const t=e.touches[0];if(t){mouse.tx=t.clientX;mouse.ty=t.clientY}},{passive:true});
const colors=['','b2','b3'];
const blobs=colors.map((c,i)=>{
  const el=document.createElement('div');el.className='blob '+c;stage.appendChild(el);
  return {el,x:innerWidth*.5+(i-1)*70,y:innerHeight*.5+(i-1)*40,vx:0,vy:0,off:i*2.1};
});
const visc=document.getElementById('visc'),size=document.getElementById('size'),filter=document.querySelector('#goo feGaussianBlur');
visc.addEventListener('input',()=>filter.setAttribute('stdDeviation',visc.value));
function frame(t){
  const time=t/1000;
  mouse.x+=(mouse.tx-mouse.x)*.08;mouse.y+=(mouse.ty-mouse.y)*.08;
  const S=+size.value;
  blobs.forEach((b,i)=>{
    const ox=Math.cos(time*.7+b.off)*S*.55, oy=Math.sin(time*.9+b.off*1.3)*S*.4;
    const tx=mouse.x+ox, ty=mouse.y+oy;
    b.vx+=(tx-b.x)*.045;b.vy+=(ty-b.y)*.045;b.vx*=.86;b.vy*=.86;
    b.x+=b.vx;b.y+=b.vy;
    const s=S*(i===0?1:.72);
    b.el.style.width=b.el.style.height=s+'px';
    b.el.style.transform='translate('+(b.x-s/2)+'px,'+(b.y-s/2)+'px)';
  });
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
document.getElementById('burst').onclick=()=>{
  const cx=mouse.x,cy=mouse.y;
  blobs.forEach((b,i)=>{b.x=cx+(Math.random()-.5)*40;b.y=cy+(Math.random()-.5)*40;b.vx=(Math.random()-.5)*40;b.vy=(Math.random()-.5)*40});
};
''',
hint="Move to drag the bodies; they merge through an SVG goo filter.",
),
]
