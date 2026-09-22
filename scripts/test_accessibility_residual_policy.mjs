import assert from "node:assert/strict";

import {
  EXPECTED_STREAMLIT_SIDEBAR_RESIDUALS,
  assertExpectedStreamlitSidebarResiduals,
} from "./accessibility_residual_policy.mjs";

assert.equal(EXPECTED_STREAMLIT_SIDEBAR_RESIDUALS, 0);
assert.doesNotThrow(() => assertExpectedStreamlitSidebarResiduals(0));
assert.throws(
  () => assertExpectedStreamlitSidebarResiduals(1),
  /Expected exactly 0.*observed 1/,
);

console.log("PASS: accessibility residual count fails closed unless it is exactly 0");
