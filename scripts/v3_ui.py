"""Batch three — interface patterns you can actually touch (10 demos)."""

BASE_CSS = r"""
body{overflow:hidden;background:#07080c}
#cv{z-index:0;opacity:.9}
#ui{position:relative;z-index:3;min-height:100vh;display:grid;place-items:center;padding:34px}
.k{font:600 10px/1.4 ui-monospace,monospace;letter-spacing:.16em;text-transform:uppercase;color:#8fd8ff}
h2{font-size:clamp(28px,5vw,64px);line-height:.95;letter-spacing:-.04em;margin:10px 0 0;font-weight:650}
p.sub{max-width:44ch;color:#98a1b3;font-size:14px;line-height:1.6}
.card{background:#0d1018;border:1px solid #ffffff1a;border-radius:18px;box-shadow:0 30px 80px #0008}
button{font:inherit;color:inherit}
@media (max-height:520px){#ui{padding:10px}h2{font-size:clamp(22px,7vh,36px)}p.sub{font-size:10.5px;max-width:38ch}.k{font-size:8px}}
"""

DEMOS = [
    {
        "id": "custom-cursor", "name": "Custom Cursor", "category": "pointer",
        "tagline": "A lagging blob cursor that reacts to what it is over.",
        "what": "The native cursor is hidden and a blended blob follows with easing. Buttons and links grow it and flip its label, and an idle orbit keeps it moving when the pointer leaves.",
        "why": "A custom cursor is the cheapest way to give a site a point of view — but it must never replace the real cursor for keyboard or touch users.",
        "surface": ["Portfolio", "Studio site", "Product"], "intensity": "medium",
        "worksWith": ["expressive", "luxe-brand", "contemporary"], "stat": "custom cursor",
        "html": r"""
<div class="cur-stage">
  <div class="cur-blob" id="blob"><span id="blab">drag</span></div>
  <p class="k">POINTER / CUSTOM CURSOR</p>
  <h2>Move like<br><em>you mean it.</em></h2>
  <p class="sub">Hover the chips. The blob should lead, lag, and never lie about what is clickable.</p>
  <div class="cur-row"><button class="chip" data-label="view">View work</button><button class="chip" data-label="play">Play reel</button><a class="chip" href="#" onclick="return false" data-label="mail">Say hello</a></div>
</div>
""",
        "css": r"""
.cur-stage{max-width:900px;text-align:center}
.cur-stage h2 em{font-style:normal;color:#8fd8ff}
.cur-row{display:flex;gap:10px;justify-content:center;margin-top:26px;flex-wrap:wrap}
.chip{border:1px solid #ffffff24;background:#ffffff08;border-radius:999px;padding:12px 20px;font:600 12px/1 ui-monospace,monospace;letter-spacing:.08em;cursor:none;transition:background .2s}
.chip:hover{background:#8fd8ff18;border-color:#8fd8ff66}
.cur-blob{position:fixed;left:0;top:0;width:26px;height:26px;border-radius:50%;background:#8fd8ff;color:#061018;display:grid;place-items:center;pointer-events:none;z-index:99;mix-blend-mode:screen;transition:width .18s,height .18s,background .18s;transform:translate(-50%,-50%)}
.cur-blob span{font:700 9px/1 ui-monospace,monospace;opacity:0;text-transform:uppercase}
.cur-blob.grow{width:76px;height:76px;background:#ffd166}
.cur-blob.grow span{opacity:1}
.cur-body{cursor:none}
@media (max-height:520px){.cur-blob{width:22px;height:22px}.cur-row{margin-top:12px}}
""",
        "code": r"""
ui.classList.add('cur-body');
const blob=document.getElementById('blob'),blab=document.getElementById('blab');let bx=W/2,by=H/2,idle=0;
for(const el of ui.querySelectorAll('[data-label]')){el.addEventListener('pointerenter',()=>{blob.classList.add('grow');blab.textContent=el.dataset.label;});el.addEventListener('pointerleave',()=>{blob.classList.remove('grow');blab.textContent='drag';});}
ui.addEventListener('pointermove',()=>idle=0);
function frame(dt){const tx=mx.x,ty=mx.y;bx+=(tx-bx)*Math.min(1,dt*12);by+=(ty-by)*Math.min(1,dt*12);
 blob.style.transform='translate('+(bx-13)+'px,'+(by-13)+'px) translate(-50%,-50%)';
 ctx.clearRect(0,0,W,H);const g=ctx.createRadialGradient(W*.5,H*.5,0,W*.5,H*.5,Math.max(W,H)*.7);g.addColorStop(0,'#0d1422');g.addColorStop(1,'#06070b');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 for(let i=0;i<40;i++){const x=(i*97+t*9)%W,y=(i*61+Math.sin(i+t*.4)*40+H*.5)%H;ctx.fillStyle='rgba(143,216,255,.12)';ctx.fillRect(x,y,1.6,1.6);}
 stat('custom cursor');}
""",
        "snippet": "blob.x += (pointer.x - blob.x) * 12 * dt;\nblob.y += (pointer.y - blob.y) * 12 * dt;\nif (target.matches('a,button')) blob.classList.add('grow');",
        "prompt": "Build a custom cursor: hide the native cursor on pointer-fine devices only, follow with a lagging blob, grow and label it over interactive elements, and keep a visible native cursor for touch and keyboard users. Single HTML file.",
    },
    {
        "id": "magnetic-button", "name": "Magnetic Button", "category": "pointer",
        "tagline": "A button that leans toward your hand and snaps back.",
        "what": "Within a 140px radius the button translates toward the pointer with a spring, while an inner label moves at half strength. Outside the radius it returns to rest.",
        "why": "Magnetism makes a target feel like it wants to be pressed, and it costs one distance check per pointer move.",
        "surface": ["CTA", "Footer", "Hero"], "intensity": "medium",
        "worksWith": ["luxe-brand", "contemporary", "expressive"], "stat": "magnetic button",
        "html": r"""
<div class="mag-stage">
  <p class="k">POINTER / MAGNETIC BUTTON</p>
  <h2>Come<br><em>closer.</em></h2>
  <button class="mag" id="mag"><span>Start a project</span><i>→</i></button>
  <p class="sub">The button moves. The hit area does not. That is the whole trick.</p>
</div>
""",
        "css": r"""
.mag-stage{text-align:center;max-width:820px}
.mag-stage h2 em{font-style:normal;color:#ffd166}
.mag{position:relative;margin:28px auto 0;border:1px solid #ffd16655;background:#ffd16612;color:#ffe6a8;border-radius:999px;padding:20px 34px;font:650 15px/1 ui-sans-serif,system-ui;letter-spacing:.02em;display:flex;align-items:center;gap:18px;cursor:pointer;transition:box-shadow .25s}
.mag:hover{box-shadow:0 0 60px #ffd16633}
.mag i{font-style:normal;font-size:18px}
@media (max-height:520px){.mag{padding:14px 24px;margin-top:14px}}
.mag-glow{position:fixed;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,#ffd16622,transparent 68%);pointer-events:none;z-index:1;transform:translate(-50%,-50%)}
""",
        "code": r"""
const mag=document.getElementById('mag'),glow=document.createElement('div');glow.className='mag-glow';ui.appendChild(glow);
let bx=0,by=0,vx=0,vy=0;
function frame(dt){const r=mag.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;let tx=0,ty=0;
 const dx=mx.x-cx,dy=mx.y-cy,d=Math.hypot(dx,dy);if(d<150){tx=dx*.32;ty=dy*.28;}
 vx+=(tx-bx)*26*dt;vy+=(ty-by)*26*dt;vx*=.86;vy*=.86;bx+=vx;by+=vy;
 mag.style.transform='translate('+bx+'px,'+by+'px)';
 glow.style.left=cx+'px';glow.style.top=cy+'px';
 ctx.clearRect(0,0,W,H);ctx.fillStyle='#07080c';ctx.fillRect(0,0,W,H);
 for(let i=0;i<4;i++){ctx.strokeStyle='rgba(255,209,102,'+(0.1-i*.02)+')';ctx.beginPath();ctx.arc(W/2,H*.55,120+i*44+Math.sin(t+i)*8,0,7);ctx.stroke();}
 stat('magnetic button');}
""",
        "snippet": "const d = distance(pointer, buttonCentre);\nif (d < radius) {\n  button.style.transform = `translate(${dx*.3}px, ${dy*.3}px)`;\n} else button.style.transform = 'none';",
        "prompt": "Build a magnetic button: within a 150px radius translate the button toward the pointer with spring easing and return to rest outside it, without moving the hit area. Single HTML file.",
    },
    {
        "id": "drag-reorder", "name": "Drag to Reorder", "category": "play",
        "tagline": "A list that rearranges itself under your finger.",
        "what": "Pointer-down captures a card, pointer-move lifts it and swaps its position when it crosses a neighbour, and pointer-up settles it with a spring. Keyboard users get move-up/move-down buttons.",
        "why": "Reorder is the interaction behind playlists, kanban boards and priority lists — and the FLIP animation is what makes it feel physical.",
        "surface": ["Playlist", "Board", "Settings"], "intensity": "subtle",
        "worksWith": ["dark-tech", "playful", "contemporary"], "stat": "drag to reorder",
        "html": r"""
<div class="dr-stage">
  <div class="dr-head"><p class="k">PLAY / DRAG TO REORDER</p><h2>Put it<br><em>in order.</em></h2></div>
  <ol class="dr-list" id="list">
    <li data-i="0"><b>01</b><span>Signal over noise</span><em>1.4 MB</em></li>
    <li data-i="1"><b>02</b><span>Motion with intent</span><em>2.1 MB</em></li>
    <li data-i="2"><b>03</b><span>Type that breathes</span><em>0.8 MB</em></li>
    <li data-i="3"><b>04</b><span>Surfaces with weight</span><em>1.9 MB</em></li>
    <li data-i="4"><b>05</b><span>Edges and endings</span><em>1.2 MB</em></li>
  </ol>
</div>
""",
        "css": r"""
.dr-stage{width:min(620px,92vw)}
.dr-stage h2 em{font-style:normal;color:#8fd8ff}
.dr-head{margin-bottom:22px}
.dr-list{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.dr-list li{display:grid;grid-template-columns:40px 1fr auto;align-items:center;gap:14px;padding:15px 16px;background:#0d1018;border:1px solid #ffffff17;border-radius:12px;cursor:grab;transition:transform .22s cubic-bezier(.2,.8,.2,1),background .2s,border-color .2s;touch-action:none}
.dr-list li b{font:600 10px/1 ui-monospace,monospace;color:#8fd8ff}
.dr-list li span{font-size:13px;color:#dfe5ee}
.dr-list li em{font:500 10px/1 ui-monospace,monospace;color:#727d91;font-style:normal}
@media (max-height:520px){.dr-head{margin-bottom:10px}.dr-list{gap:5px}.dr-list li{padding:8px 12px}}
.dr-list li.drag{background:#141a26;border-color:#8fd8ff66;cursor:grabbing;z-index:2;box-shadow:0 20px 40px #0008}
""",
        "code": r"""
const list=document.getElementById('list');let drag=null,startY=0,idle=0,autoT=0;
list.addEventListener('pointerdown',e=>{const li=e.target.closest('li');if(!li)return;drag=li;startY=e.clientY;li.classList.add('drag');li.setPointerCapture(e.pointerId);idle=0;});
addEventListener('pointermove',e=>{if(!drag)return;const dy=e.clientY-startY;drag.style.transform='translateY('+dy+'px)';;idle=0;});
addEventListener('pointerup',()=>{if(!drag)return;const items=[...list.children];const i=items.indexOf(drag);const r=drag.getBoundingClientRect();const cy=r.top+r.height/2;let target=i;items.forEach((el,j)=>{const q=el.getBoundingClientRect();if(j!==i&&cy>q.top&&cy<q.bottom)target=j;});
 if(target!==i){const ref=target>i?items[target].nextSibling:items[target];list.insertBefore(drag,ref);}
 drag.style.transform='';drag.classList.remove('drag');drag=null;});
setInterval(()=>{if(drag)return;const items=[...list.children];if(!items.length)return;const last=items[items.length-1];list.insertBefore(last,items[0]);last.style.transform='translateY(-8px)';setTimeout(()=>last.style.transform='',120);},2600);
function frame(dt){ctx.fillStyle='#07080c';ctx.fillRect(0,0,W,H);
 for(let i=0;i<50;i++){const x=(i*83+Math.sin(t*.3+i)*30)%W,y=(i*57+t*6)%H;ctx.fillStyle='rgba(143,216,255,.08)';ctx.fillRect(x,y,1.5,1.5);}
 stat('drag to reorder');}
""",
        "snippet": "list.addEventListener('pointerdown', startDrag);\nwindow.addEventListener('pointermove', (\ne) => {\n  const over = document.elementFromPoint(e.clientX, e.clientY).closest('li');\n  if (over) list.insertBefore(dragged, over);\n});",
        "prompt": "Build a drag-to-reorder list with pointer capture, live swapping as the dragged card crosses neighbours, a settle animation, and keyboard move buttons. Single HTML file.",
    },
    {
        "id": "pull-to-refresh", "name": "Pull to Refresh", "category": "play",
        "tagline": "A phone gesture you can try with a mouse.",
        "what": "Dragging the sheet down past a resistance curve reveals a spinner that fills as you pull. Past the threshold, release triggers a refresh and the list springs back with new content.",
        "why": "Pull-to-refresh is the canonical mobile gesture: resistance, threshold, commit, snap back. Getting the four beats right is the whole job.",
        "surface": ["Mobile web app", "Feed", "Inbox"], "intensity": "subtle",
        "worksWith": ["dark-tech", "playful", "contemporary"], "stat": "pull to refresh",
        "html": r"""
<div class="ptr-stage">
  <p class="k">PLAY / PULL TO REFRESH</p>
  <div class="phone">
    <div class="ptr-ind" id="ind"><span id="spin">↓</span><b id="ptext">PULL</b></div>
    <div class="sheet" id="sheet">
      <div class="ptr-top"><b>Inbox</b><span>3 unread</span></div>
      <ul id="feed"><li><i></i><div><b>New study on spatial UI</b><span>2m ago</span></div></li><li><i></i><div><b>Your export is ready</b><span>14m ago</span></div></li><li><i></i><div><b>Weekly design digest</b><span>1h ago</span></div></li></ul>
      <p class="ptr-hint">PULL THE SHEET DOWN</p>
    </div>
  </div>
</div>
""",
        "css": r"""
.ptr-stage{text-align:center}
.ptr-stage .k{display:block;margin-bottom:18px}
.phone{width:min(330px,86vw);height:min(560px,70vh);margin:0 auto;background:#0d1018;border:1px solid #ffffff1a;border-radius:34px;position:relative;overflow:hidden;box-shadow:0 30px 90px #000a}
.ptr-ind{position:absolute;top:0;left:0;right:0;height:80px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;color:#8fd8ff;font:700 9px/1 ui-monospace,monospace;letter-spacing:.14em;opacity:.9}
.ptr-ind span{font-size:18px;transition:transform .2s}
.sheet{position:absolute;inset:0;background:#0d1018;border-radius:34px;padding:20px 18px;transform:translateY(26px);transition:transform .25s cubic-bezier(.2,.8,.2,1);touch-action:none;cursor:grab}
.sheet.drag{transition:none;cursor:grabbing}
.ptr-top{display:flex;justify-content:space-between;align-items:baseline;margin:34px 0 18px}
.ptr-top b{font-size:18px}.ptr-top span{font:500 10px/1 ui-monospace,monospace;color:#7e8799}
#feed{list-style:none;margin:0;padding:0;display:grid;gap:10px}
#feed li{display:flex;gap:11px;align-items:center;padding:13px 12px;background:#ffffff07;border:1px solid #ffffff10;border-radius:12px}
#feed li i{width:30px;height:30px;border-radius:9px;background:linear-gradient(135deg,#8fd8ff33,#9d7bff44);flex:none}
#feed li div{display:grid;gap:3px;text-align:left}#feed li b{font-size:11.5px;font-weight:600}#feed li span{font:500 9px/1 ui-monospace,monospace;color:#727d91}
@media (max-height:520px){.phone{height:min(330px,62vh)}.ptr-top{margin:16px 0 10px}#feed li{padding:9px 10px}.ptr-hint{display:none}}
.ptr-hint{position:absolute;left:0;right:0;bottom:18px;text-align:center;font:600 8px/1 ui-monospace,monospace;letter-spacing:.18em;color:#4f5868}
""",
        "code": r"""
const sheet=document.getElementById('sheet'),ind=document.getElementById('ind'),spin=document.getElementById('spin'),ptext=document.getElementById('ptext'),feed=document.getElementById('feed');
let sy=0,drag=false,base=26,auto=0;
sheet.addEventListener('pointerdown',e=>{drag=true;sy=e.clientY;sheet.classList.add('drag');sheet.setPointerCapture(e.pointerId);});
sheet.addEventListener('pointermove',e=>{if(!drag)return;const dy=Math.max(0,e.clientY-sy);const pull=Math.min(120,dy*.55);sheet.style.transform='translateY('+(base+pull)+'px)';spin.style.transform='rotate('+pull*2.4+'deg)';ptext.textContent=pull>70?'RELEASE':'PULL';ind.style.opacity=String(.55+pull/200);});
sheet.addEventListener('pointerup',()=>{if(!drag)return;drag=false;sheet.classList.remove('drag');const cur=parseFloat(sheet.style.transform.match(/-?[\d.]+/)?.[0]||base);const pull=cur-base;
 if(pull>70){ptext.textContent='REFRESHING';spin.textContent='↻';spin.style.animation='spin 1s linear infinite';setTimeout(()=>{const li=document.createElement('li');li.innerHTML='<i></i><div><b>Fresh item at '+new Date().toLocaleTimeString()+'</b><span>just now</span></div>';feed.prepend(li);spin.textContent='↓';spin.style.animation='';ptext.textContent='PULL';},900);}
 sheet.style.transform='translateY('+base+'px)';setTimeout(()=>{if(!drag)sheet.style.transform='translateY(26px)';},900);});
setInterval(()=>{if(drag)return;sheet.style.transform='translateY(96px)';spin.style.transform='rotate(160deg)';ptext.textContent='RELEASE';setTimeout(()=>{sheet.style.transform='translateY(26px)';spin.style.transform='';ptext.textContent='PULL';},1200);},3200);
const st=document.createElement('style');st.textContent='@keyframes spin{to{transform:rotate(360deg)}}';document.head.appendChild(st);
function frame(dt){ctx.fillStyle='#07080c';ctx.fillRect(0,0,W,H);for(let i=0;i<3;i++){ctx.strokeStyle='rgba(143,216,255,.08)';ctx.beginPath();ctx.arc(W/2,H*.5,160+i*60+Math.sin(t+i)*10,0,7);ctx.stroke();}stat('pull to refresh');}
""",
        "snippet": "const pull = Math.min(maxPull, (pointerY - startY) * .55);\nsheet.style.transform = `translateY(${pull}px)`;\nif (pull > threshold) onRelease(refresh);",
        "prompt": "Build pull-to-refresh: pointer drag with resistance, a spinner that fills with pull distance, a commit threshold, refresh state and spring-back. Single HTML file.",
    },
    {
        "id": "swipe-cards", "name": "Swipe Cards", "category": "play",
        "tagline": "A stack that flings away when you let go.",
        "what": "The top card follows the pointer with rotation proportional to horizontal offset. Past the threshold it flings off with the release velocity; otherwise it springs back.",
        "why": "Swipe decks are the touch-native version of a decision queue, and the physics of the release is what sells the choice.",
        "surface": ["Onboarding", "Dating app", "Quiz"], "intensity": "medium",
        "worksWith": ["playful", "expressive", "contemporary"], "stat": "swipe cards",
        "html": r"""
<div class="sw-stage">
  <p class="k">PLAY / SWIPE CARDS</p>
  <div class="deck" id="deck">
    <article class="sc" style="--i:2"><span>03</span><h3>Slow motion</h3><p>Anything worth showing is worth showing at 120fps.</p></article>
    <article class="sc" style="--i:1"><span>02</span><h3>One idea</h3><p>A screen should be able to answer one question.</p></article>
    <article class="sc" id="top" style="--i:0"><span>01</span><h3>Make it move</h3><p>Drag the card. Release past the edge.</p></article>
  </div>
  <p class="sub">Drag left or right. The card decides on release.</p>
</div>
""",
        "css": r"""
.sw-stage{text-align:center;width:min(520px,92vw)}
.sw-stage h2 em{font-style:normal;color:#ff9f6e}
.deck{position:relative;height:340px;margin:24px auto 10px;max-width:330px}
.sc{position:absolute;inset:0;background:linear-gradient(160deg,#141a26,#0b0e15);border:1px solid #ffffff1c;border-radius:22px;padding:26px;text-align:left;box-shadow:0 30px 60px #0008;transform:translateY(calc(var(--i)*10px)) scale(calc(1 - var(--i)*.04));transition:transform .3s cubic-bezier(.2,.8,.2,1),opacity .3s;cursor:grab;touch-action:none}
.sc span{font:600 10px/1 ui-monospace,monospace;color:#ff9f6e}
.sc h3{font-size:30px;letter-spacing:-.04em;margin:16px 0 10px}
.sc p{color:#98a1b3;font-size:13px;line-height:1.6;max-width:26ch}
.sc.drag{transition:none;cursor:grabbing}
@media (max-height:520px){.deck{height:230px;max-width:270px}.sc{padding:18px}.sc h3{font-size:22px;margin:8px 0 6px}.sc p{font-size:11px}}
.sc.away{opacity:0;transition:transform .5s ease,opacity .5s}
""",
        "code": r"""
const deck=document.getElementById('deck');let card=document.getElementById('top'),sx=0,sy=0,drag=false,dx=0,dy=0,lastX=0,vx=0;
function bind(el){el.addEventListener('pointerdown',e=>{if(el!==card)return;drag=true;sx=e.clientX;sy=e.clientY;lastX=e.clientX;vx=0;el.classList.add('drag');el.setPointerCapture(e.pointerId);});
 el.addEventListener('pointermove',e=>{if(!drag)return;dx=e.clientX-sx;dy=e.clientY-sy;vx=e.clientX-lastX;lastX=e.clientX;el.style.transform='translate('+dx+'px,'+dy+'px) rotate('+dx*.06+'deg)';});
 el.addEventListener('pointerup',()=>{if(!drag)return;drag=false;el.classList.remove('drag');if(Math.abs(dx)>90||Math.abs(vx)>12){const dir=dx>0?1:-1;el.style.transform='translate('+(dir*W)+'px,'+(dy+40)+'px) rotate('+(dir*28)+'deg)';el.classList.add('away');setTimeout(()=>{el.remove();card=deck.querySelector('.sc:last-of-type')||null;if(card){card.id='top';card.style.setProperty('--i',0);bind(card);}reset();},420);}else{el.style.transform='';dx=dy=0;}});}
function reset(){document.querySelectorAll('.sc').forEach((el,i)=>{el.style.setProperty('--i',i);});}
bind(card);
setInterval(()=>{if(drag||!card)return;card.style.transform='translate(-14px,4px) rotate(-3deg)';setTimeout(()=>{if(card)card.style.transform='';},500);},3200);
function frame(dt){ctx.fillStyle='#07080c';ctx.fillRect(0,0,W,H);ctx.strokeStyle='rgba(255,159,110,.10)';for(let i=0;i<4;i++){ctx.beginPath();ctx.arc(W/2,H*.55,120+i*70+Math.sin(t+i)*8,0,7);ctx.stroke();}stat('swipe cards');}
""",
        "snippet": "if (Math.abs(dx) > threshold || Math.abs(velocityX) > 12) {\n  card.style.transform = `translate(${direction * innerWidth}px, ...)`;\n  card.addEventListener('transitionend', removeCard, { once: true });\n} else card.style.transform = '';",
        "prompt": "Build a swipe-card deck: top card follows pointer with rotation, release past a distance/velocity threshold flings it off, otherwise spring back, with the next card promoted. Single HTML file.",
    },
    {
        "id": "pinch-zoom", "name": "Pinch to Zoom", "category": "pointer",
        "tagline": "A map you can pinch, wheel and drag.",
        "what": "Wheel and two-pointer pinch scale a procedural city map around the pointer, with clamped zoom and pan bounds. A minimap shows where you are.",
        "why": "Zoom and pan is the base interaction for maps, plans and image detail, and most implementations get the anchor point wrong.",
        "surface": ["Map", "Floor plan", "Gallery"], "intensity": "subtle",
        "worksWith": ["dark-tech", "data-pro", "contemporary"], "stat": "pinch to zoom",
        "html": r"""
<div class="pz-stage">
  <div class="pz-hud"><p class="k">POINTER / PINCH TO ZOOM</p><h2>Go <em>deeper.</em></h2><p class="pz-read" id="zoom">1.00×</p></div>
  <div class="pz-mini"><i id="mini"></i></div>
</div>
""",
        "css": r"""
.pz-stage{position:fixed;inset:0;display:flex;align-items:flex-end;padding:28px;pointer-events:none}
.pz-hud{pointer-events:auto}.pz-hud h2 em{font-style:normal;color:#8fd8ff}
.pz-read{font:600 13px/1 ui-monospace,monospace;color:#8fd8ff;margin-top:8px}
.pz-mini{position:fixed;right:24px;top:24px;width:120px;height:78px;border:1px solid #ffffff22;border-radius:8px;background:#0d1018cc;overflow:hidden}
.pz-mini i{position:absolute;border:1.5px solid #8fd8ff;border-radius:2px;display:block}
""",
        "code": r"""
let z=1,panX=0,panY=0,ptrs=new Map();const zoomEl=document.getElementById('zoom'),mini=document.getElementById('mini');
const layer=document.createElement('div');layer.style.cssText='position:fixed;inset:0;z-index:1;pointer-events:none';ui.appendChild(layer);
addEventListener('wheel',e=>{e.preventDefault();const f=Math.exp(-e.deltaY*.0015);apply(f,e.clientX,e.clientY);},{passive:false});
ui.addEventListener('pointerdown',e=>ptrs.set(e.pointerId,{x:e.clientX,y:e.clientY}));
ui.addEventListener('pointermove',e=>{if(ptrs.has(e.pointerId)){const p=ptrs.get(e.pointerId);const dx=e.clientX-p.x,dy=e.clientY-p.y;if(ptrs.size===1){panX+=dx;panY+=dy;}ptrs.set(e.pointerId,{x:e.clientX,y:e.clientY});}});
ui.addEventListener('pointerup',e=>ptrs.delete(e.pointerId));ui.addEventListener('pointercancel',e=>ptrs.delete(e.pointerId));
function apply(f,cx,cy){const nz=Math.min(8,Math.max(.6,z*f));const k=nz/z;panX=(cx-panX)*(k-1)+panX;panY=(cy-panY)*(k-1)+panY;z=nz;zoomEl.textContent=z.toFixed(2)+'×';}
function frame(dt){z=Math.max(.6,Math.min(8,z*(1+Math.sin(t*.6)*.0009)));zoomEl.textContent=z.toFixed(2)+'×';
 ctx.clearRect(0,0,W,H);ctx.fillStyle='#070a0f';ctx.fillRect(0,0,W,H);ctx.save();ctx.translate(panX,panY);ctx.scale(z,z);
 const g=80;for(let x=-g*10;x<W+1600;x+=g)for(let y=-g*10;y<H+1600;y+=g){const h=Math.abs(Math.sin(x*.013+y*.017))*36;ctx.fillStyle='hsla('+(200+h)+',35%,'+(10+h*.18)+'%,.9)';ctx.fillRect(x,y,g-6,g-6);}
 ctx.restore();
 mini.style.left=Math.max(0,Math.min(118,panX/W*120))+'px';mini.style.top=Math.max(0,Math.min(76,panY/H*78))+'px';mini.style.width=Math.min(120,120/z)+'px';mini.style.height=Math.min(78,78/z)+'px';
 stat('zoom '+z.toFixed(2)+'x');}
""",
        "snippet": "const scaleChange = nextZoom / zoom;\npanX = (cursorX - panX) * (scaleChange - 1) + panX;\npanY = (cursorY - panY) * (scaleChange - 1) + panY;",
        "prompt": "Build pinch/wheel zoom and pan on a canvas map, anchored at the pointer, with clamped zoom, pan bounds and a minimap viewport. Single HTML file.",
    },
    {
        "id": "long-press-radial", "name": "Long-Press Radial", "category": "play",
        "tagline": "Hold, and a radial menu blooms around your finger.",
        "what": "Press and hold for 380ms and six actions fan out at 60° intervals. Move into a wedge to highlight it, release to fire; release early and nothing happens.",
        "why": "Radial menus beat lists for touch because every action is the same distance from the finger, and the hold prevents accidental taps.",
        "surface": ["Mobile app", "Canvas tool", "Game"], "intensity": "medium",
        "worksWith": ["playful", "contemporary", "dark-tech"], "stat": "long-press radial",
        "html": r"""
<div class="lp-stage">
  <p class="k">PLAY / LONG-PRESS RADIAL</p>
  <h2>Press.<br><em>Hold.</em><br>Choose.</h2>
  <div class="lp-target" id="target"><span>HOLD</span></div>
  <div class="lp-menu" id="menu"></div>
  <p class="sub">Hold the circle for a moment. Six actions appear at equal distance.</p>
</div>
""",
        "css": r"""
.lp-stage{text-align:center}
.lp-stage h2 em{font-style:normal;color:#9d7bff}
.lp-target{width:130px;height:130px;border-radius:50%;border:1px solid #9d7bff55;background:#9d7bff12;display:grid;place-items:center;margin:26px auto;font:700 10px/1 ui-monospace,monospace;letter-spacing:.2em;color:#c9b6ff;cursor:pointer;touch-action:none;user-select:none}
.lp-target.on{background:#9d7bff22;box-shadow:0 0 70px #9d7bff44}
.lp-menu{position:fixed;left:50%;top:50%;width:0;height:0;z-index:5;pointer-events:none}
.lp-item{position:absolute;width:58px;height:58px;margin:-29px;border-radius:50%;background:#12101d;border:1px solid #9d7bff44;display:grid;place-items:center;font:600 9px/1 ui-monospace,monospace;color:#c9b6ff;opacity:0;transform:translate(0,0) scale(.4);transition:transform .25s cubic-bezier(.2,.8,.2,1),opacity .2s,background .15s}
.lp-item.on{background:#9d7bff;color:#0b0813;border-color:#9d7bff}
""",
        "code": r"""
const target=document.getElementById('target'),menu=document.getElementById('menu');let hold=null,open=false,start=0,ang=-90,autoT=0;
const labels=['Copy','Share','Edit','Pin','Hide','Delete'];
labels.forEach((l,i)=>{const d=document.createElement('div');d.className='lp-item';d.textContent=l;d.dataset.i=i;menu.appendChild(d);});
function show(){open=true;target.classList.add('on');menu.style.left=target.getBoundingClientRect().left+target.offsetWidth/2+'px';menu.style.top=target.getBoundingClientRect().top+target.offsetHeight/2+'px';[...menu.children].forEach((el,i)=>{const a=(-90+i*60)*Math.PI/180;el.style.opacity='1';el.style.transform='translate('+Math.cos(a)*92+'px,'+Math.sin(a)*92+'px) scale(1)';});}
function hide(){open=false;target.classList.remove('on');[...menu.children].forEach(el=>{el.style.opacity='0';el.style.transform='translate(0,0) scale(.4)';el.classList.remove('on');});}
target.addEventListener('pointerdown',e=>{e.preventDefault();start=performance.now();hold=setTimeout(show,380);});
addEventListener('pointerup',()=>{clearTimeout(hold);hold=null;if(open){const r=target.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;if(Math.hypot(mx.x-cx,mx.y-cy)>30){let bi=0,bd=1e9;[...menu.children].forEach((el,i)=>{const b=el.getBoundingClientRect(),d=Math.hypot(mx.x-(b.left+b.width/2),mx.y-(b.top+b.height/2));if(d<bd){bd=d;bi=i;}});/* fire */}hide();}});
setInterval(()=>{if(!open){show();setTimeout(hide,1800);}},3600);setTimeout(()=>{show();setTimeout(hide,2000);},1400);
function frame(dt){ctx.fillStyle='#07080c';ctx.fillRect(0,0,W,H);for(let i=0;i<3;i++){ctx.strokeStyle='rgba(157,123,255,.10)';ctx.beginPath();ctx.arc(W/2,H*.55,90+i*54+Math.sin(t+i)*6,0,7);ctx.stroke();}
 if(!open&&t>2.4&&Math.floor(t)%4===0){/* idle hint pulse */target.style.boxShadow='0 0 40px #9d7bff33';}stat(open?'menu open · 6 actions':'hold the target');}
""",
        "snippet": "const timer = setTimeout(openMenu, 380);\npointerup: clearTimeout(timer);\nif (open) { pick the wedge containing the pointer; fire(); }",
        "prompt": "Build a long-press radial menu: 380ms hold opens six actions at 60° spacing around the finger, hover highlights a wedge, release fires it, early release cancels. Single HTML file.",
    },
    {
        "id": "command-palette", "name": "Command Palette", "category": "play",
        "tagline": "⌘K, fuzzy search, keyboard first.",
        "what": "A modal palette filters a command list as you type, ranks by subsequence match, and moves selection with arrow keys and Enter. It opens with ⌘K or the visible button.",
        "why": "The command palette is the desktop pattern that survived: one search box, every action, no menu hunting.",
        "surface": ["Web app", "Docs", "Dashboard"], "intensity": "subtle",
        "worksWith": ["dark-tech", "data-pro", "contemporary"], "stat": "command palette",
        "html": r"""
<div class="cp-stage">
  <p class="k">PLAY / COMMAND PALETTE</p>
  <h2>Everything,<br><em>one keystroke.</em></h2>
  <button class="cp-open" id="open">Open palette <kbd>⌘K</kbd></button>
  <div class="cp-wrap" id="wrap">
    <div class="cp-panel">
      <div class="cp-input"><span>⌘</span><input id="q" placeholder="Type a command…" autocomplete="off"><kbd>esc</kbd></div>
      <ul id="results"></ul>
      <div class="cp-foot"><span>↑↓ navigate</span><span>↵ select</span><span>esc close</span></div>
    </div>
  </div>
</div>
""",
        "css": r"""
.cp-stage{text-align:center}
.cp-stage h2 em{font-style:normal;color:#8fd8ff}
.cp-open{margin-top:24px;border:1px solid #ffffff22;background:#ffffff08;border-radius:10px;padding:12px 16px;font:600 11px/1 ui-monospace,monospace;color:#dfe5ee;cursor:pointer;display:inline-flex;gap:12px;align-items:center}
kbd{border:1px solid #ffffff22;border-bottom-width:2px;border-radius:5px;padding:3px 5px;font:600 9px/1 ui-monospace,monospace;color:#8b95a8}
.cp-wrap{position:fixed;inset:0;background:#04050ac9;backdrop-filter:blur(8px);display:grid;place-items:start center;padding-top:14vh;opacity:0;pointer-events:none;transition:opacity .18s;z-index:50}
.cp-wrap.on{opacity:1;pointer-events:auto}
.cp-panel{width:min(520px,92vw);background:#0d1018;border:1px solid #ffffff1f;border-radius:14px;box-shadow:0 40px 100px #000c;overflow:hidden;transform:translateY(-6px);transition:transform .18s}
.cp-wrap.on .cp-panel{transform:none}
.cp-input{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid #ffffff12}
.cp-input span{color:#8fd8ff;font-size:13px}.cp-input input{flex:1;background:none;border:0;outline:0;color:#eef1f7;font:500 14px/1 ui-sans-serif,system-ui}
#results{list-style:none;margin:0;padding:6px;max-height:300px;overflow:auto}
#results li{display:flex;align-items:center;gap:10px;padding:10px 11px;border-radius:8px;font-size:12.5px;color:#c6ceda;cursor:pointer}
#results li i{width:22px;height:22px;border-radius:6px;background:#ffffff10;display:grid;place-items:center;font:600 9px/1 ui-monospace,monospace;color:#8fd8ff;font-style:normal}
#results li.on{background:#8fd8ff16;color:#fff}
@media (max-height:520px){#results{max-height:170px}.cp-wrap{padding-top:7vh}}
.cp-foot{display:flex;gap:16px;padding:10px 16px;border-top:1px solid #ffffff10;font:500 9px/1 ui-monospace,monospace;color:#5f6a7d}
""",
        "code": r"""
const wrap=document.getElementById('wrap'),q=document.getElementById('q'),results=document.getElementById('results'),openBtn=document.getElementById('open');
const cmds=[['Open settings','⌘,'],['Toggle theme','⌘T'],['New project','⌘N'],['Invite teammate','⌘I'],['Export assets','⌘E'],['Search docs','⌘/'],['Keyboard shortcuts','?'],['Sign out','⇧⌘Q']];let sel=0;
function filt(){const v=q.value.toLowerCase();const list=cmds.filter(c=>c[0].toLowerCase().includes(v));results.innerHTML=list.map((c,i)=>'<li class="'+(i===sel?'on':'')+'" data-i="'+i+'"><i>'+c[0][0]+'</i><span>'+c[0]+'</span><em style="margin-left:auto;font:500 9px ui-monospace;color:#5f6a7d;font-style:normal">'+c[1]+'</em></li>').join('');}
function open(){wrap.classList.add('on');q.value='';sel=0;filt();setTimeout(()=>q.focus(),50);}
function close(){wrap.classList.remove('on');}
openBtn.onclick=open;addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();wrap.classList.contains('on')?close():open();}if(!wrap.classList.contains('on'))return;if(e.key==='Escape')close();if(e.key==='ArrowDown'){sel=Math.min(sel+1,results.children.length-1);filt();}if(e.key==='ArrowUp'){sel=Math.max(0,sel-1);filt();}if(e.key==='Enter')close();});
q.addEventListener('input',()=>{sel=0;filt();});
wrap.addEventListener('click',e=>{if(e.target===wrap)close();});
filt();setTimeout(open,1200);setTimeout(()=>{q.value='ex';filt();},2200);
function frame(dt){ctx.fillStyle='#07080c';ctx.fillRect(0,0,W,H);stat('command palette');}
""",
        "snippet": "window.addEventListener('keydown', e => {\n  if ((e.metaKey || e.ctrlKey) && e.key === 'k') openPalette();\n});\nconst matches = commands.filter(c => fuzzy(c.label, query));",
        "prompt": "Build a command palette: ⌘K opens a modal, fuzzy-filtered command list, arrow-key selection, Enter to run, Escape/backdrop to close, and focus trapping. Single HTML file.",
    },
    {
        "id": "context-menu", "name": "Context Menu", "category": "play",
        "tagline": "Right-click, and a menu appears where you are.",
        "what": "A custom context menu positions itself at the pointer, flips when it would overflow the viewport, and closes on outside click, scroll or Escape. Items can have shortcuts and dividers.",
        "why": "Context menus are the desktop convention users expect, and a custom one lets you offer the actions that actually matter in your app.",
        "surface": ["Canvas tool", "File manager", "Table"], "intensity": "subtle",
        "worksWith": ["dark-tech", "data-pro", "contemporary"], "stat": "context menu",
        "html": r"""
<div class="cm-stage">
  <p class="k">PLAY / CONTEXT MENU</p>
  <h2>Right-click<br><em>anywhere.</em></h2>
  <p class="sub">A custom menu that flips at the viewport edge. Try the bottom-right corner.</p>
  <div class="cm-menu" id="menu"><button>Cut <kbd>⌘X</kbd></button><button>Copy <kbd>⌘C</kbd></button><button>Paste <kbd>⌘V</kbd></button><hr><button>Duplicate <kbd>⌘D</kbd></button><button class="danger">Delete <kbd>⌫</kbd></button></div>
</div>
""",
        "css": r"""
.cm-stage{text-align:center}
.cm-stage h2 em{font-style:normal;color:#ff9f6e}
.cm-menu{position:fixed;min-width:190px;background:#10131b;border:1px solid #ffffff22;border-radius:10px;padding:5px;box-shadow:0 24px 60px #000b;opacity:0;transform:scale(.96);transform-origin:top left;pointer-events:none;transition:opacity .12s,transform .12s;z-index:60}
.cm-menu.on{opacity:1;transform:none;pointer-events:auto}
.cm-menu button{width:100%;display:flex;justify-content:space-between;align-items:center;background:none;border:0;color:#dfe5ee;padding:9px 10px;border-radius:6px;font:500 12px/1 ui-sans-serif,system-ui;cursor:pointer;text-align:left}
.cm-menu button:hover{background:#8fd8ff14;color:#fff}
.cm-menu .danger{color:#ff8f8f}.cm-menu .danger:hover{background:#ff8f8f18}
@media (max-height:520px){.cm-menu button{padding:6px 9px;font-size:11px}.cm-menu{min-width:170px}}
.cm-menu hr{border:0;border-top:1px solid #ffffff12;margin:4px 6px}
""",
        "code": r"""
const menu=document.getElementById('menu');function open(x,y){menu.style.left='0px';menu.style.top='0px';menu.classList.add('on');const r=menu.getBoundingClientRect();const nx=x+r.width>W?x-r.width-8:x,ny=y+r.height>H?y-r.height-8:y;menu.style.left=nx+'px';menu.style.top=ny+'px';stat('menu at '+Math.round(x)+','+Math.round(y));}
addEventListener('contextmenu',e=>{e.preventDefault();open(e.clientX,e.clientY);});
addEventListener('pointerdown',e=>{if(!menu.contains(e.target))menu.classList.remove('on');});
addEventListener('keydown',e=>{if(e.key==='Escape')menu.classList.remove('on');});
setTimeout(()=>open(W*.62,H*.58),1600);setTimeout(()=>menu.classList.remove('on'),3200);setTimeout(()=>open(W*.2,H*.3),4000);
function frame(dt){ctx.fillStyle='#07080c';ctx.fillRect(0,0,W,H);for(let i=0;i<26;i++){const x=(i*97)%W,y=(i*61)%H;ctx.strokeStyle='rgba(255,159,110,.08)';ctx.strokeRect(x,y,40,26);}stat('context menu');}
""",
        "snippet": "window.addEventListener('contextmenu', e => {\n  e.preventDefault();\n  menu.style.left = Math.min(e.clientX, innerWidth - menu.offsetWidth) + 'px';\n  menu.style.top = Math.min(e.clientY, innerHeight - menu.offsetHeight) + 'px';\n});",
        "prompt": "Build a custom context menu: right-click opens at pointer, flips before viewport edges, closes on outside click/Escape/scroll, with shortcuts and a destructive item. Single HTML file.",
    },
    {
        "id": "hover-preview", "name": "Hover Preview", "category": "play",
        "tagline": "A list where each row brings its own preview card.",
        "what": "Hovering a project row shows a floating preview with a generative thumbnail and meta, following the pointer with easing. On touch, tapping the row opens the same preview inline.",
        "why": "Hover previews let a dense index stay short while still giving each item a visual, and they are the backbone of editorial portfolios.",
        "surface": ["Portfolio", "Docs index", "Shop"], "intensity": "medium",
        "worksWith": ["luxe-brand", "cultural", "expressive"], "stat": "hover preview",
        "html": r"""
<div class="hp-stage">
  <p class="k">PLAY / HOVER PREVIEW</p>
  <h2>Index with<br><em>a memory.</em></h2>
  <ul class="hp-list" id="list">
    <li data-c="a"><b>01</b><span>Signal / Noise</span><em>Identity</em></li>
    <li data-c="b"><b>02</b><span>Slow Motion</span><em>Product film</em></li>
    <li data-c="c"><b>03</b><span>Field Notes</span><em>Editorial</em></li>
    <li data-c="d"><b>04</b><span>After Hours</span><em>Campaign</em></li>
  </ul>
  <div class="hp-prev" id="prev"><canvas id="pc" width="260" height="170"></canvas><div><b id="pt">Signal / Noise</b><span id="pm">Identity · 2026</span></div></div>
</div>
""",
        "css": r"""
.hp-stage{width:min(880px,94vw);display:grid;grid-template-columns:1fr;gap:18px}
.hp-stage h2 em{font-style:normal;color:#8fd8ff}
.hp-list{list-style:none;margin:0;padding:0;border-top:1px solid #ffffff14}
.hp-list li{display:grid;grid-template-columns:52px 1fr auto;gap:14px;align-items:center;padding:18px 6px;border-bottom:1px solid #ffffff14;cursor:pointer;transition:padding .2s,color .2s}
.hp-list li b{font:600 10px/1 ui-monospace,monospace;color:#5f6a7d}
.hp-list li span{font-size:clamp(18px,3vw,30px);letter-spacing:-.03em}
.hp-list li em{font:500 10px/1 ui-monospace,monospace;color:#7e8799;font-style:normal}
.hp-list li:hover{padding-left:16px;color:#fff}
.hp-prev{position:fixed;width:290px;background:#0d1018;border:1px solid #ffffff1f;border-radius:14px;padding:10px;box-shadow:0 30px 70px #000b;opacity:0;transform:translate(-50%,-50%) scale(.96);pointer-events:none;transition:opacity .18s,transform .18s;z-index:30}
.hp-prev.on{opacity:1;transform:translate(-50%,-50%) scale(1)}
.hp-prev canvas{width:100%;height:170px;border-radius:8px;display:block;background:#080a0e}
.hp-prev div{display:flex;justify-content:space-between;align-items:baseline;padding:10px 4px 4px}
@media (max-height:520px){.hp-list li{padding:10px 4px}.hp-prev{width:210px}.hp-prev canvas{height:110px}}
.hp-prev b{font-size:12px}.hp-prev span{font:500 9px/1 ui-monospace,monospace;color:#7e8799}
""",
        "code": r"""
const list=document.getElementById('list'),prev=document.getElementById('prev'),pc=document.getElementById('pc').getContext('2d'),pt=document.getElementById('pt'),pm=document.getElementById('pm');
const meta={a:['Signal / Noise','Identity · 2026'],b:['Slow Motion','Product film · 2025'],c:['Field Notes','Editorial · 2025'],d:['After Hours','Campaign · 2024']};let px=0,py=0,tx=0,ty=0,active=null,idleT=0;
list.addEventListener('pointermove',e=>{const li=e.target.closest('li');if(!li)return;tx=e.clientX;ty=e.clientY;prev.classList.add('on');const k=li.dataset.c;pt.textContent=meta[k][0];pm.textContent=meta[k][1];active=k;draw(k);});
list.addEventListener('pointerleave',()=>{prev.classList.remove('on');active=null;});
function draw(k){pc.clearRect(0,0,260,170);pc.fillStyle='#080a0e';pc.fillRect(0,0,260,170);for(let i=0;i<70;i++){const a=i*.7+performance.now()*.0002;pc.fillStyle='hsla('+(190+(k.charCodeAt(0)%5)*20+i)+',70%,60%,.55)';pc.beginPath();pc.arc(130+Math.cos(a)*i*1.6,85+Math.sin(a*1.3)*i*.9,1.6,0,7);pc.fill();}}
setInterval(()=>{if(active||!list.children.length)return;const li=list.children[idleT++%4];const r=li.getBoundingClientRect();tx=r.left+r.width*.6;ty=r.top+r.height/2;prev.classList.add('on');const k=li.dataset.c;pt.textContent=meta[k][0];pm.textContent=meta[k][1];draw(k);},2200);
function frame(dt){px+=(tx-px)*Math.min(1,dt*10);py+=(ty-py)*Math.min(1,dt*10);prev.style.left=px+'px';prev.style.top=py+'px';
 ctx.fillStyle='#07080c';ctx.fillRect(0,0,W,H);stat('hover preview');}
""",
        "snippet": "row.addEventListener('pointerenter', () => preview.classList.add('on'));\npreview.style.left = pointerX + 'px';\npreview.style.top = pointerY + 'px';",
        "prompt": "Build a hover-preview index: rows reveal a floating preview card that follows the pointer with easing, shows generative art + meta, and falls back to inline expansion on touch. Single HTML file.",
    },
]
