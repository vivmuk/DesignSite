/**
 * Smoke-check every interactive demo in headless Chromium.
 *
 * Fails (non-zero exit) on console errors, a 404, or a canvas that is still
 * blank after 600ms. Also reports the HUD stat line so the demo is doing the
 * thing its card claims.
 */
import { chromium } from 'playwright';
import { readdirSync } from 'node:fs';
import { resolve } from 'node:path';

const EXEC = process.env.CHROMIUM || '/usr/sbin/chromium';
const ROOT = resolve('public/interactive');
const files = readdirSync(ROOT).filter((f) => f.endsWith('.html')).sort();
const browser = await chromium.launch({ executablePath: EXEC, args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 960, height: 600 } });
const failures = [];

for (const file of files) {
  const errors = [];
  const onConsole = (msg) => { if (msg.type() === 'error') errors.push(msg.text()); };
  const onPageError = (err) => errors.push(String(err));
  page.on('console', onConsole);
  page.on('pageerror', onPageError);
  try {
    const res = await page.goto(`file://${ROOT}/${file}`, { waitUntil: 'load', timeout: 8000 });
    await page.waitForTimeout(700);
    const state = await page.evaluate(() => {
      const c = document.querySelector('canvas');
      const statEl = document.querySelector('#stat');
      let urlLen = 0;
      if (c) { try { urlLen = c.toDataURL().length; } catch { urlLen = -1; } }
      return {
        title: document.title,
        stat: statEl?.textContent || null,
        generated: !!statEl,
        urlLen,
        canvas: !!c,
      };
    });
    if (!res || res.status() !== 200) errors.push(`HTTP ${res?.status()}`);
    if (state.generated && !state.canvas) errors.push('no canvas');
    if (state.generated && state.urlLen < 6000) errors.push(`blank canvas (dataURL=${state.urlLen})`);
    if (errors.length) failures.push({ file, errors, state });
    console.log(`${errors.length ? 'FAIL' : 'ok  '} ${file.padEnd(30)} ${state.stat ?? ''}`);
  } catch (error) {
    failures.push({ file, errors: [String(error)] });
    console.log(`FAIL ${file} ${String(error).slice(0, 120)}`);
  } finally {
    page.off('console', onConsole);
    page.off('pageerror', onPageError);
  }
}

await browser.close();
console.log(`\n${files.length - failures.length}/${files.length} passed`);
if (failures.length) {
  console.log(JSON.stringify(failures, null, 2));
  process.exit(1);
}
