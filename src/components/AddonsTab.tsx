import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import './AddonsTab.css';
import {
  visualAddons, addonCategories,
  type AddonCategory, type VisualAddon, type AddonGroup,
} from '../data/visualAddons';
import { ShareLink } from './ShareLink';
import { interactiveAddons, interactiveCategories } from '../data/interactiveAddons';
import { interactiveAddonsExtra } from '../data/interactiveAddonsExtra';
import { interactiveAddonsExtra2 } from '../data/interactiveAddonsExtra2';

/** The Interactive tab grew from 25 to 125 playgrounds; the original 25 keep
 *  their order and the batch of 50 appends after them. */
const allInteractive = [...interactiveAddons, ...interactiveAddonsExtra, ...interactiveAddonsExtra2];

const INTENSITY_DOTS: Record<VisualAddon['intensity'], number> = { subtle: 1, medium: 2, bold: 3 };

const STYLE_LABEL: Record<string, string> = {
  classic: 'Classic', contemporary: 'Contemporary', 'dark-tech': 'Dark Tech',
  'immersive-3d': 'Immersive 3D', scrollcraft: 'Scrollcraft', expressive: 'Expressive',
  'luxe-brand': 'Luxe Brand', 'data-pro': 'Data Pro', cultural: 'Cultural',
  'component-kit': 'Component Kit',
};
const styleLabel = (s: string) => STYLE_LABEL[s] || s;

function copyText(text: string): Promise<boolean> {
  return navigator.clipboard.writeText(text).then(
    () => true,
    () => {
      try {
        const ta = document.createElement('textarea');
        ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        const ok = document.execCommand('copy');
        document.body.removeChild(ta);
        return ok;
      } catch { return false; }
    },
  );
}

function parseHash(base: string): { id: string | null; cat: AddonCategory | 'all'; q: string } {
  const h = window.location.hash;
  const usp = new URLSearchParams(h.split('?')[1] || '');
  const cat = (usp.get('cat') || 'all') as AddonCategory | 'all';
  const q = usp.get('q') || '';
  const prefix = base + '/';
  if (h.startsWith(prefix)) {
    return { id: decodeURIComponent(h.slice(prefix.length).split('?')[0].split('/')[0]), cat, q };
  }
  return { id: null, cat, q };
}

/** Renders a demo at a real 960×800 desktop viewport, scaled to the card.
 *  This keeps the preview honest: the piece is designed for desktop, and a
 *  300px-wide iframe would silently switch every demo into its mobile layout. */
function ScaledPreview({ src, title }: { src: string; title: string }) {
  const wrap = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(0.34);
  useEffect(() => {
    const el = wrap.current;
    if (!el) return;
    const measure = () => setScale(Math.max(.2, el.clientWidth / 960));
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return (
    <div className="av-thumb" ref={wrap} style={{ height: Math.round(800 * scale) }}>
      <iframe
        src={src}
        title={title}
        className="av-thumb-frame"
        style={{ width: 960, height: 800, transform: `scale(${scale})` }}
        sandbox="allow-scripts allow-same-origin"
        loading="lazy"
        tabIndex={-1}
      />
    </div>
  );
}

function CountUp({ value }: { value: string }) {
  const target = Number(value);
  const [shown, setShown] = useState<number | string>(Number.isFinite(target) ? 0 : value);

  useEffect(() => {
    if (!Number.isFinite(target)) { setShown(value); return; }
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { setShown(target); return; }
    let raf = 0;
    const started = performance.now();
    const tick = (now: number) => {
      const p = Math.min(1, (now - started) / 950);
      setShown(Math.round(target * (1 - Math.pow(1 - p, 3))));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, value]);

  return <>{shown}</>;
}

/** A quiet field of family-coloured points that leans toward the pointer.
 *  It is the one moving thing in the hero — deliberately cheap (no library). */
function HeroField() {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = ref.current;
    const ctx = canvas?.getContext('2d');
    if (!canvas || !ctx) return;
    const colours = ['#ff8a5c', '#7fb2ff', '#c084fc', '#3ddc84', '#ffd166'];
    const pointer = { x: -9999, y: -9999 };
    let hasPointer = false;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let width = 0;
    let height = 0;
    let raf = 0;

    const resize = () => {
      const box = canvas.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = box.width;
      height = box.height;
      canvas.width = Math.max(1, Math.round(width * dpr));
      canvas.height = Math.max(1, Math.round(height * dpr));
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    const move = (e: PointerEvent) => {
      const box = canvas.getBoundingClientRect();
      hasPointer = true;
      pointer.x = e.clientX - box.left;
      pointer.y = e.clientY - box.top;
    };

    const draw = (now: number) => {
      ctx.clearRect(0, 0, width, height);
      const phase = reduce ? 0 : now;
      const target = hasPointer
        ? pointer
        : {
            x: width * (0.5 + Math.sin(phase * 0.00055) * 0.28),
            y: height * (0.5 + Math.cos(phase * 0.00042) * 0.22),
          };

      // Five slow ribbons — motion even before the pointer arrives.
      ctx.globalCompositeOperation = 'lighter';
      for (let band = 0; band < colours.length; band++) {
        ctx.beginPath();
        for (let x = 0; x <= width; x += 8) {
          const y =
            height * (0.24 + band * 0.13) +
            Math.sin(x * 0.008 + phase * 0.00045 + band * 0.9) * 20 +
            Math.sin(x * 0.021 - phase * 0.0003 + band) * 6;
          if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = colours[band];
        ctx.globalAlpha = 0.65;
        ctx.lineWidth = 2;
        ctx.shadowBlur = 14;
        ctx.shadowColor = colours[band];
        ctx.stroke();
      }
      ctx.shadowBlur = 0;
      const glow = ctx.createRadialGradient(target.x, target.y, 0, target.x, target.y, 240);
      glow.addColorStop(0, 'rgba(255, 210, 186, .7)');
      glow.addColorStop(0.42, 'rgba(192, 132, 252, .18)');
      glow.addColorStop(1, 'rgba(255, 107, 53, 0)');
      ctx.fillStyle = glow;
      ctx.fillRect(target.x - 240, target.y - 240, 480, 480);
      ctx.globalCompositeOperation = 'source-over';

      const gap = 22;
      for (let y = gap / 2; y < height; y += gap) {
        for (let x = gap / 2; x < width; x += gap) {
          const dx = x - target.x;
          const dy = y - target.y;
          const dist = Math.hypot(dx, dy) || 1;
          const pull = Math.max(0, 1 - dist / 180);
          const wobble = reduce ? 0 : Math.sin(now * 0.0011 + x * 0.016 + y * 0.01) * 2.2;
          const px = x - (dx / dist) * pull * 13 + wobble;
          const py = y - (dy / dist) * pull * 13 + wobble * 0.6;
          const colour = colours[Math.min(colours.length - 1, Math.floor((px / Math.max(width, 1)) * colours.length))];
          const seed = Math.sin(x * 12.9898 + y * 78.233) * 43758.5453;
          const frac = seed - Math.floor(seed);
          const pulse = reduce ? 0.5 : 0.5 + 0.5 * Math.sin(now * 0.0018 + frac * 6.283);
          const base = 1.15 + frac * 1.5;
          ctx.beginPath();
          ctx.arc(px, py, base * 3.4 + pull * 8 + pulse * 1.4, 0, Math.PI * 2);
          ctx.fillStyle = colour;
          ctx.globalAlpha = 0.1 + pull * 0.22 + pulse * 0.1;
          ctx.fill();
          ctx.beginPath();
          ctx.arc(px, py, base + pull * 2.4 + pulse * 0.7, 0, Math.PI * 2);
          ctx.fillStyle = colour;
          ctx.globalAlpha = 1;
          ctx.fill();
        }
      }
      ctx.globalAlpha = 1;
      if (!reduce) raf = requestAnimationFrame(draw);
    };

    resize();
    window.addEventListener('resize', resize);
    window.addEventListener('pointermove', move);
    const observer = new ResizeObserver(() => {
      resize();
      if (reduce) draw(0);
    });
    if (canvas.parentElement) observer.observe(canvas.parentElement);
    raf = requestAnimationFrame(draw);
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener('resize', resize);
      window.removeEventListener('pointermove', move);
      observer.disconnect();
    };
  }, []);

  return <canvas ref={ref} className="av-hero-field" aria-hidden="true" />;
}

type UserPicture = { id: string; name: string; src: string; addedAt: number };

const PICTURES_KEY = 'vivdesign.user-pictures.v1';
const MAX_PICTURES = 12;

function readStoredPictures(): UserPicture[] {
  try {
    const raw = localStorage.getItem(PICTURES_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed.filter((p): p is UserPicture => !!p?.src && !!p?.id) : [];
  } catch {
    return [];
  }
}

/** Downscale and compress in the browser. Keeps localStorage from filling up. */
function fileToPicture(file: File): Promise<UserPicture> {
  return new Promise((resolve, reject) => {
    if (!file.type.startsWith('image/')) { reject(new Error('That file is not an image.')); return; }
    const reader = new FileReader();
    reader.onerror = () => reject(new Error('Could not read that file.'));
    reader.onload = () => {
      const img = new Image();
      img.onerror = () => reject(new Error('Could not decode that image.'));
      img.onload = () => {
        try {
          const max = 1400;
          const scale = Math.min(1, max / Math.max(img.width, img.height));
          const w = Math.max(1, Math.round(img.width * scale));
          const h = Math.max(1, Math.round(img.height * scale));
          const c = document.createElement('canvas');
          c.width = w; c.height = h;
          const x = c.getContext('2d');
          if (!x) { reject(new Error('Canvas is unavailable.')); return; }
          x.fillStyle = '#080a0e'; x.fillRect(0, 0, w, h);
          x.imageSmoothingQuality = 'high';
          x.drawImage(img, 0, 0, w, h);
          resolve({
            id: (crypto.randomUUID?.() || `${Date.now()}-${Math.random().toString(36).slice(2)}`),
            name: file.name.replace(/\.[^.]+$/, '').replace(/[-_]+/g, ' ').slice(0, 60) || 'Untitled picture',
            src: c.toDataURL('image/jpeg', 0.84),
            addedAt: Date.now(),
          });
        } catch {
          reject(new Error('Could not process that image.'));
        }
      };
      img.src = String(reader.result);
    };
    reader.readAsDataURL(file);
  });
}

/** Halftone portrait: the uploaded picture is rebuilt out of dots, then the
 *  pointer opens a clean window onto the original. No server, no upload. */
function PicturePreview({ src, dotScale = 1, contrast = 1.15, reveal = 68 }: {
  src: string;
  dotScale?: number;
  contrast?: number;
  reveal?: number;
}) {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const img = new Image();
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const pointer = { x: -1, y: -1 };
    let hasPointer = false;
    let width = 0, height = 0, raf = 0, dead = false;
    let cells: { r: number; g: number; b: number; l: number }[] = [];
    const tile = 7;

    const cover = (iw: number, ih: number, w: number, h: number) => {
      const s = Math.max(w / iw, h / ih);
      const dw = iw * s, dh = ih * s;
      return { x: (w - dw) / 2, y: (h - dh) / 2, w: dw, h: dh };
    };

    const build = () => {
      const box = canvas.getBoundingClientRect();
      width = Math.max(1, box.width); height = Math.max(1, box.height);
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const cols = Math.max(1, Math.ceil(width / tile));
      const rows = Math.max(1, Math.ceil(height / tile));
      const off = document.createElement('canvas');
      off.width = cols; off.height = rows;
      const offCtx = off.getContext('2d', { willReadFrequently: true });
      if (!offCtx) return;
      const cr = cover(img.width, img.height, cols, rows);
      offCtx.drawImage(img, cr.x, cr.y, cr.w, cr.h);
      const data = offCtx.getImageData(0, 0, cols, rows).data;
      cells = [];
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i], g = data[i + 1], b = data[i + 2];
        cells.push({ r, g, b, l: (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255 });
      }
    };

    const draw = (now: number) => {
      if (dead || !img.complete || !img.naturalWidth) return;
      if (!width) build();
      ctx.clearRect(0, 0, width, height);
      ctx.fillStyle = '#080a0e'; ctx.fillRect(0, 0, width, height);
      const cols = Math.ceil(width / tile);
      for (let i = 0; i < cells.length; i++) {
        const c = cells[i];
        const row = Math.floor(i / cols);
        const cx = (i % cols) * tile + tile / 2 + (row % 2 ? tile * 0.5 : 0);
        const cy = row * tile + tile / 2;
        const tone = Math.max(0, Math.min(1, (c.l - 0.5) * contrast + 0.5));
        if (tone < 0.045) continue;
        // One ordered ramp (violet → orange → cream) keeps the photograph legible.
        const a = tone < 0.5 ? [95, 75, 216] : [255, 154, 108];
        const b = tone < 0.5 ? [255, 154, 108] : [255, 243, 224];
        const t = (tone < 0.5 ? tone * 2 : (tone - 0.5) * 2);
        const r = Math.round(a[0] + (b[0] - a[0]) * t);
        const g = Math.round(a[1] + (b[1] - a[1]) * t);
        const bl = Math.round(a[2] + (b[2] - a[2]) * t);
        const radius = Math.min(tile * 0.72, tile * (0.06 + tone * 0.5) * dotScale);
        ctx.beginPath();
        ctx.arc(cx, cy, radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgb(${r}, ${g}, ${bl})`;
        ctx.globalAlpha = 0.96;
        ctx.fill();
      }
      // Warm print tint + scanlines.
      ctx.globalCompositeOperation = 'soft-light';
      ctx.fillStyle = 'rgba(255, 122, 66, .34)';
      ctx.fillRect(0, 0, width, height);
      ctx.globalCompositeOperation = 'source-over';
      ctx.fillStyle = 'rgba(8, 10, 14, .14)';
      for (let y = 0; y < height; y += 4) ctx.fillRect(0, y, width, 1);

      const tx = hasPointer ? pointer.x : width * (0.5 + Math.sin(now * 0.0007) * 0.22);
      const ty = hasPointer ? pointer.y : height * (0.48 + Math.cos(now * 0.00055) * 0.16);
      ctx.save();
      ctx.beginPath(); ctx.arc(tx, ty, reveal, 0, Math.PI * 2); ctx.clip();
      const cr = cover(img.width, img.height, width, height);
      ctx.globalAlpha = 1;
      ctx.drawImage(img, cr.x, cr.y, cr.w, cr.h);
      ctx.restore();
      // A real cut-out: dark halo, crisp rim, dashed outer handle.
      ctx.save();
      ctx.beginPath(); ctx.arc(tx, ty, reveal + 1, 0, Math.PI * 2);
      ctx.shadowColor = 'rgba(0, 0, 0, .95)'; ctx.shadowBlur = 26;
      ctx.strokeStyle = 'rgba(255, 255, 255, .95)'; ctx.lineWidth = 3; ctx.stroke();
      ctx.restore();
      ctx.save();
      ctx.beginPath(); ctx.arc(tx, ty, reveal + 9, 0, Math.PI * 2);
      ctx.setLineDash([3, 6]);
      ctx.strokeStyle = 'rgba(255, 191, 157, .62)'; ctx.lineWidth = 1.5; ctx.stroke();
      ctx.restore();
      ctx.beginPath();
      ctx.arc(tx + reveal * 0.72, ty - reveal * 0.72, 5.5, 0, Math.PI * 2);
      ctx.fillStyle = '#ffbf9d'; ctx.fill();
      ctx.strokeStyle = '#080a0e'; ctx.lineWidth = 1.5; ctx.stroke();
      if (!reduce) raf = requestAnimationFrame(draw);
    };

    const measure = () => {
      build();
      if (reduce) draw(performance.now());
    };
    const move = (e: PointerEvent) => {
      const box = canvas.getBoundingClientRect();
      pointer.x = e.clientX - box.left; pointer.y = e.clientY - box.top; hasPointer = true;
      if (reduce) draw(performance.now());
    };
    const leave = () => { hasPointer = false; if (reduce) draw(performance.now()); };

    img.onload = () => {
      if (dead) return;
      measure();
      raf = requestAnimationFrame(draw);
    };
    img.src = src;
    const ro = new ResizeObserver(measure);
    ro.observe(canvas);
    canvas.addEventListener('pointermove', move);
    canvas.addEventListener('pointerleave', leave);
    return () => {
      dead = true; cancelAnimationFrame(raf); ro.disconnect();
      canvas.removeEventListener('pointermove', move);
      canvas.removeEventListener('pointerleave', leave);
    };
  }, [src, dotScale, contrast, reveal]);

  return <canvas ref={ref} className="av-picture-canvas" aria-label="Your picture as an interactive halftone" />;
}

function ImageLab({ pictures, activeId, note, onSelect, onAdd, onRemove, onClose }: {
  pictures: UserPicture[];
  activeId: string | null;
  note: string;
  onSelect: (id: string) => void;
  onAdd: (p: UserPicture) => void;
  onRemove: (id: string) => void;
  onClose: () => void;
}) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [drag, setDrag] = useState(false);
  const [dotScale, setDotScale] = useState(1);
  const [contrast, setContrast] = useState(1.15);
  const [reveal, setReveal] = useState(68);
  const input = useRef<HTMLInputElement>(null);
  const active = pictures.find(p => p.id === activeId) || pictures[0] || null;

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    window.addEventListener('keydown', onKey);
    return () => { document.body.style.overflow = prev; window.removeEventListener('keydown', onKey); };
  }, [onClose]);

  const takeFiles = async (files: FileList | File[]) => {
    const list = Array.from(files).filter(f => f.type.startsWith('image/'));
    if (!list.length) { setError('Choose an image file — JPG, PNG, WebP or GIF.'); return; }
    if (pictures.length >= MAX_PICTURES) { setError(`You can keep ${MAX_PICTURES} pictures here. Remove one first.`); return; }
    setBusy(true); setError('');
    const room = MAX_PICTURES - pictures.length;
    for (const file of list.slice(0, room)) {
      try { onAdd(await fileToPicture(file)); }
      catch (e) { setError(e instanceof Error ? e.message : 'Could not add that picture.'); }
    }
    setBusy(false);
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault(); setDrag(false);
    if (e.dataTransfer.files.length) void takeFiles(e.dataTransfer.files);
  };

  useEffect(() => {
    const onPaste = (e: ClipboardEvent) => {
      const files = Array.from(e.clipboardData?.files || []).filter(f => f.type.startsWith('image/'));
      if (files.length) void takeFiles(files);
    };
    window.addEventListener('paste', onPaste);
    return () => window.removeEventListener('paste', onPaste);
  });

  return (
    <div className="av-lab-backdrop" onMouseDown={e => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="av-lab" role="dialog" aria-modal="true" aria-label="Add your pictures">
        <header className="av-lab-head">
          <div>
            <p className="av-kicker">PICTURE LAB · YOUR OWN WORK</p>
            <h2>Put a picture in the field.</h2>
            <p>Drop an image and it becomes a halftone you can move through. Your pictures appear on this page, in a private row above the catalogue.</p>
          </div>
          <button className="av-lab-close" onClick={onClose} aria-label="Close picture lab">✕</button>
        </header>

        <div className="av-lab-body">
          <div
            className={`av-lab-stage${drag ? ' is-drag' : ''}${active ? '' : ' is-empty'}`}
            onDragOver={e => { e.preventDefault(); setDrag(true); }}
            onDragLeave={() => setDrag(false)}
            onDrop={onDrop}
            onClick={() => { if (!active) input.current?.click(); }}
          >
            {active ? (
              <>
                <PicturePreview key={active.id} src={active.src} dotScale={dotScale} contrast={contrast} reveal={reveal} />
                <span className="av-lab-badge"><i />MOVE TO REVEAL</span>
              </>
            ) : (
              <div className="av-lab-empty">
                <span>＋</span>
                <b>Drop a picture here.</b>
                <p>Or click to choose a file.</p>
                <em>JPG · PNG · WEBP · GIF · up to {MAX_PICTURES} images</em>
              </div>
            )}
          </div>

          <aside className="av-lab-side">
            <input
              ref={input}
              type="file"
              accept="image/*"
              multiple
              className="av-lab-file"
              onChange={e => { if (e.target.files) void takeFiles(e.target.files); e.target.value = ''; }}
            />
            <div className="av-lab-actions">
              <button className="av-drop-btn" onClick={() => input.current?.click()} disabled={busy}>
                {busy ? 'Adding…' : active ? 'Add another' : 'Choose pictures'}
              </button>
              <p>Drop or paste anywhere in the frame.</p>
            </div>

            {active && (
              <p className="av-lab-caption"><b>{active.name}</b><span>{pictures.length} / {MAX_PICTURES} pictures</span></p>
            )}

            {pictures.length > 0 && (
              <div className="av-lab-gallery">
                <p className="av-kicker">YOUR PICTURES · {pictures.length}</p>
                <div>
                  {pictures.map(p => (
                    <div key={p.id} className={`av-lab-thumb${p.id === active?.id ? ' on' : ''}`}>
                      <button onClick={() => onSelect(p.id)} aria-label={`Preview ${p.name}`}>
                        <img src={p.src} alt="" />
                      </button>
                      <button className="av-lab-remove" onClick={() => onRemove(p.id)} aria-label={`Remove ${p.name}`}>×</button>
                    </div>
                  ))}
                  {pictures.length < MAX_PICTURES && (
                    <button className="av-lab-add-tile" onClick={() => input.current?.click()} aria-label="Add another picture">
                      <span>＋</span><b>Add</b>
                    </button>
                  )}
                </div>
              </div>
            )}

            {active && (
              <div className="av-lab-controls">
                <label>
                  <span>DOT SIZE</span>
                  <input type="range" min="0.6" max="1.45" step="0.05" value={dotScale} onChange={e => setDotScale(Number(e.target.value))} />
                  <b>{dotScale.toFixed(2)}×</b>
                </label>
                <label>
                  <span>CONTRAST</span>
                  <input type="range" min="0.7" max="2" step="0.05" value={contrast} onChange={e => setContrast(Number(e.target.value))} />
                  <b>{contrast.toFixed(2)}</b>
                </label>
                <label>
                  <span>REVEAL</span>
                  <input type="range" min="34" max="130" step="2" value={reveal} onChange={e => setReveal(Number(e.target.value))} />
                  <b>{reveal}px</b>
                </label>
              </div>
            )}

            {(error || note) && <p className="av-lab-error">{error || note}</p>}
            <div className="av-lab-foot">
              <p className="av-lab-note">Saved in this browser only. Nothing is uploaded to a server, so each visitor builds their own private row.</p>
              <button className="av-lab-done" onClick={onClose} disabled={!pictures.length}>Done</button>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}

function YourPictures({ pictures, onOpen, onRemove }: {
  pictures: UserPicture[];
  onOpen: (id?: string) => void;
  onRemove: (id: string) => void;
}) {
  if (!pictures.length) return null;
  return (
    <section className="av-your-strip" aria-label="Your pictures">
      <div className="av-your-strip-title">
        <span>＋</span>
        <div>
          <h2>Your pictures</h2>
          <p>Private to this browser</p>
        </div>
        <b>{String(pictures.length).padStart(2, '0')}</b>
      </div>
      <div className="av-your-strip-thumbs">
        {pictures.map(p => (
          <div key={p.id} className="av-your-thumb">
            <button onClick={() => onOpen(p.id)} title={p.name} aria-label={`Open ${p.name} in the picture lab`}>
              <img src={p.src} alt={p.name} loading="lazy" />
            </button>
            <button className="av-your-remove" onClick={() => onRemove(p.id)} aria-label={`Remove ${p.name}`}>×</button>
          </div>
        ))}
        <button className="av-your-add" onClick={() => onOpen()} aria-label="Add another picture">
          <span>＋</span><b>Add</b>
        </button>
      </div>
      <button className="av-your-open" onClick={() => onOpen()}>Open lab →</button>
    </section>
  );
}

function useCopy() {
  const [copied, setCopied] = useState<string | null>(null);
  const copy = useCallback(async (key: string, text: string) => {
    if (await copyText(text)) {
      setCopied(key);
      setTimeout(() => setCopied(null), 1800);
    }
  }, []);
  return { copied, copy };
}

type GroupConfig = {
  base: string;
  list: VisualAddon[];
  cats: typeof addonCategories;
  noun: string;
  kicker: string;
  headline: React.ReactNode;
  lede: string;
  stats: [string, string][];
  howto: [string, string][];
  howtoTitle: string;
  searchPlaceholder: string;
  snippetNote: string;
  principles: [string, string, string][];
  other: { href: string; label: string; blurb: string };
};

const CONFIG: Record<AddonGroup, GroupConfig> = {
  visual: {
    base: '#/addons',
    list: visualAddons,
    cats: addonCategories,
    noun: 'add-on',
    kicker: 'Visual add-ons · 25 drop-ins',
    headline: <>The finish,<br /><em>not the direction.</em></>,
    lede: 'The Styles DB decides what a page is. These are the layers that make it feel made: grain, light, depth, motion and the small interactions at the edges. Every one is a self-contained snippet that drops into any of the 150 directions.',
    stats: [['25', 'add-ons'], ['5', 'categories'], ['0', 'dependencies'], ['1', 'snippet each']],
    howtoTitle: 'HOW TO USE THEM',
    howto: [
      ['Pick a direction', 'Start in the Styles DB — one style, not a pile.'],
      ['Add two or three', 'One atmosphere, one surface, one motion. Stop there.'],
      ['Copy the snippet', 'Swap the accent values for the style’s palette.'],
      ['Check the edges', 'Reduced motion, AA contrast, touch fallback.'],
    ],
    searchPlaceholder: 'Search effects, surfaces, snippets…',
    snippetNote: 'Self-contained CSS + markup. Paste into the page, then swap the accent values for your brand tokens.',
    principles: [
      ['01', 'One light source', 'Never run a cursor spotlight and a section glow in the same viewport. The eye can only believe one.'],
      ['02', 'Two per page, three max', 'Atmosphere + surface is a page. Add motion only if something actually enters or moves.'],
      ['03', 'Motion earns its keep', 'Every effect gets a prefers-reduced-motion branch and a static fallback that still looks designed.'],
      ['04', 'Contrast is not negotiable', 'Grain, glass and duotone all reduce legibility. Check body text at AA after the effect, not before.'],
    ],
    other: {
      href: '#/interactive',
      label: 'Interactive elements →',
      blurb: 'Want the visitor to touch something? The 125 playgrounds.',
    },
  },
  interactive: {
    base: '#/interactive',
    list: allInteractive,
    cats: interactiveCategories,
    noun: 'element',
    kicker: 'Interactive elements · 125 playgrounds',
    headline: <>Not a picture.<br /><em>A playground.</em></>,
    lede: 'These are the parts a visitor can grab: generative canvases, pointer physics, 3D depth, type that bends, sound that draws itself. Each one is a single HTML file with no libraries — open it, drag it, then copy the core loop into the page.',
    stats: [['125', 'playgrounds'], ['5', 'families'], ['0', 'libraries'], ['60', 'fps target']],
    howtoTitle: 'HOW TO USE THEM',
    howto: [
      ['Pick the moment', 'Hero, product reveal, success state, gallery. One job per piece.'],
      ['Keep it contained', 'One interactive canvas per viewport. It should not fight the copy.'],
      ['Start from the loop', 'Copy the core loop, then add your palette and real content.'],
      ['Design the edges', 'Touch, reduced motion, keyboard and a paused fallback.'],
    ],
    searchPlaceholder: 'Search canvases, physics, 3D, type…',
    snippetNote: 'The core loop, stripped to the essentials. The live demo adds the artwork, controls and polish — open it full screen to see the full file.',
    principles: [
      ['01', 'One playground per viewport', 'Two animated canvases compete for the same attention. Pick the one that carries the message.'],
      ['02', 'The pointer is not the only input', 'Every draggable piece needs a keyboard or button equivalent, and a touch path.'],
      ['03', 'Cheap beats clever', 'Canvas at 60fps, capped DPR, no libraries. If it cannot hold 60, cut particle count before cutting frames.'],
      ['04', 'Always have a still', 'Pause the loop when off-screen and give reduced-motion visitors the same composition, frozen.'],
    ],
    other: {
      href: '#/addons',
      label: 'Visual add-ons →',
      blurb: 'Need the finishing layer? Grain, light, borders and depth.',
    },
  },
};

export function AddonsTab({ group = 'visual' }: { group?: AddonGroup }) {
  const cfg = CONFIG[group];
  const [route, setRoute] = useState(() => parseHash(cfg.base));
  const [visible, setVisible] = useState<Set<string>>(new Set());
  const [query, setQuery] = useState(route.q);
  const [pictures, setPictures] = useState<UserPicture[]>(readStoredPictures);
  const [labOpen, setLabOpen] = useState(false);
  const [activePicture, setActivePicture] = useState<string | null>(null);
  const [pictureNote, setPictureNote] = useState('');
  const { copied, copy } = useCopy();

  useEffect(() => {
    try {
      localStorage.setItem(PICTURES_KEY, JSON.stringify(pictures));
      setPictureNote('');
    } catch {
      setPictureNote('This browser is out of storage. Remove a picture to keep adding.');
    }
  }, [pictures]);

  const addPicture = useCallback((p: UserPicture) => {
    setPictures(prev => [p, ...prev].slice(0, MAX_PICTURES));
    setActivePicture(p.id);
  }, []);

  const removePicture = useCallback((id: string) => {
    setPictures(prev => prev.filter(p => p.id !== id));
    setActivePicture(current => current === id ? null : current);
  }, []);

  const closeLab = useCallback(() => setLabOpen(false), []);

  const openLab = useCallback((id?: string) => {
    setActivePicture(id || pictures[0]?.id || null);
    setLabOpen(true);
  }, [pictures]);

  useEffect(() => {
    const onHash = () => {
      const next = parseHash(cfg.base);
      setRoute(next);
      setQuery(next.q);
      window.scrollTo(0, 0);
    };
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, [cfg.base]);

  const setHash = useCallback((id: string | null, cat: AddonCategory | 'all', q: string) => {
    const usp = new URLSearchParams();
    if (cat !== 'all') usp.set('cat', cat);
    if (q) usp.set('q', q);
    const qs = usp.toString() ? '?' + usp.toString() : '';
    window.location.hash = id ? `${cfg.base}/${encodeURIComponent(id)}${qs}` : `${cfg.base}${qs}`;
  }, [cfg.base]);

  const filtered = useMemo(() => {
    const q = route.q.toLowerCase();
    const byCat = route.cat === 'all' ? cfg.list : cfg.list.filter(a => a.category === route.cat);
    return byCat.filter(a =>
      !q || (a.name + ' ' + a.tagline + ' ' + a.what + ' ' + a.surface.join(' ')).toLowerCase().includes(q),
    );
  }, [cfg.list, route.cat, route.q]);

  /* lazy iframes: only mount previews when the card is near the viewport */
  useEffect(() => {
    if (route.id) { setVisible(new Set()); return; }
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        const id = (e.target as HTMLElement).dataset.aid;
        if (!id) return;
        setVisible(prev => {
          const n = new Set(prev);
          if (e.isIntersecting) n.add(id); else n.delete(id);
          return n;
        });
      });
    }, { rootMargin: '320px' });
    document.querySelectorAll('[data-aid]').forEach(el => io.observe(el));
    return () => io.disconnect();
  }, [route.id, filtered.length]);

  /* ── DETAIL ─────────────────────────────────────────────── */
  if (route.id) {
    const idx = cfg.list.findIndex(a => a.id === route.id);
    const a = cfg.list[idx];
    if (!a) {
      return (
        <div className="av-missing">
          Not found. <a href={cfg.base}>← All {cfg.list.length} {cfg.noun}s</a>
        </div>
      );
    }
    const cat = cfg.cats.find(c => c.id === a.category)!;
    const prev = cfg.list[idx - 1];
    const next = cfg.list[idx + 1];
    const pairs = cfg.list
      .filter(x => x.id !== a.id && (x.category === a.category || x.worksWith.some(w => a.worksWith.includes(w))))
      .slice(0, 3);

    return (
      <div className="av-detail">
        <div className="av-detail-top">
          <button className="av-back" onClick={() => setHash(null, route.cat, route.q)}>← All {cfg.list.length} {cfg.noun}s</button>
          <div className="av-detail-actions">
            <ShareLink section={group === 'interactive' ? 'interactive' : 'addons'} id={a.id} label={a.name} />
          </div>
          <div className="av-detail-nav">
            {prev && <button onClick={() => setHash(prev.id, route.cat, route.q)}>← {prev.name}</button>}
            <span className="av-posn">{a.n} of {cfg.list.length}</span>
            {next && <button onClick={() => setHash(next.id, route.cat, route.q)}>{next.name} →</button>}
          </div>
        </div>

        <header className="av-head">
          <div className="av-head-meta">
            <span className="av-cat-chip" style={{ color: cat.color, borderColor: cat.color + '55', background: cat.color + '16' }}>
              {cat.emoji} {cat.label}
            </span>
            <span className="av-intensity" title={`${a.intensity} intensity`}>
              {[0, 1, 2].map(i => (
                <i key={i} style={{ background: i < INTENSITY_DOTS[a.intensity] ? cat.color : '#2a303c' }} />
              ))}
              {a.intensity}
            </span>
          </div>
          <h1>{a.name}</h1>
          <p className="av-tagline">{a.tagline}</p>
        </header>

        <div className="av-demo">
          <div className="av-demo-bar">
            <span className="av-live"><i />LIVE DEMO — INTERACT WITH IT</span>
            <div>
              <button className="av-btn primary" onClick={() => copy('prompt', a.prompt)}>
                {copied === 'prompt' ? '✓ Prompt copied' : '🪄 Copy agent prompt'}
              </button>
              <a className="av-btn" href={a.demo} target="_blank" rel="noreferrer">↗ Full screen</a>
            </div>
          </div>
          <iframe className="av-demo-frame" src={a.demo} sandbox="allow-scripts allow-same-origin" loading="lazy" title={a.name} />
        </div>

        <div className="av-explain">
          <div className="av-explain-card">
            <h3>WHAT IT IS</h3>
            <p>{a.what}</p>
          </div>
          <div className="av-explain-card">
            <h3>WHY IT WORKS</h3>
            <p>{a.why}</p>
          </div>
        </div>

        <div className="av-tags-row">
          <span className="av-tags-label">BEST ON</span>
          {a.surface.map(s => <span key={s} className="av-tag">{s}</span>)}
          <span className="av-tags-label" style={{ marginLeft: 14 }}>PAIRS WITH STYLES</span>
          {a.worksWith.map(s => <span key={s} className="av-tag style">{styleLabel(s)}</span>)}
        </div>

        <section className="av-code-block">
          <div className="av-code-head">
            <div>
              <h3>{group === 'interactive' ? 'Core loop' : 'Drop-in snippet'}</h3>
              <p>{cfg.snippetNote}</p>
            </div>
            <button className={`av-btn primary ${copied === 'snippet' ? 'ok' : ''}`} onClick={() => copy('snippet', a.snippet)}>
              {copied === 'snippet' ? '✓ Copied' : '⧉ Copy code'}
            </button>
          </div>
          <pre className="av-pre"><code>{a.snippet}</code></pre>
        </section>

        <section className="av-prompt-block">
          <div className="av-code-head">
            <div>
              <h3>Agent prompt</h3>
              <p>Paste this into the coding agent that is building the page. It carries the interaction, performance and accessibility constraints.</p>
            </div>
            <button className="av-btn" onClick={() => copy('prompt2', a.prompt)}>
              {copied === 'prompt2' ? '✓ Copied' : '⧉ Copy prompt'}
            </button>
          </div>
          <pre className="av-pre prompt"><code>{a.prompt}</code></pre>
        </section>

        <section className="av-pairs">
          <h3>Pairs well with</h3>
          <div className="av-pairs-grid">
            {pairs.map(p => {
              const pc = cfg.cats.find(c => c.id === p.category)!;
              return (
                <button key={p.id} className="av-pair" onClick={() => setHash(p.id, route.cat, route.q)}>
                  <span className="av-cat-chip small" style={{ color: pc.color, borderColor: pc.color + '55', background: pc.color + '16' }}>
                    {pc.emoji} {pc.label}
                  </span>
                  <b>{p.name}</b>
                  <span>{p.tagline}</span>
                </button>
              );
            })}
          </div>
        </section>

        <div className="av-foot-nav">
          {prev ? <button onClick={() => setHash(prev.id, route.cat, route.q)}>← {prev.name}</button> : <span />}
          <a href={cfg.other.href}>{cfg.other.label}</a>
          {next ? <button onClick={() => setHash(next.id, route.cat, route.q)}>{next.name} →</button> : <span />}
        </div>
      </div>
    );
  }

  /* ── INDEX ──────────────────────────────────────────────── */
  const isInteractive = group === 'interactive';
  const grouped = isInteractive && route.cat === 'all' && !route.q;

  const track = (e: React.PointerEvent<HTMLElement>) => {
    const box = e.currentTarget.getBoundingClientRect();
    const px = (e.clientX - box.left) / box.width;
    const py = (e.clientY - box.top) / box.height;
    e.currentTarget.style.setProperty('--mx', `${px * 100}%`);
    e.currentTarget.style.setProperty('--my', `${py * 100}%`);
    e.currentTarget.style.setProperty('--rx', `${(0.5 - py) * 3.2}deg`);
    e.currentTarget.style.setProperty('--ry', `${(px - 0.5) * 3.2}deg`);
  };

  const resetTrack = (e: React.PointerEvent<HTMLElement>) => {
    e.currentTarget.style.setProperty('--rx', '0deg');
    e.currentTarget.style.setProperty('--ry', '0deg');
  };

  const renderCard = (a: VisualAddon, feature = false, number?: number) => {
    const cat = cfg.cats.find(c => c.id === a.category)!;
    const displayN = number ?? a.n;
    // Interactive cards ship an animated GIF illustration of the engine.
    const thumb = a.thumb || (isInteractive ? `/interactive/thumbs/${a.id}.gif` : null);
    return (
      <article
        key={a.id}
        className={`av-card${feature ? ' is-feature' : ''}`}
        data-aid={a.id}
        style={{ '--cat': cat.color } as React.CSSProperties}
        onClick={() => setHash(a.id, route.cat, route.q)}
        onPointerMove={track}
        onPointerLeave={resetTrack}
      >
        <div className="av-thumb-wrap">
          {thumb ? (
            <img
              className="av-thumb-gif"
              src={thumb}
              alt={`${a.name} animated preview`}
              loading={displayN <= 8 ? 'eager' : 'lazy'}
              decoding="async"
            />
          ) : visible.has(a.id) ? (
            <ScaledPreview src={a.demo} title={a.name} />
          ) : (
            <div className="av-thumb" style={{ height: 248 }}>
              <div className="av-thumb-placeholder">PREVIEW LOADS ON SCROLL</div>
            </div>
          )}
          <span className="av-num">{String(displayN).padStart(2, '0')}</span>
          <ShareLink section={isInteractive ? 'interactive' : 'addons'} id={a.id} label={a.name} compact className="corner" />
          {isInteractive && (
            <>
              <div className="av-thumb-head">
                <span className="av-thumb-kind">{String(displayN).padStart(2, '0')} · {cat.emoji} {cat.label}</span>
                {feature && <span className="av-live-chip"><i />LIVE DEMO</span>}
              </div>
            </>
          )}
          {isInteractive && <span className="av-play-btn" aria-hidden="true">↗</span>}
        </div>
        <div className="av-card-body">
          <div className="av-card-meta">
            {!isInteractive && (
              <span className="av-cat-chip small" style={{ color: cat.color, borderColor: cat.color + '55', background: cat.color + '16' }}>
                {cat.emoji} {cat.label}
              </span>
            )}
            <span className="av-intensity" title={`${a.intensity} intensity`}>
              {[0, 1, 2].map(i => (
                <i key={i} style={{ background: i < INTENSITY_DOTS[a.intensity] ? cat.color : '#2a303c' }} />
              ))}
            </span>
          </div>
          <h3>{a.name}</h3>
          <p>{a.tagline}</p>
          {feature && <p className="av-card-what">{a.what}</p>}
          <div className="av-card-foot">
            <span>Open {cfg.noun} →</span>
            <span className="av-surfaces">{a.surface.slice(0, 2).join(' · ')}</span>
          </div>
        </div>
      </article>
    );
  };

  let cardNo = 0;
  return (
    <div className={`av-index${isInteractive ? ' is-interactive' : ''}`}>
      <header className={`av-hero${isInteractive ? ' av-hero-interactive' : ''}`}>
        <div className="av-hero-copy">
          <p className="av-kicker">{cfg.kicker}</p>
          <h1>{cfg.headline}</h1>
          <p className="av-lede">{cfg.lede}</p>
          <div className="av-stats">
            {cfg.stats.map(([n, label]) => (
              <div key={label}><b>{isInteractive ? <CountUp value={n} /> : n}</b><span>{label}</span></div>
            ))}
          </div>
          {!isInteractive && (
            <a className="av-crosslink" href={cfg.other.href}>
              <span>{cfg.other.blurb}</span>
              <b>{cfg.other.label}</b>
            </a>
          )}
        </div>
        {isInteractive ? (
          <div className="av-hero-stage">
            <HeroField />
            <span className="av-hero-stage-top"><i />LIVE FIELD <em>MOVE TO PLAY</em></span>
            <span className="av-hero-stage-bottom">DRAG · SWIPE · PLAY</span>
          </div>
        ) : (
          <aside className="av-howto">
            <h3>{cfg.howtoTitle}</h3>
            <ol>
              {cfg.howto.map(([b, span]) => (
                <li key={b}><b>{b}</b><span>{span}</span></li>
              ))}
            </ol>
          </aside>
        )}
      </header>

      <div className="av-controls">
        <div className="av-cats">
          <button className={`av-cat ${route.cat === 'all' ? 'on' : ''}`} onClick={() => setHash(null, 'all', route.q)}>
            🌐 All <span>{cfg.list.length}</span>
          </button>
          {cfg.cats.map(c => (
            <button
              key={c.id}
              className={`av-cat ${route.cat === c.id ? 'on' : ''}`}
              onClick={() => setHash(null, c.id, route.q)}
              style={route.cat === c.id ? { borderColor: c.color + '88', color: c.color } : undefined}
            >
              <i className="av-dot" style={{ background: c.color }} />
              {c.label} <span>{cfg.list.filter(a => a.category === c.id).length}</span>
            </button>
          ))}
        </div>
        {isInteractive && (
          <button className="av-add-pic" onClick={() => openLab()}>
            <span>＋</span> Add pictures {pictures.length > 0 && <b>{pictures.length}</b>}
          </button>
        )}
        <input
          className="av-search"
          placeholder={cfg.searchPlaceholder}
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter') setHash(null, route.cat, query); }}
        />
      </div>

      {isInteractive && <YourPictures pictures={pictures} onOpen={openLab} onRemove={removePicture} />}

      {route.cat !== 'all' && (
        <p className="av-cat-blurb">{cfg.cats.find(c => c.id === route.cat)!.blurb}</p>
      )}

      {grouped ? (
        cfg.cats.map(c => {
          const items = filtered.filter(a => a.category === c.id);
          if (!items.length) return null;
          return (
            <section className="av-family" key={c.id}>
              <header className="av-family-head">
                <span className="av-family-mark" style={{ color: c.color, borderColor: c.color + '55', background: c.color + '12' }}>
                  {c.emoji}
                </span>
                <div>
                  <h2>{c.label}</h2>
                  <p>{c.blurb}</p>
                </div>
                <span className="av-family-count">{String(items.length).padStart(2, '0')}</span>
              </header>
              <div className="av-grid">{items.map((a, i) => { cardNo += 1; return renderCard(a, i === 0, cardNo); })}</div>
            </section>
          );
        })
      ) : (
        <div className="av-grid">{filtered.map((a, i) => renderCard(a, false, i + 1))}</div>
      )}

      {filtered.length === 0 && (
        <div className="av-empty">No {cfg.noun}s match “{route.q}”. <button onClick={() => { setQuery(''); setHash(null, 'all', ''); }}>Clear</button></div>
      )}

      {isInteractive && (
        <div className="av-howto-strip av-howto-strip-bottom">
          <div className="av-howto-strip-head">
            <p className="av-kicker">{cfg.howtoTitle}</p>
          </div>
          <ol>
            {cfg.howto.map(([b, span]) => (
              <li key={b}><b>{b}</b><span>{span}</span></li>
            ))}
          </ol>
        </div>
      )}

      <section className="av-principles">
        <h2>{group === 'interactive' ? 'Rules that keep interaction from becoming a gimmick' : 'Rules that keep add-ons from becoming noise'}</h2>
        <div className="av-principles-grid">
          {cfg.principles.map(([n, h, p]) => (
            <div key={n}><b>{n}</b><h3>{h}</h3><p>{p}</p></div>
          ))}
        </div>
      </section>

      {isInteractive && labOpen && (
        <ImageLab
          pictures={pictures}
          activeId={activePicture}
          note={pictureNote}
          onSelect={setActivePicture}
          onAdd={addPicture}
          onRemove={removePicture}
          onClose={closeLab}
        />
      )}
    </div>
  );
}
