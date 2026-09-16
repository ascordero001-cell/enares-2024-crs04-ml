// This exception is pinned to Streamlit 1.63.0. Revalidate the signature and
// expected count before changing the pinned runtime version.
export const EXPECTED_STREAMLIT_SIDEBAR_RESIDUALS = 9;

export function assertExpectedStreamlitSidebarResiduals(actual) {
  if (actual !== EXPECTED_STREAMLIT_SIDEBAR_RESIDUALS) {
    throw new Error(
      `Expected exactly ${EXPECTED_STREAMLIT_SIDEBAR_RESIDUALS} known Streamlit ` +
        `1.63.0 sidebar residuals, observed ${actual}`,
    );
  }
}
