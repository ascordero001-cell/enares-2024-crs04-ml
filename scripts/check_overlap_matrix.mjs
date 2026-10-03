import { mkdir } from "node:fs/promises";
import { chromium } from "playwright";

const baseUrl = process.env.APP_URL ?? "http://127.0.0.1:8080";
const artifactDir = process.env.UI_ARTIFACT_DIR ?? "artifacts/ui-overlap";
const authToken = process.env.APP_AUTH_TOKEN;
const authOptions = authToken ? { extraHTTPHeaders: { Authorization: `Bearer ${authToken}` } } : {};

await mkdir(artifactDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
try {
  const context = await browser.newContext({
    viewport: { width: 1536, height: 864 },
    colorScheme: "light",
    ...authOptions,
  });
  const page = await context.newPage();
  const response = await page.goto(
    `${baseUrl}?view=M%C3%B3dulo+3.4&topic=3.4.04`,
    { waitUntil: "networkidle" },
  );
  if (!response?.ok()) throw new Error(`HTTP ${response?.status()}`);
  await page.getByText("Coincidencia entre formas ICVAC de violencia sexual", { exact: true }).first().waitFor();
  await page.waitForFunction(() => document.querySelectorAll('[data-testid="stVegaLiteChart"]').length === 4);
  const table = page.locator(".st-key-stage04_center .table-wrap table.data").first();
  if (await table.locator("tbody tr").count() !== 16) {
    throw new Error("The V0 overlap table must contain all 16 approved rows");
  }
  const chartTexts = await page.locator('[data-testid="stVegaLiteChart"] svg text').allTextContents();
  if (!chartTexts.some((text) => text.includes("Forma observada"))) {
    throw new Error("Matrix x-axis did not render");
  }
  const groupTitles = await page.locator(".chart-group-head").allTextContents();
  for (const expected of [
    "Últimos 12 meses · matriz 2×2",
    "Últimos 12 meses · matriz 3×3",
    "Alguna vez en la vida · matriz 2×2",
    "Alguna vez en la vida · matriz 3×3",
  ]) {
    if (!groupTitles.some((title) => title.includes(expected))) {
      throw new Error(`Missing approved matrix group: ${expected}`);
    }
  }
  await table.scrollIntoViewIfNeeded();
  await page.screenshot({ path: `${artifactDir}/v0-overlap-1536.png`, fullPage: true });
  await page.locator(".chart-group-head").first().scrollIntoViewIfNeeded();
  await page.screenshot({ path: `${artifactDir}/v0-overlap-matrices-1536.png` });
  console.log("PASS: 16 approved V0 rows and four rendered, period-separated matrices");
  await context.close();
} finally {
  await browser.close();
}
