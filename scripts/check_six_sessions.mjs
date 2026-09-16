import { chromium } from "playwright";

const baseUrl = process.env.APP_URL ?? "http://127.0.0.1:8501";
const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
const timeoutMs = 30_000;
const scenarios = [
  {
    id: "S01",
    page: "Resumen",
    dimension: "Nacional",
    expected: "Resumen nacional · Módulo 3.2",
  },
  {
    id: "S02",
    page: "Módulo 3.1",
    dimension: "Nacional",
    expected: "Quién realiza tareas en el hogar",
  },
  {
    id: "S03",
    page: "Módulo 3.2",
    dimension: "Nacional",
    expected: "Estados visuales didácticos",
    action: async (page) => {
      await page.getByText("Demo sintético", { exact: true }).click();
    },
  },
  {
    id: "S04",
    page: "Módulo 3.5",
    dimension: "Nacional",
    expected: "Matrices de solapamiento de violencia sexual",
  },
  {
    id: "S05",
    page: "Módulo 3.2",
    dimension: "Departamento",
    expected: "Departamento: sin datos autorizados",
  },
  {
    id: "S06",
    page: "Metodología",
    dimension: "Nacional",
    expected: "Metodología y límites",
  },
];

if (scenarios.length !== 6 || new Set(scenarios.map(({ id }) => id)).size !== 6) {
  throw new Error("Step 48 requires exactly six distinct browser sessions");
}

const browser = await chromium.launch({
  headless: true,
  ...(executablePath ? { executablePath } : {}),
});

const rssBefore = process.memoryUsage().rss;
const wallStarted = performance.now();

async function runScenario(scenario) {
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    extraHTTPHeaders: { "X-Enares-Test-Session": scenario.id },
  });
  const page = await context.newPage();
  const pageErrors = [];
  page.on("pageerror", (error) => pageErrors.push(String(error)));

  const url = new URL(baseUrl);
  url.searchParams.set("page", scenario.page);
  url.searchParams.set("dimension", scenario.dimension);
  const started = performance.now();

  try {
    const response = await page.goto(url.toString(), {
      waitUntil: "networkidle",
      timeout: timeoutMs,
    });
    await page.locator('[data-testid="stAppViewContainer"]').waitFor({
      state: "visible",
      timeout: timeoutMs,
    });
    if (scenario.action) {
      await scenario.action(page);
    }
    await page.getByText(scenario.expected, { exact: false }).first().waitFor({
      state: "visible",
      timeout: timeoutMs,
    });

    const browserMetrics = await page.evaluate(() => {
      const navigation = performance.getEntriesByType("navigation")[0];
      const memory = performance.memory;
      return {
        domCompleteMs: navigation ? Math.round(navigation.domComplete) : null,
        usedJsHeapBytes: memory ? memory.usedJSHeapSize : null,
      };
    });
    const elapsedMs = Math.round(performance.now() - started);
    if (!response?.ok() || pageErrors.length || elapsedMs > timeoutMs) {
      throw new Error(
        `${scenario.id} failed: status=${response?.status()} ` +
          `errors=${pageErrors.length} elapsedMs=${elapsedMs}`,
      );
    }
    return {
      id: scenario.id,
      page: scenario.page,
      dimension: scenario.dimension,
      status: response.status(),
      elapsedMs,
      ...browserMetrics,
    };
  } finally {
    await context.close();
  }
}

try {
  const results = await Promise.all(scenarios.map(runScenario));
  const wallMs = Math.round(performance.now() - wallStarted);
  const rssAfter = process.memoryUsage().rss;
  const sortedLatencies = results.map((result) => result.elapsedMs).sort((a, b) => a - b);
  const p95Index = Math.ceil(sortedLatencies.length * 0.95) - 1;
  const evidence = {
    result: "PASS",
    concurrentContexts: results.length,
    wallMs,
    latencyP95Ms: sortedLatencies[p95Index],
    driverRssDeltaBytes: rssAfter - rssBefore,
    cloudConsumption: "PENDING_CLOUD_RUN",
    instanceCount: "PENDING_CLOUD_RUN",
    sessions: results,
  };
  console.log(JSON.stringify(evidence, null, 2));
} finally {
  await browser.close();
}
