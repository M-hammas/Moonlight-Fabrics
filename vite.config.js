import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "node:path";

// Keep Vite strictly inside this project directory.
// This prevents Vite from discovering a package/workspace in the Windows
// user folder and accidentally watching locked AppData files.
const projectRoot = process.cwd();

export default defineConfig({
  root: projectRoot,

  base: "/Moonlight-Fabrics/",

  plugins: [react()],

  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: false,

    // Never allow Vite to watch files outside this project.
    fs: {
      strict: true,
      allow: [projectRoot],
    },

    // Windows-safe watcher.
    watch: {
      usePolling: true,
      interval: 200,
      ignored: [
        "**/node_modules/**",
        "**/.git/**",
        "**/backend/**",
        "**/dist/**",
        "**/build/**",
      ],
    },
  },

  optimizeDeps: {
    // Start dependency scanning from the real app entry only.
    entries: [resolve(projectRoot, "index.html")],
    force: false,
  },

  preview: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: false,
  },
});
