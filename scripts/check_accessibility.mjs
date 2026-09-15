import AxeBuilder from "@axe-core/playwright";
import { chromium } from "playwright";

const baseUrl = process.env.APP_URL ?? "http://127.0.0.1:8501";
const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
const pages = [
  "Resumen",
  "Módulo 3.1",
  "Módulo 3.2",
  "Módulo 3.3",
  "Módulo 3.4",
  "Módulo 3.5",
  "Módulo 3.6",
  "Metodología",
  "Estado del release",
];
const tags = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"];

const browser = await chromium.launch({
  headless: true,
  ...(executablePath ? { executablePath } : {}),
});

let failed = false;
let acceptedStreamlitResiduals = 0;
try {
  for (const pageName of pages) {
    const context = await browser.newContext({
      viewport: { width: 1280, height: 900 },
    });
    const page = await context.newPage();
    const url = new URL(baseUrl);
    url.searchParams.set("page", pageName);
    url.searchParams.set("dimension", "Nacional");
    await page.goto(url.toString(), { waitUntil: "networkidle" });
    await page.locator('[data-testid="stAppViewContainer"]').waitFor();

    const result = await new AxeBuilder({ page }).withTags(tags).analyze();
    const actionable = result.violations.flatMap((violation) => {
      const remainingNodes = violation.nodes.filter((node) => {
        const streamlitSidebarResidual =
          violation.id === "aria-allowed-attr" &&
          node.target.some((target) => target === ".stSidebar") &&
          node.failureSummary?.includes('aria-expanded="true"');
        if (streamlitSidebarResidual) {
          acceptedStreamlitResiduals += 1;
        }
        return !streamlitSidebarResidual;
      });
      return remainingNodes.length ? [{ ...violation, nodes: remainingNodes }] : [];
    });
    console.log(`${pageName}: ${actionable.length} actionable violation(s)`);
    for (const violation of actionable) {
      failed = true;
      console.error(`- ${violation.id}: ${violation.help}`);
      for (const node of violation.nodes) {
        console.error(`  ${node.target.join(" ")}: ${node.failureSummary ?? ""}`);
      }
    }
    await context.close();
  }
} finally {
  await browser.close();
}

if (failed) {
  process.exitCode = 1;
} else {
  console.log(
    `PASS: no actionable WCAG 2.2 AA violations; ` +
      `${acceptedStreamlitResiduals} known Streamlit sidebar occurrence(s) recorded`,
  );
}
