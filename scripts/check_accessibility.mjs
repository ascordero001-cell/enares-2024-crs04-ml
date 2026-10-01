import AxeBuilder from "@axe-core/playwright";
import { chromium } from "playwright";

import { assertExpectedStreamlitSidebarResiduals } from "./accessibility_residual_policy.mjs";

const baseUrl = process.env.APP_URL ?? "http://127.0.0.1:8501";
const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
const views = [
  { name: "Resumen nacional", selected: "Resumen nacional", content: "Resumen nacional" },
  ...["3.1", "3.2", "3.3", "3.4", "3.5", "3.6"].map((module) => ({
    name: `Módulo ${module}`,
    selected: module,
    content: `${module} ·`,
  })),
  { name: "Brechas", selected: "Brechas", content: "Solo cifras V0 existentes" },
  { name: "Calidad y notas", selected: "Calidad y notas", content: "Cómo leer los estados" },
  { name: "Estado del gate", selected: "Estado del gate", content: "Release agregado en shadow privado" },
  { name: "Historial", selected: "Historial", content: "Release vigente:" },
];
const tags = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"];

const browser = await chromium.launch({
  headless: true,
  ...(executablePath ? { executablePath } : {}),
});

let failed = false;
let acceptedStreamlitResiduals = 0;
try {
  for (const view of views) {
    const context = await browser.newContext({
      viewport: { width: 1280, height: 900 },
    });
    const page = await context.newPage();
    const pageErrors = [];
    page.on("pageerror", (error) => pageErrors.push(String(error)));
    const url = new URL(baseUrl);
    url.searchParams.set("view", view.name);
    const response = await page.goto(url.toString(), { waitUntil: "networkidle" });
    if (!response?.ok()) {
      throw new Error(`${view.name}: HTTP ${response?.status() ?? "no response"}`);
    }
    await page.locator('[data-testid="stAppViewContainer"]').waitFor();
    const selected = page.locator('[role="radiogroup"][aria-label="Vista"] [role="radio"][aria-checked="true"]');
    await selected.waitFor({ state: "visible" });
    const selectedName = (await selected.innerText()).trim();
    if (selectedName !== view.selected) {
      throw new Error(`${view.name}: opened ${selectedName} instead`);
    }
    const content = page.locator(".st-key-stage04_center");
    const expected = content.getByText(view.content, { exact: false });
    await expected.first().waitFor({ state: "visible" });
    const exceptions = await page.locator('[data-testid="stException"]').count();
    const errorMessages = await page.locator(
      '[data-testid="stAlertContentError"]',
    ).allTextContents();
    const unexpectedErrors = errorMessages.filter(
      (message) =>
        message.trim() !==
        "Suprimido — ningún campo estadístico protegido llega a la vista.",
    );
    if (exceptions || unexpectedErrors.length || pageErrors.length) {
      throw new Error(
        `${view.name}: ${exceptions} exception(s), ` +
          `${unexpectedErrors.length} unexpected Streamlit error(s), ` +
          `${pageErrors.length} page error(s)`,
      );
    }

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
    console.log(
      `${view.name}: selected, content loaded, no app errors, ` +
        `${actionable.length} actionable violation(s)`,
    );
    for (const violation of actionable) {
      failed = true;
      console.error(`- ${violation.id}: ${violation.help}`);
      for (const node of violation.nodes.slice(0, 12)) {
        console.error(`  ${node.target.join(" ")}: ${node.failureSummary ?? ""}`);
      }
      if (violation.nodes.length > 12) {
        console.error(`  ... and ${violation.nodes.length - 12} more node(s)`);
      }
    }
    await context.close();
  }
} finally {
  await browser.close();
}

assertExpectedStreamlitSidebarResiduals(acceptedStreamlitResiduals);

if (failed) {
  process.exitCode = 1;
} else {
  console.log(
    `PASS: no actionable WCAG 2.2 AA violations; ` +
      `${acceptedStreamlitResiduals} known Streamlit sidebar occurrence(s) recorded`,
  );
}
