"""Canvas engines for the interactive batch.

Each engine branches on a variant so the demo actually does what its card
promises (a gravity well pulls, a vortex spins, a scratch card erases, a slot
machine lands on a word). No libraries, no build step.
"""

VARIANTS = {
    "voronoi-repel": "repel", "crystal-growth": "crystal",
    "silk-flow-field": "silk", "ember-drift": "ember", "vortex-chamber": "vortex",
    "magnetic-filings": "filings", "marbled-paper": "marbled", "aurora-curtain": "aurora",
    "orbital-dust": "dust", "gravity-wells": "gravity", "slingshot-orbit": "slingshot",
    "wireframe-torus": "torus", "star-nursery": "nursery", "parallax-starfield": "stars",
    "interference-weave": "interference", "seismograph-grid": "seismo",
    "pressure-field": "pressure", "applause-meter": "bars",
    "bloom-metaballs": "metaballs", "cell-division": "division",
    "magnetic-ink": "ink", "elastic-cursor": "elastic", "repulsion-dots": "repel",
    "drag-constellation": "constellation", "halftone-breathe": "halftone",
    "scratch-to-reveal": "scratch",
    "particle-fountain": "fountain", "comet-trails": "comet",
    "confetti-cannon": "confetti", "sparkler-trail": "sparkler",
    "glyph-storm": "storm", "letter-magnet": "magnet",
    "text-vortex": "vortex", "word-constellation": "constellation",
    "slot-machine-glyphs": "slot",
    "decode-rain": "decode", "ascii-current": "ascii", "pixel-sort-live": "pixelsort",
    "isometric-city": "city", "voxel-dunes": "dunes", "cube-stack": "stack",
    "floating-glyph-cubes": "glyphcubes",
    "contour-drift": "contour", "topographic-scan": "scan", "terrain-flyover": "flyover",
    "ripple-pond": "ripple", "tunnel-vision": "tunnel", "countdown-burst": "countdown",
    "harmonograph-ribbons": "harmonograph", "mirrored-wedges": "kaleido",
}

ENGINES = {}

ENGINES["voronoi"] = r"""
const V='__V__';
let sites=[];for(let i=0;i<__N__;i++)sites.push({x:rnd(W),y:rnd(H),ph:rnd(TAU)});
function clip(poly,ax,ay,nx,ny){const out=[];for(let i=0;i<poly.length;i++){const p=poly[i],q=poly[(i+1)%poly.length];const dp=(p[0]-ax)*nx+(p[1]-ay)*ny,dq=(q[0]-ax)*nx+(q[1]-ay)*ny;if(dp<=0)out.push(p);if(dp*dq<0){const k=dp/(dp-dq);out.push([p[0]+(q[0]-p[0])*k,p[1]+(q[1]-p[1])*k]);}}return out;}
function cell(s){let poly=[[0,0],[W,0],[W,H],[0,H]];for(const o of sites){if(o===s)continue;poly=clip(poly,(s.x+o.x)/2,(s.y+o.y)/2,o.x-s.x,o.y-s.y);if(poly.length<3)break;}return poly;}
function frame(dt){ctx.fillStyle=P[0];ctx.fillRect(0,0,W,H);let n=0;
 for(const s of sites){const slow=V==='crystal'?.2:.7,jit=V==='crystal'?2:8;
  s.ph+=dt*slow;s.x+=Math.sin(s.ph)*jit*dt;s.y+=Math.cos(s.ph*1.3)*jit*dt;
  if(V!=='crystal'){const dx=s.x-mx.x,dy=s.y-mx.y,d=Math.hypot(dx,dy);if(d<160&&d>1){const f=(1-d/160)*340;s.x+=dx/d*f*dt;s.y+=dy/d*f*dt;}}
  s.x=Math.max(0,Math.min(W,s.x));s.y=Math.max(0,Math.min(H,s.y));}
 for(const s of sites){const p=cell(s);if(p.length<3)continue;let a=0;for(let i=0;i<p.length;i++){const q=p[i],r=p[(i+1)%p.length];a+=q[0]*r[1]-r[0]*q[1];}a=Math.abs(a/2);
  const k=Math.min(1,Math.log10(a+1)/4.2);
  const c=V==='crystal'?(a>12000?P[4]:a>6000?P[3]:P[2]):P[1+Math.floor(k*(P.length-2))];
  ctx.fillStyle=c;ctx.strokeStyle=V==='crystal'?P[4]:P[0];ctx.lineWidth=V==='crystal'?1.5:1.2;
  ctx.beginPath();p.forEach((q,i)=>i?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1]));ctx.closePath();ctx.fill();ctx.stroke();n++;}
 stat(n+(V==='crystal'?' crystal cells':' cells'));}
"""

ENGINES["flow"] = r"""
const V='__V__';
const ps=[];for(let i=0;i<950;i++)ps.push({x:rnd(W),y:rnd(H),px:0,py:0,h:Math.random(),age:Math.random()});
function frame(dt){
 if(V==='filings'){
  ctx.fillStyle='rgba(6,6,10,.3)';ctx.fillRect(0,0,W,H);ctx.lineWidth=1.2;
  for(const p of ps){const dx=mx.x-p.x,dy=mx.y-p.y,d=Math.hypot(dx,dy)||1,fall=Math.max(0,1-d/240);
   const base=Math.sin(p.x*.004+t*.4)*1.6+Math.cos(p.y*.003-t*.3)*1.2;
   const a=base*(1-fall)+Math.atan2(dy,dx)*fall, len=4+fall*16;
   ctx.strokeStyle=P[2+(fall>.5?1:0)];ctx.globalAlpha=.35+fall*.6;
   ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p.x+Math.cos(a)*len,p.y+Math.sin(a)*len);ctx.stroke();
   p.x+=Math.cos(a)*16*dt;p.y+=Math.sin(a)*16*dt;
   if(p.x<0||p.x>W||p.y<0||p.y>H){p.x=rnd(W);p.y=rnd(H);}}
  ctx.globalAlpha=1;stat(ps.length+' filings');return;
 }
 const fade=V==='marbled'?.02:V==='ember'?.10:.09;
 ctx.fillStyle='rgba(6,6,10,'+fade+')';ctx.fillRect(0,0,W,H);
 for(const p of ps){let ang=Math.sin(p.x*.0035+t*.55)*1.9+Math.cos(p.y*.003-t*.4)*1.3;
  if(V==='vortex'){const dx=p.x-mx.x,dy=p.y-mx.y,d=Math.hypot(dx,dy)||1,fall=Math.max(0,1-d/340);ang=Math.atan2(dy,dx)+Math.PI/2*(.35+fall*1.8);}
  if(V==='ember'){ang=-Math.PI/2+Math.sin(p.x*.006+t*.8)*.95;p.age+=dt*.28;}
  const sp=V==='marbled'?26:V==='ember'?72:82;
  p.px=p.x;p.py=p.y;p.x+=Math.cos(ang)*sp*dt;p.y+=Math.sin(ang)*sp*dt;
  if(V!=='marbled'){const dx=p.x-mx.x,dy=p.y-mx.y,d=Math.hypot(dx,dy);if(d<190&&d>1){p.x+=dx/d*110*dt;p.y+=dy/d*110*dt;}}
  let out=p.x<-12||p.x>W+12||p.y<-12||p.y>H+12;
  if(V==='ember'&&p.y<-12){out=true;}
  if(out){p.x=rnd(W);p.y=V==='ember'?H+10:rnd(H);p.px=p.x;p.py=p.y;p.age=0;}
  const ci=V==='ember'?P[1+Math.min(P.length-2,Math.floor(p.age*(P.length-1)))]:P[1+Math.floor(p.h*(P.length-2))];
  ctx.strokeStyle=ci;ctx.globalAlpha=V==='marbled'?.7:.55;ctx.lineWidth=V==='marbled'?1.6:1;
  ctx.beginPath();ctx.moveTo(p.px,p.py);ctx.lineTo(p.x,p.y);ctx.stroke();}
 ctx.globalAlpha=1;stat(ps.length+' particles');}
"""

ENGINES["aurora"] = r"""
const V='__V__';
function frame(dt){ctx.fillStyle='rgba(4,7,10,.12)';ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='lighter';
 for(let i=0;i<64;i++){const bx=(i/63)*W, lean=(mx.x-W/2)/W*.16;
  const x=bx+Math.sin(t*.5+i*.27)*36+lean*W*(i/63);
  const y0=H*.08, h=H*(.5+.28*Math.sin(t*.3+i*.19)), sway=10+14*Math.sin(i*.4);
  const g=ctx.createLinearGradient(x,y0,x+sway,y0+h);
  g.addColorStop(0,P[3]+'00');g.addColorStop(.28,P[3]+'66');g.addColorStop(.62,P[2]+'77');g.addColorStop(1,P[1]+'00');
  ctx.strokeStyle=g;ctx.lineWidth=5+3*Math.sin(i);
  ctx.beginPath();for(let y=0;y<=h;y+=10)ctx.lineTo(x+Math.sin(y*.018+t*1.1+i*.3)*sway,y0+y);ctx.stroke();}
 ctx.globalCompositeOperation='source-over';stat('64 curtains');}
"""

ENGINES["orbit"] = r"""
const V='__V__';
let ps=[],pmx=mx.x,pmy=mx.y,pvx=0,pvy=0;
if(V==='torus'){for(let i=0;i<520;i++)ps.push({u:rnd(TAU),v:rnd(TAU),s:rnd(1,.3)});}
else if(V==='gravity'||V==='slingshot'){for(let i=0;i<260;i++)ps.push({x:rnd(W),y:rnd(H),vx:rnd(60,-60),vy:rnd(60,-60),a:rnd(TAU),r:rnd(240,40),sp:rnd(1,.2),ph:rnd(TAU)});}
else{for(let i=0;i<300;i++)ps.push({a:rnd(TAU),r:rnd(Math.min(W,H)*.47,24),sp:rnd(1.1,.15)*(Math.random()<.5?-1:1),ph:rnd(TAU),life:rnd(1)});}
function frame(dt){
 pvx=(mx.x-pmx)/Math.max(dt,.001);pvy=(mx.y-pmy)/Math.max(dt,.001);pmx=mx.x;pmy=mx.y;
 if(V==='torus'){
  ctx.fillStyle='rgba(5,6,11,.22)';ctx.fillRect(0,0,W,H);
  const cx=W/2,cy=H/2,R=Math.min(W,H)*.30,rr=R*.36,ax=t*.35+(mx.x-W/2)/W*1.4,ay=t*.27+(mx.y-H/2)/H*1.2;
  for(const p of ps){const u=p.u+ax,v=p.v+ay;
   const x3=(R+rr*Math.cos(v))*Math.cos(u),y3=(R+rr*Math.cos(v))*Math.sin(u),z3=rr*Math.sin(v);
   const k=520/(520+z3),x=cx+x3*k,y=cy+y3*k;
   ctx.fillStyle=P[2+(z3>0?2:0)];ctx.globalAlpha=.55+.4*k;
   ctx.beginPath();ctx.arc(x,y,1.1+p.s*1.6,0,TAU);ctx.fill();}
  ctx.globalAlpha=1;stat(ps.length+' torus points');return;
 }
 if(V==='gravity'||V==='slingshot'){
  ctx.fillStyle='rgba(5,6,11,.16)';ctx.fillRect(0,0,W,H);
  if(V==='gravity'){const g=ctx.createRadialGradient(mx.x,mx.y,0,mx.x,mx.y,190);g.addColorStop(0,P[4]+'66');g.addColorStop(.2,P[2]+'44');g.addColorStop(1,P[0]+'00');ctx.fillStyle=g;ctx.beginPath();ctx.arc(mx.x,mx.y,190,0,TAU);ctx.fill();
   ctx.strokeStyle=P[3];ctx.globalAlpha=.13;ctx.lineWidth=1;
   for(let gy=0;gy<=H;gy+=34){ctx.beginPath();for(let gx=0;gx<=W;gx+=10){const dx=gx-mx.x,dy=gy-mx.y,d=Math.hypot(dx,dy)||1,pull=Math.min(46,9000/(d+60));const x=gx-dx/d*pull,y=gy-dy/d*pull*.7;gx?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.stroke();}
   for(let gx=0;gx<=W;gx+=34){ctx.beginPath();for(let gy=0;gy<=H;gy+=10){const dx=gx-mx.x,dy=gy-mx.y,d=Math.hypot(dx,dy)||1,pull=Math.min(46,9000/(d+60));const x=gx-dx/d*pull,y=gy-dy/d*pull*.7;gy?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.stroke();}
   ctx.globalAlpha=1;}
  for(const p of ps){
   if(V==='gravity'){const dx=mx.x-p.x,dy=mx.y-p.y,d=Math.max(26,Math.hypot(dx,dy));const f=Math.min(2400,240000/(d*d));p.vx+=dx/d*f;p.vy+=dy/d*f;}
   else{p.a+=p.sp*dt;p.r+=Math.sin(t*1.3+p.ph)*8*dt;p.x=W/2+Math.cos(p.a)*p.r;p.y=H/2+Math.sin(p.a)*p.r*.7;
    const dx=p.x-mx.x,dy=p.y-mx.y,d=Math.hypot(dx,dy)||1,spd=Math.hypot(pvx,pvy);
    if(d<180&&spd>700){p.r+=Math.min(90,spd/60)*dt;}}
   p.vx*=1-dt*.25;p.vy*=1-dt*.25;const px=p.x,py=p.y;p.x+=p.vx*dt;p.y+=p.vy*dt;
   if(p.x<-40||p.x>W+40||p.y<-40||p.y>H+40){const a=rnd(TAU);p.x=W/2+Math.cos(a)*W*.62;p.y=H/2+Math.sin(a)*H*.62;p.vx=rnd(160,-160);p.vy=rnd(160,-160);}
   ctx.strokeStyle=P[2+(V==='gravity'?2:0)];ctx.globalAlpha=V==='gravity'?.9:.55;ctx.lineWidth=V==='gravity'?1.8:1.2;ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(p.x,p.y);ctx.stroke();}
  ctx.globalAlpha=1;stat(ps.length+(V==='gravity'?' in the well':' slingshots'));return;
 }
 ctx.fillStyle='rgba(5,6,11,.14)';ctx.fillRect(0,0,W,H);
 const cx=W/2+(mx.x-W/2)*.18,cy=H/2+(mx.y-H/2)*.18;
 for(const p of ps){p.a+=p.sp*dt;p.r+=Math.sin(t*1.4+p.ph)*10*dt;
  if(V==='nursery'){p.r+=6*dt;p.life-=dt*.12;if(p.life<=0){p.r=12;p.life=1;}}
  const x=cx+Math.cos(p.a)*p.r,y=cy+Math.sin(p.a)*p.r*.68;
  ctx.fillStyle=P[2+Math.min(P.length-3,Math.floor((p.r/(Math.min(W,H)*.55))*(P.length-3)))];
  ctx.globalAlpha=(V==='nursery'?.4:.75)*Math.min(1,p.life);
  ctx.beginPath();ctx.arc(x,y,1.8,0,TAU);ctx.fill();}
 ctx.globalAlpha=1;stat(ps.length+(V==='nursery'?' nursery stars':' orbits'));}
function myadj(p){return mx.y-p.y;}
"""

ENGINES["waves"] = r"""
const V='__V__';
const COLS=46,ROWS=27;let pts=[],imp=0,impX=0,impY=0,pressure=0;
function reset(){pts=[];for(let y=0;y<ROWS;y++)for(let x=0;x<COLS;x++)pts.push({hx:x/(COLS-1),hy:y/(ROWS-1),x:0,y:0});}
reset();
function frame(dt){
 ctx.fillStyle=P[0];ctx.fillRect(0,0,W,H);
 const s1=[W*.3+Math.cos(t*.4)*W*.15,H*.35+Math.sin(t*.5)*H*.15],s2=[W*.72,H*.62+Math.cos(t*.35)*H*.2];
 if(V==='seismo'){const mx0=mx.x,my0=mx.y;if(Math.hypot(mx0-impX,my0-impY)>6){imp=Math.min(1,imp+dt*8);impX=mx0;impY=my0;}imp=Math.max(0,imp-dt*1.5);}
 if(V==='pressure'){pressure+=((mx.down?1:0)-pressure)*Math.min(1,dt*6);}
 for(const p of pts){const bx=p.hx*W,by=p.hy*H;
  const d1=Math.hypot(bx-s1[0],by-s1[1]),d2=Math.hypot(bx-s2[0],by-s2[1]);
  let w=Math.sin(d1*.03-t*2)*10+Math.sin(d2*.026+t*1.6)*8;
  if(V==='seismo'){const dm=Math.hypot(bx-impX,by-impY);w+=Math.sin(dm*.06-t*8)*40*imp*Math.max(0,1-dm/520);}
  else if(V==='pressure'){const dm=Math.hypot(bx-mx.x,by-mx.y);w+=Math.cos(dm*.04-t*3)*70*pressure*Math.max(0,1-dm/460);}
  else{const dm=Math.hypot(bx-mx.x,by-mx.y);w+=Math.sin(dm*.05-t*3)*14*Math.max(0,1-dm/300);}
  p.x=bx;p.y=by+w;}
 ctx.lineWidth=1;
 for(let r=0;r<ROWS;r++){ctx.strokeStyle=P[2];ctx.globalAlpha=.35;ctx.beginPath();for(let c=0;c<COLS;c++){const p=pts[r*COLS+c];c?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y);}ctx.stroke();}
 for(let c=0;c<COLS;c++){ctx.strokeStyle=P[3];ctx.globalAlpha=.22;ctx.beginPath();for(let r=0;r<ROWS;r++){const p=pts[r*COLS+c];r?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y);}ctx.stroke();}
 ctx.globalAlpha=1;stat(COLS*ROWS+' nodes');}
"""

ENGINES["bars"] = r"""
const V='__V__',N=64,hs=[];for(let i=0;i<N;i++)hs.push(0);
function frame(dt){ctx.fillStyle='rgba(5,7,10,.22)';ctx.fillRect(0,0,W,H);
 const energy=mx.down?1:.55;
 for(let i=0;i<N;i++){const target=(.25+.55*Math.abs(Math.sin(t*2.1+i*.31))+.2*Math.abs(Math.cos(t*3.3-i*.19)))*energy;
  hs[i]+=(target-hs[i])*Math.min(1,dt*12);
  const h=hs[i]*H*.78,bw=W/N*.62,x=i*(W/N)+W/N*.19,y=H-h;
  const g=ctx.createLinearGradient(0,y,0,H);g.addColorStop(0,P[4]);g.addColorStop(.5,P[3]);g.addColorStop(1,P[2]);
  ctx.fillStyle=g;ctx.fillRect(x,y,bw,h);}
 stat('crowd '+Math.round(energy*100)+'%');}
"""

ENGINES["blobs"] = r"""
const V='__V__';
let bs=[];for(let i=0;i<11;i++)bs.push({x:rnd(W),y:rnd(H),r:rnd(150,70),vx:rnd(30,-30),vy:rnd(30,-30),c:P[2+i%2],split:0});
function frame(dt){ctx.fillStyle=P[0];ctx.fillRect(0,0,W,H);ctx.globalCompositeOperation='lighter';
 if(V==='division'&&mx.down&&bs.length<26){for(const b of bs){if(Math.hypot(b.x-mx.x,b.y-mx.y)<b.r&&b.split<=0&&Math.random()<.08){b.split=2;b.r*=.55;bs.push({x:b.x+rnd(40,-40),y:b.y+rnd(40,-40),r:b.r,vx:rnd(30,-30),vy:rnd(30,-30),c:P[2],split:1});}}}
 const all=bs.concat([{x:mx.x,y:mx.y,r:mx.down?180:110,c:P[3]}]);
 for(const b of all){const free=b!==all[all.length-1];
  if(free){b.x+=b.vx*dt;b.y+=b.vy*dt;if(b.x<0||b.x>W)b.vx*=-1;if(b.y<0||b.y>H)b.vy*=-1;if(b.split>0)b.split-=dt;}
  const g=ctx.createRadialGradient(b.x,b.y,0,b.x,b.y,b.r);g.addColorStop(0,b.c+'cc');g.addColorStop(.55,b.c+'44');g.addColorStop(1,b.c+'00');
  ctx.fillStyle=g;ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,TAU);ctx.fill();}
 ctx.globalCompositeOperation='source-over';stat(all.length+(V==='division'?' cells':' fields'));}
"""

ENGINES["grid"] = r"""
const V='__V__';
const STEP=__STEP__;let dots=[],stars=[],mask=null,art=null,erased=0,dragIdx=-1;
function reset(){
 dots=[];stars=[];erased=0;
 if(V==='constellation'){for(let i=0;i<90;i++)stars.push({x:rnd(W),y:rnd(H),vx:0,vy:0,ph:rnd(TAU)});return;}
 for(let y=STEP/2;y<H;y+=STEP)for(let x=STEP/2;x<W;x+=STEP)dots.push({x,y,dx:0,dy:0,vx:0,vy:0});
 if(V==='scratch'){art=document.createElement('canvas');art.width=W;art.height=H;const a=art.getContext('2d');
  const g=a.createLinearGradient(0,0,W,H);g.addColorStop(0,P[2]);g.addColorStop(.45,P[3]);g.addColorStop(1,P[4]);a.fillStyle=g;a.fillRect(0,0,W,H);
  for(let i=0;i<70;i++){a.fillStyle=i%3?P[4]+'99':P[1]+'aa';a.beginPath();a.arc(rnd(W),rnd(H),rnd(110,24),0,TAU);a.fill();}
  a.strokeStyle=P[4]+'cc';a.lineWidth=10;for(let i=0;i<14;i++){a.beginPath();a.moveTo(rnd(W),rnd(H));a.lineTo(rnd(W),rnd(H));a.stroke();}
  mask=document.createElement('canvas');mask.width=W;mask.height=H;const m=mask.getContext('2d');m.fillStyle='#191b24';m.fillRect(0,0,W,H);
  m.fillStyle='#ffffff';m.font='700 18px ui-monospace,monospace';m.textAlign='center';m.fillText('SCRATCH TO REVEAL',W/2,H/2);
  for(let i=0;i<2400;i++){m.fillStyle=i%3?'#232633':'#0e1016';m.fillRect(rnd(W),rnd(H),2,2);}
  m.strokeStyle='#2c3040';m.lineWidth=1;for(let i=-H;i<W;i+=26){m.beginPath();m.moveTo(i,0);m.lineTo(i+H,H);m.stroke();}
  m.globalCompositeOperation='destination-out';for(let i=0;i<9;i++){m.beginPath();m.arc(W*.5+(i-4)*26,H*.5+(i-4)*10,54,0,TAU);m.fill();}m.globalCompositeOperation='source-over'; }
}
reset();addEventListener('resize',reset);
function frame(dt){
 ctx.fillStyle=P[0];ctx.fillRect(0,0,W,H);
 if(V==='scratch'){ctx.drawImage(art,0,0);const m=mask.getContext('2d');m.globalCompositeOperation='destination-out';
  if(mx.x>0){m.beginPath();m.arc(mx.x,mx.y,52,0,TAU);m.fill();}
  m.globalCompositeOperation='source-over';ctx.drawImage(mask,0,0);
  if(mx.x>0)erased=Math.min(1,erased+dt*.25);
  ctx.fillStyle=P[4];ctx.font='600 12px ui-monospace,monospace';ctx.fillText('scratch ' + Math.round(erased*100) + '%',16,H-18);
  stat('scratch to reveal');return;}
 if(V==='constellation'){if(mx.down){if(dragIdx<0){let best=40;stars.forEach((s,i)=>{const d=Math.hypot(s.x-mx.x,s.y-mx.y);if(d<best){best=d;dragIdx=i;}});}if(dragIdx>=0){stars[dragIdx].x=mx.x;stars[dragIdx].y=mx.y;}}else dragIdx=-1;
  for(const s of stars){s.x+=Math.sin(t+s.ph)*6*dt;s.y+=Math.cos(t*1.2+s.ph)*6*dt;const dx=s.x-mx.x,dy=s.y-mx.y,d=Math.hypot(dx,dy)||1;if(d<130&&s!==stars[dragIdx]){s.x+=dx/d*40*dt;s.y+=dy/d*40*dt;}}
  ctx.strokeStyle=P[2];ctx.globalAlpha=.35;ctx.lineWidth=1;
  for(let i=0;i<stars.length;i++)for(let j=i+1;j<stars.length;j++){const a=stars[i],b=stars[j];if(Math.hypot(a.x-b.x,a.y-b.y)<120){ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}}
  ctx.globalAlpha=1;for(const s of stars){ctx.fillStyle=P[3];ctx.beginPath();ctx.arc(s.x,s.y,2.2,0,TAU);ctx.fill();}
  const dm=Math.hypot(mx.x-W/2,mx.y-H/2);
  stat(stars.length+' stars');return;}
 for(const d of dots){
  if(V==='halftone'){const dm=Math.hypot(d.x-mx.x,d.y-mx.y);const r=2+2.6*Math.sin(d.x*.03+d.y*.02-t*2)+5*Math.max(0,1-dm/220);
   ctx.fillStyle=P[2+((d.x/STEP|0)+(d.y/STEP|0))%2];ctx.globalAlpha=.75;ctx.beginPath();ctx.arc(d.x,d.y,Math.max(.6,r),0,TAU);ctx.fill();continue;}
  const tx=mx.x-d.x,ty=mx.y-d.y,dist=Math.hypot(tx,ty)||1,fall=Math.max(0,1-dist/190);
  if(V==='ink'){const len=2+fall*26;ctx.strokeStyle=P[2+(fall>.45?2:0)];ctx.globalAlpha=.3+fall*.7;ctx.lineWidth=1.2;
   ctx.beginPath();ctx.moveTo(d.x,d.y);ctx.lineTo(d.x+tx/dist*len,d.y+ty/dist*len);ctx.stroke();continue;}
  if(V==='elastic'){const k=fall*fall*70;d.vx+=(tx/dist*k-d.vx*6)*dt;d.vy+=(ty/dist*k-d.vy*6)*dt;d.vx+=(d.x+0-d.x)*0;d.dx+=d.vx*dt;d.dy+=d.vy*dt;
   d.dx*=1-Math.min(1,dt*4);d.dy*=1-Math.min(1,dt*4);
   const m=Math.hypot(d.dx,d.dy);ctx.fillStyle=P[1+Math.min(P.length-2,1+Math.floor(m/18))];ctx.globalAlpha=.7;ctx.beginPath();ctx.arc(d.x+d.dx,d.y+d.dy,1.8,0,TAU);ctx.fill();
   if(m>4){ctx.strokeStyle=P[2];ctx.globalAlpha=.3;ctx.beginPath();ctx.moveTo(d.x+d.dx,d.y+d.dy);ctx.lineTo(d.x+STEP+d.dx,d.y+d.dy);ctx.stroke();}
   continue;}
  const k=fall*fall*46;d.dx+=((tx/dist)*k-d.dx)*Math.min(1,dt*10);d.dy+=((ty/dist)*k-d.dy)*Math.min(1,dt*10);
  const m=Math.hypot(d.dx,d.dy),ci=Math.min(P.length-1,1+Math.floor(m/16));
  ctx.fillStyle=P[ci];ctx.globalAlpha=.45+Math.min(.55,m/40);ctx.beginPath();ctx.arc(d.x+d.dx,d.y+d.dy,1.6+m*.045,0,TAU);ctx.fill();
  if(m>3){ctx.strokeStyle=P[2];ctx.globalAlpha=.22;ctx.beginPath();ctx.moveTo(d.x,d.y);ctx.lineTo(d.x+d.dx,d.y+d.dy);ctx.stroke();}}
 ctx.globalAlpha=1;stat(dots.length+(V==='elastic'?' springs':V==='ink'?' filings':' points'));}
"""

ENGINES["particles"] = r"""
const V='__V__';
const ps=[];const MAX=1400;let pmx=mx.x,pmy=mx.y,hist=[],amb=0,idle=0;
function spawn(x,y,n,opts){for(let i=0;i<n;i++){if(ps.length>=MAX)ps.shift();const a=opts?.a??rnd(TAU),sp=opts?.sp??rnd(__SPEED__,20);
 ps.push({x,y,vx:Math.cos(a)*sp+(opts?.vx||0),vy:Math.sin(a)*sp+(opts?.vy||0),life:opts?.life??1,r:opts?.r??rnd(3.4,.8),rot:rnd(TAU),vr:rnd(8,-8),c:P[1+Math.floor(Math.random()*(P.length-2))],rect:opts?.rect});}}
function frame(dt){ctx.fillStyle='rgba(6,6,10,'+(V==='sparkler'?.22:.16)+')';ctx.fillRect(0,0,W,H);
 if(V==='comet'){const ix=mx.x>0?mx.x:W/2+Math.cos(t*.8)*W*.24,iy=mx.y>0?mx.y:H/2+Math.sin(t*1.1)*H*.2;
  hist.push({x:ix,y:iy});if(hist.length>22)hist.shift();
  const p=hist[Math.floor(Math.random()*hist.length)];if(isFinite(p.x))spawn(p.x+rnd(6,-6),p.y+rnd(6,-6),5,{sp:rnd(60,6),life:rnd(1.4,.7),r:rnd(4.6,2)});}
 else if(V==='confetti'){amb+=dt;const rate=mx.down?.12:.3;
  if(Math.floor(t*2)!==Math.floor((t-dt)*2)){for(let i=0;i<18;i++)spawn(W/2+Math.cos(t*3)*30,H-14,1,{sp:rnd(420,180),a:rnd(-Math.PI*.82,-Math.PI*.18),vy:-80,rect:true,r:rnd(10,5),life:rnd(2.4,1.4)});}
  while(amb>rate){amb-=rate;for(let i=0;i<9;i++)spawn(rnd(W),-10,1,{sp:rnd(90,20),a:rnd(Math.PI*.15,Math.PI*.85),vy:rnd(10,-40),rect:true,r:rnd(11,6),life:rnd(2.6,1.6)});}
  if(mx.x>0)spawn(mx.x,mx.y,mx.down?8:3,{sp:rnd(360,140),a:rnd(-Math.PI*.9,-Math.PI*.1),vy:-140,rect:true,r:rnd(11,6),life:rnd(2.2,1.2)});}
 else if(V==='sparkler'){idle+=dt;const spd=Math.hypot(mx.x-pmx,mx.y-pmy)/Math.max(dt,.001);const n=Math.min(6,Math.floor(spd/90));
  if(mx.x>0)spawn(mx.x,mx.y,n,{sp:rnd(60,10),life:rnd(.8,.3),r:rnd(2.4,.8)});
  else if(idle>.02){idle=0;const ix=W/2+Math.cos(t*.9)*W*.22,iy=H/2+Math.sin(t*1.3)*H*.18;spawn(ix,iy,6,{sp:rnd(80,12),life:rnd(1.3,.5),r:rnd(4.6,2)});}}
 else{if(mx.x>0)spawn(mx.x,mx.y,mx.down?7:2,{sp:rnd(__SPEED__,20),a:rnd(TAU),vy:-60,life:1});if(Math.random()<.5)spawn(W/2,H+10,1,{sp:rnd(60,-60),vy:-rnd(160,80)});}
 pmx=mx.x;pmy=mx.y;
 for(let i=ps.length-1;i>=0;i--){const p=ps[i];p.vy+=__GRAV__*dt;p.vx*=1-dt*.7;p.vy*=1-dt*(p.rect?.8:.25);p.x+=p.vx*dt;p.y+=p.vy*dt;p.life-=dt*(p.rect?.35:.5);p.rot+=p.vr*dt;
  if(p.life<=0||p.y>H+60){ps.splice(i,1);continue;}
  ctx.globalAlpha=Math.max(0,Math.min(1,p.life));ctx.fillStyle=p.c;
  if(p.rect){ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot);ctx.fillRect(-p.r,-p.r*.55,p.r*2,p.r*1.1);ctx.restore();}
  else{ctx.beginPath();ctx.arc(p.x,p.y,p.r*Math.max(.2,p.life),0,TAU);ctx.fill();}}
 ctx.globalAlpha=1;stat(ps.length+(V==='comet'?' comet tails':V==='confetti'?' confetti':V==='sparkler'?' sparks':' particles'));}
"""

ENGINES["type"] = r"""
const V='__V__';
const CHARS='__CHARS__',STEP=__STEP__;let gl=[],words=[],reels=[0,0,0],speeds=[0,0,0],pmx=mx.x,spin=false,dragW=-1;
const WORDS=['FORM','FOLLOWS','FEELING','AND','THE','TABLE','READS','IT'];
if(V==='vortex'){for(let i=0;i<30;i++)words.push({w:WORDS[i%WORDS.length],a:i*.55,r:40+i*13,sp:.22+i*.012});}
else if(V==='constellation'){for(let i=0;i<WORDS.length;i++){const a=i/WORDS.length*TAU;words.push({w:WORDS[i],hx:W/2+Math.cos(a)*Math.min(W,H)*.31,hy:H/2+Math.sin(a)*Math.min(W,H)*.29,x:0,y:0});}for(const w of words){w.x=w.hx;w.y=w.hy;}}
else if(V!=='slot'){for(let y=STEP;y<H-20;y+=STEP)for(let x=STEP*.7;x<W-10;x+=STEP){const g={hx:x,hy:y,x,y,vx:0,vy:0,ch:CHARS[Math.floor(Math.random()*CHARS.length)]};gl.push(g);}}
function frame(dt){ctx.fillStyle=P[0];ctx.fillRect(0,0,W,H);
 if(V==='slot'){const target='MENU';ctx.textAlign='center';ctx.textBaseline='middle';
  if(mx.down&&!spin){spin=true;speeds[0]=rnd(24,14);speeds[1]=rnd(20,11);speeds[2]=rnd(28,17);}
  pmx=mx.x;
  for(let i=0;i<3;i++){if(spin){if(!mx.down){speeds[i]*=Math.pow(.08,dt);if(speeds[i]<.5){speeds[i]=0;reels[i]=CHARS.indexOf(target[i]);}}reels[i]+=(speeds[i]||0)*dt;}
   const x=W/2+(i-1)*W*.19,ch=CHARS[Math.floor(reels[i])%CHARS.length];
   ctx.strokeStyle=P[2];ctx.lineWidth=2;ctx.strokeRect(x-34,H/2-48,68,96);
   ctx.fillStyle=P[4];ctx.font='900 44px ui-monospace,monospace';ctx.fillText(ch,x,H/2);
   ctx.fillStyle=P[3];ctx.font='600 11px ui-monospace,monospace';ctx.fillText('REEL '+(i+1),x,H/2+70);}
  if(spin&&!mx.down&&speeds.every(s=>s===0))spin=false;
  ctx.fillStyle=P[4];ctx.font='700 14px ui-monospace,monospace';ctx.fillText(spin?'SPINNING…':'DRAG TO SPIN',W/2,H/2+110);
  stat(spin?'spinning':'slot landed on '+target);return;}
 if(V==='vortex'){ctx.textAlign='center';ctx.textBaseline='middle';const tw=(mx.x-W/2)/W*.8;
  ctx.strokeStyle=P[2];ctx.globalAlpha=.16;ctx.beginPath();for(let i=0;i<180;i++){const a=i*.11+tw*2,r=20+i*1.5;const x=W/2+Math.cos(a)*r,y=H/2+Math.sin(a)*r*.72;i?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.stroke();ctx.globalAlpha=1;
  for(const o of words){o.a+=o.sp*dt;const x=W/2+Math.cos(o.a+tw)*o.r,y=H/2+Math.sin(o.a+tw)*o.r*.72;
   ctx.fillStyle=o.r<100?P[4]:P[2];ctx.font='700 '+(12+Math.max(0,130-o.r)*.09)+'px ui-monospace,monospace';ctx.fillText(o.w,x,y);}
  stat(words.length+' words');return;}
 if(V==='constellation'){ctx.textAlign='center';ctx.textBaseline='middle';
  if(mx.down){if(dragW<0){let best=50;words.forEach((o,i)=>{const d=Math.hypot(o.x-mx.x,o.y-mx.y);if(d<best){best=d;dragW=i;}});}if(dragW>=0){words[dragW].x=mx.x;words[dragW].y=mx.y;}}else dragW=-1;
  for(const o of words){const dx=o.x-mx.x,dy=o.y-mx.y,d=Math.hypot(dx,dy)||1,fall=Math.max(0,1-d/160);const k=fall*fall*260;
   if(o!==words[dragW]){o.x+=((o.hx-o.x)*4+dx/d*k)*dt;o.y+=((o.hy-o.y)*4+dy/d*k)*dt;}}
  ctx.strokeStyle=P[2];ctx.globalAlpha=.4;
  for(let i=0;i<words.length;i++){const a=words[i],b=words[(i+1)%words.length];ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}
  ctx.globalAlpha=1;for(const o of words){ctx.fillStyle=P[4];ctx.font='700 14px ui-monospace,monospace';ctx.fillText(o.w,o.x,o.y);}
  stat(words.length+' words');return;}
 ctx.textAlign='center';ctx.textBaseline='middle';ctx.font='__FONT__';
 if(V==='magnet'){const g=ctx.createRadialGradient(mx.x,mx.y,0,mx.x,mx.y,140);g.addColorStop(0,P[3]+'44');g.addColorStop(1,P[0]+'00');ctx.fillStyle=g;ctx.beginPath();ctx.arc(mx.x,mx.y,140,0,TAU);ctx.fill();ctx.strokeStyle=P[3];ctx.globalAlpha=.35;ctx.beginPath();ctx.arc(mx.x,mx.y,26,0,TAU);ctx.stroke();ctx.globalAlpha=1;}
 if(Math.random()<.4){const g=gl[Math.floor(Math.random()*gl.length)];g.ch=CHARS[Math.floor(Math.random()*CHARS.length)];}
 for(const g of gl){const tx=g.x-mx.x,ty=g.y-mx.y,d=Math.hypot(tx,ty)||1,fall=Math.max(0,1-d/150);
  const k=fall*fall*(V==='magnet'?900:380);g.vx+=((tx/d)*k-g.vx*14)*dt;g.vy+=((ty/d)*k-g.vy*14)*dt;
  g.vx+=(g.hx-g.x)*(V==='magnet'?8:22)*dt;g.vy+=(g.hy-g.y)*(V==='magnet'?8:22)*dt;g.x+=g.vx*dt;g.y+=g.vy*dt;
  const m=Math.hypot(g.vx,g.vy);ctx.fillStyle=P[2+Math.min(P.length-3,Math.floor(m/90))];ctx.globalAlpha=.78+Math.min(.22,m/500);ctx.fillText(g.ch,g.x,g.y);}
 ctx.globalAlpha=1;stat(gl.length+(V==='magnet'?' magnets':' glyphs'));}
"""

ENGINES["matrix"] = r"""
const V='__V__';
const FS=__FS__;let cols=[],grid=null;
if(V==='ascii'){grid=[];for(let y=8;y<H;y+=FS)for(let x=6;x<W;x+=FS*.62)grid.push({x,y});}
else if(V==='pixelsort'){cols=[];for(let x=0;x<W;x+=W/48)cols.push({x,h:rnd(H),o:rnd(360)});}
else{for(let x=8;x<W;x+=FS)cols.push({x,y:rnd(H),s:rnd(260,40),ch:[]});for(const c of cols)for(let i=0;i<14;i++)c.ch.push(String.fromCharCode(33+Math.floor(Math.random()*90)));}
function frame(dt){ctx.fillStyle='rgba(5,6,9,'+(V==='pixelsort'?.3:.18)+')';ctx.fillRect(0,0,W,H);
 if(V==='ascii'){const ramp=' .:-=+*#%@';ctx.font=FS+'px ui-monospace,monospace';ctx.textAlign='center';ctx.textBaseline='middle';
  for(const p of grid){let v=.5+.3*Math.sin(p.x*.02+t*1.4)+.2*Math.cos(p.y*.03-t);const dm=Math.hypot(p.x-mx.x,p.y-mx.y);v+=Math.max(0,1-dm/200)*.45;
   const ch=ramp[Math.max(0,Math.min(ramp.length-1,Math.floor(v*ramp.length)))];ctx.fillStyle=v>.7?P[4]:P[2];ctx.globalAlpha=.4+v*.6;ctx.fillText(ch,p.x,p.y);}
  ctx.globalAlpha=1;stat(grid.length+' cells');return;}
 if(V==='pixelsort'){cols.sort((a,b)=>Math.abs(a.o+(mx.x-W/2)*.4)-Math.abs(b.o));
  for(let i=0;i<cols.length;i++){const c=cols[i],h=(.25+.65*Math.abs(Math.sin(c.o*.05+t)))*H;
   const g=ctx.createLinearGradient(c.x,H-h,c.x,H);g.addColorStop(0,P[4]);g.addColorStop(.5,P[2+ i%2]);g.addColorStop(1,P[1]);
   ctx.fillStyle=g;ctx.fillRect(c.x,0,W/48-1,Math.max(6,h));}
  stat(cols.length+' strips');return;}
 ctx.font=FS+'px ui-monospace,monospace';ctx.textAlign='center';
 for(const c of cols){const near=Math.abs(mx.x-c.x)<80;c.y+=(c.s*(near?2.2:1))*dt;if(c.y>H+FS*14)c.y=-FS*2;
  for(let i=0;i<c.ch.length;i++){const y=c.y-i*FS;if(y<-FS||y>H+FS)continue;ctx.fillStyle=i===0?P[4]:P[2];ctx.globalAlpha=i===0?.95:Math.max(.06,.5-i*.04);ctx.fillText(c.ch[i],c.x,y);}
  if(Math.random()<.3)c.ch[Math.floor(Math.random()*c.ch.length)]=String.fromCharCode(33+Math.floor(Math.random()*90));}
 ctx.globalAlpha=1;stat(cols.length+' columns');}
"""

ENGINES["voxel"] = r"""
const V='__V__',G=__GRID__;let hs=[];
for(let y=0;y<G;y++)for(let x=0;x<G;x++)hs.push({x,y,h:0,ch:String.fromCharCode(65+((x*7+y*3)%26))});
function frame(dt){ctx.fillStyle=P[0];ctx.fillRect(0,0,W,H);
 const tw=W/(G*1.45),th=tw*.5,bw=tw*.40,bh=th*.40,ox=W/2,oy=H*.16;
 for(const c of hs){const px=ox+(c.x-c.y)*tw/2,py=oy+(c.x+c.y)*th/2;
  const d=Math.hypot(px-mx.x,py-mx.y),lift=Math.max(0,1-d/220);
  let target;
  if(V==='city'||V==='glyphcubes'){target=.16+Math.abs(Math.sin(c.x*12.9898+c.y*78.233))*.95+lift*1.15;}
  else if(V==='dunes'){target=.32+.26*Math.sin(c.x*.55+t*.55)+.22*Math.cos(c.y*.45-t*.4)+lift*.25;}
  else{const ring=1-Math.max(Math.abs(c.x-G/2),Math.abs(c.y-G/2))/(G/2);target=.12+Math.max(0,ring)*1.7;}
  c.h+=(target-c.h)*Math.min(1,dt*2.4);}
 const sorted=hs.slice().sort((a,b)=>(a.x+a.y)-(b.x+b.y));
 for(const c of sorted){const sx=ox+(c.x-c.y)*tw/2,sy=oy+(c.x+c.y)*th/2,hv=Math.max(1.5,c.h*tw*.8);
  const top=[[sx,sy-hv],[sx+bw,sy-hv+bh],[sx,sy-hv+2*bh],[sx-bw,sy-hv+bh]];
  const left=[[sx-bw,sy+bh-hv],[sx,sy+2*bh-hv],[sx,sy+2*bh],[sx-bw,sy+bh]];
  const right=[[sx,sy+2*bh-hv],[sx+bw,sy+bh-hv],[sx+bw,sy+bh],[sx,sy+2*bh]];
  ctx.strokeStyle=P[0];ctx.lineWidth=.8;
  ctx.fillStyle=P[1];ctx.beginPath();left.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();ctx.fill();ctx.stroke();
  ctx.fillStyle=P[3];ctx.beginPath();right.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();ctx.fill();ctx.stroke();
  ctx.fillStyle=P[2];ctx.beginPath();top.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();ctx.fill();ctx.stroke();
  if(V==='glyphcubes'&&c.h>.7){ctx.fillStyle=P[0];ctx.font='700 '+(tw*.34)+'px ui-monospace,monospace';ctx.textAlign='center';ctx.fillText(c.ch,sx,sy-hv+bh*1.05);}}
 stat(G*G+(V==='stack'?' stacked':V==='dunes'?' dunes':V==='glyphcubes'?' blocks':' columns'));}
"""

ENGINES["terrain"] = r"""
const V='__V__',LAYERS=9;
function frame(dt){ctx.fillStyle=P[0];ctx.fillRect(0,0,W,H);
 if(V==='scan'){for(let l=LAYERS-1;l>=0;l--){const y0=H*(.16+l*.09),amp=16+l*5;
  const pts=[];for(let x=0;x<=W;x+=8){const y=y0+Math.sin(x*.0028+t*.7+l)*amp+Math.cos(x*.006-t*.4)*amp*.4;pts.push([x,y]);}
  ctx.beginPath();ctx.moveTo(0,H);pts.forEach(p=>ctx.lineTo(p[0],p[1]));ctx.lineTo(W,H);ctx.closePath();
  ctx.fillStyle=P[1+Math.min(P.length-2,l%3)];ctx.globalAlpha=.10+l*.02;ctx.fill();
  ctx.strokeStyle=P[3];ctx.globalAlpha=.5;ctx.lineWidth=1;ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();}
  const sx=(t*140)%W;ctx.globalAlpha=.7;ctx.strokeStyle=P[4];ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(sx,0);ctx.lineTo(sx,H);ctx.stroke();
  ctx.globalAlpha=1;stat('scanning');return;}
 for(let l=LAYERS-1;l>=0;l--){const y0=H*(.22+l*.085),amp=18+l*5,sp=.0018+l*.0007;
  const off=V==='flyover'?t*(40+l*28):0;
  ctx.beginPath();for(let x=0;x<=W;x+=8){const xx=x+off;const dm=Math.hypot(x-mx.x,y0-mx.y);const dent=Math.max(0,1-dm/240)*(V==='flyover'?20:60);
   const y=y0+Math.sin(xx*sp+l)*amp+Math.cos(xx*sp*2.3-t*.4)*amp*.4+dent;x?ctx.lineTo(x,y):ctx.moveTo(x,y);}
  ctx.strokeStyle=P[1+Math.min(P.length-2,l%3)];ctx.globalAlpha=.35+l*.05;ctx.lineWidth=1+l*.18;ctx.stroke();}
 ctx.globalAlpha=1;stat(LAYERS+(V==='flyover'?' parallax layers':' contours'));}
"""

ENGINES["rings"] = r"""
const V='__V__';
const rs=[];let lastX=0,lastY=0,beat=0,rings=[];
if(V==='tunnel'){for(let i=0;i<14;i++)rings.push({z:i/14});}
function add(x,y){rs.push({x,y,r:4,v:rnd(150,80),a:1,w:rnd(2.2,.7),c:P[2+Math.floor(Math.random()*(P.length-2))]});}
function frame(dt){ctx.fillStyle='rgba(5,6,10,.2)';ctx.fillRect(0,0,W,H);
 if(V==='tunnel'){const cx=mx.x>0?mx.x:W/2,cy=mx.y>0?mx.y:H/2;
  for(const r of rings){r.z+=dt*.18;if(r.z>1)r.z-=1;const rad=8+Math.pow(r.z,2.1)*Math.min(W,H)*.75;
   ctx.strokeStyle=P[2+Math.floor(r.z*2)];ctx.globalAlpha=.15+.7*(1-r.z);ctx.lineWidth=1+3*(1-r.z);
   ctx.beginPath();ctx.arc(cx,cy,rad,0,TAU);ctx.stroke();}
  ctx.globalAlpha=1;stat('14 tunnel rings');return;}
 if(V==='countdown'){beat+=dt;if(beat>1){beat-=1;add(W/2,H/2);}
  for(let i=rs.length-1;i>=0;i--){const r=rs[i];r.r+=r.v*1.4*dt;r.a-=dt*.7;if(r.a<=0){rs.splice(i,1);continue;}
   ctx.strokeStyle=r.c;ctx.globalAlpha=r.a;ctx.lineWidth=r.w*1.6;ctx.beginPath();ctx.arc(r.x,r.y,r.r,0,TAU);ctx.stroke();}
  ctx.globalAlpha=1;ctx.fillStyle=P[4];ctx.font='900 40px ui-monospace,monospace';ctx.textAlign='center';ctx.fillText(String(3-Math.floor(beat*3)),W/2,H/2+14);
  stat('countdown');return;}
 if(Math.hypot(mx.x-lastX,mx.y-lastY)>45){add(mx.x,mx.y);lastX=mx.x;lastY=mx.y;}
 if(Math.random()<.06)add(W/2+Math.cos(t)*W*.2,H/2+Math.sin(t*.7)*H*.2);
 for(let i=rs.length-1;i>=0;i--){const r=rs[i];r.r+=r.v*dt;r.a-=dt*.55;if(r.a<=0){rs.splice(i,1);continue;}
  ctx.strokeStyle=r.c;ctx.globalAlpha=r.a*.8;ctx.lineWidth=r.w;ctx.beginPath();ctx.arc(r.x,r.y,r.r,0,TAU);ctx.stroke();}
 ctx.globalAlpha=1;stat(rs.length+' ripples');}
"""

ENGINES["spiral"] = r"""
const trail=[];
for(let i=0;i<700;i++){const tt=-12+i*.017;trail.push({x:W/2+Math.sin(tt*.73)*W*.28+Math.sin(tt*1.91)*W*.09,y:H/2+Math.cos(tt*.61)*H*.3+Math.cos(tt*2.23)*H*.08});}
function frame(dt){ctx.fillStyle='rgba(5,6,10,.055)';ctx.fillRect(0,0,W,H);
 const cx=W/2+(mx.x-W/2)*.1,cy=H/2+(mx.y-H/2)*.1;
 const p={x:cx+Math.sin(t*.73)*W*.28+Math.sin(t*1.91)*W*.09,y:cy+Math.cos(t*.61)*H*.3+Math.cos(t*2.23)*H*.08};
 trail.push(p);if(trail.length>2600)trail.shift();
 for(let i=1;i<trail.length;i++){const a=i/trail.length;ctx.strokeStyle=P[1+Math.floor(a*(P.length-2))];ctx.globalAlpha=a*.55;ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(trail[i-1].x,trail[i-1].y);ctx.lineTo(trail[i].x,trail[i].y);ctx.stroke();}
 ctx.globalAlpha=1;ctx.fillStyle=P[4];ctx.beginPath();ctx.arc(p.x,p.y,2.6,0,TAU);ctx.fill();stat(trail.length+' points');}
"""

ENGINES["kaleido"] = r"""
function frame(dt){ctx.fillStyle=P[0];ctx.fillRect(0,0,W,H);const cx=W/2,cy=H/2;const S=6;ctx.save();ctx.translate(cx,cy);
 for(let s=0;s<S;s++){ctx.save();ctx.rotate(s*TAU/S+t*.06);if(s%2)ctx.scale(1,-1);
  for(let i=0;i<5;i++){const r=Math.min(W,H)*.16+i*14;const a=t*.5+i*.7;
   ctx.fillStyle=P[2+(i%3)];ctx.globalAlpha=.4;ctx.beginPath();ctx.ellipse(Math.cos(a)*r,Math.sin(a*.8)*r,r*.28,r*.12,a,0,TAU);ctx.fill();
   ctx.strokeStyle=P[4];ctx.globalAlpha=.5;ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(Math.cos(a)*r*1.2,Math.sin(a*.8)*r*1.2);ctx.stroke();}
  ctx.restore();}
 ctx.restore();ctx.globalAlpha=1;stat(S+' mirrors');}
"""

ENGINES["starfield"] = r"""
const st=[];for(let i=0;i<620;i++)st.push({x:rnd(700,-700),y:rnd(460,-460),z:rnd(900,1),pz:0});
function frame(dt){ctx.fillStyle='rgba(4,5,9,.28)';ctx.fillRect(0,0,W,H);const cx=W/2+(mx.x-W/2)*.14,cy=H/2+(mx.y-H/2)*.14;
 for(const s of st){s.pz=s.z;s.z-=__SPEED__*dt;if(s.z<1){s.x=rnd(700,-700);s.y=rnd(460,-460);s.z=900;s.pz=900;continue;}
  const k=420/s.z,pk=420/s.pz,x=cx+s.x*k,y=cy+s.y*k,px=cx+s.x*pk,py=cy+s.y*pk;
  ctx.strokeStyle=P[2+Math.floor((1-s.z/900)*(P.length-3))];ctx.globalAlpha=Math.min(1,(1-s.z/900)*1.4);ctx.lineWidth=Math.max(.6,2.4-s.z/380);
  ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(x,y);ctx.stroke();}
 ctx.globalAlpha=1;stat(st.length+' stars');}
"""
