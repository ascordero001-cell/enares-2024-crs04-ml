import { initializeApp } from "firebase/app";
import {
  inMemoryPersistence,
  getAuth,
  setPersistence,
  signInWithEmailAndPassword,
} from "firebase/auth";
import * as ciap from "gcip-iap";
import { identityEmailForAlias } from "./alias.mjs";

const form = document.getElementById("login-form");
const status = document.getElementById("status");
const button = document.getElementById("submit");
const configResponse = await fetch("/config", { cache: "no-store" }).catch(() => null);
if (!configResponse?.ok) {
  showError("El servicio de acceso no está disponible. Intenta nuevamente más tarde.");
  throw new Error("Access configuration unavailable");
}
const config = await configResponse.json();
let authInstance;
let attempts = 0;
let blockedUntil = 0;

function showError(message) {
  status.textContent = message;
  status.hidden = false;
}

class Stage04AuthHandler {
  getAuth(apiKey, tenantId) {
    if (apiKey !== config.apiKey || tenantId !== null) {
      throw new Error("Unexpected identity project or tenant");
    }
    if (!authInstance) {
      const app = initializeApp({ apiKey, authDomain: config.authDomain });
      authInstance = getAuth(app);
    }
    return authInstance;
  }

  startSignIn(auth) {
    form.hidden = false;
    button.disabled = false;
    return new Promise((resolve) => {
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (Date.now() < blockedUntil) {
          showError("Espera un momento antes de volver a intentar.");
          return;
        }
        const username = document.getElementById("username").value.trim();
        const passwordField = document.getElementById("password");
        const password = passwordField.value;
        const email = identityEmailForAlias(username, config.identityEmail);
        button.disabled = true;
        status.hidden = true;
        try {
          if (!email) {
            throw new Error("Invalid credentials");
          }
          // Never reuse credentials across tabs or after an IAP sign-out.
          await setPersistence(auth, inMemoryPersistence);
          const credential = await signInWithEmailAndPassword(auth, email, password);
          passwordField.value = "";
          attempts = 0;
          resolve(credential);
        } catch {
          passwordField.value = "";
          // Fixed event only: no username, password, or Firebase error detail.
          void fetch("/auth-failure", { method: "POST", keepalive: true }).catch(() => {});
          attempts += 1;
          if (attempts >= 3) {
            blockedUntil = Date.now() + Math.min(60_000, 5_000 * 2 ** (attempts - 3));
          }
          showError("Usuario o contraseña incorrectos.");
        } finally {
          button.disabled = false;
        }
      });
    });
  }

  handleError() {
    showError("No se pudo completar el acceso. Vuelve a intentarlo.");
  }

  completeSignOut() {
    form.hidden = false;
    showError("Sesión cerrada. Ingresa nuevamente.");
  }
}

new ciap.Authentication(new Stage04AuthHandler()).start();
