import assert from "node:assert/strict";

import {
  EXPECTED_STREAMLIT_SIDEBAR_RESIDUALS,
  assertExpectedStreamlitSidebarResiduals,
} from "./accessibility_residual_policy.mjs";

assert.equal(EXPECTED_STREAMLIT_SIDEBAR_RESIDUALS, 9);
assert.doesNotThrow(() => assertExpectedStreamlitSidebarResiduals(9));
assert.throws(
  () => assertExpectedStreamlitSidebarResiduals(8),
  /Expected exactly 9.*observed 8/,
);
assert.throws(
  () => assertExpectedStreamlitSidebarResiduals(10),
  /Expected exactly 9.*observed 10/,
);

console.log("PASS: accessibility residual count fails closed unless it is exactly 9");
