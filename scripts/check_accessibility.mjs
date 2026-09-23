import AxeBuilder from "@axe-core/playwright";
import { chromium } from "playwright";

import { assertExpectedStreamlitSidebarResiduals } from "./accessibility_residual_policy.mjs";

const baseUrl = process.env.APP_URL ?? "http://127.0.0.1:8501";
const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
const views = [
  { name: "Resumen nacional", content: "Resultados visibles" },
  ...["3.1", "3.2", "3.3", "3.4", "3.5", "3.6"].map((module) => ({
    name: `Módulo ${module}`,
    content: `Módulo ${module}`,
    heading: true,
  })),
  { name: "Brechas", content: "no calcula diferencias nuevas" },
  { name: "Calidad y notas", content: "Cómo leer los estados" },
  { name: "Estado del gate", content: "Integración autorizada en shadow" },
  { name: "Historial", content: "Release vigente:" },
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
    if (selectedName !== view.name) {
      throw new Error(`${view.name}: opened ${selectedName} instead`);
    }
    const content = page.locator(".st-key-stage04_center");
    const expected = view.heading
      ? content.getByRole("heading", { name: view.content, exact: true })
      : content.getByText(view.content, { exact: false });
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
      for (const node of violation.nodes) {
        console.error(`  ${node.target.join(" ")}: ${node.failureSummary ?? ""}`);
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
