import { chromium } from "playwright";

const baseUrl = process.env.APP_URL ?? "http://127.0.0.1:8512";
const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
const browser = await chromium.launch({
  headless: true,
  ...(executablePath ? { executablePath } : {}),
});

const scenarios = [
  {
    name: "desktop",
    viewport: { width: 1440, height: 1000 },
    path: "docs/stage04/evidence/ui-entrypoint-desktop.png",
  },
  {
    name: "mobile",
    viewport: { width: 390, height: 844 },
    path: "docs/stage04/evidence/ui-entrypoint-mobile.png",
  },
];

try {
  for (const scenario of scenarios) {
    const context = await browser.newContext({ viewport: scenario.viewport });
    const page = await context.newPage();
    const pageErrors = [];
    page.on("pageerror", (error) => pageErrors.push(String(error)));
    const response = await page.goto(baseUrl, {
      waitUntil: "networkidle",
      timeout: 30_000,
    });
    await page.locator('[data-testid="stAppViewContainer"]').waitFor();
    await page.getByText("516 indicadores", { exact: false }).first().waitFor();
    if (!response?.ok() || pageErrors.length) {
      throw new Error(
        `${scenario.name}: status=${response?.status()} pageErrors=${pageErrors.length}`,
      );
    }
    await page.screenshot({ path: scenario.path, fullPage: true });
    console.log(`${scenario.name}: PASS -> ${scenario.path}`);
    await context.close();
  }
} finally {
  await browser.close();
}
