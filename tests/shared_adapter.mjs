import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";

const site = pathToFileURL(process.argv[2] + "/");
const values = new Map();
globalThis.localStorage = {
  getItem: (key) => values.get(key) ?? null,
  setItem: (key, value) => values.set(key, value),
};
const storage = await import(new URL("src/settings/storage.js", site));
assert.equal(storage.loadPreferences().theme, "system");
values.set("patterns.theme", "dark");
assert.equal(storage.loadPreferences().theme, "verdandi_alter");
values.set("patterns.editor", JSON.stringify({ theme: "light", font: "fira", indents: true, size: 18 }));
assert.deepEqual(storage.loadPreferences(), { theme: "verdandi", font: "fira_code", indents: "plain", size: 18 });
storage.savePreferences({ theme: "one_dark", size: 20 });
assert.equal(storage.loadPreferences().theme, "one_dark");
assert.equal(values.get("algorithms.preferences"), undefined);
storage.saveReading({ topic: "adapter", top: 120 });
assert.deepEqual(JSON.parse(storage.loadReading()), { topic: "adapter", top: 120 });

const { sourceHeader } = await import(new URL("src/code_viewer/source.js", site));
assert.ok(sourceHeader({ path: "x.py", side: "before" }).includes("Без паттерна"));
assert.ok(sourceHeader({ path: "x.py", side: "after" }).includes("С паттерном"));
assert.ok(sourceHeader({ path: "x.py", side: "after", common: true }).includes("Общий файл"));

globalThis.window = {};
await import(new URL("course-data.js", site));
const topics = window.COURSE_TOPICS;
assert.equal(topics.length, 25);
const { parseHash, hash } = await import(new URL("src/navigation/router.js", site));
globalThis.location = { hash: "#unknown/read" };
assert.equal(parseHash(topics, new Map()).topic, "strategy");
for (const legacy of ["#strategy/code", "#adapter/python/code", "#adapter/examples"]) {
  location.hash = legacy;
  const state = parseHash(topics, new Map());
  assert.equal(state.view, "read");
  assert.equal(state.section, "s2");
}
location.hash = "#adapter/implementation/base/main.py/main.py";
assert.equal(parseHash(topics, new Map()).view, "code");
for (const topic of topics) {
  location.hash = `#${topic.id}/code/base/operation/after`;
  const state = parseHash(topics, new Map());
  location.hash = hash(state);
  assert.deepEqual(parseHash(topics, new Map()), state);
}
console.log("Shared adapter: legacy preferences, reading, labels and all 25 canonical routes passed");
