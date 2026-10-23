# Interactive visuals — part C (19-25)

ADDONS_C = [
dict(
id="glitch-slicer", name="Glitch Slicer",
css=r'''
body{overflow:hidden;background:#06070b}
#cv{position:fixed;inset:0;touch-action:none;cursor:crosshair}
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
<div class="hud"><span class="t">INTERACTIVE 19 · GLITCH SLICER</span>move to tear · <b id="shift">0</b>px shift</div>
<div class="panel">
  <label>TEAR <input id="tear" type="range" min="0" max="100" value="55"></label>
  <label>SLICES <input id="slices" type="range" min="6" max="48" value="18"></label>
</div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,DPR=Math.min(devicePixelRatio||1,2),scene=null;
function makeScene(){
  const c=document.createElement('canvas');c.width=1600;c.height=1000;const x=c.getContext('2d');
  const g=x.createLinearGradient(0,0,1600,1000);
  g.addColorStop(0,'#ff8a5c');g.addColorStop(.45,'#c084fc');g.addColorStop(1,'#0a1030');
  x.fillStyle=g;x.fillRect(0,0,1600,1000);
  x.globalAlpha=.9;
  for(let i=0;i<7;i++){
    x.beginPath();x.arc(240+i*190,320+Math.sin(i*1.7)*120,110+i*14,0,Math.PI*2);
    x.fillStyle=['#f4f0e6','#ffd166','#3ddc84','#7fb2ff','#ff5a1f','#c084fc','#5ec8ff'][i];x.fill();
  }
  x.globalAlpha=1;
  x.fillStyle='#08090e';x.fillRect(80,700,1440,5);
  x.fillStyle='#f4f0e6';x.font='900 190px system-ui,sans-serif';x.textAlign='left';x.fillText('SIGNAL',80,880);
  x.fillStyle='#08090e';x.font='600 22px ui-monospace,monospace';x.fillText('TRANSMISSION / 19 — DISTORTION STUDY',84,940);
  return c;
}
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);if(!scene)scene=makeScene();}
fit();addEventListener('resize',fit);
const mouse={x:-9999,y:-9999};
addEventListener('pointermove',e=>{mouse.x=e.clientX;mouse.y=e.clientY});
addEventListener('pointerleave',()=>{mouse.x=-9999});
const tear=document.getElementById('tear'),slicesEl=document.getElementById('slices');
let t=0;
function frame(){
  t+=.016;
  const slices=+slicesEl.value, amp=+tear.value/100;
  ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);
  const sh=H/slices;
  for(let i=0;i<slices;i++){
    const y=i*sh;
    const proximity=mouse.y<0?0:Math.max(0,1-Math.abs(y+sh/2-mouse.y)/(H*.28));
    const noise=(Math.sin(i*12.9898+t*3)*43758.5453)%1;
    const shift=(noise*amp*90 + proximity*amp*120)*Math.sin(t*2+i);
    ctx.drawImage(scene,0,y/scene.height*scene.height,scene.width,sh/scene.height*scene.height+1,shift,y,W,sh+1);
    if(proximity>.25){
      ctx.fillStyle='rgba(255,60,80,'+(proximity*.16)+')';
      ctx.fillRect(0,y,W,sh);
      ctx.fillStyle='rgba(0,220,255,'+(proximity*.10)+')';
      ctx.fillRect(-6,y+2,W,sh);
    }
  }
  document.getElementById('shift').textContent=Math.round(amp*90);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Move vertically through the image: nearby bands tear and split into RGB.",
),
dict(
id="ascii-portrait", name="ASCII Portrait",
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
.panel button:hover{border-color:#ff8a5c;color:#fff}
''',
html=r'''
<canvas id="cv"></canvas>
<div class="hud"><span class="t">INTERACTIVE 20 · ASCII PORTRAIT</span>move for gamma · <b id="chars">0</b> glyphs</div>
<div class="panel">
  <label>SIZE <input id="cell" type="range" min="5" max="16" value="8"></label>
  <label>GAMMA <input id="gam" type="range" min="40" max="220" value="110"></label>
  <button id="mono">Colour / Mono</button><button id="upload">Use my image</button>
  <input type="file" id="file" accept="image/*" hidden>
</div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,DPR=Math.min(devicePixelRatio||1,2),scene=null,mono=false;
function makeScene(){
  const c=document.createElement('canvas');c.width=1200;c.height=900;const x=c.getContext('2d');
  const g=x.createRadialGradient(600,380,60,600,450,700);
  g.addColorStop(0,'#ffd9a0');g.addColorStop(.4,'#ff6b35');g.addColorStop(.7,'#5a2a6b');g.addColorStop(1,'#07080c');
  x.fillStyle=g;x.fillRect(0,0,1200,900);
  // abstract head silhouette
  x.fillStyle='#0b0c12';x.beginPath();x.ellipse(600,430,230,300,0,0,Math.PI*2);x.fill();
  x.fillStyle='#ffb08a';x.beginPath();x.ellipse(600,400,150,210,0,0,Math.PI*2);x.fill();
  x.fillStyle='#0b0c12';
  x.beginPath();x.ellipse(545,380,26,14,-.2,0,Math.PI*2);x.fill();
  x.beginPath();x.ellipse(655,380,26,14,.2,0,Math.PI*2);x.fill();
  x.beginPath();x.ellipse(600,400,7,18,0,0,Math.PI*2);x.fill();
  x.beginPath();x.ellipse(600,505,52,10,0,0,Math.PI*2);x.fill();
  x.strokeStyle='#0b0c12';x.lineWidth=14;x.beginPath();x.arc(600,470,90,.25,Math.PI-.25);x.stroke();
  x.fillStyle='#3ddc84';x.fillRect(250,140,18,18);x.fillStyle='#7fb2ff';x.fillRect(930,700,18,18);
  x.fillStyle='#f4f0e6';x.font='500 20px ui-monospace,monospace';x.fillText('SUBJECT / 20',60,80);x.fillText('ASCII STUDY',60,110);
  return c;
}
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);if(!scene)scene=makeScene();}
fit();addEventListener('resize',fit);
const cell=document.getElementById('cell'),gam=document.getElementById('gam');
let mx=.5;
addEventListener('pointermove',e=>{mx=e.clientX/innerWidth});
const CH=' .:-=+*#%@';
let raf=null;
function render(){
  const cs=+cell.value, gamma=+gam.value/100 + (mx-.5)*.5;
  const cols=Math.floor(W/cs), rows=Math.floor(H/cs*.95);
  const off=document.createElement('canvas');off.width=cols;off.height=rows;
  const oc=off.getContext('2d');oc.drawImage(scene,0,0,cols,rows);
  const data=oc.getImageData(0,0,cols,rows).data;
  ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);
  ctx.font='600 '+Math.round(cs*1.15)+'px ui-monospace,monospace';
  ctx.textAlign='center';ctx.textBaseline='middle';
  for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){
    const i=(y*cols+x)*4;
    const r=data[i],g=data[i+1],b=data[i+2];
    const lum=Math.pow((r*.299+g*.587+b*.114)/255,gamma);
    const ch=CH[Math.min(CH.length-1,Math.floor(lum*CH.length))];
    if(ch===' ')continue;
    ctx.fillStyle=mono?'rgba(230,236,246,'+(0.25+lum*.75)+')':'rgba('+Math.min(255,r*1.4)+','+Math.min(255,g*1.3)+','+Math.min(255,b*1.5)+',.9)';
    ctx.fillText(ch,x*cs+cs/2,y*cs+cs/2);
  }
  document.getElementById('chars').textContent=(cols*rows).toLocaleString();
}
function queue(){if(raf)return;raf=requestAnimationFrame(()=>{raf=null;render()})}
cell.addEventListener('input',queue);gam.addEventListener('input',queue);addEventListener('pointermove',queue);
document.getElementById('mono').onclick=()=>{mono=!mono;queue()};
document.getElementById('upload').onclick=()=>document.getElementById('file').click();
document.getElementById('file').addEventListener('change',e=>{
  const f=e.target.files[0];if(!f)return;
  const img=new Image();img.onload=()=>{
    const c=document.createElement('canvas');c.width=1200;c.height=Math.round(1200*img.height/img.width);
    const x=c.getContext('2d');const r=Math.max(c.width/img.width,c.height/img.height);
    x.drawImage(img,(c.width-img.width*r)/2,(c.height-img.height*r)/2,img.width*r,img.height*r);
    scene=c;render();
  };img.src=URL.createObjectURL(f);
});
render();
''',
hint="Move sideways to change gamma. Try a photo — it converts any upload to glyphs.",
),
dict(
id="audio-visualizer", name="Audio Visualizer",
css=r'''
body{overflow:hidden;background:#04050a}
#cv{position:fixed;inset:0}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:14px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:10px 16px;backdrop-filter:blur(10px);flex-wrap:wrap;justify-content:center}
.panel label{display:flex;align-items:center;gap:8px;color:#8b95a8;font:500 10px/1 ui-monospace,monospace;letter-spacing:.08em}
.panel input{width:95px;accent-color:#ff6b35}
.panel button{background:#171b24;border:1px solid #2a3040;color:#cdd4e1;border-radius:999px;padding:8px 14px;
font:600 10px/1 ui-monospace,monospace;cursor:pointer}
.panel button.primary{background:#f2f4f8;color:#0a0a0e;border-color:#f2f4f8}
''',
html=r'''
<canvas id="cv"></canvas>
<div class="hud"><span class="t">INTERACTIVE 21 · AUDIO VISUALIZER</span><b id="state">PAUSED</b> · click play to enable audio</div>
<div class="panel">
  <label>FREQ <input id="freq" type="range" min="60" max="900" value="220"></label>
  <label>LEVEL <input id="gain" type="range" min="0" max="100" value="45"></label>
  <button class="primary" id="play">▶ Play tone</button>
  <button id="wave">Sine ▸</button>
</div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
fit();addEventListener('resize',fit);
let audio=null,osc=null,analyser=null,data=null,playing=false,type='sine';
const types=['sine','triangle','sawtooth','square'];
function start(){
  if(!audio){
    audio=new (window.AudioContext||window.webkitAudioContext)();
    osc=audio.createOscillator();analyser=audio.createAnalyser();
    analyser.fftSize=2048;data=new Uint8Array(analyser.frequencyBinCount);
    const g=audio.createGain();g.gain.value=+document.getElementById('gain').value/100*.08;
    osc.type=type;osc.frequency.value=+document.getElementById('freq').value;
    osc.connect(g);g.connect(analyser);analyser.connect(audio.destination);osc.start();
    window.__gain=g;
  }
  audio.resume();playing=true;
  document.getElementById('state').textContent='PLAYING';
  document.getElementById('play').textContent='■ Stop';
}
function stop(){
  if(audio)audio.suspend();
  playing=false;
  document.getElementById('state').textContent='PAUSED';
  document.getElementById('play').textContent='▶ Play tone';
}
document.getElementById('play').onclick=()=>playing?stop():start();
document.getElementById('wave').onclick=()=>{
  type=types[(types.indexOf(type)+1)%types.length];
  if(osc)osc.type=type;
  document.getElementById('wave').textContent=type[0].toUpperCase()+type.slice(1)+' ▸';
};
document.getElementById('freq').addEventListener('input',e=>{if(osc)osc.frequency.value=+e.target.value});
document.getElementById('gain').addEventListener('input',e=>{if(window.__gain)window.__gain.gain.value=+e.target.value/100*.08});
let t=0;
function frame(){
  t+=.016;
  ctx.fillStyle='rgba(4,5,10,.35)';ctx.fillRect(0,0,W,H);
  const cx=W/2,cy=H/2,R=Math.min(W,H)*.19;
  if(analyser&&playing)analyser.getByteFrequencyData(data);
  const bars=128;
  ctx.globalCompositeOperation='lighter';
  for(let i=0;i<bars;i++){
    const idx=Math.floor(Math.pow(i/bars,1.7)*(data?data.length:256)*.7);
    const v=playing&&data?data[idx]/255:(.08+.05*Math.sin(t*2+i*.3));
    const a=(i/bars)*Math.PI*2;
    const len=12+v*Math.min(W,H)*.28;
    const x1=cx+Math.cos(a)*R,y1=cy+Math.sin(a)*R;
    const x2=cx+Math.cos(a)*(R+len),y2=cy+Math.sin(a)*(R+len);
    const hue=200+v*120;
    ctx.strokeStyle='hsla('+hue+',90%,62%,'+(0.25+v*.7)+')';
    ctx.lineWidth=2.2;
    ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
  }
  ctx.globalCompositeOperation='source-over';
  const g=ctx.createRadialGradient(cx,cy,R*.2,cx,cy,R);
  g.addColorStop(0,'rgba(90,140,255,.16)');g.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=g;ctx.beginPath();ctx.arc(cx,cy,R,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle='rgba(255,255,255,.10)';ctx.lineWidth=1;ctx.beginPath();ctx.arc(cx,cy,R,0,Math.PI*2);ctx.stroke();
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Press Play (browser audio needs the click), then change frequency and waveform.",
),
dict(
id="before-after", name="Before / After Slider",
css=r'''
body{overflow:hidden;background:#06070b}
.frame{position:fixed;inset:0}
.half{position:absolute;inset:0;overflow:hidden}
.half .art{position:absolute;inset:0;display:grid;place-items:center}
.after{clip-path:inset(0 0 0 50%)}
.shot{width:min(70vw,900px);aspect-ratio:16/10;border-radius:8px;position:relative;overflow:hidden;box-shadow:0 40px 100px -30px #000}
.shot .sun{position:absolute;width:42%;aspect-ratio:1;border-radius:50%;left:12%;top:16%;filter:blur(1px)}
.shot .hill{position:absolute;left:-10%;right:-10%;bottom:-20%;height:62%;border-radius:50% 50% 0 0/70% 70% 0 0}
.shot .hill.two{bottom:-32%;height:70%;left:-30%;right:20%;opacity:.9}
.shot .word{position:absolute;left:6%;bottom:7%;font:900 clamp(30px,6vw,84px)/.9 system-ui,sans-serif;letter-spacing:-.05em}
.grade-warm .sun{background:radial-gradient(circle at 40% 35%,#fff3d0,#ffb066 60%,#ff5a1f 100%)}
.grade-warm .hill{background:linear-gradient(180deg,#b8552f,#5a1e12)}
.grade-warm .hill.two{background:#3a140d}
.grade-warm .word{color:#f7e9d2}
.grade-warm{background:linear-gradient(170deg,#ffe0b0,#e0875a 55%,#7a3520)}
.grade-cool .sun{background:radial-gradient(circle at 40% 35%,#eaf6ff,#8fd0ff 60%,#3d6bff 100%)}
.grade-cool .hill{background:linear-gradient(180deg,#2f5f8a,#0d2238)}
.grade-cool .hill.two{background:#081726}
.grade-cool .word{color:#e8f4ff}
.grade-cool{background:linear-gradient(170deg,#b8dcff,#5f8fc4 55%,#14263d)}
.tag{position:absolute;top:18px;font:600 9.5px/1 ui-monospace,monospace;letter-spacing:.2em;color:#ffffffcc;
background:#00000055;border:1px solid #ffffff2e;border-radius:999px;padding:6px 10px;backdrop-filter:blur(6px)}
.before .tag{left:18px}
.after .tag{right:18px}
.divider{position:absolute;top:0;bottom:0;width:2px;background:#fff;left:50%;z-index:5;box-shadow:0 0 24px #000}
.handle{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:42px;height:42px;border-radius:50%;
background:#fff;color:#090a0e;display:grid;place-items:center;font:600 14px/1 ui-monospace,monospace;box-shadow:0 8px 30px #0007;z-index:6}
#range{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:ew-resize;z-index:10;margin:0}
.hud{position:fixed;top:16px;left:16px;z-index:20;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
''',
html=r'''
<div class="frame" id="frame">
  <div class="half before"><div class="art"><div class="shot grade-warm"><div class="sun"></div><div class="hill"></div><div class="hill two"></div><div class="word">DUSK</div></div></div><span class="tag">BEFORE · RAW</span></div>
  <div class="half after" id="after"><div class="art"><div class="shot grade-cool"><div class="sun"></div><div class="hill"></div><div class="hill two"></div><div class="word">DUSK</div></div></div><span class="tag">AFTER · GRADED</span></div>
  <div class="divider" id="line"><span class="handle">↔</span></div>
  <input type="range" id="range" min="0" max="100" value="50" aria-label="Comparison position">
</div>
<div class="hud"><span class="t">INTERACTIVE 22 · BEFORE / AFTER</span>drag or use arrow keys · <b id="pct">50%</b></div>
''',
js=r'''
const range=document.getElementById('range'),after=document.getElementById('after'),line=document.getElementById('line'),pct=document.getElementById('pct'),frame=document.getElementById('frame');
function set(v){
  range.value=v;
  after.style.clipPath='inset(0 0 0 '+v+'%)';
  line.style.left=v+'%';
  pct.textContent=Math.round(v)+'%';
}
range.addEventListener('input',()=>set(+range.value));
frame.addEventListener('pointerdown',e=>{
  if(e.target===range)return;
  const r=frame.getBoundingClientRect();
  set(Math.max(0,Math.min(100,(e.clientX-r.left)/r.width*100)));
});
''',
hint="Drag anywhere, or tab to the divider and use ← →. Works with touch.",
),
dict(
id="kaleidoscope", name="Kaleidoscope Painter",
css=r'''
body{overflow:hidden;background:#05060a;cursor:crosshair}
#cv{position:fixed;inset:0;touch-action:none}
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
.panel button:hover{border-color:#ff8a5c;color:#fff}
''',
html=r'''
<canvas id="cv"></canvas>
<div class="hud"><span class="t">INTERACTIVE 23 · KALEIDOSCOPE</span>draw anywhere · <b id="seg">8</b> mirrors · hue <b id="hue">0</b>°</div>
<div class="panel">
  <label>MIRRORS <input id="mirrors" type="range" min="3" max="16" value="8"></label>
  <label>WIDTH <input id="w" type="range" min="1" max="26" value="9"></label>
  <button id="clear">Clear</button>
</div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);ctx.fillStyle='#05060a';ctx.fillRect(0,0,W,H);}
fit();addEventListener('resize',fit);
let drawing=false,lx=0,ly=0,hue=0;
cv.addEventListener('pointerdown',e=>{drawing=true;lx=e.clientX;ly=e.clientY;draw(e)});
cv.addEventListener('pointermove',e=>{if(drawing)draw(e)});
addEventListener('pointerup',()=>drawing=false);
const mirrors=document.getElementById('mirrors'),wEl=document.getElementById('w');
function draw(e){
  const x=e.clientX,y=e.clientY,cx=W/2,cy=H/2;
  const n=+mirrors.value, seg=Math.PI*2/n;
  hue=(hue+1.4)%360;
  ctx.globalCompositeOperation='lighter';
  ctx.lineCap='round';
  for(let i=0;i<n;i++){
    for(const flip of [1,-1]){
      ctx.save();
      ctx.translate(cx,cy);ctx.rotate(i*seg);ctx.scale(flip,1);
      const x1=lx-cx,y1=ly-cy,x2=x-cx,y2=y-cy;
      ctx.strokeStyle='hsla('+((hue+i*14)%360)+',90%,64%,.5)';
      ctx.lineWidth=+wEl.value;
      ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
      ctx.restore();
    }
  }
  ctx.globalCompositeOperation='source-over';
  lx=x;ly=y;
  document.getElementById('hue').textContent=Math.round(hue);
  document.getElementById('seg').textContent=n;
}
mirrors.addEventListener('input',()=>{document.getElementById('seg').textContent=mirrors.value});
document.getElementById('clear').onclick=()=>{ctx.fillStyle='#05060a';ctx.fillRect(0,0,W,H)};
''',
hint="Press and drag across the canvas — the stroke is mirrored around the centre.",
),
dict(
id="confetti-physics", name="Confetti Physics",
css=r'''
body{overflow:hidden;background:#06070b;cursor:crosshair}
#cv{position:fixed;inset:0;touch-action:none}
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
.panel button:hover{border-color:#ff8a5c;color:#fff}
''',
html=r'''
<canvas id="cv"></canvas>
<div class="hud"><span class="t">INTERACTIVE 24 · CONFETTI</span>pieces <b id="n">0</b> · click to burst</div>
<div class="panel">
  <label>GRAVITY <input id="grav" type="range" min="10" max="120" value="45"></label>
  <label>WIND <input id="wind" type="range" min="-60" max="60" value="8"></label>
  <button id="rain">Confetti rain</button><button id="clear">Clear</button>
</div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
fit();addEventListener('resize',fit);
const COL=['#ff5a1f','#ffd166','#3ddc84','#7fb2ff','#c084fc','#f4f0e6','#ff5c8a'];
const P=[];const MAX=900;
function spawn(x,y,n,power){
  for(let i=0;i<n;i++){
    if(P.length>MAX)P.shift();
    const a=Math.random()*Math.PI*2, s=Math.random()*power;
    P.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s-4,w:5+Math.random()*7,h:8+Math.random()*10,
      rot:Math.random()*6,vr:(Math.random()-.5)*.3,c:COL[Math.floor(Math.random()*COL.length)],life:1});
  }
  document.getElementById('n').textContent=P.length;
}
cv.addEventListener('pointerdown',e=>spawn(e.clientX,e.clientY,90,9));
const grav=document.getElementById('grav'),wind=document.getElementById('wind');
document.getElementById('rain').onclick=()=>{for(let i=0;i<10;i++)spawn(Math.random()*W,-10,40,3)};
document.getElementById('clear').onclick=()=>{P.length=0;document.getElementById('n').textContent=0};
function frame(){
  ctx.fillStyle='rgba(6,7,11,.20)';ctx.fillRect(0,0,W,H);
  const g=+grav.value/100, wd=+wind.value/100;
  for(let i=P.length-1;i>=0;i--){
    const p=P[i];
    p.vy+=g;p.vx+=wd*.1+Math.sin(p.rot)*.06;p.vx*=.995;p.vy*=.995;
    p.x+=p.vx;p.y+=p.vy;p.rot+=p.vr;
    p.life-=.0015;
    if(p.y>H+40||p.life<=0){P.splice(i,1);continue}
    ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot);ctx.scale(1,Math.cos(p.rot*1.6)*.7+.3);
    ctx.fillStyle=p.c;ctx.globalAlpha=Math.max(0,Math.min(1,p.life));
    ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h);ctx.restore();
  }
  document.getElementById('n').textContent=P.length;
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Click anywhere for a burst. Change gravity and wind while the paper is falling.",
),
dict(
id="lightbox-gallery", name="Lightbox Gallery",
css=r'''
body{background:#07080c;overflow:hidden}
.grid{position:fixed;inset:0;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);gap:6px;padding:6px}
.tile{position:relative;overflow:hidden;cursor:pointer;border-radius:3px;border:0;padding:0;background:#111}
.tile .art{position:absolute;inset:0;transition:transform .5s cubic-bezier(.2,.8,.2,1)}
.tile:hover .art{transform:scale(1.06)}
.tile .cap{position:absolute;left:12px;bottom:10px;z-index:2;font:600 9.5px/1 ui-monospace,monospace;letter-spacing:.16em;
color:#fff;text-shadow:0 2px 10px #000;opacity:0;transform:translateY(4px);transition:.25s}
.tile:hover .cap{opacity:1;transform:none}
.tile:focus-visible{outline:2px solid #fff;outline-offset:-3px}
.hud{position:fixed;top:14px;left:14px;z-index:5;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:9px 12px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:2px}
.hud b{color:#ff8a5c}
.lb{position:fixed;inset:0;z-index:50;background:#04050af2;backdrop-filter:blur(14px);display:none;place-items:center;padding:56px 20px}
.lb.on{display:grid}
.lb-art{width:min(86vw,1100px);height:min(72vh,720px);border-radius:6px;position:relative;overflow:hidden;box-shadow:0 50px 120px -30px #000}
.lb-art .art{position:absolute;inset:0}
.lb-title{position:absolute;left:0;right:0;bottom:-58px;display:flex;justify-content:space-between;align-items:baseline;color:#eef1f7}
.lb-title b{font-size:18px;letter-spacing:-.01em}
.lb-title span{font:500 10px/1 ui-monospace,monospace;letter-spacing:.14em;color:#7f889c}
.lb-close{position:absolute;top:18px;right:20px;background:#ffffff12;border:1px solid #ffffff26;color:#fff;
width:38px;height:38px;border-radius:50%;font-size:15px;cursor:pointer;z-index:3}
.lb-nav{position:absolute;top:50%;transform:translateY(-50%);width:42px;height:42px;border-radius:50%;
background:#ffffff12;border:1px solid #ffffff26;color:#fff;font-size:15px;cursor:pointer;z-index:3}
.lb-nav.prev{left:18px}.lb-nav.next{right:18px}
.lb-count{position:absolute;top:24px;left:24px;font:500 10px/1 ui-monospace,monospace;letter-spacing:.18em;color:#8b95a8}
@media(max-width:700px){.grid{grid-template-columns:repeat(2,1fr);grid-template-rows:repeat(4,1fr)}.tile:nth-child(9){display:none}}
''',
html=r'''
<div class="hud"><span class="t">INTERACTIVE 25 · LIGHTBOX</span>click a work · <b id="c">01</b> / 09</div>
<div class="grid" id="grid"></div>
<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Artwork viewer">
  <span class="lb-count" id="lbcount">01 / 09</span>
  <button class="lb-close" id="close" aria-label="Close">✕</button>
  <button class="lb-nav prev" id="prev" aria-label="Previous">←</button>
  <button class="lb-nav next" id="next" aria-label="Next">→</button>
  <div class="lb-art" id="lbart"><div class="art" id="art"></div>
    <div class="lb-title"><b id="title"></b><span id="meta"></span></div>
  </div>
</div>
''',
js=r'''
const works=[
 ['Salt Flats','LANDSCAPE · 01','linear-gradient(165deg,#ffe6bb,#e6a15c 45%,#7a3f2a)'],
 ['Night Swim','STUDY · 02','linear-gradient(160deg,#9fc4ff,#263f7a 55%,#060b16)'],
 ['Red Room','INTERIOR · 03','linear-gradient(150deg,#ff9c72,#8e241c 60%,#180708)'],
 ['Greenhouse','BOTANY · 04','linear-gradient(155deg,#d2f7d9,#25855a 55%,#06170f)'],
 ['Concrete','ARCHIVE · 05','linear-gradient(160deg,#e3ded3,#85807a 55%,#161513)'],
 ['Ultraviolet','COLOUR · 06','linear-gradient(150deg,#d8b4fe,#5b21b6 55%,#0d0616)'],
 ['Paper Moon','STILL · 07','linear-gradient(160deg,#f6f2e8,#b3a692 55%,#262019)'],
 ['Signal','GRAPHIC · 08','linear-gradient(145deg,#ff5a1f,#5a1a8a 55%,#08060e)'],
 ['Tide','COAST · 09','linear-gradient(160deg,#9fe8e0,#2a7a86 55%,#041418)']
];
const grid=document.getElementById('grid'),lb=document.getElementById('lb');let idx=0,lastTile=null;
works.forEach((w,i)=>{
  const b=document.createElement('button');b.className='tile';b.type='button';b.setAttribute('aria-label','Open '+w[0]);
  b.innerHTML='<div class="art" style="background:'+w[2]+'"></div><span class="cap">'+w[0].toUpperCase()+'</span>';
  b.addEventListener('click',()=>openLB(i,b));
  grid.appendChild(b);
});
function paint(){
  const w=works[idx];
  document.getElementById('art').style.background=w[2];
  document.getElementById('title').textContent=w[0];
  document.getElementById('meta').textContent=w[1];
  document.getElementById('lbcount').textContent=String(idx+1).padStart(2,'0')+' / 09';
  document.getElementById('c').textContent=String(idx+1).padStart(2,'0');
}
function openLB(i,tile){idx=i;lastTile=tile;paint();lb.classList.add('on');document.getElementById('close').focus()}
function closeLB(){lb.classList.remove('on');if(lastTile)lastTile.focus()}
function step(d){idx=(idx+d+works.length)%works.length;paint()}
document.getElementById('close').onclick=closeLB;
document.getElementById('prev').onclick=()=>step(-1);
document.getElementById('next').onclick=()=>step(1);
lb.addEventListener('pointerdown',e=>{if(e.target===lb)closeLB()});
document.addEventListener('keydown',e=>{
  if(!lb.classList.contains('on'))return;
  if(e.key==='Escape')closeLB();
  if(e.key==='ArrowLeft')step(-1);
  if(e.key==='ArrowRight')step(1);
});
''',
hint="Click any tile. Arrows navigate, Esc closes, and focus returns to the tile.",
),
]
