import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { runInNewContext } from "node:vm";

const template = readFileSync(new URL("../../app/views/idle_guard.js", import.meta.url), "utf8");
const signoutUrl = "https://pilot.example.test?gcp-iap-mode=GCIP_SIGNOUT";
const script = template
  .replace(/^<script>\s*/, "")
  .replace(/\s*<\/script>\s*$/, "")
  .replace("__STAGE04_SIGNOUT_URL__", JSON.stringify(signoutUrl));

function browserGuard() {
  const listeners = new Map();
  let now = 0;
  let interval;
  let redirect = null;
  const document = {
    hidden: false,
    documentElement: { style: { visibility: "visible" } },
    addEventListener: (name, callback) => listeners.set(name, callback),
  };
  const window = {
    addEventListener: (name, callback) => listeners.set(name, callback),
    setInterval: (callback) => { interval = callback; },
    location: { replace: (url) => { redirect = url; } },
  };
  const context = { window, document, Date: { now: () => now } };
  runInNewContext(script, context);
  return {
    document,
    listeners,
    advance: (time) => { now = time; },
    tick: (time) => { now = time; interval(); },
    rerender: () => runInNewContext(script, context),
    get redirect() { return redirect; },
  };
}

test("exactly 300 seconds idle hides results before IAP sign-out", () => {
  const guard = browserGuard();
  guard.tick(299_999);
  assert.equal(guard.redirect, null);
  guard.tick(300_000);
  assert.equal(guard.document.documentElement.style.visibility, "hidden");
  assert.equal(guard.redirect, signoutUrl);
});

test("real activity extends the timer, but rerenders do not", () => {
  const guard = browserGuard();
  guard.tick(200_000);
  guard.listeners.get("keydown")();
  guard.rerender();
  guard.tick(499_999);
  assert.equal(guard.redirect, null);
  guard.tick(500_000);
  assert.equal(guard.redirect, signoutUrl);
});

test("returning to a background tab expires before its next interaction", () => {
  const guard = browserGuard();
  guard.document.hidden = false;
  guard.tick(299_000);
  // The browser may throttle interval timers in a hidden tab.
  guard.listeners.get("visibilitychange")();
  assert.equal(guard.redirect, null);
  guard.advance(301_000);
  guard.listeners.get("visibilitychange")();
  assert.equal(guard.redirect, signoutUrl);
});
