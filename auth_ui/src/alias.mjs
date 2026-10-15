export const VISIBLE_ALIAS = "vigilancia";

export function identityEmailForAlias(alias, configuredEmail) {
  if (alias !== VISIBLE_ALIAS || !configuredEmail || !configuredEmail.includes("@")) {
    return null;
  }
  return configuredEmail;
}
