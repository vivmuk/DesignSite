/** Verifies the detail page mounts a real, interactive demo iframe. */
import { chromium } from 'playwright';

const EXEC = process.env.CHROMIUM || '/usr/sbin/chromium';
const BASE = process.env.BASE || 'http://127.0.0.1:3110';
const ids = ['gravity-wells', 'scratch-to-reveal', 'slot-machine-glyphs', 'applause-meter'];
const browser = await chromium.launch({ executablePath: EXEC, args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
let failed = 0;

for (const id of ids) {
  await page.goto(`${BASE}/#/interactive/${id}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);
  await page.locator('.av-demo-frame').scrollIntoViewIfNeeded().catch(() => {});
  await page.waitForTimeout(700);
  const frame = page.frames().find((f) => f.url().includes(`/interactive/${id}.html`));
  if (!frame) { console.log(`FAIL ${id}: no demo iframe`); failed++; continue; }
  const box = await page.locator('.av-demo-frame').boundingBox();
  if (!box || box.height < 300) { console.log(`FAIL ${id}: iframe too small ${JSON.stringify(box)}`); failed++; continue; }
  const before = await frame.evaluate(() => document.querySelector('canvas')?.toDataURL().length || 0);
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width * .7, box.y + box.height * .35, { steps: 8 });
  await page.waitForTimeout(250);
  await page.mouse.up();
  await page.waitForTimeout(500);
  const after = await frame.evaluate(() => document.querySelector('canvas')?.toDataURL().length || 0);
  const stat = await frame.evaluate(() => document.querySelector('#stat')?.textContent || null);
  const ok = after > 6000 && before !== after;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${id} iframe=${Math.round(box.width)}x${Math.round(box.height)} canvas=${before}->${after} stat=${stat}`);
  if (!ok) failed++;
}

await browser.close();
process.exit(failed ? 1 : 0);
