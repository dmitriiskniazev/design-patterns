import { escape } from "../dom.js";
import { hash } from "../navigation/router.js";
import { pairForPaths } from "../code_viewer/selection.js";
import { copySource } from "../code_viewer/clipboard.js";
import { sourceHeader } from "../code_viewer/source.js";
export function createLesson(context) {
  function guideDiagramPair(topic) {
    const diagrams = topic.guide.diagrams,
      id = `map-${topic.id}`,
      nodes = new Map(),
      refs = { before: new Map(), after: new Map() };
    for (const side of ["before", "after"])
      diagrams[side].nodes.forEach((node, index) => {
        const key = JSON.stringify([node.label, node.role]);
        if (!nodes.has(key))
          nodes.set(key, { ...node, key, row: index, sides: [] });
        const item = nodes.get(key);
        item.row = Math.max(item.row, index);
        item.sides.push(side);
        refs[side].set(node.id, item);
      });
    const width = 800,
      height = Math.max(...[...nodes.values()].map((n) => n.row)) * 76 + 86;
    const position = (node) => ({
      x: node.sides.length === 2 ? 245 : node.sides[0] === "before" ? 20 : 470,
      y: 30 + node.row * 76,
    });
    const edges = new Map();
    for (const side of ["before", "after"])
      for (const edge of diagrams[side].edges) {
        const a = refs[side].get(edge.from),
          b = refs[side].get(edge.to),
          key = JSON.stringify([a.key, b.key, edge.label]);
        if (!edges.has(key))
          edges.set(key, { a, b, label: edge.label, sides: [] });
        edges.get(key).sides.push(side);
      }
    const paths = [...edges.values()]
      .map((edge, i) => {
        const a = position(edge.a),
          b = position(edge.b),
          forward = b.y > a.y,
          shared = edge.sides.length === 2,
          side = edge.sides[0];
        const offset = (node) =>
          node.sides.length === 2 && !shared
            ? side === "before"
              ? -90
              : 90
            : 0;
        const ax = a.x + 155 + offset(edge.a),
          bx = b.x + 155 + offset(edge.b),
          ay = a.y + 44,
          by = b.y - 5;
        const adjacent = forward && b.y - a.y === 76,
          port = side === "before" ? 310 : 0,
          lane = side === "before" ? 375 : 425;
        const path = adjacent
          ? `M ${ax} ${ay} C ${ax} ${(ay + by) / 2}, ${bx} ${(ay + by) / 2}, ${bx} ${by}`
          : `M ${a.x + port} ${a.y + 22} C ${lane} ${a.y + 22}, ${lane} ${b.y + 22}, ${b.x + port + (port ? 6 : -6)} ${b.y + 22}`;
        const tx = adjacent
            ? (ax + bx) / 2
            : lane + (side === "before" ? -5 : 12),
          ty = adjacent ? (ay + by) / 2 - 4 : (a.y + b.y) / 2 + 22;
        return `<path class="guide-edge ${shared ? "shared" : side}" d="${path}" marker-end="url(#${id}-arrow)"/><text class="guide-edge-label" text-anchor="middle" x="${tx}" y="${ty}" ${adjacent ? "" : `transform="rotate(90 ${tx} ${ty})"`}>${escape(edge.label)}</text>`;
      })
      .join("");
    const boxes = [...nodes.values()]
      .map((node) => {
        const p = position(node),
          kind = node.sides.length === 2 ? "shared" : node.sides[0];
        return `<g class="guide-node ${kind}"><rect x="${p.x}" y="${p.y}" width="310" height="44" rx="5"/><text x="${p.x + 12}" y="${p.y + 18}" class="guide-node-name">${escape(node.label)}</text><text x="${p.x + 12}" y="${p.y + 34}" class="guide-node-role">${escape(node.role)}</text></g>`;
      })
      .join("");
    const description = ["before", "after"]
      .map(
        (side) =>
          `${side === "before" ? "Без паттерна" : "С паттерном"}: ` +
          diagrams[side].edges
            .map(
              (edge) =>
                `${diagrams[side].nodes.find((n) => n.id === edge.from).label} → ${diagrams[side].nodes.find((n) => n.id === edge.to).label}: ${edge.label}`,
            )
            .join("; "),
      )
      .join(". ");
    return `<figure class="guide-diagram guide-combined"><figcaption>Один вызов: где расходятся подходы <small>Общие участники показаны один раз в центре.</small></figcaption><svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="${id}-title ${id}-desc"><title id="${id}-title">${escape(topic.name)}: сравнение подходов</title><desc id="${id}-desc">${escape(description)}</desc><defs><marker id="${id}-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z"/></marker></defs><text x="175" y="18" text-anchor="middle" class="guide-column-label">Без паттерна</text><text x="625" y="18" text-anchor="middle" class="guide-column-label">С паттерном</text>${paths}${boxes}</svg></figure>`;
  }

  function codeLink(topic, contrast) {
    return hash({
      ...context.state,
      view: "code",
      ...pairForPaths(topic.guide, contrast.before.path, contrast.after.path),
      section: null,
    });
  }
  function comparison(topic, contrast, index) {
    return `<div class="short-comparison">${["before", "after"].map((side) => `<section class="short-side">${sourceHeader({ path: contrast[side].path, side, copyAttributes: `data-copy-snippet="${index}:${side}"` })}<div class="code-window"><pre tabindex="0"><code class="source-code">${contrast[side].html}</code></pre></div></section>`).join("")}</div><p class="comparison-explanation">${escape(contrast.explanation)}</p><a class="open-code" href="${codeLink(topic, contrast)}">Открыть полный код →</a>`;
  }
  function read(topic) {
    const g = topic.guide;
    const notes = [...new Set(g.designNotes)];
    return `<div class="reader"><section class="reader-section" data-section-target="s1"><h2>${escape(topic.task.title)}</h2><p class="reader-lead">${escape(g.goal)}</p><dl class="task-facts"><div><dt>Исходные данные</dt><dd>${escape(g.input)}</dd></div><div><dt>Ожидаемый результат</dt><dd>${escape(g.invariant)}</dd></div></dl></section>
    <section class="reader-section" data-section-target="s2"><h2>От прямого решения к паттерну</h2><p>${escape(topic.startingPoint)}</p>${comparison(topic, g.contrasts[0], 0)}<div class="reader-reasons">${notes
      .slice(0, 2)
      .map((note) => `<p>${escape(note)}</p>`)
      .join(
        "",
      )}</div><details class="reader-reference"><summary>Связи участников</summary>${guideDiagramPair(topic)}<dl>${[
      ...g.terms.map((term) => ({ name: term.term, purpose: term.definition })),
      ...g.roles,
    ]
      .filter(
        (item, index, all) =>
          all.findIndex((other) => other.name === item.name && other.purpose === item.purpose) === index,
      )
      .map(
        (role) =>
          `<dt>${escape(role.name)}</dt><dd>${escape(role.purpose)}</dd>`,
      )
      .join("")}</dl></details></section>
    <section class="reader-section" data-section-target="s3"><h2>Расширение решения</h2>${g.contrasts
      .slice(1)
      .map(
        (contrast, i) =>
          `<section class="reader-extension"><h3>${escape(contrast.title === "Одно расширение" ? topic.extension.title : contrast.title)}</h3>${comparison(topic, contrast, i + 1)}</section>`,
      )
      .join(
        "",
      )}<details class="reader-reference"><summary>Другие изменения требований</summary>${g.growth.map((row) => `<h3>${escape(row.change)}</h3><p><strong>baseline.</strong> ${escape(row.before)}</p><p><strong>pattern.</strong> ${escape(row.after)}</p><p>${escape(row.verdict)}</p>`).join("")}</details></section>
    <section class="reader-section" data-section-target="s4"><h2>Цена и ограничения</h2>${[...new Set([topic.cost, g.decision.use, g.decision.skip])].map((text) => `<p>${escape(text)}</p>`).join("")}<details class="reader-reference"><summary>Подробности применения</summary>${notes
      .slice(2)
      .map((note) => `<p>${escape(note)}</p>`)
      .join(
        "",
      )}${g.applications.map((item) => `<h3>${escape(item.case)}</h3><p>${escape(item.why)}</p>`).join("")}<h3>Путь вызова</h3><p>${escape(g.trace.input)}</p><p><strong>baseline.</strong> ${escape(g.trace.before)}</p><p><strong>pattern.</strong> ${escape(g.trace.after)}</p><p>${escape(g.trace.result)}</p></details><h3>Проверьте понимание</h3><p>${escape(topic.exercise)}</p><details class="reader-reference"><summary>Вопрос для собеседования</summary><p>${escape(topic.interview)}</p></details></section><p class="reader-source"><a href="${escape(topic.source)}" target="_blank" rel="noopener">Источник: ${escape(topic.name)} ↗</a></p></div>`;
  }
  function tabs() {
    return `<nav class="mode-tabs" role="tablist" aria-label="Режим главы">${[
      ["read", "Разбор"],
      ["code", "Код"],
    ]
      .map(
        ([view, label]) =>
          `<a id="chapter-tab-${view}" role="tab" aria-controls="lesson-body" aria-selected="${context.state.view === view}" tabindex="${context.state.view === view ? 0 : -1}" href="${hash({ ...context.state, view, section: null })}">${label}</a>`,
      )
      .join("")}</nav>`;
  }
  function bind(topic) {
    document.querySelectorAll("[data-copy-snippet]").forEach((button) =>
      button.addEventListener("click", () => {
        const [index, side] = button.dataset.copySnippet.split(":");
        copySource(button, topic.guide.contrasts[Number(index)][side].code);
      }),
    );
    document
      .querySelector(".mode-tabs")
      .addEventListener("keydown", (event) => {
        if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key))
          return;
        event.preventDefault();
        const tabs = [...document.querySelectorAll(".mode-tabs a")];
        const next =
          event.key === "Home"
            ? tabs[0]
            : event.key === "End"
              ? tabs.at(-1)
              : tabs.find((tab) => tab !== document.activeElement);
        next.focus();
        next.click();
      });
  }
  return { read, tabs, bind };
}
