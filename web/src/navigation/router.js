import { workspaceSelection } from "../code_viewer/selection.js";

export function parseHash(topics, sourceSelections) {
  let parts;
  try {
    parts = location.hash.slice(1).split("/").map(decodeURIComponent);
  } catch {
    parts = [];
  }
  const topic =
    topics.find((topic) => topic.id === parts[0]) ||
    topics.find((topic) => topic.id === "strategy");
  const language = ["cpp", "python"].includes(parts[1]),
    offset = language ? 2 : 1;
  const requested = parts[offset] || "read";
  let view = ["code", "implementation"].includes(requested) ? "code" : "read";
  let section =
    parts.slice(offset + 1).find((part) => /^s[1-5]$/.test(part)) || null;
  if (requested === "code" && (language || !["base", "extended"].includes(parts[offset + 1]))) {
    view = "read";
    section = section || "s2";
  }
  if (!section)
    section =
      { examples: "s2", extension: "s3", practice: "s4", theory: "s1" }[
        requested
      ] || null;
  if (section) view = section === "s5" ? "code" : "read";
  if (!topic.ready)
    return {
      topic: topic.id,
      view: "read",
      section: null,
      mode: "base",
      pairId: null,
      side: "after",
    };
  const previous = sourceSelections.get(topic.id) || {};
  let selection = { ...previous };
  const marker = parts[offset + 1];
  if (
    requested === "code" &&
    !language &&
    ["base", "extended"].includes(marker)
  ) {
    selection = {
      mode: marker,
      pairId: parts[offset + 2],
      side: parts[offset + 3],
    };
  } else if (requested === "implementation") {
    if (["base", "extended"].includes(marker))
      selection = {
        mode: marker,
        beforeFile: parts[offset + 2],
        afterFile: parts[offset + 3],
      };
    else if (marker === "extension")
      selection = {
        mode: "extended",
        side: parts[offset + 2] === "without-pattern" ? "before" : "after",
        beforeFile: parts[offset + 3],
        afterFile: parts[offset + 4],
      };
    else if (/^v[1-9]\d*$/.test(marker || "")) {
      const index =
        topic.guide.legacyVersionIndices[Number(marker.slice(1)) - 1] ?? 1;
      const version = topic.guide.versions[index],
        side = version.key.startsWith("before") ? "before" : "after";
      selection = {
        mode: version.extended ? "extended" : "base",
        side,
        [side + "File"]: parts[offset + 2],
      };
    }
  }
  const selected = workspaceSelection(topic.guide, selection);
  return {
    topic: topic.id,
    view,
    section,
    mode: selected.mode,
    pairId: selected.pair.id,
    side: selected.side,
  };
}

export function hash(selection) {
  const source =
    selection.view === "code"
      ? `/${selection.mode || "base"}/${encodeURIComponent(selection.pairId || "operation")}/${selection.side === "before" ? "before" : "after"}`
      : "";
  return `#${selection.topic}/${selection.view || "read"}${source}${selection.section ? "/" + selection.section : ""}`;
}
