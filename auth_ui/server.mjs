import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { contentSecurityPolicy, pilotOriginFromUrl } from "./src/security.mjs";

const port = Number(process.env.PORT || "8080");
const config = {
  apiKey: process.env.STAGE04_FIREBASE_API_KEY || "",
  authDomain: process.env.STAGE04_FIREBASE_AUTH_DOMAIN || "",
  identityEmail: process.env.STAGE04_IDP_EMAIL || "",
  pilotUrl: process.env.STAGE04_PILOT_URL || "",
};

const headers = {
  "cache-control": "no-store",
  "content-security-policy": contentSecurityPolicy(config.pilotUrl),
  "referrer-policy": "no-referrer",
  "x-content-type-options": "nosniff",
  "x-frame-options": "DENY",
};

const assets = new Map([
  ["/", ["index.html", "text/html; charset=utf-8"]],
  ["/bundle.js", ["bundle.js", "text/javascript; charset=utf-8"]],
]);
let lastFailureLogAt = 0;

createServer(async (request, response) => {
  const path = new URL(request.url, "http://localhost").pathname;
  if (path === "/auth-failure" && request.method === "POST") {
    // Never accept credentials or user-provided details into Cloud Logging.
    if (Date.now() - lastFailureLogAt >= 1000) {
      lastFailureLogAt = Date.now();
      console.warn(JSON.stringify({ severity: "WARNING", event: "stage04_login_denied" }));
    }
    response.writeHead(204, headers).end();
    return;
  }
  if (request.method !== "GET") {
    response.writeHead(405, headers).end();
    return;
  }
  if (path === "/healthz") {
    response.writeHead(200, { ...headers, "content-type": "text/plain" }).end("ok");
    return;
  }
  if (
    !config.apiKey || !config.authDomain || !config.identityEmail ||
    !pilotOriginFromUrl(config.pilotUrl)
  ) {
    response.writeHead(503, headers).end();
    return;
  }
  if (path === "/config") {
    response.writeHead(200, { ...headers, "content-type": "application/json" });
    response.end(JSON.stringify(config));
    return;
  }
  const asset = assets.get(path);
  if (!asset) {
    response.writeHead(404, headers).end();
    return;
  }
  try {
    const bytes = await readFile(new URL(`./public/${asset[0]}`, import.meta.url));
    response.writeHead(200, { ...headers, "content-type": asset[1] }).end(bytes);
  } catch {
    response.writeHead(503, headers).end();
  }
}).listen(port, "0.0.0.0");
