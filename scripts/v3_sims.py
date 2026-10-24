"""Batch three — canvas simulations and generative systems (10 demos)."""

DEMOS = [
    {
        "id": "boids-flock", "name": "Boids Flock", "category": "generative",
        "tagline": "A flock that separates, aligns, coheres and dodges your cursor.",
        "what": "220 agents each sample their neighbours and add separation, alignment and cohesion forces, then steer away from the pointer. The classic Reynolds flock, drawn as motion streaks.",
        "why": "Flocking is the clearest proof that local rules beat global choreography: nobody leads, yet the group moves as one.",
        "surface": ["Hero", "Immersive page", "Data art"], "intensity": "medium",
        "worksWith": ["dark-tech", "immersive-3d", "cultural"],
        "stat": "220 boids",
        "code": r"""
const P=['#05060a','#7fe3ff','#9d7bff','#ffd166'];
const B=[];for(let i=0;i<220;i++)B.push({x:rnd(W),y:rnd(H),vx:rnd(70,-70),vy:rnd(70,-70)});
function frame(dt){ctx.fillStyle='rgba(5,6,10,.10)';ctx.fillRect(0,0,W,H);
 for(const b of B){let ax=0,ay=0,cx=0,cy=0,alx=0,aly=0,n=0;
  for(const o of B){if(o===b)continue;const dx=o.x-b.x,dy=o.y-b.y,d2=dx*dx+dy*dy;if(d2<2600){const d=Math.sqrt(d2)||1;ax-=dx/d/d*70;ay-=dy/d/d*70;alx+=o.vx;aly+=o.vy;cx+=o.x;cy+=o.y;n++;}}
  if(n){b.vx+=((alx/n)-b.vx)*dt*1.7+(cx/n-b.x)*dt*.55;b.vy+=((aly/n)-b.vy)*dt*1.7+(cy/n-b.y)*dt*.55;}
  const dx=b.x-mx.x,dy=b.y-mx.y,d=Math.hypot(dx,dy)||1;if(d<80){const f=1-d/80;b.vx+=dx/d*f*260*dt;b.vy+=dy/d*f*260*dt;}
  b.vx+=ax*dt*26;b.vy+=ay*dt*26;
  const sp=Math.hypot(b.vx,b.vy)||1;if(sp>110){b.vx=b.vx/sp*110;b.vy=b.vy/sp*110;}
  b.x+=b.vx*dt;b.y+=b.vy*dt;if(b.x<0)b.x=W;if(b.x>W)b.x=0;if(b.y<0)b.y=H;if(b.y>H)b.y=0;
  ctx.fillStyle=b.vx>0?P[1]:P[2];ctx.globalAlpha=.9;ctx.beginPath();ctx.arc(b.x,b.y,1.8,0,7);ctx.fill();
  ctx.globalAlpha=.28;ctx.beginPath();ctx.moveTo(b.x,b.y);ctx.lineTo(b.x-b.vx*.05,b.y-b.vy*.05);ctx.strokeStyle=ctx.fillStyle;ctx.stroke();}
 ctx.globalAlpha=1;stat('220 boids');}
""",
        "snippet": "separation += -offset / distance²;\nalignment += neighbour.velocity;\ncohesion += neighbour.position;\nvelocity += (alignment + cohesion + separation) * dt;",
        "prompt": "Build a boids flock: 200+ agents with separation, alignment and cohesion, pointer avoidance, capped speed, wrapped edges, drawn as streaks. Single HTML file, canvas 2D.",
    },
    {
        "id": "reaction-diffusion", "name": "Reaction Diffusion", "category": "generative",
        "tagline": "Two chemicals, one equation, endless coral growth.",
        "what": "A 160×100 Gray-Scott grid evolves six iterations per frame, seeded with noise and reseeded under the pointer. Values map to a warm palette and upscale to the screen.",
        "why": "Reaction-diffusion produces organic pattern from pure math, and it is the standard entry to continuous cellular systems.",
        "surface": ["Hero", "Texture", "Science story"], "intensity": "medium",
        "worksWith": ["dark-tech", "cultural", "expressive"],
        "stat": "Gray-Scott 160×100",
        "code": r"""
const cw=160,ch=100,oc=document.createElement('canvas');oc.width=cw;oc.height=ch;const octx=oc.getContext('2d');
let u=new Float32Array(cw*ch),v=new Float32Array(cw*ch),u2=new Float32Array(cw*ch),v2=new Float32Array(cw*ch);
const img=octx.createImageData(cw,ch);
for(let i=0;i<cw*ch;i++){u[i]=1;v[i]=Math.random()<.04?1:0;}
for(let i=0;i<40;i++){const x=Math.floor(rnd(cw)),y=Math.floor(rnd(ch));v[y*cw+x]=1;}
function frame(dt){
 for(let k=0;k<5;k++){
  for(let y=1;y<ch-1;y++)for(let x=1;x<cw-1;x++){const i=y*cw+x;
   const a=u[i],b=v[i];
   const lapU=(u[i-1]+u[i+1]+u[i-cw]+u[i+cw])*.2+(u[i-cw-1]+u[i-cw+1]+u[i+cw-1]+u[i+cw+1])*.05-a;
   const lapV=(v[i-1]+v[i+1]+v[i-cw]+v[i+cw])*.2+(v[i-cw-1]+v[i-cw+1]+v[i+cw-1]+v[i+cw+1])*.05-b;
   const abb=a*b*b;
   u2[i]=a+(.16*lapU-abb+.037*(1-a))*1.0;
   v2[i]=b+(.08*lapV+abb-(.06+.037)*b)*1.0;}
  [u,u2]=[u2,u];[v,v2]=[v2,v];}
 if(mx.down){const px=Math.floor(mx.x/W*(cw-2))+1,py=Math.floor(mx.y/H*(ch-2))+1;for(let yy=-3;yy<=3;yy++)for(let xx=-3;xx<=3;xx++){const i=(py+yy)*cw+px+xx;if(i>0&&i<cw*ch)v[i]=1;}}
 const d=img.data;
 for(let i=0;i<cw*ch;i++){const val=Math.max(0,Math.min(1,(u[i]-.2)*3.2));const t=val;
  d[i*4]=30+t*225;d[i*4+1]=10+t*150;d[i*4+2]=40+t*90;d[i*4+3]=255;}
 octx.putImageData(img,0,0);
 ctx.imageSmoothingEnabled=true;ctx.drawImage(oc,0,0,W,H);stat('Gray-Scott 160×100');}
""",
        "snippet": "u += .16 * lapU - u*v*v + .037 * (1-u);\nv += .08 * lapV + u*v*v - (.06+.037) * v;",
        "prompt": "Build a Gray-Scott reaction-diffusion simulation on a low-resolution grid, iterated several times per frame, painted to ImageData and upscaled. Pointer reseeds. Single HTML file.",
    },
    {
        "id": "game-of-life", "name": "Game of Life", "category": "generative",
        "tagline": "Conway's grid, painted by hand and left to evolve.",
        "what": "An 96×60 toroidal Life grid steps four times a second, with pointer painting and drag erasing. Cell age drives colour, so stable patterns glow differently from newborn ones.",
        "why": "Life is the smallest system that feels alive: three rules, unbounded behaviour.",
        "surface": ["Editorial", "Tech story", "Splash"], "intensity": "subtle",
        "worksWith": ["dark-tech", "classic", "contemporary"],
        "stat": "Life 96×60",
        "code": r"""
const cw=96,ch=60,cells=new Uint8Array(cw*ch),age=new Uint8Array(cw*ch);let stepAcc=0;
for(let i=0;i<cw*ch;i++)cells[i]=Math.random()<.28?1:0;
function step(){const n=new Uint8Array(cw*ch);
 for(let y=0;y<ch;y++)for(let x=0;x<cw;x++){let c=0;for(let yy=-1;yy<=1;yy++)for(let xx=-1;xx<=1;xx++){if(!xx&&!yy)continue;c+=cells[((y+yy+ch)%ch)*cw+((x+xx+cw)%cw)];}
  const i=y*cw+x;n[i]=cells[i]?(c===2||c===3?1:0):(c===3?1:0);
  age[i]=n[i]?Math.min(255,age[i]+18):0;}
 cells.set(n);}
function frame(dt){stepAcc+=dt;if(stepAcc>.22){stepAcc=0;step();}
 ctx.fillStyle='#05060a';ctx.fillRect(0,0,W,H);
 const sx=W/cw,sy=H/ch;
 if(mx.down){const gx=Math.floor(mx.x/sx),gy=Math.floor(mx.y/sy);for(let yy=-2;yy<=2;yy++)for(let xx=-2;xx<=2;xx++){const x=(gx+xx+cw)%cw,y=(gy+yy+ch)%ch;cells[y*cw+x]=1;age[y*cw+x]=200;}}
 for(let y=0;y<ch;y++)for(let x=0;x<cw;x++){const i=y*cw+x;if(!cells[i])continue;const a=age[i]/255;
  ctx.fillStyle=a>.6?'#8fd8ff':a>.3?'#5f9fff':'#335577';ctx.fillRect(x*sx+1,y*sy+1,sx-2,sy-2);}
 stat('Life 96x60');}
""",
        "snippet": "const alive = cells[i];\nconst n = countMooresNeighbours(x, y);\nnext[i] = alive ? (n === 2 || n === 3) : n === 3;",
        "prompt": "Build Conway's Game of Life on a toroidal grid with pointer painting/erasing, cell-age colouring and a stepped simulation. Single HTML file, canvas 2D.",
    },
    {
        "id": "l-system-tree", "name": "L-System Tree", "category": "generative",
        "tagline": "A recursive grammar that grows a tree as you move.",
        "what": "A bracketed L-system with depth 8 is re-evaluated each frame with a growth parameter. Pointer x bends the branch angle, pointer y sets the growth, and the whole tree redraws in one path.",
        "why": "L-systems show how a short rewrite rule becomes botanical structure — and how a parameter can steer it live.",
        "surface": ["Hero", "Editorial", "Seasonal campaign"], "intensity": "medium",
        "worksWith": ["cultural", "classic", "luxe-brand"],
        "stat": "depth 8 · 511 segments",
        "code": r"""
function grow(x,y,a,d,len,out){if(d<=0)return;const nx=x+Math.cos(a)*len,ny=y+Math.sin(a)*len;
 out.push([x,y,nx,ny,d]);const spread=.34+Math.sin(t*.8)*.08+(mx.x/W-.5)*.35;
 grow(nx,ny,a-spread,d-1,len*.74,out);grow(nx,ny,a+spread,d-1,len*.74,out);}
function frame(dt){ctx.fillStyle='#06070b';ctx.fillRect(0,0,W,H);
 const out=[];const len=Math.min(W,H)*.16;grow(W/2,H*.92,-Math.PI/2,8,len,out);
 ctx.lineCap='round';
 for(const [x1,y1,x2,y2,d] of out){const k=1-d/9;ctx.strokeStyle='hsl('+(180+k*120)+',70%,'+(40+k*30)+'%)';ctx.lineWidth=Math.max(.7,d*.9);ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();}
 ctx.fillStyle='#ffd166';for(const s of out)if(s[4]===1){ctx.beginPath();ctx.arc(s[2],s[3],2.2,0,7);ctx.fill();}
 stat('depth 8 · '+out.length+' segments');}
""",
        "snippet": "function grow(x, y, a, depth, len) {\n  const nx = x + cos(a) * len, ny = y + sin(a) * len;\n  grow(nx, ny, a - spread, depth - 1, len * .74);\n  grow(nx, ny, a + spread, depth - 1, len * .74);\n}",
        "prompt": "Build an L-system tree that regrows every frame with a recursion depth of 8, branch angle steered by the pointer, and colour by depth. Single HTML file.",
    },
    {
        "id": "space-colonization", "name": "Space Colonization", "category": "generative",
        "tagline": "Branches find the nearest light and race toward it.",
        "what": "Attractor points scattered in the canopy pull new nodes toward them. Each step, every attractor votes for the nearest branch tip; the tree grows into the light and dies back when it arrives.",
        "why": "Space colonization grows believable trees without grammar, and it is the base of most procedural foliage.",
        "surface": ["Hero", "World-building", "Editorial"], "intensity": "medium",
        "worksWith": ["cultural", "immersive-3d", "classic"],
        "stat": "space colonization",
        "code": r"""
const nodes=[{x:W/2,y:H*.94,px:W/2,py:H*.98}];for(let i=1;i<6;i++)nodes.push({x:W/2,y:H*.94-i*8,px:W/2,py:H*.94-(i-1)*8});let att=[];for(let i=0;i<220;i++)att.push({x:rnd(W*.9,W*.05),y:rnd(H*.72,H*.06)});
let growT=0;
function frame(dt){growT+=dt;
 if(nodes.length<620&&growT>.028){growT=0;
  const pull=new Map();
  for(const a of att){let bi=-1,bd=1e9;for(let i=0;i<nodes.length;i++){const d=Math.hypot(nodes[i].x-a.x,nodes[i].y-a.y);if(d<bd){bd=d;bi=i;}}
   if(bd<130&&bi>=0){const cur=pull.get(bi)||{dx:0,dy:0,n:0};cur.dx+=a.x-nodes[bi].x;cur.dy+=a.y-nodes[bi].y;cur.n++;pull.set(bi,cur);}}
  for(const [bi,v] of pull){const d=Math.hypot(v.dx,v.dy)||1;const step=Math.min(14,8+v.n*1.5);const nx=nodes[bi].x+v.dx/d*step+rnd(1.4,-1.4);const ny=nodes[bi].y+v.dy/d*step+rnd(1.4,-1.4);
   nodes.push({x:nx,y:ny,px:nodes[bi].x,py:nodes[bi].y});}
  att=att.filter(a=>!nodes.some(n=>Math.hypot(n.x-a.x,n.y-a.y)<18));}
 ctx.fillStyle='#05060a';ctx.fillRect(0,0,W,H);
 ctx.strokeStyle='#9fe8c8';ctx.lineWidth=1.4;ctx.globalAlpha=.9;
 for(const n of nodes){ctx.beginPath();ctx.moveTo(n.px,n.py);ctx.lineTo(n.x,n.y);ctx.stroke();}
 ctx.fillStyle='#ffd166';for(const a of att){ctx.beginPath();ctx.arc(a.x,a.y,1.4,0,7);ctx.fill();}
 ctx.globalAlpha=1;stat(nodes.length+' nodes · '+att.length+' lights');}
""",
        "snippet": "for each attractor:\n  find nearest node\n  add (attractor - node) to that node's direction\nfor each node with a direction:\n  grow one step along it",
        "prompt": "Build a space-colonization tree: 260 attractors vote for the nearest branch tip, nodes grow toward averaged directions, attractors die when reached. Single HTML file.",
    },
    {
        "id": "circle-packing", "name": "Circle Packing", "category": "generative",
        "tagline": "Circles keep arriving until the frame is full.",
        "what": "Random candidate circles are tested against every placed circle and the bounds; accepted ones grow slowly. The pointer deletes the nearest pack and leaves a gap that refills.",
        "why": "Circle packing is the simplest organic layout algorithm, and it demonstrates rejection sampling in one loop.",
        "surface": ["Portfolio", "Gallery", "Data art"], "intensity": "subtle",
        "worksWith": ["classic", "cultural", "contemporary"],
        "stat": "circle packing",
        "code": r"""
const cs=[];let tries=0;
function frame(dt){ctx.fillStyle='#07080d';ctx.fillRect(0,0,W,H);
 for(let k=0;k<14;k++){tries++;const r=rnd(46,10),x=rnd(W-r,r),y=rnd(H-r,r);
  let ok=true;for(const c of cs){if(Math.hypot(c.x-x,c.y-y)<c.r+r+3){ok=false;break;}}
  if(ok)cs.push({x,y,r,r0:r});}
 if(cs.length>420)cs.splice(0,40);
 for(const c of cs){ctx.strokeStyle='hsl('+(190+c.r*3)+',65%,60%)';ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(c.x,c.y,c.r,0,7);ctx.stroke();ctx.fillStyle='rgba(120,200,255,.035)';ctx.fill();}
 if(mx.down){let bi=-1,bd=1e9;cs.forEach((c,i)=>{const d=Math.hypot(c.x-mx.x,c.y-mx.y);if(d<bd){bd=d;bi=i;}});if(bi>=0&&bd<200)cs.splice(bi,1);}
 ctx.fillStyle='#8fd8ff';ctx.font='600 11px ui-monospace,monospace';ctx.fillText(cs.length+' circles · '+tries+' tries',16,H-18);
 stat(cs.length+' circles');}
""",
        "snippet": "const candidate = randomCircle();\nif (circles.every(c => dist(c, candidate) > c.r + candidate.r)) {\n  circles.push(candidate);\n}",
        "prompt": "Build animated circle packing with rejection sampling, slow radius growth, and pointer removal. Single HTML file.",
    },
    {
        "id": "phyllotaxis-bloom", "name": "Phyllotaxis Bloom", "category": "generative",
        "tagline": "The golden angle, drawn at 900 points.",
        "what": "Each dot sits at index × 137.5°, with radius √index. The pointer warps the radius and the whole bloom rotates, so the spiral arms tighten and relax.",
        "why": "Phyllotaxis is nature's most efficient packing, and one constant reproduces sunflower, pinecone and cactus geometry.",
        "surface": ["Hero", "Product", "Editorial"], "intensity": "medium",
        "worksWith": ["classic", "luxe-brand", "contemporary"],
        "stat": "900 dots · 137.5°",
        "code": r"""
const N=900,GA=Math.PI*(3-Math.sqrt(5));
function frame(dt){ctx.fillStyle='#07080d';ctx.fillRect(0,0,W,H);
 const cx=W/2,cy=H/2,scale=Math.min(W,H)*.028,spin=t*.12;
 for(let i=0;i<N;i++){const a=i*GA+spin,r=Math.sqrt(i)*scale;const dx=Math.cos(a)*r,dy=Math.sin(a)*r;const d=Math.hypot(dx,dy)||1;
  const push=Math.max(0,1-Math.hypot(cx+dx-mx.x,cy+dy-mx.y)/180);
  const rr=r*(1+push*.5);
  const x=cx+Math.cos(a)*rr,y=cy+Math.sin(a)*rr;
  const k=i/N;ctx.fillStyle='hsl('+(190+k*150)+',75%,'+(45+k*25)+'%)';
  ctx.beginPath();ctx.arc(x,y,2.2+push*4,0,7);ctx.fill();}
 stat('900 dots · 137.5°');}
""",
        "snippet": "const angle = i * 2.399963229728653;\nconst radius = Math.sqrt(i) * scale;\nx = cos(angle) * radius;\ny = sin(angle) * radius;",
        "prompt": "Build a phyllotaxis bloom with 900 dots at the golden angle, sqrt radius and pointer warping. Single HTML file.",
    },
    {
        "id": "maze-generator", "name": "Maze Generator", "category": "play",
        "tagline": "A recursive backtracker carving a new maze live.",
        "what": "A 31×19 grid is carved by depth-first search, one cell at a time, then the solved path is traced. When it finishes, the maze resets with a new seed.",
        "why": "Maze generation is the friendliest introduction to graph algorithms — every carve is an edge in a spanning tree.",
        "surface": ["Game page", "Puzzle", "Loading state"], "intensity": "subtle",
        "worksWith": ["dark-tech", "playful", "contemporary"],
        "stat": "recursive backtracker",
        "code": r"""
const C=31,R=19,cw=W/C,chh=H/R,walls=[],vis=new Uint8Array(C*R),stack=[],path=[];
for(let i=0;i<C*R;i++)walls.push([1,1,1,1]);vis[0]=1;stack.push([0,0]);let done=false,hold=0;
function carve(){if(done){hold+=1;if(hold>240){vis.fill(0);walls.forEach(w=>{w[0]=w[1]=w[2]=w[3]=1});stack.length=0;path.length=0;stack.push([0,0]);vis[0]=1;done=false;hold=0;}return;}
 const [x,y]=stack[stack.length-1];const dirs=[[1,0],[-1,0],[0,1],[0,-1]].sort(()=>Math.random()-.5);let moved=false;
 for(const [dx,dy] of dirs){const nx=x+dx,ny=y+dy;if(nx<0||ny<0||nx>=C||ny>=R||vis[ny*C+nx])continue;
  walls[y*C+x][dx>0?1:dx<0?3:dy>0?2:0]=0;walls[ny*C+nx][dx>0?3:dx<0?1:dy>0?0:2]=0;
  vis[ny*C+nx]=1;stack.push([nx,ny]);moved=true;break;}
 if(!moved){stack.pop();if(!stack.length)done=true;}
}
function frame(dt){for(let i=0;i<4;i++)carve();
 ctx.fillStyle='#07080d';ctx.fillRect(0,0,W,H);
 for(let y=0;y<R;y++)for(let x=0;x<C;x++){const w=walls[y*C+x],px=x*cw,py=y*chh;
  ctx.strokeStyle='#2b5a70';ctx.lineWidth=1.4;ctx.beginPath();
  if(w[0]){ctx.moveTo(px,py);ctx.lineTo(px+cw,py);}if(w[2]){ctx.moveTo(px,py+chh);ctx.lineTo(px+cw,py+chh);}
  if(w[3]){ctx.moveTo(px,py);ctx.lineTo(px,py+chh);}if(w[1]){ctx.moveTo(px+cw,py);ctx.lineTo(px+cw,py+chh);}ctx.stroke();}
 const tip=stack[stack.length-1];if(tip){ctx.fillStyle='#8fd8ff';ctx.fillRect(tip[0]*cw+cw*.3,tip[1]*chh+chh*.3,cw*.4,chh*.4);}
 stat(done?'solved · resetting':stack.length+' cells carving');}
""",
        "snippet": "const stack = [[0,0]];\nwhile (stack.length) {\n  const cell = stack[stack.length-1];\n  const next = unvisitedNeighbour(cell);\n  if (next) { carve(cell, next); stack.push(next); }\n  else stack.pop();\n}",
        "prompt": "Build an animated recursive-backtracker maze generator on a 31×19 grid, drawing walls and the carve path, resetting when solved. Single HTML file.",
    },
    {
        "id": "slime-mold", "name": "Slime Mold", "category": "generative",
        "tagline": "Ten thousand agents leaving a living map.",
        "what": "4000 particles sense the trail ahead-left, ahead and ahead-right, turn toward the strongest, and deposit. The trail diffuses and decays, so paths reinforce and evaporate.",
        "why": "Slime-mold simulation is the canonical stigmergy demo: simple agents, emergent transport networks.",
        "surface": ["Data art", "Hero", "Science story"], "intensity": "medium",
        "worksWith": ["dark-tech", "cultural", "immersive-3d"],
        "stat": "4000 agents",
        "code": r"""
const cw=240,ch=150,trail=new Float32Array(cw*ch),tmp=new Float32Array(cw*ch),oc=document.createElement('canvas');
oc.width=cw;oc.height=ch;const octx=oc.getContext('2d'),img=octx.createImageData(cw,ch);
const A=[];for(let i=0;i<4000;i++)A.push({x:rnd(cw),y:rnd(ch),a:rnd(Math.PI*2)});
function sense(x,y,a){const xx=Math.floor(x+Math.cos(a)*3),yy=Math.floor(y+Math.sin(a)*3);if(xx<0||yy<0||xx>=cw||yy>=ch)return -1;return trail[yy*cw+xx];}
function frame(dt){const speed=1.15;
 for(const p of A){const fl=sense(p.x,p.y,p.a-.5),f=sense(p.x,p.y,p.a),fr=sense(p.x,p.y,p.a+.5);
  if(f>fl&&f>fr)p.a+=rnd(.25,-.25);else if(fl>fr)p.a-=.3;else if(fr>fl)p.a+=.3;else p.a+=rnd(.2,-.2);
  p.x+=Math.cos(p.a)*speed;p.y+=Math.sin(p.a)*speed;
  if(p.x<0||p.y<0||p.x>=cw||p.y>=ch){p.x=rnd(cw);p.y=rnd(ch);p.a=rnd(Math.PI*2);}
  const i=Math.floor(p.y)*cw+Math.floor(p.x);trail[i]=Math.min(1.6,trail[i]+.22);}
 if(mx.down){for(let i=0;i<200;i++){const x=Math.floor(mx.x/W*cw+rnd(9,-9)),y=Math.floor(mx.y/H*ch+rnd(9,-9));if(x>=0&&y>=0&&x<cw&&y<ch)trail[y*cw+x]=1.5;}}
 for(let y=0;y<ch;y++)for(let x=0;x<cw;x++){const i=y*cw+x;let s=0,n=0;
  for(let yy=-1;yy<=1;yy++)for(let xx=-1;xx<=1;xx++){const j=(y+yy+ch)%ch*cw+(x+xx+cw)%cw;s+=trail[j];n++;}
  tmp[i]=s/n*.92;}
 trail.set(tmp);
 const d=img.data;for(let i=0;i<cw*ch;i++){const v=Math.min(1,trail[i]*1.5);d[i*4]=20+v*210;d[i*4+1]=40+v*230;d[i*4+2]=50+v*150;d[i*4+3]=255;}
 octx.putImageData(img,0,0);ctx.drawImage(oc,0,0,W,H);stat('4000 agents · '+cw+'×'+ch);}
""",
        "snippet": "const ahead = sense(x + cos(a) * 3, y + sin(a) * 3);\na += (ahead - here) * turnSpeed;\ntrail[x, y] += deposit;\ntrail = diffuse(trail) * .92;",
        "prompt": "Build a slime-mold simulation: thousands of agents sense the trail at three angles, steer toward the strongest, deposit, and diffuse/decay the field. Single HTML file.",
    },
    {
        "id": "differential-growth", "name": "Differential Growth", "category": "generative",
        "tagline": "A curve that keeps folding because it grows unevenly.",
        "what": "A closed ring of nodes repels its neighbours, subdivides long edges, and is pushed by the pointer. The result is the coral-like folding used for generative sculpture.",
        "why": "Differential growth is the modern way to get organic form without noise: growth plus local repulsion does the work.",
        "surface": ["Hero", "Print", "Installation"], "intensity": "medium",
        "worksWith": ["cultural", "luxe-brand", "immersive-3d"],
        "stat": "differential growth",
        "code": r"""
let pts=[];const R0=Math.min(W,H)*.17;for(let i=0;i<70;i++){const a=i/70*Math.PI*2,r=R0*(1+.06*Math.sin(a*7));pts.push({x:W/2+Math.cos(a)*r,y:H/2+Math.sin(a)*r});}
function frame(dt){const n=pts.length,target=Math.min(W,H)*.017;
 for(let i=0;i<n;i++){const p=pts[i],a=pts[(i-1+n)%n],b=pts[(i+1)%n];
  const d0=Math.hypot(a.x-p.x,a.y-p.y),d1=Math.hypot(b.x-p.x,b.y-p.y);
  if(d0>target){p.x+=(a.x-p.x)*(d0-target)/d0*.55;p.y+=(a.y-p.y)*(d0-target)/d0*.55;}
  if(d1>target){p.x+=(b.x-p.x)*(d1-target)/d1*.55;p.y+=(b.y-p.y)*(d1-target)/d1*.55;}
  const ox=p.x-W/2,oy=p.y-H/2,od=Math.hypot(ox,oy)||1;const g=10+26*(.5+.5*Math.sin(i*1.7));p.x+=ox/od*g*dt;p.y+=oy/od*g*dt;
  const mxp=p.x-mx.x,myp=p.y-mx.y,md=Math.hypot(mxp,myp)||1;
  if(md<140){p.x+=mxp/md*(1-md/140)*90*dt;p.y+=myp/md*(1-md/140)*90*dt;}}
 for(let i=0;i<n;i++){const p=pts[i];
  for(let j=i+2;j<n;j++){if(i===0&&j===n-1)continue;const q=pts[j],dx=p.x-q.x,dy=p.y-q.y,d=Math.hypot(dx,dy)||1;
   if(d<target){const f=(target-d)/d*.7;p.x+=dx*f;p.y+=dy*f;q.x-=dx*f;q.y-=dy*f;}}}
 for(let i=pts.length-1;i>=0;i--){const p=pts[i],q=pts[(i+1)%pts.length];if(Math.hypot(q.x-p.x,q.y-p.y)>target*1.28&&pts.length<1100){pts.splice(i+1,0,{x:(p.x+q.x)/2,y:(p.y+q.y)/2});}}
 ctx.fillStyle='rgba(7,8,13,.22)';ctx.fillRect(0,0,W,H);
 ctx.strokeStyle='#ff9f6e';ctx.lineWidth=1.25;ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.closePath();ctx.stroke();
 stat(pts.length+' nodes');}
""",
        "snippet": "for each node:\n  move toward midpoint of neighbours\n  repel from nearby nodes\nif edge length > threshold: insert midpoint",
        "prompt": "Build differential growth: a closed curve whose nodes relax toward neighbour midpoints, repel locally and subdivide long edges, with pointer push. Single HTML file.",
    },
]
