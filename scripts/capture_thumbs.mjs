/**
 * Capture real animated thumbnails from every interactive demo.
 *
 * Loads each self-contained demo in headless Chromium at 960x600, hides the
 * HUD chrome, drives the pointer in a slow circle, and writes 12 frames to
 * /tmp/interactive-frames/<id>/. A Python pass turns those into 320x200 GIFs.
 */
import { chromium } from 'playwright';
import { mkdirSync, readdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const EXEC = process.env.CHROMIUM || '/usr/sbin/chromium';
const ROOT = resolve('public/interactive');
const OUT = '/tmp/interactive-frames';
const files = readdirSync(ROOT).filter((f) => f.endsWith('.html')).sort();
const FRAMES = 12;
const STEP = 110;

mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch({ executablePath: EXEC, args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 640, height: 400 }, deviceScaleFactor: 1 });

for (const file of files) {
  const id = file.replace(/\.html$/, '');
  const dir = resolve(OUT, id);
  mkdirSync(dir, { recursive: true });
  await page.goto(`file://${ROOT}/${file}`, { waitUntil: 'load', timeout: 8000 });
  await page.addStyleTag({ content: '.hud,.hint,.pause{display:none!important}body{cursor:none!important}' });
  await page.waitForTimeout(1800);
  for (let f = 0; f < FRAMES; f++) {
    const a = (f / FRAMES) * Math.PI * 2;
    await page.mouse.move(320 + Math.cos(a) * 150, 200 + Math.sin(a) * 80);
    if (f === 2) await page.mouse.down();
    if (f === 7) await page.mouse.up();
    await page.waitForTimeout(STEP);
    await page.screenshot({ path: resolve(dir, `f${String(f).padStart(2, '0')}.png`) });
  }
  console.log(`captured ${id}`);
}

await browser.close();
writeFileSync('/tmp/interactive-frames/manifest.json', JSON.stringify(files, null, 2));
console.log(`${files.length} demos captured`);
