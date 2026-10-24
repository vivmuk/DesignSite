#!/usr/bin/env python3
"""Build batch three of the Interactive tab (50 more playgrounds).

Run:
    python3 scripts/v3_build.py --html-only
Then:
    node scripts/check_interactive.mjs
    node scripts/capture_thumbs.mjs
    python3 scripts/assemble_thumbs.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "interactive"
TS_FILE = ROOT / "src" / "data" / "interactiveAddonsExtra2.ts"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v3_shaders import COMMON as SHADER_COMMON, DEMOS as SHADER_DEMOS  # noqa: E402
try:
    from v3_ui import BASE_CSS as UI_BASE_CSS
except ImportError:
    UI_BASE_CSS = ''
try:
    from v3_scroll import BASE as SCROLL_BASE_CSS
except ImportError:
    SCROLL_BASE_CSS = ''

DEMOS = list(SHADER_DEMOS)
try:
    from v3_sims import DEMOS as SIM_DEMOS  # noqa: E402
    DEMOS += SIM_DEMOS
except ImportError:
    pass
try:
    from v3_physics import DEMOS as PHYS_DEMOS  # noqa: E402
    DEMOS += PHYS_DEMOS
except ImportError:
    pass
try:
    from v3_ui import DEMOS as UI_DEMOS  # noqa: E402
    DEMOS += UI_DEMOS
except ImportError:
    pass
try:
    from v3_scroll import DEMOS as SCROLL_DEMOS  # noqa: E402
    DEMOS += SCROLL_DEMOS
except ImportError:
    pass
try:
    from v3_data import DEMOS as DATA_DEMOS  # noqa: E402
    DEMOS += DATA_DEMOS
except ImportError:
    pass

CSS = r"""
*,*::before,*::after{box-sizing:border-box}
html,body{margin:0;min-height:100%;background:#07080c}
body{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;color:#eef1f7;overflow:hidden;-webkit-font-smoothing:antialiased}
canvas{display:block;position:fixed;inset:0;touch-action:none}
#cv{cursor:crosshair}
.hud{position:fixed;top:16px;left:16px;z-index:20;background:#0b0d13cc;border:1px solid #ffffff1c;border-radius:10px;padding:10px 13px;font:500 10px/1.6 ui-monospace,monospace;letter-spacing:.1em;color:#939caf;backdrop-filter:blur(8px)}
.hud b{color:#8fd8ff;font-weight:600}
.hud .t{display:block;color:#eef1f7;font-size:11px;letter-spacing:.16em;margin-bottom:3px}
.hint{position:fixed;left:16px;bottom:14px;margin:0;z-index:20;font:500 10px/1 ui-monospace,monospace;letter-spacing:.14em;color:#7e8799;text-transform:uppercase}
.pause{position:fixed;right:16px;bottom:12px;z-index:20;background:#0b0d13cc;border:1px solid #ffffff22;color:#cfd6e2;border-radius:999px;padding:8px 12px;font:600 10px/1 ui-monospace,monospace;letter-spacing:.1em;cursor:pointer}
.pause:focus-visible{outline:2px solid #8fd8ff;outline-offset:2px}
"""

CANVAS_HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="__TAGLINE__">
<title>__NAME__ — Interactive</title>
<style>__CSS__</style></head>
<body data-canvas="1">
<canvas id="cv" aria-label="__NAME__ interactive canvas"></canvas>
__UI__
<div class="hud"><span class="t">__KICKER__ · __NAME__</span><b id="stat">ready</b> · <b id="fps">60</b> fps</div>
<p class="hint">__HINT__</p>
<button class="pause" id="pause" type="button" aria-pressed="false">PAUSE</button>
<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W=0,H=0,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=Math.floor(W*DPR);cv.height=Math.floor(H*DPR);cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
fit();addEventListener('resize',fit);
const mx={x:W/2,y:H/2,down:false};
addEventListener('pointermove',e=>{mx.x=e.clientX;mx.y=e.clientY;},{passive:true});
addEventListener('pointerdown',e=>{mx.down=true;mx.x=e.clientX;mx.y=e.clientY;});
addEventListener('pointerup',()=>mx.down=false);
addEventListener('pointerleave',()=>{mx.x=W/2;mx.y=H/2;});
const rnd=(a=1,b=0)=>b+Math.random()*(a-b);
const statEl=document.getElementById('stat'),fpsEl=document.getElementById('fps');
let statText='__STAT__';const stat=v=>{statText=v};
let t=0,paused=false,last=performance.now(),acc=0,frames=0;
const pauseBtn=document.getElementById('pause');
function setPaused(v){paused=v;pauseBtn.textContent=paused?'PLAY':'PAUSE';pauseBtn.setAttribute('aria-pressed',String(paused));}
pauseBtn.addEventListener('click',()=>setPaused(!paused));
addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();setPaused(!paused);}});
__CODE__
function loop(now){const dt=Math.min(.05,(now-last)/1000);last=now;
 if(!paused){t+=dt;frame(dt);}
 acc+=dt;frames++;if(acc>.5){statEl.textContent=statText;fpsEl.textContent=Math.round(frames/acc);frames=0;acc=0;}
 requestAnimationFrame(loop);}
if(matchMedia('(prefers-reduced-motion: reduce)').matches){frame(0);statEl.textContent=statText;setPaused(true);}
requestAnimationFrame(loop);
</script></body></html>
"""

WEBGL_HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="__TAGLINE__">
<title>__NAME__ — Interactive</title>
<style>__CSS__</style></head>
<body data-canvas="1">
<canvas id="cv" aria-label="__NAME__ interactive canvas"></canvas>
<div class="hud"><span class="t">__KICKER__ · __NAME__</span><b id="stat">ready</b> · <b id="fps">60</b> fps</div>
<p class="hint">MOVE THE CURSOR · SPACE TO PAUSE</p>
<button class="pause" id="pause" type="button" aria-pressed="false">PAUSE</button>
<script>
const cv=document.getElementById('cv');
let W=0,H=0,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=Math.floor(W*DPR);cv.height=Math.floor(H*DPR);cv.style.width=W+'px';cv.style.height=H+'px';}
fit();addEventListener('resize',fit);
const mx={x:W/2,y:H/2,down:false};
addEventListener('pointermove',e=>{mx.x=e.clientX;mx.y=e.clientY;},{passive:true});
addEventListener('pointerdown',e=>{mx.down=true;mx.x=e.clientX;mx.y=e.clientY;});
addEventListener('pointerup',()=>mx.down=false);
addEventListener('pointerleave',()=>{mx.x=W/2;mx.y=H/2;});
const gl=cv.getContext('webgl',{antialias:true,alpha:false,preserveDrawingBuffer:true});
const statEl=document.getElementById('stat'),fpsEl=document.getElementById('fps');
let statText='__STAT__';const stat=v=>{statText=v};
let t=0,paused=false,last=performance.now(),acc=0,frames=0;
const pauseBtn=document.getElementById('pause');
function setPaused(v){paused=v;pauseBtn.textContent=paused?'PLAY':'PAUSE';pauseBtn.setAttribute('aria-pressed',String(paused));}
pauseBtn.addEventListener('click',()=>setPaused(!paused));
addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();setPaused(!paused);}});
function sh(type,src){const s=gl.createShader(type);gl.shaderSource(s,src);gl.compileShader(s);
 if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)){console.error(gl.getShaderInfoLog(s));return null;}return s;}
const vs=sh(gl.VERTEX_SHADER,'attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}');
const fs=sh(gl.FRAGMENT_SHADER,__FS__);
let prog=null;
if(gl&&vs&&fs){prog=gl.createProgram();gl.attachShader(prog,vs);gl.attachShader(prog,fs);gl.linkProgram(prog);
 if(!gl.getProgramParameter(prog,gl.LINK_STATUS)){console.error(gl.getProgramInfoLog(prog));prog=null;}}
if(gl&&prog){gl.useProgram(prog);const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);
 gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
 const a=gl.getAttribLocation(prog,'a');gl.enableVertexAttribArray(a);gl.vertexAttribPointer(a,2,gl.FLOAT,false,0,0);}
const uRes=prog&&gl.getUniformLocation(prog,'u_res'),uT=prog&&gl.getUniformLocation(prog,'u_t'),uM=prog&&gl.getUniformLocation(prog,'u_m');
function frame(){
 if(!gl||!prog){stat('WebGL unavailable');return;}
 gl.viewport(0,0,cv.width,cv.height);
 gl.uniform2f(uRes,cv.width,cv.height);
 gl.uniform1f(uT,t);
 gl.uniform2f(uM,mx.x/W,1-mx.y/H);
 gl.drawArrays(gl.TRIANGLES,0,3);
 stat('__STAT__');
}
function loop(now){const dt=Math.min(.05,(now-last)/1000);last=now;
 if(!paused){t+=dt;frame();}
 acc+=dt;frames++;if(acc>.5){statEl.textContent=statText;fpsEl.textContent=Math.round(frames/acc);frames=0;acc=0;}
 requestAnimationFrame(loop);}
frame();requestAnimationFrame(loop);
</script></body></html>
"""

PAGE_HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="__TAGLINE__">
<title>__NAME__ — Interactive</title>
<style>__CSS____PAGE_CSS__</style></head>
<body data-canvas="0" data-scroll="__SCROLL__">
<canvas id="cv" aria-hidden="true"></canvas>
__UI__
<div class="hud"><span class="t">__KICKER__ · __NAME__</span><b id="stat">ready</b></div>
<p class="hint">__HINT__</p>
<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W=0,H=0,DPR=Math.min(devicePixelRatio||1,2);
function fit(){W=innerWidth;H=innerHeight;cv.width=Math.floor(W*DPR);cv.height=Math.floor(H*DPR);cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
fit();addEventListener('resize',fit);
const mx={x:W/2,y:H/2,down:false};
addEventListener('pointermove',e=>{mx.x=e.clientX;mx.y=e.clientY;},{passive:true});
addEventListener('pointerdown',e=>{mx.down=true;});
addEventListener('pointerup',()=>{mx.down=false;});
const rnd=(a=1,b=0)=>b+Math.random()*(a-b);
const statEl=document.getElementById('stat');
let statText='__STAT__';const stat=v=>{statText=v};
const ui=document.getElementById('ui');
__CODE__
function loop(now){const dt=Math.min(.05,(now-last)/1000);last=now;if(!window.__paused){t+=dt;frame(dt);}
 statEl.textContent=statText;requestAnimationFrame(loop);}
let t=0,last=performance.now();window.__paused=false;
frame(0);requestAnimationFrame(loop);
</script></body></html>
"""


def kicker(cat: str) -> str:
    return {
        "generative": "GENERATIVE", "pointer": "POINTER", "spatial": "3D / DEPTH",
        "typefx": "TYPE / IMAGE", "play": "PLAY / REVEAL",
    }[cat]


def build_html(demo):
    did = demo["id"]
    name = demo["name"]
    cat = demo["category"]
    base = {"__NAME__": name, "__TAGLINE__": demo["tagline"], "__KICKER__": kicker(cat),
            "__STAT__": demo.get("stat", ""), "__HINT__": demo.get("hint", "MOVE · DRAG · SPACE TO PAUSE"),
            "__CSS__": CSS}
    if demo.get("fs"):
        fs = SHADER_COMMON + demo["fs"]
        html = WEBGL_HTML
        for k, v in base.items():
            html = html.replace(k, v)
        return html.replace("__FS__", json.dumps(fs))
    if demo.get("kind") == "page" or demo.get("html"):
        html = PAGE_HTML
        for k, v in base.items():
            html = html.replace(k, v)
        html = html.replace("__PAGE_CSS__", UI_BASE_CSS + SCROLL_BASE_CSS + demo.get("page_css", "") + demo.get("css", ""))
        html = html.replace("__UI__", "<div id=\"ui\">" + demo.get("html", "") + "</div>")
        html = html.replace("__CODE__", demo["code"])
        html = html.replace("__SCROLL__", "1" if demo.get("scroll") else "0")
        return html
    html = CANVAS_HTML
    for k, v in base.items():
        html = html.replace(k, v)
    return html.replace("__CODE__", demo["code"]).replace("__UI__", demo.get("html", ""))


def ts_entries():
    rows = []
    for i, d in enumerate(DEMOS, start=76):
        rows.append({
            "n": i, "id": d["id"], "name": d["name"], "category": d["category"],
            "group": "interactive", "tagline": d["tagline"], "what": d["what"],
            "why": d["why"], "surface": d["surface"], "intensity": d["intensity"],
            "worksWith": d["worksWith"], "snippet": d["snippet"], "prompt": d["prompt"],
            "demo": f"/interactive/{d['id']}.html",
            "thumb": f"/interactive/thumbs/{d['id']}.gif",
        })
    body = ",\n".join("  " + json.dumps(r, ensure_ascii=False) for r in rows)
    return ("/**\n * Interactive elements — batch three (76–125).\n *\n * WebGL shaders, simulations, physics, UI patterns, scroll scenes,\n * data viz, SVG and audio. Generated by scripts/v3_build.py.\n */\n"
            "import type { VisualAddon } from './visualAddons';\n\n"
            "export const interactiveAddonsExtra2: VisualAddon[] = [\n" + body + ",\n];\n")


def main():
    html_only = "--html-only" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    for demo in DEMOS:
        (OUT / f"{demo['id']}.html").write_text(build_html(demo))
        print("wrote", demo["id"])
    TS_FILE.write_text(ts_entries())
    print(f"{len(DEMOS)} demos")


if __name__ == "__main__":
    main()
