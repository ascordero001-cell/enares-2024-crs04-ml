<script>
(() => {
  const key = "__stage04IdleGuardV1";
  if (window[key]) return;

  const signoutUrl = __STAGE04_SIGNOUT_URL__;
  const timeoutMs = 300_000;
  const guard = { lastActivityAt: Date.now(), expired: false };
  window[key] = guard;

  function expireIfIdle() {
    if (guard.expired || Date.now() - guard.lastActivityAt < timeoutMs) return;
    guard.expired = true;
    // Hide any previously rendered aggregate before attempting navigation.
    document.documentElement.style.visibility = "hidden";
    window.location.replace(signoutUrl);
  }

  function recordActivity() {
    if (guard.expired) return;
    expireIfIdle();
    if (!guard.expired) guard.lastActivityAt = Date.now();
  }

  for (const eventName of ["pointerdown", "keydown", "touchstart", "wheel"]) {
    document.addEventListener(eventName, recordActivity, { capture: true, passive: true });
  }
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) expireIfIdle();
  });
  window.addEventListener("pageshow", expireIfIdle);
  window.setInterval(expireIfIdle, 1000);
})();
</script>
