# Interactive visuals — part B (10-18)

ADDONS_B = [
dict(
id="image-lens", name="Image Lens",
css=r'''
body{overflow:hidden;background:#06070b}
#base{position:fixed;inset:0;width:100%;height:100%;display:block;cursor:none}
.lens{position:fixed;left:0;top:0;width:220px;height:220px;border-radius:50%;pointer-events:none;z-index:5;
box-shadow:0 0 0 1px #ffffff66,0 30px 70px -10px #000;overflow:hidden;transform:translate(-50%,-50%);
opacity:0;transition:opacity .2s}
.lens.on{opacity:1}
.lens canvas{width:100%;height:100%;display:block}
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
''',
html=r'''
<canvas id="base"></canvas>
<div class="lens" id="lens"><canvas id="zoom" width="440" height="440"></canvas></div>
<div class="hud"><span class="t">INTERACTIVE 10 · IMAGE LENS</span>move to inspect · <b id="z">2.4×</b></div>
<div class="panel">
  <label>ZOOM <input id="zoomR" type="range" min="12" max="50" value="24"></label>
  <label>SIZE <input id="size" type="range" min="120" max="340" value="220"></label>
  <button id="upload">Use my image</button>
  <input type="file" id="file" accept="image/*" hidden>
</div>
''',
js=r'''
const base=document.getElementById('base'),bctx=base.getContext('2d');
const lens=document.getElementById('lens'),zoom=document.getElementById('zoom'),zctx=zoom.getContext('2d');
let W,H,DPR=Math.min(devicePixelRatio||1,2),scene=null;
function paintScene(w,h){
  const c=document.createElement('canvas');c.width=w;c.height=h;const x=c.getContext('2d');
  const sky=x.createLinearGradient(0,0,0,h);
  sky.addColorStop(0,'#1a2240');sky.addColorStop(.38,'#6b4760');sky.addColorStop(.62,'#e07a4f');sky.addColorStop(.72,'#3a2b3c');sky.addColorStop(1,'#0a0d16');
  x.fillStyle=sky;x.fillRect(0,0,w,h);
  const sun=x.createRadialGradient(w*.62,h*.52,2,w*.62,h*.52,w*.16);
  sun.addColorStop(0,'#ffe9c4');sun.addColorStop(.35,'#ffb066');sun.addColorStop(1,'#ff6b3500');
  x.fillStyle=sun;x.beginPath();x.arc(w*.62,h*.52,w*.16,0,Math.PI*2);x.fill();
  x.fillStyle='#ffeccb';x.beginPath();x.arc(w*.62,h*.52,w*.045,0,Math.PI*2);x.fill();
  // mountains
  const ranges=[{y:.58,amp:.12,col:'#241d2c'},{y:.64,amp:.10,col:'#171525'},{y:.71,amp:.075,col:'#0d0e18'}];
  ranges.forEach((r,ri)=>{
    x.beginPath();x.moveTo(0,h);
    for(let i=0;i<=40;i++){const px=i/40*w;const py=h*r.y+Math.sin(i*.55+ri*2.1)*h*r.amp*.5+Math.cos(i*.21+ri)*h*r.amp*.35;x.lineTo(px,py)}
    x.lineTo(w,h);x.closePath();x.fillStyle=r.col;x.fill();
  });
  // water + reflections
  x.fillStyle='#0a0d16';x.fillRect(0,h*.78,w,h*.22);
  for(let i=0;i<70;i++){
    const y=h*.78+Math.random()*h*.22, ww=20+Math.random()*90;
    x.fillStyle='rgba(255,150,90,'+(0.03+Math.random()*.09)+')';
    x.fillRect(w*.62-ww/2+(Math.random()-.5)*60,y,ww,1.4);
  }
  // stars
  for(let i=0;i<90;i++){x.fillStyle='rgba(255,255,255,'+(Math.random()*.5)+')';x.fillRect(Math.random()*w,Math.random()*h*.4,1.2,1.2)}
  return c;
}
function fit(){
  W=innerWidth;H=innerHeight;base.width=W*DPR;base.height=H*DPR;base.style.width=W+'px';base.style.height=H+'px';
  bctx.setTransform(DPR,0,0,DPR,0,0);
  if(!scene||scene.dataset==='gen')scene=paintScene(1600,1000);
  bctx.drawImage(scene,0,0,W,H);
}
fit();addEventListener('resize',fit);
const lensEl=document.getElementById('lens'),zoomR=document.getElementById('zoomR'),sizeR=document.getElementById('size');
let z=2.4,s=220;
function move(e){
  const x=e.clientX,y=e.clientY;
  lens.style.left=x+'px';lens.style.top=y+'px';lens.classList.add('on');
  const d=Math.min(innerWidth,innerHeight);
  zctx.fillStyle='#0a0d16';zctx.fillRect(0,0,440,440);
  const sx=(x/innerWidth)*scene.width, sy=(y/innerHeight)*scene.height;
  const sw=(s/z)/innerWidth*scene.width, sh=(s/z)/innerHeight*scene.height;
  zctx.drawImage(scene,sx-sw/2,sy-sh/2,sw,sh,0,0,440,440);
  zctx.strokeStyle='rgba(255,255,255,.12)';zctx.lineWidth=1;
  zctx.beginPath();zctx.moveTo(220,0);zctx.lineTo(220,440);zctx.moveTo(0,220);zctx.lineTo(440,220);zctx.stroke();
}
addEventListener('pointermove',move);
addEventListener('pointerleave',()=>lens.classList.remove('on'));
zoomR.addEventListener('input',()=>{z=+zoomR.value/10;document.getElementById('z').textContent=z.toFixed(1)+'×'});
sizeR.addEventListener('input',()=>{s=+sizeR.value;lens.style.width=lens.style.height=s+'px'});
document.getElementById('upload').onclick=()=>document.getElementById('file').click();
document.getElementById('file').addEventListener('change',e=>{
  const f=e.target.files[0];if(!f)return;
  const img=new Image();img.onload=()=>{
    const c=document.createElement('canvas');c.width=1600;c.height=Math.round(1600*img.height/img.width);c.dataset='gen';
    const x=c.getContext('2d');const r=Math.max(c.width/img.width,c.height/img.height);
    x.drawImage(img,(c.width-img.width*r)/2,(c.height-img.height*r)/2,img.width*r,img.height*r);
    scene=c;fit();
  };img.src=URL.createObjectURL(f);
});
''',
hint="Move over the scene. Upload your own image and the lens works on it too.",
),
dict(
id="carousel-3d", name="3D Carousel",
css=r'''
body{overflow:hidden;background:radial-gradient(70% 60% at 50% 45%,#151a28,#05060a 72%)}
.stage{position:fixed;inset:0;display:grid;place-items:center;perspective:1300px;touch-action:none;cursor:grab}
.stage.drag{cursor:grabbing}
.ring{position:relative;width:260px;height:360px;transform-style:preserve-3d;transition:transform .12s linear}
.card{position:absolute;inset:0;border-radius:16px;border:1px solid #ffffff26;overflow:hidden;
box-shadow:0 40px 80px -30px #000;display:flex;flex-direction:column;justify-content:flex-end;padding:18px;
backface-visibility:hidden}
.card .no{position:absolute;top:14px;left:16px;font:600 11px/1 ui-monospace,monospace;letter-spacing:.16em;color:#ffffffb0}
.card b{font-size:22px;letter-spacing:-.02em;text-shadow:0 2px 20px #0008}
.card span{font:500 10px/1.5 ui-monospace,monospace;letter-spacing:.12em;color:#ffffffa8;margin-top:4px}
.card .orb{position:absolute;width:170px;height:170px;border-radius:50%;top:70px;left:45px;filter:blur(2px);opacity:.9}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:10px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:9px 12px;backdrop-filter:blur(10px)}
.panel button{background:#171b24;border:1px solid #2a3040;color:#cdd4e1;border-radius:999px;padding:8px 14px;
font:500 11px/1 ui-monospace,monospace;cursor:pointer}
.panel button:hover{border-color:#ff8a5c;color:#fff}
''',
html=r'''
<div class="stage" id="stage"><div class="ring" id="ring"></div></div>
<div class="hud"><span class="t">INTERACTIVE 11 · 3D CAROUSEL</span>drag to spin · <b id="idx">01</b> / 08</div>
<div class="panel"><button id="prev">←</button><button id="auto">Pause spin</button><button id="next">→</button></div>
''',
js=r'''
const ring=document.getElementById('ring'),stage=document.getElementById('stage');
const items=[
 ['Mercury','01','#ff8a5c','#5b1c00'],['Venus','02','#ffd166','#6b4a00'],['Earth','03','#5ec8ff','#003a5b'],
 ['Mars','04','#ff5a1f','#4a1200'],['Jupiter','05','#e0b48a','#4a2c14'],['Saturn','06','#d9c9a3','#4a3d1f'],
 ['Uranus','07','#7ff5e0','#004a40'],['Neptune','08','#5a6bff','#0a124a']
];
const n=items.length, step=360/n;
items.forEach((it,i)=>{
  const c=document.createElement('div');c.className='card';
  c.style.transform='rotateY('+(i*step)+'deg) translateZ(430px)';
  c.style.background='linear-gradient(160deg,'+it[2]+'33,#0a0c12 60%)';
  c.innerHTML='<span class="no">'+it[1]+'</span><div class="orb" style="background:radial-gradient(circle at 35% 30%,'+it[2]+','+it[3]+' 70%)"></div><b>'+it[0]+'</b><span>'+it[1]+' / 08 · SECTOR</span>';
  ring.appendChild(c);
});
let angle=0,target=0,auto=true,last=performance.now();
let down=false,startX=0,startAngle=0,vel=0;
stage.addEventListener('pointerdown',e=>{down=true;startX=e.clientX;startAngle=target;stage.classList.add('drag');stage.setPointerCapture(e.pointerId)});
stage.addEventListener('pointermove',e=>{
  if(!down)return;
  target=startAngle+(e.clientX-startX)*.32;
});
addEventListener('pointerup',()=>{if(down){vel=(target-startAngle)*.02}down=false;stage.classList.remove('drag')});
function frame(t){
  const dt=(t-last)/1000;last=t;
  if(auto&&!down)target+=dt*9;
  if(!down&&Math.abs(vel)>.02){target+=vel;vel*=.94}
  angle+=(target-angle)*.09;
  ring.style.transform='rotateY('+angle+'deg)';
  const idx=((Math.round(angle/step)%n)+n)%n;
  document.getElementById('idx').textContent=String(idx+1).padStart(2,'0');
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
document.getElementById('next').onclick=()=>{target+=step;auto=false;document.getElementById('auto').textContent='Resume spin'};
document.getElementById('prev').onclick=()=>{target-=step;auto=false;document.getElementById('auto').textContent='Resume spin'};
document.getElementById('auto').onclick=()=>{auto=!auto;document.getElementById('auto').textContent=auto?'Pause spin':'Resume spin'};
''',
hint="Drag the ring in either direction, or use the arrows. Pause freezes the spin.",
),
dict(
id="dot-globe", name="Dot Globe",
css=r'''
body{overflow:hidden;background:radial-gradient(60% 60% at 50% 45%,#0e1626,#04050a 70%)}
#cv{position:fixed;inset:0;touch-action:none;cursor:grab}
#cv.drag{cursor:grabbing}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:16px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:10px 18px;backdrop-filter:blur(10px)}
.panel label{display:flex;align-items:center;gap:8px;color:#8b95a8;font:500 10px/1 ui-monospace,monospace;letter-spacing:.08em}
.panel input{width:100px;accent-color:#7fb2ff}
.panel button{background:#171b24;border:1px solid #2a3040;color:#cdd4e1;border-radius:999px;padding:7px 11px;
font:500 10px/1 ui-monospace,monospace;cursor:pointer}
''',
html=r'''
<canvas id="cv"></canvas>
<div class="hud"><span class="t">INTERACTIVE 12 · DOT GLOBE</span>nodes <b id="n">0</b> · drag to rotate</div>
<div class="panel">
  <label>DENSITY <input id="dens" type="range" min="600" max="4000" value="2200"></label>
  <label>SPREAD <input id="spread" type="range" min="0" max="100" value="55"></label>
  <button id="auto">Pause spin</button>
</div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
fit();addEventListener('resize',fit);
let pts=[];
function build(n){
  pts=[];
  const ga=Math.PI*(3-Math.sqrt(5));
  for(let i=0;i<n;i++){
    const y=1-(i/(n-1))*2, r=Math.sqrt(1-y*y), th=ga*i;
    pts.push({x:Math.cos(th)*r,y:y,z:Math.sin(th)*r});
  }
  document.getElementById('n').textContent=n;
}
build(2200);
let yaw=.4,pitch=-.15,auto=true,drag=false,lx=0,ly=0,vy=0,vp=0;
cv.addEventListener('pointerdown',e=>{drag=true;lx=e.clientX;ly=e.clientY;cv.classList.add('drag');cv.setPointerCapture(e.pointerId)});
cv.addEventListener('pointermove',e=>{
  if(!drag)return;
  vy=(e.clientX-lx)*.006;vp=(e.clientY-ly)*.006;
  yaw+=vy;pitch=Math.max(-1.2,Math.min(1.2,pitch+vp));
  lx=e.clientX;ly=e.clientY;
});
addEventListener('pointerup',()=>{drag=false;cv.classList.remove('drag')});
const dens=document.getElementById('dens');
dens.addEventListener('input',()=>build(+dens.value));
document.getElementById('auto').onclick=()=>{auto=!auto;document.getElementById('auto').textContent=auto?'Pause spin':'Resume spin'};
const spread=document.getElementById('spread');
function frame(t){
  const time=t/1000;
  if(auto&&!drag)yaw+=.0035;
  ctx.fillStyle='rgba(4,5,10,.35)';ctx.fillRect(0,0,W,H);
  const cx=W/2,cy=H/2,R=Math.min(W,H)*.34;
  const cyaw=Math.cos(yaw),syaw=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);
  const S=+spread.value/100;
  const bucket={};
  for(const p of pts){
    let x=p.x*cyaw-p.z*syaw, z=p.x*syaw+p.z*cyaw;
    let y=p.y*cp-z*sp; z=p.y*sp+z*cp;
    const d=(z+1)/2;
    if(z<-.15)continue;
    const sx=cx+x*R*(1+S*.4), sy=cy+y*R;
    const b=Math.floor(d*8);
    (bucket[b]||(bucket[b]=[])).push([sx,sy,d]);
  }
  Object.keys(bucket).sort((a,b)=>a-b).forEach(k=>{
    for(const [x,y,d] of bucket[k]){
      const a=.06+Math.pow(d,3)*.85;
      ctx.fillStyle='rgba('+(120+d*80)+','+(170+d*60)+',255,'+a+')';
      const s=.7+d*1.9;
      ctx.fillRect(x-s/2,y-s/2,s,s);
    }
  });
  const g=ctx.createRadialGradient(cx,cy,R*.55,cx,cy,R*1.22);
  g.addColorStop(0,'rgba(90,140,255,0)');
  g.addColorStop(.78,'rgba(90,140,255,.08)');
  g.addColorStop(.94,'rgba(150,195,255,.22)');
  g.addColorStop(1,'rgba(90,140,255,0)');
  ctx.fillStyle=g;ctx.beginPath();ctx.arc(cx,cy,R*1.22,0,Math.PI*2);ctx.fill();
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Drag to spin the globe with inertia. Density redraws the point cloud live.",
),
dict(
id="scroll-gallery", name="Scroll 3D Gallery",
css=r'''
body{background:#05060a;overflow-x:hidden}
.spacer{height:360vh}
.stage{position:sticky;top:0;height:100vh;display:grid;place-items:center;perspective:1400px;overflow:hidden}
.ring{position:relative;width:280px;height:380px;transform-style:preserve-3d;will-change:transform}
.card{position:absolute;inset:0;border-radius:14px;overflow:hidden;border:1px solid #ffffff26;
box-shadow:0 40px 100px -40px #000;display:flex;flex-direction:column;justify-content:flex-end;padding:18px}
.card .art{position:absolute;inset:0}
.card b{position:relative;font-size:19px;letter-spacing:-.01em;text-shadow:0 2px 18px #000}
.card span{position:relative;font:500 9.5px/1.4 ui-monospace,monospace;letter-spacing:.16em;color:#ffffffb0;margin-top:5px}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.prog{position:fixed;left:0;top:0;height:2px;background:#ff6b35;z-index:30;width:0;box-shadow:0 0 12px #ff6b35}
.hint{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);color:#5e687c;font:500 9.5px/1 ui-monospace,monospace;letter-spacing:.18em;z-index:10}
''',
html=r'''
<div class="prog" id="prog"></div>
<div class="stage"><div class="ring" id="ring"></div></div>
<div class="spacer"></div>
<div class="hud"><span class="t">INTERACTIVE 13 · SCROLL GALLERY</span>scroll or drag · <b id="idx">01</b> / 07</div>
<div class="hint">SCROLL ↓</div>
''',
js=r'''
const ring=document.getElementById('ring');
const works=[
 ['Salt Flats','LANDSCAPE · 01','linear-gradient(160deg,#ffd9a0,#c97b4a 45%,#2b1a22)'],
 ['Night Swim','STUDY · 02','linear-gradient(150deg,#7fb2ff,#1b2a5e 55%,#050811)'],
 ['Red Room','INTERIOR · 03','linear-gradient(160deg,#ff8a5c,#7a1f1a 60%,#160608)'],
 ['Greenhouse','BOTANY · 04','linear-gradient(150deg,#b7f5c8,#1f7a4d 55%,#06140d)'],
 ['Concrete','ARCHIVE · 05','linear-gradient(160deg,#d7d2c8,#6b6760 55%,#141312)'],
 ['Ultraviolet','COLOUR · 06','linear-gradient(150deg,#c084fc,#4a1d7a 55%,#0d0616)'],
 ['Paper Moon','STILL · 07','linear-gradient(160deg,#f4f0e6,#a89a86 55%,#241f1a)']
];
const n=works.length,step=360/n;
works.forEach((w,i)=>{
  const c=document.createElement('div');c.className='card';
  c.style.transform='rotateY('+(i*step)+'deg) translateZ(460px)';
  c.innerHTML='<div class="art" style="background:'+w[2]+'"></div><b>'+w[0]+'</b><span>'+w[1]+'</span>';
  ring.appendChild(c);
});
let angle=0,drag=false,lx=0,offset=0;
addEventListener('pointerdown',e=>{drag=true;lx=e.clientX});
addEventListener('pointermove',e=>{if(drag){angle+=(e.clientX-lx)*.3;lx=e.clientX}});
addEventListener('pointerup',()=>drag=false);
function frame(){
  const max=document.body.scrollHeight-innerHeight;
  const p=max>0?scrollY/max:0;
  document.getElementById('prog').style.width=(p*100)+'%';
  const target=p*(n-1)*step;
  offset+=(target-offset)*.08;
  ring.style.transform='rotateY('+(angle+offset)+'deg)';
  const idx=((Math.round(-(angle+offset)/step)%n)+n)%n;
  document.getElementById('idx').textContent=String(idx+1).padStart(2,'0');
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Scroll the page: the ring turns one card per section. You can also drag it.",
),
dict(
id="voxel-terrain", name="Voxel Terrain",
css=r'''
body{overflow:hidden;background:radial-gradient(70% 60% at 50% 40%,#101a20,#04060a 72%)}
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
<div class="hud"><span class="t">INTERACTIVE 14 · VOXEL TERRAIN</span>drag to raise · <b id="h">0.0</b> max height</div>
<div class="panel">
  <label>SCALE <input id="height" type="range" min="30" max="100" value="62"></label>
  <button id="rotate">Rotate 90°</button>
  <button id="regen">New terrain</button>
</div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
fit();addEventListener('resize',fit);
const N=12;let grid=[],rot=0,seed=Math.random()*100;
function build(){
  grid=[];
  for(let x=0;x<N;x++){grid[x]=[];for(let y=0;y<N;y++){
    const d=Math.hypot(x-N/2,y-N/2)/(N/2);
    const ridge=Math.exp(-Math.pow((x-5.5)/3.2,2))*Math.exp(-Math.pow((y-6.5)/4.2,2))*.9;
    const h=.55+Math.sin(x*.62+seed)*.28+Math.cos(y*.5+seed*1.3)*.26+Math.sin((x+y)*.38+seed*.7)*.22+ridge;
    grid[x][y]=Math.max(.12,h*(1-d*.5));
  }}
}
build();
function rotateGrid(){
  const g=[];for(let x=0;x<N;x++){g[x]=[];for(let y=0;y<N;y++)g[x][y]=grid[N-1-y][x]}
  grid=g;rot++;
}
document.getElementById('rotate').onclick=rotateGrid;
document.getElementById('regen').onclick=()=>{seed=Math.random()*100;build()};
let down=false;
function raise(e){
  const tw=Math.min(W/(N*1.55),72), th=tw*.55;
  const ox=W/2, oy=H*.2;
  const sx=e.clientX-ox, sy=e.clientY-oy;
  const gx=Math.round(sx/tw+sy/th), gy=Math.round(sy/th-sx/tw);
  if(gx<1||gy<1||gx>=N-1||gy>=N-1)return;
  for(let dx=-1;dx<=1;dx++)for(let dy=-1;dy<=1;dy++){
    const x=gx+dx,y=gy+dy;if(x<0||y<0||x>=N||y>=N)continue;
    const f=(dx||dy)?(dx&&dy?.5:1):1.6;
    grid[x][y]=Math.min(2.4,grid[x][y]+.11*f);
  }
}
cv.addEventListener('pointerdown',e=>{down=true;raise(e);cv.setPointerCapture(e.pointerId)});
cv.addEventListener('pointermove',e=>{if(down)raise(e)});
addEventListener('pointerup',()=>down=false);
const heightEl=document.getElementById('height');
function frame(){
  ctx.fillStyle='#04060a';ctx.fillRect(0,0,W,H);
  const tw=Math.min(W/(N*1.55),72), th=tw*.55;
  const ox=W/2, oy=H*.2;
  const hMax=+heightEl.value, maxH=2.4;
  document.getElementById('h').textContent=Math.max(...grid.flat()).toFixed(1);
  const cubes=[];
  for(let x=0;x<N;x++)for(let y=0;y<N;y++){
    cubes.push({x,y,h:grid[x][y],depth:x+y});
  }
  cubes.sort((a,b)=>a.depth-b.depth);
  for(const c of cubes){
    const px=ox+(c.x-c.y)*tw/2, py=oy+(c.x+c.y)*th/2 - c.h*(hMax/100)*105;
    const w=tw*.86, hh=th*.5, depth=c.h*(hMax/100)*95;
    // faces
    ctx.fillStyle='rgba(20,60,52,.95)';
    ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(px-w/2,py+hh/2);ctx.lineTo(px-w/2,py+hh/2+depth);ctx.lineTo(px,py+depth);ctx.closePath();ctx.fill();
    ctx.fillStyle='rgba(12,40,36,.95)';
    ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(px+w/2,py+hh/2);ctx.lineTo(px+w/2,py+hh/2+depth);ctx.lineTo(px,py+depth);ctx.closePath();ctx.fill();
    const shade=.28+c.h*.62;
    ctx.fillStyle='rgba('+Math.round(50*shade+14)+','+Math.round(215*shade+16)+','+Math.round(150*shade+18)+',.97)';
    ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(px+w/2,py+hh/2);ctx.lineTo(px,py+hh);ctx.lineTo(px-w/2,py+hh/2);ctx.closePath();ctx.fill();
  }
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Drag across the terrain to push hills up. Rotate and regenerate reshuffle it.",
),
dict(
id="parallax-scene", name="Parallax Scene",
css=r'''
body{overflow:hidden;background:#05060a}
.scene{position:fixed;inset:-6%;perspective:1200px;overflow:hidden}
.world{position:absolute;inset:0;transform-style:preserve-3d;transition:transform .12s ease-out;will-change:transform}
.layer{position:absolute;inset:-10%;will-change:transform}
.sky{background:linear-gradient(180deg,#0a1030,#26264f 35%,#6b4560 62%,#c47a56 78%,#151018 100%)}
.stars{background-image:radial-gradient(1.4px 1.4px at 20% 18%,#fff9,transparent),radial-gradient(1.2px 1.2px at 68% 12%,#fff7,transparent),radial-gradient(1px 1px at 42% 30%,#fff6,transparent),radial-gradient(1.6px 1.6px at 82% 34%,#fff8,transparent),radial-gradient(1px 1px at 12% 42%,#fff5,transparent),radial-gradient(1.2px 1.2px at 55% 8%,#fff6,transparent);background-size:100% 100%}
.moon{background:radial-gradient(circle at 66% 40%,#fff3d6 0 3.2%,#ffe9b0 3.3% 3.6%,transparent 4%),radial-gradient(circle at 66% 40%,#ffcf8a44,transparent 22%)}
.far{background:linear-gradient(180deg,transparent 55%,#1c1a2c 55.4%,#141322 72%,transparent 72.4%)}
.mid{background:linear-gradient(180deg,transparent 63%,#0f1420 63.3%,#0a0e17 82%,transparent 82.3%)}
.trees{background:
 repeating-linear-gradient(90deg,transparent 0 60px,#06080e 60px 66px,transparent 66px 120px);
 -webkit-mask:linear-gradient(180deg,transparent 60%,#000 70%);mask:linear-gradient(180deg,transparent 60%,#000 70%)}
.fog{background:linear-gradient(180deg,transparent 58%,#8b7a9a33 66%,#c9a98a22 76%,transparent 86%);filter:blur(14px)}
.fore{background:linear-gradient(180deg,transparent 84%,#05060a 84.3%)}
.tip{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);color:#ffffff55;font:500 9.5px/1 ui-monospace,monospace;letter-spacing:.2em;z-index:10}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);z-index:10;display:flex;gap:16px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:10px 18px;backdrop-filter:blur(10px)}
.panel label{display:flex;align-items:center;gap:8px;color:#8b95a8;font:500 10px/1 ui-monospace,monospace;letter-spacing:.08em}
.panel input{width:110px;accent-color:#7fb2ff}
''',
html=r'''
<div class="scene"><div class="world" id="world">
  <div class="layer sky"></div><div class="layer stars" data-z="0.1"></div><div class="layer moon" data-z="0.16"></div>
  <div class="layer far" data-z="0.3"></div><div class="layer fog" data-z="0.5"></div>
  <div class="layer mid" data-z="0.7"></div><div class="layer trees" data-z="1"></div><div class="layer fore" data-z="1.3"></div>
</div></div>
<div class="hud"><span class="t">INTERACTIVE 15 · PARALLAX SCENE</span>move the pointer · <b id="d">1.0</b>× depth</div>
<div class="panel"><label>DEPTH <input id="depth" type="range" min="0" max="220" value="100"></label></div>
''',
js=r'''
const world=document.getElementById('world'),layers=[...document.querySelectorAll('.layer')],depth=document.getElementById('depth');
let tx=0,ty=0,cx=0,cy=0;
addEventListener('pointermove',e=>{
  tx=(e.clientX/innerWidth-.5);ty=(e.clientY/innerHeight-.5);
});
function frame(){
  cx+=(tx-cx)*.06;cy+=(ty-cy)*.06;
  const D=+depth.value/100;
  world.style.transform='rotateX('+(-cy*5*D)+'deg) rotateY('+(cx*7*D)+'deg)';
  layers.forEach(l=>{
    const z=parseFloat(l.dataset.z||0);
    l.style.transform='translate3d('+(cx*z*30*D)+'px,'+(cy*z*22*D)+'px,0)';
  });
  document.getElementById('d').textContent=D.toFixed(1);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Move the pointer: each layer shifts by a different depth. Depth at 0 flattens it.",
),
dict(
id="text-particles", name="Text to Particles",
css=r'''
body{overflow:hidden;background:#05060a}
#cv{position:fixed;inset:0;touch-action:none}
.bar{position:fixed;left:50%;top:22px;transform:translateX(-50%);z-index:10;display:flex;gap:8px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:7px 8px 7px 16px;backdrop-filter:blur(10px)}
.bar label{color:#6d778c;font:500 9.5px/1 ui-monospace,monospace;letter-spacing:.14em}
.bar input{background:none;border:0;outline:none;color:#eef1f7;font:600 13px/1 ui-monospace,monospace;letter-spacing:.06em;width:180px}
.bar button{background:#f2f4f8;color:#0a0a0e;border:0;border-radius:999px;padding:8px 13px;font:700 10px/1 ui-monospace,monospace;cursor:pointer}
.bar button.ghost{background:#171b24;color:#cdd4e1;border:1px solid #2a3040;font-weight:500}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
''',
html=r'''
<canvas id="cv"></canvas>
<div class="hud"><span class="t">INTERACTIVE 16 · TEXT PARTICLES</span>particles <b id="n">0</b> · move to scatter</div>
<div class="bar"><label>TEXT</label><input id="txt" value="FORM" maxlength="12" spellcheck="false"><button id="explode">Explode</button><button class="ghost" id="reset">Reset</button></div>
''',
js=r'''
const cv=document.getElementById('cv'),ctx=cv.getContext('2d'),input=document.getElementById('txt');
let W,H,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);ctx.fillStyle='#05060a';ctx.fillRect(0,0,W,H);}
fit();addEventListener('resize',fit);
const mouse={x:-9999,y:-9999};
addEventListener('pointermove',e=>{mouse.x=e.clientX;mouse.y=e.clientY});
addEventListener('pointerleave',()=>{mouse.x=-9999});
let parts=[],built='';
function targetPoints(text){
  const off=document.createElement('canvas');off.width=W;off.height=H;
  const x=off.getContext('2d');
  const size=Math.min(W/(text.length*.62),H*.42);
  x.fillStyle='#fff';x.textAlign='center';x.textBaseline='middle';
  x.font='900 '+size+'px system-ui,sans-serif';
  x.fillText(text,W/2,H/2);
  const data=x.getImageData(0,0,W,H).data, pts=[];
  const gap=Math.max(3,Math.round(size/36));
  for(let y=0;y<H;y+=gap)for(let xx=0;xx<W;xx+=gap){
    if(data[(y*W+xx)*4+3]>128)pts.push([xx,y]);
  }
  return pts;
}
function build(text,animate){
  const pts=targetPoints(text);
  const max=7000;const step=Math.max(1,Math.floor(pts.length/max));
  const chosen=pts.filter((_,i)=>i%step===0);
  if(!animate||!parts.length){
    parts=chosen.map((p,i)=>({x:Math.random()*W,y:Math.random()*H,tx:p[0],ty:p[1],vx:0,vy:0,
      h:205+Math.random()*40,s:1+Math.random()*1.4}));
  }else{
    parts.forEach((p,i)=>{const t=chosen[i%chosen.length];p.tx=t[0];p.ty=t[1]});
  }
  built=text;
  document.getElementById('n').textContent=parts.length;
}
build('FORM',false);
input.addEventListener('input',()=>{if(input.value.trim())build(input.value.toUpperCase().slice(0,12),true)});
document.getElementById('explode').onclick=()=>parts.forEach(p=>{p.vx=(Math.random()-.5)*44;p.vy=(Math.random()-.5)*44});
document.getElementById('reset').onclick=()=>{parts.forEach(p=>{p.x=Math.random()*W;p.y=Math.random()*H;p.vx=0;p.vy=0})};
function frame(){
  ctx.fillStyle='rgba(5,6,10,.20)';ctx.fillRect(0,0,W,H);
  ctx.globalCompositeOperation='lighter';
  for(const p of parts){
    const dx=p.x-mouse.x,dy=p.y-mouse.y,d=Math.hypot(dx,dy);
    if(d<90&&d>1){p.vx+=dx/d*(90-d)*.14;p.vy+=dy/d*(90-d)*.14}
    p.vx+=(p.tx-p.x)*.028;p.vy+=(p.ty-p.y)*.028;
    p.vx*=.90;p.vy*=.90;p.x+=p.vx;p.y+=p.vy;
    ctx.fillStyle='hsla('+p.h+',90%,66%,.55)';
    ctx.fillRect(p.x,p.y,p.s,p.s);
  }
  ctx.globalCompositeOperation='source-over';
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Type a word in the field (up to 12 characters). Explode scatters it, Reset rebuilds.",
),
dict(
id="kinetic-type", name="Kinetic Type Lab",
css=r'''
body{overflow:hidden;background:#07080c;cursor:crosshair}
.stage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;padding:0 4vw}
.word{display:flex;line-height:.8;user-select:none}
.word span{display:inline-block;font:900 clamp(64px,15vw,220px)/.8 system-ui,sans-serif;letter-spacing:-.06em;color:#f2f4f8;
will-change:transform;transform-origin:50% 80%}
.hud{position:fixed;top:16px;left:16px;z-index:10;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;
padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#8b95a8;backdrop-filter:blur(8px)}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hud b{color:#ff8a5c}
.panel{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);z-index:10;display:flex;gap:16px;align-items:center;
background:#0b0d13d9;border:1px solid #ffffff1f;border-radius:999px;padding:10px 18px;backdrop-filter:blur(10px);flex-wrap:wrap;justify-content:center}
.panel label{display:flex;align-items:center;gap:8px;color:#8b95a8;font:500 10px/1 ui-monospace,monospace;letter-spacing:.08em}
.panel input{width:90px;accent-color:#ff6b35}
.panel button{background:#171b24;border:1px solid #2a3040;color:#cdd4e1;border-radius:999px;padding:7px 11px;
font:500 10px/1 ui-monospace,monospace;cursor:pointer}
''',
html=r'''
<div class="stage"><div class="word" id="word"></div></div>
<div class="hud"><span class="t">INTERACTIVE 17 · KINETIC TYPE</span>point to bend · click to change word</div>
<div class="panel">
  <label>WAVE <input id="amp" type="range" min="0" max="100" value="42"></label>
  <label>SPEED <input id="speed" type="range" min="0" max="100" value="34"></label>
  <label>TRACK <input id="track" type="range" min="-8" max="14" value="0"></label>
</div>
''',
js=r'''
const word=document.getElementById('word'),amp=document.getElementById('amp'),speed=document.getElementById('speed'),track=document.getElementById('track');
const words=['MOTION','FORM','RHYTHM','TYPE','SIGNAL'];
let wi=0,letters=[];
function build(){
  word.innerHTML='';
  const w=words[wi];
  letters=[...w].map((ch,i)=>{
    const s=document.createElement('span');s.textContent=ch;word.appendChild(s);
    s.style.color=i%2?'#ff8a5c':'#f2f4f8';
    return s;
  });
}
build();
word.addEventListener('click',()=>{wi=(wi+1)%words.length;build()});
const mouse={x:-9999,y:-9999};
addEventListener('pointermove',e=>{mouse.x=e.clientX;mouse.y=e.clientY});
addEventListener('pointerleave',()=>{mouse.x=-9999});
let t=0,last=performance.now();
function frame(now){
  const dt=Math.min((now-last)/1000,.05);last=now;t+=dt;
  const A=+amp.value/100, T=+speed.value/100;
  const trackPx=+track.value;
  letters.forEach((el,i)=>{
    const r=el.getBoundingClientRect(),l=r.left+r.width/2,top=r.top+r.height/2;
    const d=Math.hypot(mouse.x-l,mouse.y-top);
    const near=Math.max(0,1-d/360);
    const wave=Math.sin(t*T*8+i*.55)*A*26;
    const bend=(mouse.x>l?-1:1)*near*near*26;
    const sc=1+near*.18;
    el.style.transform='translateY('+(wave+near*12)+'px) rotate('+bend+'deg) scale('+sc+')';
    el.style.marginLeft=trackPx+'px';
  });
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
''',
hint="Click the word to cycle. Hover to bend letters; the three sliders reshape the field.",
),
dict(
id="dither-lab", name="Dither Lab",
css=r'''
body{overflow:hidden;background:#06070b}
#out{position:fixed;inset:0;width:100%;height:100%;display:block;cursor:crosshair;image-rendering:pixelated}
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
<canvas id="out"></canvas>
<div class="hud"><span class="t">INTERACTIVE 18 · DITHER LAB</span>move to change threshold · <b id="mode">BAYER 8×8</b></div>
<div class="panel">
  <label>GRAIN <input id="px" type="range" min="2" max="16" value="6"></label>
  <label>CONTRAST <input id="th" type="range" min="-40" max="40" value="0"></label>
  <button id="invert">Invert</button><button id="upload">Use my image</button>
  <input type="file" id="file" accept="image/*" hidden>
</div>
''',
js=r'''
const out=document.getElementById('out'),octx=out.getContext('2d');
let W,H,scene=null,DPR=1;
const BAYER=[[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],[60,28,52,20,62,30,54,22],[3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],[15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]];
function sceneCanvas(w,h){
  const c=document.createElement('canvas');c.width=w;c.height=h;const x=c.getContext('2d');
  const g=x.createLinearGradient(0,0,w,h);
  g.addColorStop(0,'#ffd9a0');g.addColorStop(.4,'#ff6b35');g.addColorStop(.7,'#6b2f5a');g.addColorStop(1,'#0a0d16');
  x.fillStyle=g;x.fillRect(0,0,w,h);
  x.fillStyle='#0a0d16';x.beginPath();
  for(let i=0;i<=40;i++){const px=i/40*w;const py=h*.62+Math.sin(i*.6)*h*.08+Math.cos(i*.23)*h*.05;x.lineTo(px,py)}
  x.lineTo(w,h);x.lineTo(0,h);x.fill();
  x.globalAlpha=.85;
  for(let i=0;i<5;i++){
    x.beginPath();x.arc(w*(.2+i*.15),h*(.3+ (i%2)*.08),w*.09*(1+i*.12),0,Math.PI*2);
    x.fillStyle=['#f4f0e6','#ffb08a','#c084fc','#7fb2ff','#3ddc84'][i];x.fill();
  }
  x.globalAlpha=1;
  return c;
}
function fit(){
  W=innerWidth;H=innerHeight;DPR=Math.min(devicePixelRatio||1,2);
  out.width=W;out.height=H;out.style.width=W+'px';out.style.height=H+'px';
  if(!scene)scene=sceneCanvas(1600,1000);
}
fit();addEventListener('resize',fit);
const pxEl=document.getElementById('px'),thEl=document.getElementById('th');
let invert=false, mx=.5;
addEventListener('pointermove',e=>{mx=e.clientX/innerWidth});
const off=document.createElement('canvas'),offc=off.getContext('2d');
function render(){
  const block=+pxEl.value;
  const cols=Math.max(40,Math.round(W/block)), rows=Math.max(24,Math.round(H/block));
  off.width=cols;off.height=rows;
  offc.drawImage(scene,0,0,cols,rows);
  const data=offc.getImageData(0,0,cols,rows).data;
  out.width=cols;out.height=rows;out.style.width=W+'px';out.style.height=H+'px';
  const img=octx.createImageData(cols,rows);
  const tint=[255,138,92];
  const thBase=+thEl.value/100 + (mx-.5)*.5;
  for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){
    const i=(y*cols+x)*4;
    const lum=(data[i]*.299+data[i+1]*.587+data[i+2]*.114)/255;
    const t=(BAYER[y%8][x%8]/64-.5)*.5;
    let on=lum+t> .5-thBase;
    if(invert)on=!on;
    const o=i;
    if(on){
      const k=.55+lum*.6;
      img.data[o]=tint[0]*k;img.data[o+1]=tint[1]*k;img.data[o+2]=tint[2]*k;img.data[o+3]=255;
    }else{img.data[o]=8;img.data[o+1]=9;img.data[o+2]=14;img.data[o+3]=255;}
  }
  octx.putImageData(img,0,0);
}
let raf=null;
function queue(){if(raf)return;raf=requestAnimationFrame(()=>{raf=null;render()})}
pxEl.addEventListener('input',queue);thEl.addEventListener('input',queue);
addEventListener('pointermove',queue);
document.getElementById('invert').onclick=()=>{invert=!invert;queue()};
document.getElementById('upload').onclick=()=>document.getElementById('file').click();
document.getElementById('file').addEventListener('change',e=>{
  const f=e.target.files[0];if(!f)return;
  const img=new Image();img.onload=()=>{
    const c=document.createElement('canvas');c.width=1600;c.height=Math.round(1600*img.height/img.width);
    const x=c.getContext('2d');const r=Math.max(c.width/img.width,c.height/img.height);
    x.drawImage(img,(c.width-img.width*r)/2,(c.height-img.height*r)/2,img.width*r,img.height*r);
    scene=c;fit();render();
  };img.src=URL.createObjectURL(f);
});
render();
''',
hint="Move sideways to push the threshold. Upload a photo and it dithers that instead.",
),
]
