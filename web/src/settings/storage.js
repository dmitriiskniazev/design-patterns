import { createStorage } from "./store.js";

export const {
  readStored, writeStored, loadPreferences, savePreferences, loadReading, saveReading,
} = createStorage("patterns", {
  migrate(readStored) {
    const old = JSON.parse(readStored("editor") || "null");
    if (!old) return { theme: readStored("theme") === "dark" ? "verdandi_alter" : "system" };
    return {
      ...old,
      theme: old.theme === "dark" ? "verdandi_alter" : old.theme === "light" ? "verdandi" : "system",
      font: { jetbrains: "jetbrains_mono", fira: "fira_code" }[old.font] || "jetbrains_mono",
      indents: old.indents ? "plain" : "off",
    };
  },
});
