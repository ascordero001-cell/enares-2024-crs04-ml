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
    { width: 1536, height: 864 },
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
    if (container.width > 1600) throw new Error(`${viewport.width}: container too wide`);
    if (left.width > 210 || right.width > 220 || center.width < viewport.width / 2) {
      throw new Error(`${viewport.width}: rail/center widths ${left.width}/${center.width}/${right.width}`);
    }
    close(center.x - (left.x + left.width), 18, 4, `${viewport.width}: left gap`);
    close(right.x - (center.x + center.width), 18, 4, `${viewport.width}: right gap`);
    close(left.y, center.y, 4, `${viewport.width}: top alignment`);
    close(right.y, center.y, 4, `${viewport.width}: top alignment`);
    const cards = page.locator('.st-key-stage04_module_cards button');
    await page.waitForFunction(() => document.querySelectorAll('.st-key-stage04_module_cards button').length === 6);
    if (await cards.count() !== 6) throw new Error("Expected six module cards");
    const cardBoxes = await Promise.all(Array.from({ length: 6 }, (_, index) => cards.nth(index).boundingBox()));
    if (cardBoxes.some((item) => !item || Math.abs(item.y - cardBoxes[0].y) > 2)) {
      throw new Error(`${viewport.width}: cards are not on one row`);
    }
    for (let index = 0; index < 6; index += 1) {
      const overflow = await cards.nth(index).evaluate((node) => node.scrollWidth > node.clientWidth + 1);
      if (overflow) throw new Error(`${viewport.width}: card ${index + 1} overflows`);
      const text = await cards.nth(index).innerText();
      if ((index === 0 && text.includes('(últimos 12 meses)')) || (index > 0 && !text.includes('(últimos 12 meses)'))) {
        throw new Error(`${viewport.width}: card ${index + 1} reference period`);
      }
    }
    const tabs = page.locator('.st-key-stage04_visible_tab [role="radio"]');
    // A remote Streamlit session can render the header and cards before its
    // segmented control replaces the loading skeleton.
    await page.waitForFunction(
      () => document.querySelectorAll('.st-key-stage04_visible_tab [role="radio"]').length === 11,
      null,
      { timeout: 30000 },
    );
    if (await tabs.count() !== 11) throw new Error(`${viewport.width}: expected 11 tabs`);
    const tabOverflow = await page.locator('.st-key-stage04_visible_tab').evaluate(
      (node) => node.scrollWidth > node.clientWidth + 1,
    );
    if (tabOverflow) throw new Error(`${viewport.width}: tabs overflow`);
    const paper = await page.locator(".stApp").evaluate((node) => getComputedStyle(node).backgroundColor);
    if (paper !== "rgb(241, 244, 249)") throw new Error(`Paper color: ${paper}`);
    const basePanel = page.locator('.st-key-stage04_base_panel');
    const baseText = await basePanel.innerText();
    if (!baseText.includes('3\u00a0014') || /3\s*\/\s*014/.test(baseText)) {
      throw new Error(`${viewport.width}: V0 base count split or missing`);
    }
    const baseOverflow = await basePanel.evaluate((node) => node.scrollWidth > node.clientWidth + 1);
    if (baseOverflow) throw new Error(`${viewport.width}: V0 base panel overflows`);
    const downloads = page.locator('.st-key-stage04_export_panel [data-testid="stDownloadButton"] button');
    await downloads.first().waitFor();
    const downloadLabels = await downloads.allTextContents();
    if (downloadLabels.map((value) => value.trim()).join('|') !== 'CSV|Excel') {
      throw new Error(`${viewport.width}: export labels ${JSON.stringify(downloadLabels)}`);
    }
    for (const button of await downloads.all()) {
      const overflow = await button.evaluate((node) => node.scrollWidth > node.clientWidth + 1);
      if (overflow) throw new Error(`${viewport.width}: export button overflows`);
    }
    await page.screenshot({ path: `${artifactDir}/stage04-${viewport.width}x${viewport.height}.png`, fullPage: true });
    if (viewport.width === 1536) {
      await page.screenshot({ path: `${artifactDir}/stage04-1536x864-viewport.png` });
    }
    const filters = await page.locator('.st-key-stage04_left_rail [data-testid="stSelectbox"] label').allTextContents();
    const expectedFilters = [
      "Departamento", "Ámbito de la IIEE", "Sexo", "Sexo × ámbito de la IIEE",
      "Idioma del hogar", "Autoidentificación étnica", "Vive con padres",
      "Discapacidad", "Otras características",
    ];
    if (filters.some((value, index) => value.trim() !== expectedFilters[index])) {
      throw new Error(`${viewport.width}: filter order/labels ${JSON.stringify(filters)}`);
    }
    await context.close();
  }

  for (const moduleId of modules) {
    const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
    const page = await context.newPage();
    await page.goto(baseUrl, { waitUntil: "networkidle" });
    await page.waitForFunction(
      () => document.querySelectorAll('.st-key-stage04_module_cards button').length === 6
        && document.querySelectorAll('.st-key-stage04_visible_tab [role="radio"]').length === 11,
      null,
      { timeout: 30000 },
    );
    const card = page.locator('.st-key-stage04_module_cards button').nth(modules.indexOf(moduleId));
    const documentEpoch = await page.evaluate(() => performance.timeOrigin);
    const navigationStart = performance.now();
    await card.focus();
    await card.press("Enter");
    await page.waitForURL(
      (value) => value.searchParams.get("view") === `Módulo ${moduleId}`
        && value.searchParams.get("topic") === `${moduleId}.01`,
      { timeout: 30000 },
    );
    await page.waitForFunction(
      (title) => document.querySelector('.section-head.topic h2')?.textContent?.includes(title),
      boundaryTitles[moduleId][0],
      { timeout: 30000 },
    );
    const navigationMs = Math.round(performance.now() - navigationStart);
    console.log(`${moduleId}: card-to-topic ${navigationMs} ms`);
    if (await page.evaluate(() => performance.timeOrigin) !== documentEpoch) {
      throw new Error(`${moduleId}: card caused a full document reload`);
    }
    const url = new URL(page.url());
    if (url.searchParams.get("view") !== `Módulo ${moduleId}` || url.searchParams.get("topic") !== `${moduleId}.01`) {
      throw new Error(`${moduleId}: card did not activate its first topic`);
    }
    const links = page.locator('.st-key-stage04_topic_catalog [role="radio"]');
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
    const catalogText = await page.locator('.st-key-stage04_topic_catalog').innerText();
    if (technicalCode.test(catalogText)) throw new Error(`${moduleId}: technical code in catalog`);
    const lastTitle = boundaryTitles[moduleId][1];
    const topicNavigationStart = performance.now();
    await links.last().focus();
    await links.last().press("Enter");
    const expectedLast = `${moduleId}.${String(counts[moduleId]).padStart(2, "0")}`;
    await page.waitForURL(
      (value) => value.searchParams.get("topic") === expectedLast,
      { timeout: 30000 },
    );
    await page.waitForFunction(
      (title) => document.querySelector('[data-testid="stage04-detail-sheet"]')?.textContent?.includes(title),
      lastTitle,
      { timeout: 30000 },
    );
    console.log(`${moduleId}: topic-to-detail ${Math.round(performance.now() - topicNavigationStart)} ms`);
    if (await page.evaluate(() => performance.timeOrigin) !== documentEpoch) {
      throw new Error(`${moduleId}: topic caused a full document reload`);
    }
    if (new URL(page.url()).searchParams.get("topic") !== expectedLast) {
      throw new Error(`${moduleId}: topic keyboard navigation failed`);
    }
    const body = await page.locator("body").innerText();
    if (/\d\.\d{2,}\s?%/.test(body)) throw new Error(`${moduleId}: percentage precision leaked`);
    if (/Código:/.test(body) || technicalCode.test(body)) throw new Error(`${moduleId}: technical code leaked`);
    if (body.includes("99.9%")) throw new Error(`${moduleId}: suppression sentinel leaked`);
    const sheet = await page.locator(".st-key-stage04_sheet_panel").innerText();
    for (const field of ["Módulo", "Tema", "Período", "Universo", "Denominador", "Corte", "Estado"]) {
      if (!sheet.toLocaleLowerCase("es").includes(field.toLocaleLowerCase("es"))) {
        throw new Error(`${moduleId}: missing sheet field ${field}`);
      }
    }
    await context.close();
  }

  const detailContext = await browser.newContext({ viewport: { width: 1536, height: 864 } });
  const detailPage = await detailContext.newPage();
  await detailPage.goto(`${baseUrl}?view=M%C3%B3dulo+3.2&topic=3.2.01`, { waitUntil: "networkidle" });
  await detailPage.locator(".chart-group-head").first().waitFor();
  if (!(await detailPage.locator('.chart-group-head').first().innerText()).includes('(últimos 12 meses)')) {
    throw new Error('3.2.01: chart period is missing from heading');
  }
  const topicTable = detailPage.locator('.table-wrap table.data').first();
  if (await topicTable.locator('th', { hasText: 'Período' }).count()) {
    throw new Error('3.2.01: period must be attached to the indicator, not a separate column');
  }
  if (!(await topicTable.locator('tbody td').first().innerText()).includes('(últimos 12 meses)')) {
    throw new Error('3.2.01: table indicator is missing its period');
  }
  await detailPage.waitForFunction(
    () => document.querySelector('[data-testid="stVegaLiteChart"] svg')?.querySelectorAll("text").length >= 26,
    null,
    { timeout: 30000 },
  );
  await detailPage.screenshot({ path: `${artifactDir}/stage04-1536-topic-3.2.01.png`, fullPage: true });
  await detailPage.screenshot({ path: `${artifactDir}/stage04-1536-topic-3.2.01-viewport.png` });
  const departments = [
    "Amazonas", "Áncash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca", "Callao",
    "Cusco", "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad", "Lambayeque",
    "Lima Metropolitana", "Loreto", "Madre de Dios", "Moquegua", "Pasco", "Piura",
    "Puno", "Región Lima", "San Martín", "Tacna", "Tumbes", "Ucayali",
  ];
  const chartLabels = await detailPage.locator('[data-testid="stVegaLiteChart"]').first().locator("svg text").allTextContents();
  for (const department of departments) {
    if (!chartLabels.includes(department)) throw new Error(`3.2.01: missing complete chart label ${department}`);
  }
  if (!await detailPage.getByRole("button", { name: "Volver a Nacional" }).isDisabled()) {
    throw new Error("3.2.01: reset should be disabled at national default");
  }
  if (!(await detailPage.locator(".table-wrap").first().innerText()).includes("Nacional")) {
    throw new Error("3.2.01: national default missing from table");
  }
  for (const [index, required, forbidden] of [
    [1, ["Urbano", "Rural"], ["1", "2"]],
    [4, ["Castellano", "Lengua originaria de los Andes: Quechua/Aymara"], ["1", "3", "Idioma extranjero / No sabe"]],
    [5, ["Blanco/Mestizo", "Otro / No sabe"], ["1", "3", "5", "6", "9"]],
    [6, ["Ambos", "Uno", "Ninguno"], ["1", "2", "3"]],
  ]) {
    const control = detailPage.locator('.st-key-stage04_left_rail [role="combobox"]').nth(index);
    await control.scrollIntoViewIfNeeded();
    await control.click();
    await detailPage.getByRole("option", { name: required[0], exact: true }).waitFor();
    const options = await detailPage.getByRole("option").allTextContents();
    for (const label of required) if (!options.includes(label)) throw new Error(`Filter ${index}: missing ${label}`);
    for (const label of forbidden) if (options.includes(label)) throw new Error(`Filter ${index}: raw code ${label}`);
    await detailPage.keyboard.press("Escape");
    await detailPage.getByRole("option").first().waitFor({ state: "hidden" });
  }
  for (const [selector, expected] of [
    [".section-head:not(.topic) h2", 18],
    [".section-head.topic h2", 15],
    [".table-wrap table.data", 12.6],
    [".st-key-stage04_visible_tab [role=radio]", 12.8],
    [".st-key-stage04_right_rail .ficha", 12.3],
  ]) {
    const size = await detailPage.locator(selector).first().evaluate((node) => parseFloat(getComputedStyle(node).fontSize));
    close(size, expected, 0.5, `3.2.01: font ${selector}`);
  }
  const tableFit = await detailPage.locator(".table-wrap").first().evaluate((node) => ({
    scroll: node.scrollWidth, client: node.clientWidth,
    nWhiteSpace: getComputedStyle(node.querySelector("td:nth-child(6)")).whiteSpace,
  }));
  if (tableFit.scroll > tableFit.client + 1 || tableFit.nWhiteSpace !== "nowrap") {
    throw new Error(`3.2.01: table overflow or N wraps ${JSON.stringify(tableFit)}`);
  }
  const filterPage = await detailContext.newPage();
  await filterPage.goto(`${baseUrl}?view=M%C3%B3dulo+3.2&topic=3.2.01`, { waitUntil: "networkidle" });
  const departmentControl = filterPage.locator('.st-key-stage04_left_rail [role="combobox"]').first();
  await departmentControl.scrollIntoViewIfNeeded();
  await departmentControl.click();
  await filterPage.getByRole("option", { name: "Callao" }).click();
  await filterPage.locator(".chart-group-head").filter({ hasText: "Departamento" }).waitFor();
  await filterPage.waitForFunction(() => document.querySelectorAll(".chart-group-head").length === 1);
  await filterPage.waitForFunction(() => document.querySelector(".table-wrap")?.textContent?.includes("Departamento · Callao"));
  if (!(await filterPage.locator(".table-wrap").first().innerText()).includes("Departamento · Callao")) {
    throw new Error("3.2.01: selected department missing from table");
  }
  await filterPage.getByRole("button", { name: "Volver a Nacional" }).click();
  await filterPage.waitForFunction(() => document.querySelector(".table-wrap")?.textContent?.includes("Nacional"));
  if (!await filterPage.getByRole("button", { name: "Volver a Nacional" }).isDisabled()) {
    throw new Error("3.2.01: reset did not clear active disaggregation");
  }
  await detailContext.close();

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
    await checkPage.locator('.st-key-stage04_topic_catalog').waitFor();
    for (const phrase of required) {
      await checkPage.locator(".st-key-stage04_center").getByText(phrase, { exact: false }).first().waitFor({ timeout: 30000 });
    }
    await checkContext.close();
  }
} finally {
  await browser.close();
}
  console.log("PASS: geometry, colors, six native cards, 80 topic controls, keyboard navigation, precision and disabled filters");
