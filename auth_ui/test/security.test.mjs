import assert from "node:assert/strict";
import test from "node:test";
import { contentSecurityPolicy, pilotOriginFromUrl } from "../src/security.mjs";

test("pilot cookie target is an explicit CSP connect source", () => {
  const url = "https://enares-stage04-iap-pilot.example.run.app/?topic=3.1.01";
  assert.equal(pilotOriginFromUrl(url), "https://enares-stage04-iap-pilot.example.run.app");
  assert.match(
    contentSecurityPolicy(url),
    /connect-src[^;]+ https:\/\/enares-stage04-iap-pilot\.example\.run\.app/,
  );
});

test("invalid or credential-bearing pilot URLs do not enter the CSP", () => {
  for (const url of ["http://example.run.app", "https://user:pass@example.run.app", "not a url"]) {
    assert.equal(pilotOriginFromUrl(url), null);
    assert.doesNotMatch(contentSecurityPolicy(url), /example\.run\.app/);
  }
});
