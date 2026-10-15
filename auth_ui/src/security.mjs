export function pilotOriginFromUrl(value) {
  try {
    const parsed = new URL(value);
    if (parsed.protocol !== "https:" || parsed.username || parsed.password) {
      return null;
    }
    return parsed.origin;
  } catch {
    return null;
  }
}

export function contentSecurityPolicy(pilotUrl) {
  const pilotOrigin = pilotOriginFromUrl(pilotUrl);
  return [
    "default-src 'none'",
    "script-src 'self'",
    "style-src 'self' 'unsafe-inline'",
    `connect-src 'self' https://www.googleapis.com https://identitytoolkit.googleapis.com https://securetoken.googleapis.com https://iap.googleapis.com${pilotOrigin ? ` ${pilotOrigin}` : ""}`,
    "frame-src https://*.firebaseapp.com https://*.web.app",
    "form-action 'self'",
    "base-uri 'none'",
    "frame-ancestors 'none'",
  ].join("; ");
}
