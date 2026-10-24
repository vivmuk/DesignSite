"""Batch three — raw WebGL fragment-shader playgrounds (10 demos)."""

COMMON = r"""
precision highp float;
uniform vec2 u_res;
uniform float u_t;
uniform vec2 u_m;
#define PI 3.14159265
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float vnoise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
  return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);}
float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*vnoise(p);p*=2.02;a*=.5;}return v;}
vec3 pal(float t){return .5+.5*cos(6.28318*(vec3(.0,.33,.67)+t));}
mat2 rot(float a){return mat2(cos(a),-sin(a),sin(a),cos(a));}
float sdSphere(vec3 p,float r){return length(p)-r;}
"""

DEMOS = [
    {
        "id": "plasma-field", "name": "Plasma Field", "category": "generative",
        "tagline": "A full-screen plasma that bends toward the pointer.",
        "what": "A fragment shader sums four sine fields plus a radial wave centred on the pointer, then maps the result through a cosine palette. Every pixel is evaluated on the GPU.",
        "why": "Plasma is the canonical fragment-shader hello-world: four sines, one palette, and an image that never repeats.",
        "surface": ["Hero", "Music visual", "Event page"], "intensity": "bold",
        "worksWith": ["dark-tech", "expressive", "cultural"],
        "fs": r"""
void main(){
  vec2 uv=(gl_FragCoord.xy-.5*u_res)/u_res.y;
  vec2 m=(u_m-.5)*vec2(u_res.x/u_res.y,1.);
  float v=sin(uv.x*7.+u_t*.9)+sin(uv.y*8.-u_t*1.1)+sin((uv.x+uv.y)*6.+u_t*.6)
    +sin(length(uv-m)*13.-u_t*2.2)+sin(length(uv+m*.7)*9.+u_t*1.4);
  float k=v*.11+u_t*.03;
  vec3 c=pal(k)*.55+.28;
  c*=.65+.35*sin(v*2.6);
  gl_FragColor=vec4(c,1.);
}""",
        "snippet": "float v = sin(uv.x*7. + t) + sin(uv.y*8. - t) + sin(length(uv-m)*13. - t*2.);\ngl_FragColor = vec4(pal(v * .11), 1.);",
        "prompt": "Build a full-screen plasma fragment shader: sum four sine fields, one radial wave from the pointer, map through a cosine palette. Single HTML file, raw WebGL, no libraries.",
    },
    {
        "id": "mandelbrot-zoom", "name": "Mandelbrot Zoom", "category": "generative",
        "tagline": "An infinite fractal you can steer with the cursor.",
        "what": "Each pixel runs the Mandelbrot iteration to a bounded escape count. The pointer sets the centre and the horizontal position sets the zoom, so the set keeps resolving new detail.",
        "why": "The Mandelbrot set is the clearest demonstration that a tiny loop can hold unbounded detail.",
        "surface": ["Hero", "Data-art print", "Title sequence"], "intensity": "bold",
        "worksWith": ["dark-tech", "expressive", "luxe-brand"],
        "fs": r"""
void main(){
  vec2 uv=(gl_FragCoord.xy-.5*u_res)/u_res.y;
  vec2 m=(u_m-.5)*2.4;
  float zoom=mix(.55,3.2,u_m.x);
  vec2 c=vec2(-.745+u_m.x*.9,.113+u_m.y*.5)+uv*zoom*.55;
  vec2 z=vec2(0.);
  float it=0.;
  for(int i=0;i<120;i++){
    z=vec2(z.x*z.x-z.y*z.y,2.*z.x*z.y)+c;
    if(dot(z,z)>16.){break;}
    it+=1.;
  }
  float f=it/120.;
  vec3 col=pal(f*.9+u_t*.02);
  col*=smoothstep(0.,.08,f);
  col=mix(vec3(.02,.02,.04),col,pow(f,.55));
  gl_FragColor=vec4(col,1.);
}""",
        "snippet": "for (int i = 0; i < 120; i++) {\n  z = vec2(z.x*z.x - z.y*z.y, 2.*z.x*z.y) + c;\n  if (dot(z,z) > 16.) break;\n  it += 1.;\n}",
        "prompt": "Build an interactive Mandelbrot zoom in raw WebGL. Pointer sets the centre, horizontal position sets zoom, escape count drives a smooth palette. Single HTML file.",
    },
    {
        "id": "julia-drift", "name": "Julia Drift", "category": "generative",
        "tagline": "A Julia set whose constant follows your hand.",
        "what": "The pointer picks the complex constant c; the shader iterates z² + c per pixel. Small movements reshape the whole set continuously.",
        "why": "Julia sets show how a single complex parameter controls an entire family of forms.",
        "surface": ["Hero", "Album art", "Splash"], "intensity": "bold",
        "worksWith": ["dark-tech", "immersive-3d", "expressive"],
        "fs": r"""
void main(){
  vec2 uv=(gl_FragCoord.xy-.5*u_res)/u_res.y*1.6;
  vec2 c=(u_m-.5)*1.8+vec2(-.12+sin(u_t*.13)*.28,.74+cos(u_t*.17)*.12);
  vec2 z=uv;
  float it=0.;
  for(int i=0;i<90;i++){
    z=vec2(z.x*z.x-z.y*z.y,2.*z.x*z.y)+c;
    if(dot(z,z)>9.){break;}
    it+=1.;
  }
  float f=it/90.;
  vec3 col=pal(.05+f*.9+u_t*.03);
  col=mix(vec3(.03,.02,.06),col,smoothstep(0.,.35,f));
  col+=pow(f,2.)*vec3(.6,.3,.9);
  gl_FragColor=vec4(col,1.);
}""",
        "snippet": "vec2 c = pointer * 1.8 + vec2(-.12, .74);\nfor (int i = 0; i < 90; i++) z = vec2(z.x*z.x-z.y*z.y, 2.*z.x*z.y) + c;",
        "prompt": "Build a Julia-set shader whose constant follows the pointer, with an escape-time palette. Raw WebGL, single HTML file, no libraries.",
    },
    {
        "id": "raymarch-spheres", "name": "Raymarched Spheres", "category": "spatial",
        "tagline": "Lit spheres you can orbit by moving the cursor.",
        "what": "A signed-distance scene of five moving spheres is sphere-traced per pixel. Normals are estimated from the distance field and lit with a single key light.",
        "why": "Raymarching is how shaders make solid form without meshes: distance fields in, lighting out.",
        "surface": ["Hero", "AI product", "Splash"], "intensity": "bold",
        "worksWith": ["dark-tech", "immersive-3d", "contemporary"],
        "fs": r"""
float map(vec3 p){
  float d=1e9;
  for(int i=0;i<5;i++){
    float fi=float(i);
    vec3 q=p-vec3(sin(u_t*.5+fi*1.7)*1.1,cos(u_t*.4+fi)*.55,sin(u_t*.3+fi*2.1)*.5);
    d=min(d,sdSphere(q,.28+fi*.05));
  }
  d=min(d,p.y+.9);
  return d;
}
vec3 nrm(vec3 p){vec2 e=vec2(.001,0.);return normalize(vec3(map(p+e.xyy)-map(p-e.xyy),map(p+e.yxy)-map(p-e.yxy),map(p+e.yyx)-map(p-e.yyx)));}
void main(){
  vec2 uv=(gl_FragCoord.xy-.5*u_res)/u_res.y;
  vec3 ro=vec3(0.,0.,3.2),rd=normalize(vec3(uv,-1.6));
  float d=0.;
  for(int i=0;i<72;i++){float h=map(ro+rd*d);if(h<.001||d>8.)break;d+=h;}
  vec3 p=ro+rd*d;
  vec3 n=nrm(p);
  float dif=max(dot(n,normalize(vec3(.6,.8,.4))),0.);
  float rim=pow(1.-max(dot(n,-rd),0.),2.5);
  vec3 col=pal(.55+sin(u_t*.1)*.1)*dif*.8+vec3(.1,.2,.3)*rim;
  col+=vec3(.9,.4,.15)*pow(max(dot(reflect(-rd,n),normalize(vec3(-.4,.6,.5))),0.),24.)*.6;
  vec3 bg=mix(vec3(.02,.03,.06),vec3(.06,.08,.14),uv.y+.5);
  col=mix(bg,col,smoothstep(8.,7.2,d));
  gl_FragColor=vec4(col,1.);
}""",
        "snippet": "for (int i = 0; i < 72; i++) { float h = map(ro + rd*d); if (h < .001) break; d += h; }\nvec3 n = normalFromDistance(p);",
        "prompt": "Build a raymarched scene of five moving spheres with SDF normals and a key light. Raw WebGL fragment shader, single HTML file, no libraries.",
    },
    {
        "id": "raymarch-tunnel", "name": "Raymarched Tunnel", "category": "spatial",
        "tagline": "A tube of light that curves toward the pointer.",
        "what": "The camera flies down a signed-distance tunnel whose axis bends with the pointer. Stripes come from a polar angle term, and distance fades to fog.",
        "why": "A tunnel is the simplest raymarch that reads as travel: one distance function, one camera, endless depth.",
        "surface": ["Game page", "Launch", "Music visual"], "intensity": "bold",
        "worksWith": ["immersive-3d", "dark-tech", "expressive"],
        "fs": r"""
float map(vec3 p){
  vec2 c=vec2(sin(p.z*.25+u_m.x*2.)*.9,cos(p.z*.2+u_m.y*2.)*.7);
  return 1.05-length(p.xy-c);
}
void main(){
  vec2 uv=(gl_FragCoord.xy-.5*u_res)/u_res.y;
  vec3 ro=vec3(0.,0.,u_t*1.6);
  vec3 rd=normalize(vec3(uv,-1.4));
  float d=0.;
  for(int i=0;i<80;i++){float h=map(ro+rd*d);if(h<.002||d>14.)break;d+=h;}
  vec3 p=ro+rd*d;
  float ang=atan(p.y-sin(p.z*.25+u_m.x*2.)*.9,p.x-cos(p.z*.2+u_m.y*2.)*.7);
  float band=.5+.5*sin(ang*8.+p.z*2.4+u_t*4.);
  vec3 col=pal(band*.25+p.z*.03+u_t*.02);
  col*=.35+.65*band;
  col=mix(vec3(.01,.012,.02),col,smoothstep(14.,9.,d));
  gl_FragColor=vec4(col,1.);
}""",
        "snippet": "vec3 ro = vec3(0., 0., t*1.6);\nvec3 rd = normalize(vec3(uv, -1.4));\n// march map(ro + rd*d), shade by tunnel angle",
        "prompt": "Build a raymarched tunnel with a bending axis, polar stripe shading and distance fog. Raw WebGL, single HTML file.",
    },
    {
        "id": "crt-signal", "name": "CRT Signal", "category": "typefx",
        "tagline": "A lost broadcast, curvature, scanlines and all.",
        "what": "A procedural test pattern is bent through a barrel distortion, split into RGB with a scanline offset, then dusted with noise and a vignette.",
        "why": "CRT is a complete visual language in five lines: curvature, scanlines, RGB shift, noise, vignette.",
        "surface": ["Music release", "Game page", "Event"], "intensity": "bold",
        "worksWith": ["dark-tech", "expressive", "cultural"],
        "fs": r"""
void main(){
  vec2 uv=(gl_FragCoord.xy-.5*u_res)/u_res.y;
  vec2 p=uv*(1.+dot(uv,uv)*.22);
  vec3 col=vec3(0.);
  for(int i=0;i<3;i++){
    vec2 q=p+vec2(float(i-1)*.004,0.);
    float bars=.5+.5*sin(q.x*34.+u_t*2.);
    float ring=smoothstep(.02,0.,abs(length(q)-.55));
    float grid=step(.96,fract(q.y*46.+u_t*.4));
    col[i]=bars*.35+ring*.6+grid*.2;
  }
  col*=vec3(.9,1.,1.05);
  col+=hash(gl_FragCoord.xy+u_t)*.12;
  col*=1.-.45*dot(uv,uv);
  col*=step(.0,fract(gl_FragCoord.y*.5));
  gl_FragColor=vec4(col,1.);
}""",
        "snippet": "vec2 p = uv * (1. + dot(uv,uv)*.22);\nfloat scan = step(.0, fract(gl_FragCoord.y*.5));\ncol += hash(gl_FragCoord.xy + t) * .12;",
        "prompt": "Build a CRT broadcast shader: barrel distortion, RGB split, scanlines, noise, vignette, procedural test pattern. Raw WebGL, single HTML file.",
    },
    {
        "id": "chromatic-shift", "name": "Chromatic Shift", "category": "typefx",
        "tagline": "RGB channels pulled apart by the pointer.",
        "what": "A procedural pattern is sampled three times with channel offsets driven by pointer distance, producing fringing that grows as you move away from centre.",
        "why": "Chromatic aberration is the cheapest way to make a flat surface feel like a lens.",
        "surface": ["Editorial", "Music", "Product detail"], "intensity": "medium",
        "worksWith": ["dark-tech", "expressive", "luxe-brand"],
        "fs": r"""
float pattern(vec2 p){
  float grid=1.-smoothstep(.0,.035,min(abs(fract(p.x*7.)-.5),abs(fract(p.y*7.)-.5)));
  float ring=1.-smoothstep(.0,.03,abs(length(p)-.62));
  float blob=1.-smoothstep(.1,.12,length(p-vec2(.25,.12)));
  return max(grid,max(ring,blob));
}
void main(){
  vec2 uv=(gl_FragCoord.xy-.5*u_res)/u_res.y;
  vec2 d=(u_m-.5)*.09;
  float r=pattern(uv+d);
  float g=pattern(uv);
  float b=pattern(uv-d);
  vec3 col=vec3(r,g,b);
  col=pal(dot(col,vec3(.33))*.9+u_t*.02);
  col+=vec3(.06,.02,.1);
  gl_FragColor=vec4(col,1.);
}""",
        "snippet": "float r = pattern(uv + d), g = pattern(uv), b = pattern(uv - d);\ngl_FragColor = vec4(r, g, b, 1.);",
        "prompt": "Build a chromatic-aberration shader where pointer distance sets the RGB channel offset over a procedural pattern. Raw WebGL, single HTML file.",
    },
    {
        "id": "fbm-displacement", "name": "FBM Displacement", "category": "generative",
        "tagline": "Domain-warped noise that folds like weather.",
        "what": "Two fbm layers warp the sampling coordinates, then a third layer colours the result. Pointer movement changes the warp origin, so the field folds around you.",
        "why": "Domain warping turns boring noise into geology, smoke and weather with almost no extra code.",
        "surface": ["Hero", "Immersive page", "Report cover"], "intensity": "medium",
        "worksWith": ["dark-tech", "cultural", "luxe-brand"],
        "fs": r"""
void main(){
  vec2 uv=(gl_FragCoord.xy-.5*u_res)/u_res.y;
  vec2 q=vec2(fbm(uv*2.2+u_t*.05),fbm(uv*2.2+vec2(3.1,1.7)-u_t*.04));
  vec2 r=vec2(fbm(uv*2.4+q*2.6+u_m*.8),fbm(uv*2.4+q*2.6+u_m*.8+vec2(4.2,2.8)));
  float f=fbm(uv*2.8+r*3.2);
  vec3 col=pal(f*.55+r.x*.2+u_t*.02);
  col=mix(vec3(.02,.03,.05),col,smoothstep(.1,.9,f));
  col*= .45+.55*smoothstep(.0,.8,r.y);
  vec2 g=uv*9.+r*4.;
  float lines=1.-smoothstep(.0,.06,min(abs(fract(g.x)-.5),abs(fract(g.y)-.5)));
  col+=lines*.28*vec3(.5,.8,1.);
  gl_FragColor=vec4(col,1.);
}""",
        "snippet": "vec2 q = vec2(fbm(uv*2.2), fbm(uv*2.2 + 3.1));\nvec2 r = vec2(fbm(uv*2.4 + q*2.6), fbm(uv*2.4 + q*2.6 + 4.2));\nfloat f = fbm(uv*2.8 + r*3.2);",
        "prompt": "Build a domain-warped fbm shader with two warp layers and a palette mapped from the final field. Raw WebGL, single HTML file.",
    },
    {
        "id": "liquid-metal", "name": "Liquid Metal", "category": "spatial",
        "tagline": "A mercury blob that chases the cursor.",
        "what": "Three moving metaballs are merged with a smooth-min, then shaded with a fake environment reflection and a tight highlight. The pointer is one of the balls.",
        "why": "Smooth-min plus environment shading is the whole recipe for liquid metal.",
        "surface": ["Product launch", "AI hero", "Splash"], "intensity": "bold",
        "worksWith": ["dark-tech", "immersive-3d", "luxe-brand"],
        "fs": r"""
float smin(float a,float b,float k){float h=clamp(.5+.5*(b-a)/k,0.,1.);return mix(b,a,h)-k*h*(1.-h);}
float map(vec3 p){
  float d=sdSphere(p-vec3(0.,0.,0.),.75);
  for(int i=0;i<3;i++){
    float fi=float(i);
    vec3 q=vec3(sin(u_t*.6+fi*2.1)*.7,cos(u_t*.5+fi*1.3)*.5,sin(u_t*.3+fi)*.3);
    d=smin(d,sdSphere(p-q,.36),.55);
  }
  vec3 m=vec3((u_m.x-.5)*2.,(u_m.y-.5)*1.4,.55);
  d=smin(d,sdSphere(p-m,.28),.5);
  return d;
}
vec3 nrm(vec3 p){vec2 e=vec2(.001,0.);return normalize(vec3(map(p+e.xyy)-map(p-e.xyy),map(p+e.yxy)-map(p-e.yxy),map(p+e.yyx)-map(p-e.yyx)));}
void main(){
  vec2 uv=(gl_FragCoord.xy-.5*u_res)/u_res.y;
  vec3 ro=vec3(0.,0.,3.),rd=normalize(vec3(uv,-1.7));
  float d=0.;
  for(int i=0;i<80;i++){float h=map(ro+rd*d);if(h<.001||d>8.)break;d+=h;}
  vec3 p=ro+rd*d,n=nrm(p);
  vec3 r=reflect(rd,n);
  float env=smoothstep(-.1,1.,r.y)*.5+.5*fbm(r.xz*3.+u_t*.1);
  vec3 col=mix(vec3(.08,.1,.16),vec3(.85,.9,1.),env);
  col+=pow(max(dot(r,normalize(vec3(.4,.8,.3))),0.),40.)*1.2;
  col*= .75+.25*max(dot(n,normalize(vec3(-.4,.6,.7))),0.);
  vec3 bg=vec3(.02,.025,.04);
  col=mix(bg,col,smoothstep(8.,7.,d));
  gl_FragColor=vec4(col,1.);
}""",
        "snippet": "d = smin(d, sdSphere(p - ball, .36), .55);\nvec3 r = reflect(rd, normal);\ncol = mix(dark, envColor(r), fresnel);",
        "prompt": "Build a liquid-metal raymarch: three moving metaballs plus the pointer merged with smooth-min, fake environment reflections and a tight specular. Raw WebGL.",
    },
    {
        "id": "truchet-weave", "name": "Truchet Weave", "category": "generative",
        "tagline": "A tile grid that rewires itself in colour.",
        "what": "Each grid cell picks one of two arc orientations from a hash, offset by a slow animation. The pointer changes the cell scale and adds a glow at its position.",
        "why": "Truchet tiles make endless, always-valid pattern from a single either/or decision per cell.",
        "surface": ["Editorial", "Brand pattern", "Hero"], "intensity": "subtle",
        "worksWith": ["classic", "cultural", "contemporary"],
        "fs": r"""
void main(){
  vec2 uv=(gl_FragCoord.xy-.5*u_res)/u_res.y;
  float scale=mix(7.,12.,u_m.x);
  vec2 p=uv*scale;
  vec2 id=floor(p),g=fract(p)-.5;
  float h=hash(id+floor(u_t*.3+hash(id)*4.));
  vec2 q=h>.5?g:g.yx;
  float arc=abs(length(q)-.5);
  float line=1.-smoothstep(.015,.035,arc);
  float ring=1.-smoothstep(.0,.02,abs(length(uv-(u_m-.5)*vec2(u_res.x/u_res.y,1.))-.28));
  vec3 col=mix(vec3(.02,.03,.05),pal(h*.6+u_t*.02),line);
  col+=ring*.35;
  col*=.5+.5*smoothstep(.6,.0,length(g));
  gl_FragColor=vec4(col,1.);
}""",
        "snippet": "vec2 id = floor(p), g = fract(p)-.5;\nfloat h = hash(id);\nvec2 q = h > .5 ? g : g.yx;\nfloat arc = abs(length(q)-.5);",
        "prompt": "Build a Truchet-tile shader: hash each cell to one of two arc orientations, draw the arcs with anti-aliasing, add a pointer glow. Raw WebGL.",
    },
]
