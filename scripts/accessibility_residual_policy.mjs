// The canonical redesigned entrypoint renders without the legacy Streamlit
// sidebar. Keep this fail-closed assertion so a residual cannot return unnoticed.
export const EXPECTED_STREAMLIT_SIDEBAR_RESIDUALS = 0;

export function assertExpectedStreamlitSidebarResiduals(actual) {
  if (actual !== EXPECTED_STREAMLIT_SIDEBAR_RESIDUALS) {
    throw new Error(
      `Expected exactly ${EXPECTED_STREAMLIT_SIDEBAR_RESIDUALS} known Streamlit ` +
        `sidebar residuals in the canonical entrypoint, observed ${actual}`,
    );
  }
}
