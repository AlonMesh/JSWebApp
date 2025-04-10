const isProd = process.env.MODE === "production";

export const API_BASE = isProd
  ? "https://jswebapp-production.up.railway.app"
  : "http://localhost:8000";

export const WS_BASE = isProd
  ? "wss://jswebapp-production.up.railway.app"
  : "ws://localhost:8000";
