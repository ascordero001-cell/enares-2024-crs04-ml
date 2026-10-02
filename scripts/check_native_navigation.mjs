import { chromium } from "playwright";

const baseUrl = process.env.APP_URL ?? "http://127.0.0.1:8080";
const repeats = Number(process.env.NAV_REPEATS ?? 5);
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1536, height: 864 } });
const metrics = {};

function percentile(values, ratio) {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.ceil(sorted.length * ratio) - 1];
}

async function ready(moduleId, topicId, title) {
  try {
    await page.waitForFunction(({ moduleId, topicId, title }) => {
    const url = new URL(window.location.href);
    const selected = document.querySelector('.st-key-stage04_topic_catalog [role="radio"][aria-checked="true"]');
    return url.searchParams.get("view") === `Módulo ${moduleId}`
      && url.searchParams.get("topic") === topicId
      && document.querySelector('.section-head.topic h2')?.textContent?.includes(title)
      && selected?.textContent?.includes(title);
    }, { moduleId, topicId, title }, { timeout: 30000 });
  } catch (error) {
    const state = await page.evaluate(() => ({
      url: window.location.href,
      heading: document.querySelector('.section-head.topic h2')?.textContent,
      selected: document.querySelector('.st-key-stage04_topic_catalog [role="radio"][aria-checked="true"]')?.textContent,
      radios: [...document.querySelectorAll('.st-key-stage04_topic_catalog [role="radio"]')].slice(0, 4).map((radio) => ({
        text: radio.textContent,
        checked: radio.getAttribute('aria-checked'),
      })),
    }));
    throw new Error(`Navigation did not settle: ${JSON.stringify(state)}`, { cause: error });
  }
}

async function record(name, action, target) {
  const epoch = await page.evaluate(() => performance.timeOrigin);
  const start = performance.now();
  await action();
  await ready(...target);
  const elapsed = performance.now() - start;
  if (await page.evaluate(() => performance.timeOrigin) !== epoch) {
    throw new Error(`${name}: full document reload`);
  }
  (metrics[name] ??= []).push(elapsed);
}

try {
  await page.goto(`${baseUrl}?view=M%C3%B3dulo+3.1&topic=3.1.01`, { waitUntil: "networkidle" });
  await ready("3.1", "3.1.01", "Normalizan que madre o padre golpeen");
  const cards = page.locator('.st-key-stage04_module_cards button');
  const topics = page.locator('.st-key-stage04_topic_catalog [role="radio"]');
  const tabs = page.locator('.st-key-stage04_visible_tab [role="radio"]');
  if (await cards.count() !== 6 || await topics.count() !== 11 || await tabs.count() !== 11) {
    throw new Error("Native module, topic or tab controls are missing");
  }
  if (await page.locator('.st-key-stage04_topic_fast_nav, .st-key-stage04_navigation_bridge').count()) {
    throw new Error("A hidden or duplicate navigation control remains");
  }

  for (let i = 0; i < repeats; i += 1) {
    await record("card_click", () => cards.nth(1).click(), ["3.2", "3.2.01", "Violencia psicológica ejercida en el hogar"]);
    await cards.nth(0).click();
    await ready("3.1", "3.1.01", "Normalizan que madre o padre golpeen");
    await record("card_enter", async () => { await cards.nth(1).focus(); await cards.nth(1).press("Enter"); }, ["3.2", "3.2.01", "Violencia psicológica ejercida en el hogar"]);
    await record("topic_click", () => topics.nth(2).click(), ["3.2", "3.2.03", "Violencia física ejercida en el hogar"]);
    await topics.nth(0).click();
    await ready("3.2", "3.2.01", "Violencia psicológica ejercida en el hogar");
    await record("topic_enter", async () => { await topics.nth(2).focus(); await topics.nth(2).press("Enter"); }, ["3.2", "3.2.03", "Violencia física ejercida en el hogar"]);
    await topics.nth(0).click();
    await ready("3.2", "3.2.01", "Violencia psicológica ejercida en el hogar");
    await record("tab_click", () => tabs.filter({ hasText: "3.3" }).click(), ["3.3", "3.3.01", "Víctimas de violencia psicológica"]);
    await tabs.filter({ hasText: "3.2" }).click();
    await ready("3.2", "3.2.01", "Violencia psicológica ejercida en el hogar");
    await record("tab_enter", async () => { const tab = tabs.filter({ hasText: "3.3" }); await tab.focus(); await tab.press("Enter"); }, ["3.3", "3.3.01", "Víctimas de violencia psicológica"]);
    await tabs.filter({ hasText: "3.1" }).click();
    await ready("3.1", "3.1.01", "Normalizan que madre o padre golpeen");
  }

  await page.goto(`${baseUrl}?view=M%C3%B3dulo+3.2&topic=3.2.03`, { waitUntil: "networkidle" });
  await ready("3.2", "3.2.03", "Violencia física ejercida en el hogar");
  await page.reload({ waitUntil: "networkidle" });
  await ready("3.2", "3.2.03", "Violencia física ejercida en el hogar");
  await topics.nth(0).click();
  await ready("3.2", "3.2.01", "Violencia psicológica ejercida en el hogar");
  await page.goBack({ waitUntil: "domcontentloaded" });
  await ready("3.2", "3.2.03", "Violencia física ejercida en el hogar");
  await page.goForward({ waitUntil: "domcontentloaded" });
  await ready("3.2", "3.2.01", "Violencia psicológica ejercida en el hogar");

  let tooSlow = false;
  for (const [name, samples] of Object.entries(metrics)) {
    const sorted = [...samples].sort((a, b) => a - b);
    const median = percentile(sorted, 0.5);
    const p95 = percentile(sorted, 0.95);
    const max = sorted.at(-1);
    console.log(`${name}: median=${Math.round(median)}ms p95=${Math.round(p95)}ms max=${Math.round(max)}ms n=${samples.length}`);
    if (median > 2000 || p95 > 2000 || max > 2000) tooSlow = true;
  }
  if (tooSlow) throw new Error("Native navigation exceeded the 2-second technical objective");
  console.log("PASS: native controls, direct URL, reload, back/forward and latency");
} finally {
  await browser.close();
}
