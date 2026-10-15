import assert from "node:assert/strict";
import test from "node:test";
import { identityEmailForAlias } from "../src/alias.mjs";

test("only the approved alias maps to the managed identity", () => {
  assert.equal(identityEmailForAlias("vigilancia", "managed@example.invalid"), "managed@example.invalid");
  assert.equal(identityEmailForAlias("other", "managed@example.invalid"), null);
  assert.equal(identityEmailForAlias("vigilancia", ""), null);
});
