"""Batch three — physics and touch toys (6 demos)."""

DEMOS = [
    {
        "id": "verlet-rope", "name": "Verlet Rope", "category": "pointer",
        "tagline": "A rope with real weight that you can grab anywhere.",
        "what": "Thirty verlet points with distance constraints hang from a fixed anchor. Dragging grabs the nearest point and the rest of the rope follows through 18 relaxation passes.",
        "why": "Verlet integration plus constraints is the smallest physics engine that feels right, and it powers everything from ropes to cloth.",
        "surface": ["Hero", "Product", "Playful 404"], "intensity": "medium",
        "worksWith": ["dark-tech", "playful", "contemporary"],
        "stat": "30 points · 18 iterations",
        "code": r"""
const pts=[];const N=30;for(let i=0;i<N;i++)pts.push({x:W*.34,y:H*.14+i*9,px:W*.34,py:H*.14+i*9,pin:i===0});
function frame(dt){ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);
 for(const p of pts){if(p.pin)continue;const vx=(p.x-p.px)*.99,vy=(p.y-p.py)*.99;p.px=p.x;p.py=p.y;p.x+=vx;p.y+=vy+520*dt*dt;}
 if(mx.down){let bi=-1,bd=60;pts.forEach((p,i)=>{const d=Math.hypot(p.x-mx.x,p.y-mx.y);if(d<bd){bd=d;bi=i;}});if(bi>=0){pts[bi].x=mx.x;pts[bi].y=mx.y;}}
 for(let k=0;k<18;k++)for(let i=0;i<N-1;i++){const a=pts[i],b=pts[i+1],dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1,diff=(d-8)/d*.5;
  if(!a.pin){a.x+=dx*diff*.5;a.y+=dy*diff*.5;}if(!b.pin){b.x-=dx*diff*.5;b.y-=dy*diff*.5;}}
 ctx.strokeStyle='#8fd8ff';ctx.lineWidth=3;ctx.lineCap='round';ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.stroke();
 ctx.fillStyle='#ffd166';ctx.beginPath();ctx.arc(pts[0].x,pts[0].y,5,0,7);ctx.fill();
 stat('30 points · 18 iterations');}
""",
        "snippet": "vy += gravity * dt * dt;\nconst vx = (x - px) * damping;\npx = x; py = y;\nx += vx; y += vy;\n// repeat: satisfy distance constraints",
        "prompt": "Build a verlet rope: 30 points, fixed anchor, gravity, damping, and 18 distance-constraint iterations. Drag grabs the nearest point. Single HTML file.",
    },
    {
        "id": "cloth-sim", "name": "Cloth Simulation", "category": "pointer",
        "tagline": "A pinned sheet that ripples when you drag through it.",
        "what": "A 16×11 mass-spring grid is pinned along the top edge and relaxed with structural and shear constraints. The pointer pushes a soft circular wind field through it.",
        "why": "Cloth is the classic stress test for constraint solvers, and a convincing one needs only points, springs and iteration.",
        "surface": ["Product", "Fashion", "Hero"], "intensity": "medium",
        "worksWith": ["luxe-brand", "dark-tech", "contemporary"],
        "stat": "176 points · cloth",
        "code": r"""
const C=16,R=11,pts=[],links=[];
for(let y=0;y<R;y++)for(let x=0;x<C;x++){const px=W*.5+(x-(C-1)/2)*Math.min(W*.045,26),py=H*.16+y*Math.min(H*.055,26);
 pts.push({x:px,y:py,px,py,pin:y===0});}
for(let y=0;y<R;y++)for(let x=0;x<C;x++){const i=y*C+x;if(x<C-1)links.push([i,i+1,Math.min(W*.045,26)]);if(y<R-1)links.push([i,i+C,Math.min(H*.055,26)]);if(x<C-1&&y<R-1){const dg=Math.hypot(Math.min(W*.045,26),Math.min(H*.055,26));links.push([i,i+C+1,dg]);links.push([i+1,i+C,dg]);}}
function frame(dt){ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);
 for(const p of pts){if(p.pin)continue;const vx=(p.x-p.px)*.97,vy=(p.y-p.py)*.97;p.px=p.x;p.py=p.y;p.x+=vx;p.y+=vy+900*dt*dt;
  const dx=p.x-mx.x,dy=p.y-mx.y,d=Math.hypot(dx,dy)||1;if(d<110){const f=(1-d/110)*55*dt;p.x+=dx/d*f;p.y+=dy/d*f;}}
 for(let k=0;k<10;k++)for(const [i,j,rest] of links){const a=pts[i],b=pts[j],dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1,diff=(d-rest)/d*.5;
  if(!a.pin){a.x+=dx*diff;a.y+=dy*diff;}if(!b.pin){b.x-=dx*diff;b.y-=dy*diff;}}
 ctx.strokeStyle='rgba(143,216,255,.45)';ctx.lineWidth=.7;
 for(const [i,j] of links){const a=pts[i],b=pts[j];ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}
 ctx.fillStyle='#ffd166';for(const p of pts)if(p.pin){ctx.beginPath();ctx.arc(p.x,p.y,2,0,7);ctx.fill();}
 stat('176 points · cloth');}
""",
        "snippet": "for (const [i,j] of links) {\n  const a = points[i], b = points[j];\n  const diff = (dist(a,b) - rest) / dist(a,b) * .5;\n  a += (b-a) * diff; b -= (b-a) * diff;\n}",
        "prompt": "Build a pinned cloth: 16×11 verlet grid with structural and shear constraints, gravity, pointer wind and 10 relaxation passes. Single HTML file.",
    },
    {
        "id": "soft-body", "name": "Soft Body", "category": "pointer",
        "tagline": "A squashable blob with a skin and a memory.",
        "what": "A ring of 64 verlet points is held by neighbour springs and an internal pressure force computed from the polygon area. The pointer deforms the skin and the blob springs back.",
        "why": "Soft bodies are how interfaces get a sense of material — buttons, avatars and loading states all benefit from a little give.",
        "surface": ["Product", "Avatar", "Playful"], "intensity": "medium",
        "worksWith": ["playful", "luxe-brand", "contemporary"],
        "stat": "64-point soft body",
        "code": r"""
const N=64,pts=[];for(let i=0;i<N;i++){const a=i/N*Math.PI*2,r=Math.min(W,H)*.2;pts.push({x:W/2+Math.cos(a)*r,y:H/2+Math.sin(a)*r,px:W/2+Math.cos(a)*r,py:H/2+Math.sin(a)*r});}
function area(){let a=0;for(let i=0;i<N;i++){const p=pts[i],q=pts[(i+1)%N];a+=p.x*q.y-q.x*p.y;}return Math.abs(a)/2;}
const restArea=Math.PI*Math.pow(Math.min(W,H)*.2,2);
function frame(dt){ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);
 for(const p of pts){const vx=Math.max(-12,Math.min(12,(p.x-p.px)*.94)),vy=Math.max(-12,Math.min(12,(p.y-p.py)*.94));p.px=p.x;p.py=p.y;p.x+=vx;p.y+=vy+22*dt*dt;
  const dx=p.x-mx.x,dy=p.y-mx.y,d=Math.hypot(dx,dy)||1;if(d<120&&d>8){const f=(1-d/120)*46*dt;p.x+=dx/d*f;p.y+=dy/d*f;}
  if(p.x<12||p.x>W-12)p.x=Math.max(12,Math.min(W-12,p.x));if(p.y<12||p.y>H-12)p.y=Math.max(12,Math.min(H-12,p.y));}
 for(let k=0;k<12;k++){
  for(let i=0;i<N;i++){const a=pts[i],b=pts[(i+1)%N],dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1,rest=Math.PI*2*Math.min(W,H)*.2/N,diff=(d-rest)/d*.5;
   a.x+=dx*diff*.5;a.y+=dy*diff*.5;b.x-=dx*diff*.5;b.y-=dy*diff*.5;}
  const pressure=(restArea-area())*.02;
  for(let i=0;i<N;i++){const p=pts[i],q=pts[(i+1)%N],a=pts[(i-1+N)%N];const nx=q.y-a.y,ny=-(q.x-a.x),nd=Math.hypot(nx,ny)||1;
   p.x+=nx/nd*pressure*.02;p.y+=ny/nd*pressure*.02;}}
 ctx.fillStyle='rgba(157,123,255,.2)';ctx.strokeStyle='#b79bff';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);pts.forEach(p=>ctx.lineTo(p.x,p.y));ctx.closePath();ctx.fill();ctx.stroke();
 stat('area '+Math.round(area())+' / rest '+Math.round(restArea));}
""",
        "snippet": "const pressure = (restArea - area()) * k;\nfor each edge:\n  push the edge outward along its normal by pressure;",
        "prompt": "Build a soft-body blob: 64-point ring with neighbour springs and an internal pressure term from polygon area, pointer deformation. Single HTML file.",
    },
    {
        "id": "domino-run", "name": "Domino Run", "category": "play",
        "tagline": "A line of tiles that falls one into the next.",
        "what": "Fourteen dominoes stand on a baseline with damped angular velocity. A pointer push or a click tips the first one; once a tile passes a threshold it knocks its neighbour.",
        "why": "Dominoes are a readable chain reaction: local energy transfer you can watch propagate.",
        "surface": ["Loading", "Onboarding", "Success"], "intensity": "subtle",
        "worksWith": ["playful", "classic", "contemporary"],
        "stat": "14 dominoes",
        "code": r"""
let started=false;const N=14,D=[];for(let i=0;i<N;i++)D.push({a:0,v:0,x:W*.16+i*Math.min(W*.052,34),y:H*.62,w:Math.min(W*.016,11),h:Math.min(H*.12,54)});
function frame(dt){ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);
 if(!started&&t>1.1){started=true;D[0].v=3.6;}
 if(mx.down){const i=Math.floor((mx.x-W*.16)/Math.min(W*.052,34));if(i>=0&&i<N&&Math.abs(mx.y-H*.62)<90&&Math.abs(D[i].a)<.2)D[i].v+=6;}
 for(let i=0;i<N;i++){const d=D[i];d.v+=(d.a*.6-d.v*2.6)*dt*6;d.a+=d.v*dt;
  if(d.a>.55&&i<N-1&&D[i+1].a<.05)D[i+1].v+=3.2;
  if(d.a>Math.PI/2-.1){d.a=Math.PI/2;d.v=0;}}
 ctx.strokeStyle='#3a4152';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(W*.08,H*.62);ctx.lineTo(W*.92,H*.62);ctx.stroke();
 for(const d of D){ctx.save();ctx.translate(d.x,d.y);ctx.rotate(d.a);ctx.fillStyle='#ffd166';ctx.fillRect(-d.w/2,-d.h,d.w,d.h);ctx.strokeStyle='#0b0d13';ctx.strokeRect(-d.w/2,-d.h,d.w,d.h);ctx.restore();}
 stat('14 dominoes');}
""",
        "snippet": "if (angle > tipThreshold && next.angle < .05) {\n  next.angularVelocity += impulse;\n}\nangle += angularVelocity * dt;",
        "prompt": "Build a domino chain: 14 upright tiles, angular velocity with damping, pointer tips the nearest, and a tile passing 0.55 rad knocks the next. Single HTML file.",
    },
    {
        "id": "sandpile", "name": "Sandpile", "category": "play",
        "tagline": "Grains fall, pile up, and avalanche when the slope is too steep.",
        "what": "A height grid receives grains at the pointer; any cell above four grains topples one to each neighbour. The pile self-organises to a critical slope.",
        "why": "The Abelian sandpile is the smallest self-organised criticality demo: simple rules, avalanches of every size.",
        "surface": ["Data art", "Loading", "Playful"], "intensity": "subtle",
        "worksWith": ["dark-tech", "playful", "cultural"],
        "stat": "Abelian sandpile",
        "code": r"""
const C=72,R=46,g=new Uint16Array(C*R);let dropAcc=0;
for(let i=0;i<2600;i++){const a=Math.random()*6.28,r=Math.random()*7;const x=Math.floor(C/2+Math.cos(a)*r),y=Math.floor(R*.55+Math.sin(a)*r);if(x>=0&&x<C&&y>=0&&y<R)g[y*C+x]++;}
for(let k=0;k<600;k++)for(let y=1;y<R-1;y++)for(let x=1;x<C-1;x++){const i=y*C+x;if(g[i]>=4){g[i]-=4;g[i-1]++;g[i+1]++;g[i-C]++;g[i+C]++;}}
function frame(dt){ctx.fillStyle='#07080d';ctx.fillRect(0,0,W,H);dropAcc+=dt;
 if(dropAcc>.03){dropAcc=0;for(let k=0;k<6;k++){const x=Math.floor(mx.x/W*C+rnd(3,-3)),y=Math.floor(mx.y/H*R+rnd(2,-2));if(x>=0&&x<C&&y>=0&&y<R)g[y*C+x]++;}}
 for(let k=0;k<2;k++)for(let y=0;y<R;y++)for(let x=0;x<C;x++){const i=y*C+x;if(g[i]>=4){g[i]-=4;if(x>0)g[i-1]++;if(x<C-1)g[i+1]++;if(y>0)g[i-C]++;if(y<R-1)g[i+C]++;}}
 const sx=W/C,sy=H/R;
 for(let y=0;y<R;y++)for(let x=0;x<C;x++){const v=g[y*C+x];if(!v)continue;ctx.fillStyle='hsl('+(190+v*28)+',75%,'+(30+v*8)+'%)';ctx.fillRect(x*sx,y*sy,sx+.5,sy+.5);}
 stat('Abelian sandpile');}
""",
        "snippet": "if (cell >= 4) {\n  cell -= 4;\n  each of the four neighbours += 1;\n}",
        "prompt": "Build an Abelian sandpile: grains drop at the pointer, any cell with 4+ topples one grain to each neighbour, height maps to colour. Single HTML file.",
    },
    {
        "id": "double-pendulum", "name": "Double Pendulum", "category": "play",
        "tagline": "Chaos you can nudge with a fingertip.",
        "what": "Two coupled rods integrate the full double-pendulum equations. The tip leaves a long fading trail, and the pointer gives the second rod a push.",
        "why": "The double pendulum is the clearest everyday system where a tiny change in initial conditions produces a completely different path.",
        "surface": ["Hero", "Science story", "Loading"], "intensity": "subtle",
        "worksWith": ["dark-tech", "classic", "immersive-3d"],
        "stat": "double pendulum · chaotic",
        "code": r"""
let a1=Math.PI*.92,a2=Math.PI*.42,w1=0,w2=0,L1=Math.min(W,H)*.22,L2=L1*.8;const trail=[];
function frame(dt){const g=9.81,steps=2,dt2=dt/steps;
 for(let s=0;s<steps;s++){
  const num1=-g*(2*Math.sin(a1)+Math.sin(a1-2*a2))-2*Math.sin(a1-a2)*(w2*w2*L2+w1*w1*L1*Math.cos(a1-a2));
  const den1=L1*(2*Math.cos(a1-a2)-Math.cos(2*a1-2*a2)+2);
  const num2=2*Math.sin(a1-a2)*(w1*w1*L1+w2*w2*L2*Math.cos(a1-a2)+g*Math.cos(a1));
  const den2=L2*(2*Math.cos(a1-a2)-Math.cos(2*a1-2*a2)+2);
  w1+=num1/den1*dt2;w2+=num2/den2*dt2;a1+=w1*dt2;a2+=w2*dt2;
  if(mx.down){w2+=((mx.x-W/2)/W)*.03;w1+=((mx.y-H/2)/H)*.02;}}
 const x1=W/2+Math.sin(a1)*L1,y1=H*.34+Math.cos(a1)*L1,x2=x1+Math.sin(a2)*L2,y2=y1+Math.cos(a2)*L2;
 trail.push([x2,y2]);if(trail.length>420)trail.shift();
 ctx.fillStyle='rgba(7,8,13,.2)';ctx.fillRect(0,0,W,H);
 ctx.strokeStyle='rgba(143,216,255,.35)';ctx.lineWidth=1;ctx.beginPath();trail.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();
 ctx.strokeStyle='#8fd8ff';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(W/2,H*.34);ctx.lineTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
 ctx.fillStyle='#ffd166';ctx.beginPath();ctx.arc(x1,y1,4,0,7);ctx.fill();ctx.beginPath();ctx.arc(x2,y2,6,0,7);ctx.fill();ctx.fillStyle='#0b0d13';ctx.beginPath();ctx.arc(W/2,H*.34,3,0,7);ctx.fill();
 stat('double pendulum · chaotic');}
""",
        "snippet": "w1 += (-g*(2sin(a1)+sin(a1-2a2)) - 2sin(a1-a2)*(w2²L2 + w1²L1cos(a1-a2))) / den1 * dt;\nw2 += (2sin(a1-a2)*(w1²L1 + w2²L2cos(a1-a2) + g cos(a1))) / den2 * dt;",
        "prompt": "Build a double pendulum with the full coupled equations of motion, a fading tip trail and pointer nudges. Single HTML file.",
    },
]
