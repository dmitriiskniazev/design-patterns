export function sourceFor(guide, ref) {
  return ref ? guide.sources.find((source) => source.id === ref.id) : null;
}

export function workspaceSelection(guide, selection = {}) {
  const mode = guide.workspaces[selection.mode] ? selection.mode : "base";
  const workspace = guide.workspaces[mode];
  function legacyName(side, name) {
    const version = guide.versions[guide.pairs[mode][side]];
    return (
      guide.variantFileAliases?.[version.key]?.[name] ||
      guide.fileAliases?.[name] ||
      name
    );
  }
  const before = legacyName("before", selection.beforeFile);
  const after = legacyName("after", selection.afterFile);
  const pairId = guide.pairAliases?.[selection.pairId] || selection.pairId;
  const pair =
    workspace.pairs.find((pair) => pair.id === pairId) ||
    workspace.pairs.find(
      (pair) => pair.before?.name === before && pair.after?.name === after,
    ) ||
    workspace.pairs.find((pair) => after && pair.after?.name === after) ||
    workspace.pairs.find((pair) => before && pair.before?.name === before) ||
    workspace.pairs[0];
  return {
    mode,
    workspace,
    pair,
    side: pair[selection.side === "before" ? "before" : "after"]
      ? selection.side === "before"
        ? "before"
        : "after"
      : pair.after
        ? "after"
        : "before",
  };
}

export function pairForPaths(guide, beforePath, afterPath) {
  for (const [mode, workspace] of Object.entries(guide.workspaces)) {
    const pair = workspace.pairs.find(
      (pair) =>
        pair.before?.path === beforePath && pair.after?.path === afterPath,
    );
    if (pair) return { mode, pairId: pair.id };
  }
  for (const [mode, workspace] of Object.entries(guide.workspaces)) {
    const pair = workspace.pairs.find(
      (pair) =>
        pair.after?.path === afterPath || pair.before?.path === beforePath,
    );
    if (pair) return { mode, pairId: pair.id };
  }
  return { mode: "base", pairId: guide.workspaces.base.defaultPair };
}
