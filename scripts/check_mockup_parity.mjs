import { mkdir } from "node:fs/promises";
import { chromium } from "playwright";

const baseUrl = process.env.APP_URL ?? "http://127.0.0.1:8080";
const artifactDir = process.env.UI_ARTIFACT_DIR ?? "artifacts/ui-parity";
const modules = ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6"];
const counts = { "3.1": 11, "3.2": 18, "3.3": 20, "3.4": 9, "3.5": 12, "3.6": 10 };
const boundaryTitles = {
  "3.1": ["Normalizan que madre o padre golpeen para corregir", "Creen que la violencia sexual ocurre más en sitios oscuros y solitarios"],
  "3.2": ["Violencia psicológica ejercida en el hogar por madre, padre o cuidadores", "Diferencia en la prevalencia de violencia física en el hogar frente a la categoría de referencia"],
  "3.3": ["Víctimas de violencia psicológica por parte de un compañero u otro estudiante", "Caracterización de la violencia física ejercida en la escuela"],
  "3.4": ["Reportaron al menos una situación de violencia sexual", "Caracterización de la violencia sexual frente a las categorías de referencia"],
  "3.5": ["Violencia psicológica y/o física en el hogar y en la escuela", "Número y tipo de consecuencias físicas y atención en salud"],
  "3.6": ["Recorrido de búsqueda y recepción de ayuda frente a la violencia en el hogar", "Institución a la que acudió por violencia sexual, ayuda recibida y conocimiento de la DEMUNA"],
};
const technicalCode = /\b(?:VF|VP|VS|PV|CONS)_[A-Z0-9_,]+\b|\bC\d+P\d+\b/i;

function close(actual, expected, tolerance, label) {
  if (Math.abs(actual - expected) > tolerance) {
    throw new Error(`${label}: expected ${expected}±${tolerance}, got ${actual}`);
  }
}

async function box(page, selector) {
  const result = await page.locator(selector).first().boundingBox();
  if (!result) throw new Error(`Missing visible element: ${selector}`);
  return result;
}

await mkdir(artifactDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
try {
  for (const viewport of [
    { width: 1920, height: 1080 },
    { width: 1366, height: 768 },
  ]) {
    const context = await browser.newContext({ viewport, colorScheme: "light" });
    const page = await context.newPage();
    const response = await page.goto(baseUrl, { waitUntil: "networkidle" });
    if (!response?.ok()) throw new Error(`HTTP ${response?.status()}`);
    await page.locator('[data-testid="stage04-exact-header"]').waitFor();
    const container = await box(page, ".block-container");
    const left = await box(page, ".st-key-stage04_left_rail");
    const center = await box(page, ".st-key-stage04_center");
    const right = await box(page, ".st-key-stage04_right_rail");
    close(container.width, 1360, 4, `${viewport.width}: container`);
    close(left.width, 270, 4, `${viewport.width}: left rail`);
    close(right.width, 272, 4, `${viewport.width}: right rail`);
    close(center.x - (left.x + left.width), 18, 4, `${viewport.width}: left gap`);
    close(right.x - (center.x + center.width), 18, 4, `${viewport.width}: right gap`);
    close(left.y, center.y, 4, `${viewport.width}: top alignment`);
    close(right.y, center.y, 4, `${viewport.width}: top alignment`);
    const cards = page.locator('[data-testid="stage04-module-cards"] .stripcard');
    if (await cards.count() !== 6) throw new Error("Expected six module cards");
    const paper = await page.locator(".stApp").evaluate((node) => getComputedStyle(node).backgroundColor);
    if (paper !== "rgb(241, 244, 249)") throw new Error(`Paper color: ${paper}`);
    await page.screenshot({ path: `${artifactDir}/stage04-${viewport.width}x${viewport.height}.png`, fullPage: true });
    await context.close();
  }

  for (const moduleId of modules) {
    const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
    const page = await context.newPage();
    await page.goto(baseUrl, { waitUntil: "networkidle" });
    const card = page.locator(`[data-testid="stage04-module-cards"] .stripcard[aria-label^="Abrir módulo ${moduleId}"]`);
    await card.focus();
    await card.press("Enter");
    await page.waitForLoadState("networkidle");
    await page.waitForURL(
      (value) => value.searchParams.get("topic") === `${moduleId}.01`,
      { timeout: 30000 },
    );
    const url = new URL(page.url());
    if (url.searchParams.get("view") !== `Módulo ${moduleId}` || url.searchParams.get("topic") !== `${moduleId}.01`) {
      throw new Error(`${moduleId}: card did not activate its first topic`);
    }
    const links = page.locator('[data-testid="stage04-topic-catalog"] .topic-link');
    await links.first().waitFor({ timeout: 30000 });
    if (await links.count() !== counts[moduleId]) {
      throw new Error(`${moduleId}: wrong topic count ${await links.count()}, url=${page.url()}`);
    }
    const normalize = (value) => value.replace(/\s+/g, " ").trim();
    if (normalize(await links.first().innerText()) !== boundaryTitles[moduleId][0]) {
      throw new Error(`${moduleId}: wrong first topic title`);
    }
    if (normalize(await links.last().innerText()) !== boundaryTitles[moduleId][1]) {
      throw new Error(`${moduleId}: wrong last topic title`);
    }
    const catalogText = await page.locator('[data-testid="stage04-topic-catalog"]').innerText();
    if (technicalCode.test(catalogText)) throw new Error(`${moduleId}: technical code in catalog`);
    await links.last().focus();
    await links.last().press("Enter");
    await page.waitForLoadState("networkidle");
    const expectedLast = `${moduleId}.${String(counts[moduleId]).padStart(2, "0")}`;
    await page.waitForURL(
      (value) => value.searchParams.get("topic") === expectedLast,
      { timeout: 30000 },
    );
    if (new URL(page.url()).searchParams.get("topic") !== expectedLast) {
      throw new Error(`${moduleId}: topic keyboard navigation failed`);
    }
    const body = await page.locator("body").innerText();
    if (/\d\.\d{2,}\s?%/.test(body)) throw new Error(`${moduleId}: percentage precision leaked`);
    if (/Código:/.test(body) || technicalCode.test(body)) throw new Error(`${moduleId}: technical code leaked`);
    if (body.includes("99.9%")) throw new Error(`${moduleId}: suppression sentinel leaked`);
    const sheet = await page.locator(".st-key-stage04_sheet_panel").innerText();
    for (const field of ["Módulo:", "Tema:", "Período:", "Universo:", "Denominador:", "Corte:", "Estado:"]) {
      if (!sheet.includes(field)) throw new Error(`${moduleId}: missing sheet field ${field}`);
    }
    await context.close();
  }

  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 }, colorScheme: "dark" });
  const page = await context.newPage();
  await page.goto(`${baseUrl}?view=M%C3%B3dulo+3.6&topic=3.6.01`, { waitUntil: "networkidle" });
  const controls = page.locator(".st-key-stage04_left_rail [role=combobox]");
  await controls.first().waitFor({ timeout: 30000 });
  if (await controls.count() !== 9) throw new Error("3.6: expected nine filters");
  for (let index = 0; index < 9; index += 1) {
    if (!await controls.nth(index).isDisabled()) throw new Error(`3.6: filter ${index + 1} is enabled`);
  }
  const paper = await page.locator(".stApp").evaluate((node) => getComputedStyle(node).backgroundColor);
  if (paper !== "rgb(241, 244, 249)") throw new Error(`Dark mode changed paper: ${paper}`);
  await context.close();

  for (const [topic, required] of [
    ["3.4.01", ["Últimos 12 meses", "Alguna vez en la vida"]],
    ["3.2.17", ["Conductas de riesgo personales"]],
  ]) {
    const moduleId = topic.slice(0, 3);
    const checkContext = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
    const checkPage = await checkContext.newPage();
    await checkPage.goto(`${baseUrl}?view=M%C3%B3dulo+${moduleId}&topic=${topic}`);
    await checkPage.locator('[data-testid="stage04-topic-catalog"]').waitFor();
    for (const phrase of required) {
      await checkPage.locator(".st-key-stage04_center").getByText(phrase, { exact: false }).first().waitFor({ timeout: 30000 });
    }
    await checkContext.close();
  }
} finally {
  await browser.close();
}
console.log("PASS: geometry, colors, six cards, 80 topic links, keyboard navigation, precision and disabled filters");
