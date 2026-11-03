import { $, escape } from "../dom.js";
import { hash } from "../navigation/router.js";
import { workspaceSelection, sourceFor } from "./selection.js";
import { copySource } from "./clipboard.js";
import { sourceHeader } from "./source.js";

export function createCodeViewer(context) {
  let observer = null,
    frame = 0,
    activeKey = null,
    selection = null,
    topic = null,
    compact = false;
  const positions = new Map();
  let scroll = null,
    comparison = null,
    lastAnchor = null;
  function visiblePane() {
    return comparison?.querySelector(
      `[data-pane="${selection.pair.common ? "after" : selection.side}"]`,
    );
  }
  function captureAnchor() {
    if (!scroll) return lastAnchor;
    const top = scroll.getBoundingClientRect().top;
    const rows = [
      ...(visiblePane()?.querySelectorAll("[data-row]") || []),
    ].filter((row) => row.offsetHeight);
    const row =
      rows.find((row) => row.getBoundingClientRect().bottom > top) ||
      rows.at(-1);
    return row
      ? {
          index: Number(row.dataset.row),
          offset: row.getBoundingClientRect().top - top,
        }
      : lastAnchor;
  }
  function restoreAnchor(anchor) {
    if (!anchor || !scroll) return;
    const rows = [
      ...(visiblePane()?.querySelectorAll("[data-row]") || []),
    ].filter((row) => row.offsetHeight);
    const row =
      rows.find((row) => Number(row.dataset.row) >= anchor.index) ||
      rows.at(-1);
    if (row)
      scroll.scrollTop +=
        row.getBoundingClientRect().top -
        scroll.getBoundingClientRect().top -
        anchor.offset;
  }
  function remember() {
    if (!scroll || !activeKey) return;
    positions.set(activeKey, {
      top: scroll.scrollTop,
      anchor: captureAnchor(),
      left: [...comparison.querySelectorAll(".pane-source")].map(
        (pane) => pane.scrollLeft,
      ),
    });
  }
  function prepareRender() {
    remember();
    observer?.disconnect();
    observer = null;
    cancelAnimationFrame(frame);
    frame = 0;
    scroll = null;
    comparison = null;
    activeKey = null;
  }
  function scheduleLayout() {
    if (frame || !comparison) return;
    frame = requestAnimationFrame(() => {
      frame = 0;
      if (!comparison.isConnected) return;
      const anchor = captureAnchor();
      const layout = $(".code-layout");
      layout.dataset.narrow = String(layout.clientWidth < 900);
      $(".code-workspace").dataset.narrow = layout.dataset.narrow;
      compact = comparison.clientWidth < 720;
      comparison.dataset.compact = String(compact);
      const before = [
        ...comparison.querySelectorAll('[data-pane="before"] [data-row]'),
      ];
      const after = [
        ...comparison.querySelectorAll('[data-pane="after"] [data-row]'),
      ];
      [...before, ...after].forEach((row) => (row.style.minHeight = ""));
      if (
        !compact &&
        !selection.pair.common &&
        document.documentElement.dataset.codeWrap === "true"
      ) {
        const heights = before.map((row, index) =>
          Math.max(
            row.getBoundingClientRect().height,
            after[index]?.getBoundingClientRect().height || 0,
          ),
        );
        before.forEach((row, index) => {
          row.style.minHeight = heights[index] + "px";
          if (after[index])
            after[index].style.minHeight = heights[index] + "px";
        });
      }
      restoreAnchor(anchor);
    });
  }
  function setDiff(value) {
    context.showSourceDiff = value;
    if (comparison) comparison.dataset.changes = String(value);
    $("#code-changes")?.setAttribute("aria-pressed", String(value));
  }
  function fileList(workspace, selected, mobile = false) {
    if (mobile)
      return `<label class="file-select-label">Файл<select id="code-file-select">${[
        false,
        true,
      ]
        .map(
          (common) =>
            `<optgroup label="${common ? "Общие файлы" : "Сравнение"}">${workspace.pairs
              .filter((pair) => pair.common === common)
              .map(
                (pair) =>
                  `<option value="${pair.id}" ${pair.id === selected ? "selected" : ""}>${escape(common ? (pair.after || pair.before).name : pair.label)}</option>`,
              )
              .join("")}</optgroup>`,
        )
        .join("")}</select></label>`;
    return [false, true]
      .map((common) => {
        const pairs = workspace.pairs.filter((pair) => pair.common === common);
        if (!pairs.length) return "";
        return `<section class="file-group"><h2>${common ? "Общие файлы" : "Сравнение"}</h2><ul>${pairs.map((pair) => `<li><a class="file-choice" data-pair="${pair.id}" href="${hash({ ...context.state, pairId: pair.id, section: null })}" ${pair.id === selected ? 'aria-current="page"' : ""}>${escape(common ? (pair.after || pair.before).name : pair.label)}</a></li>`).join("")}</ul></section>`;
      })
      .join("");
  }
  function paneHeader(pair, side) {
    const ref = pair[side];
    return sourceHeader({
      path: ref?.path,
      side,
      common: pair.common,
      copyAttributes: `data-copy-source="${ref?.id}" data-copy-side="${side}"`,
    });
  }
  function pane(pair, side) {
    if (!pair[side])
      return `<section class="pane-source pane-empty" data-pane="${side}"><p>В этой реализации файла нет.</p></section>`;
    return `<section class="pane-source code-window" data-pane="${side}" aria-label="${side === "before" ? "baseline" : "pattern"}: ${escape(pair[side].name)}"><pre tabindex="0"><code class="source-code">${pair.rows
      .map((row, index) => {
        const cell = row[side];
        return `<span class="code-row ${cell ? "row-" + cell.kind : "is-gap"}" data-row="${index}" ${cell ? `data-line="${cell.number}"` : 'aria-hidden="true"'}><span class="code-line-number" aria-hidden="true">${cell?.number || ""}</span><span class="code-line-content">${cell?.html || ""}</span></span>`;
      })
      .join("")}</code></pre></section>`;
  }
  function html(currentTopic) {
    const picked = workspaceSelection(currentTopic.guide, context.state),
      pair = picked.pair;
    const common = pair.common;
    return `<section class="code-workspace" aria-label="Просмотр исходников"><div class="code-toolbar">${currentTopic.guide.workspaces.extended ? `<label>Пример<select id="code-stage"><option value="base" ${picked.mode === "base" ? "selected" : ""}>Основной</option><option value="extended" ${picked.mode === "extended" ? "selected" : ""}>Расширенный</option></select></label>` : ""}${fileList(picked.workspace, pair.id, true)}<button type="button" id="code-changes" aria-pressed="${context.showSourceDiff}" ${common ? "disabled" : ""}>Изменения</button><details class="code-actions"><summary>Действия</summary><div><a href="${hash({ ...context.state, section: null })}">Ссылка на сравнение</a><h3>Запуск baseline</h3><code>${escape(picked.workspace.commands.before)}</code><h3>Запуск pattern</h3><code>${escape(picked.workspace.commands.after)}</code><h3>О файлах</h3>${["before", "after"].map((side) => (pair[side] ? `<p><strong>${side === "before" ? "baseline" : "pattern"}</strong><br>${escape(pair[side].path)}<br>${escape(pair[side].role)}</p>` : "")).join("")}</div></details></div><div class="code-layout"><nav class="file-tree" aria-label="Файлы примера">${fileList(picked.workspace, pair.id)}</nav><div class="code-comparison" data-common="${common}" data-side="${picked.side}" data-changes="${context.showSourceDiff}"><div class="mobile-sides" role="group" aria-label="Реализация">${["before", "after"].map((side) => `<button type="button" data-code-side="${side}" aria-pressed="${picked.side === side}" ${pair[side] ? "" : "disabled"}>${side === "before" ? "baseline" : "pattern"}</button>`).join("")}</div><div class="pane-headers">${common ? paneHeader(pair, "after") : paneHeader(pair, "before") + paneHeader(pair, "after")}</div><div class="code-scroll" tabindex="0" aria-label="Код выбранного сравнения"><div class="code-columns">${common ? pane(pair, "after") : pane(pair, "before") + pane(pair, "after")}</div></div></div></div></section>`;
  }
  function bind(currentTopic) {
    topic = currentTopic;
    selection = workspaceSelection(topic.guide, context.state);
    activeKey = `${topic.id}/${selection.mode}/${selection.pair.id}`;
    comparison = $(".code-comparison");
    scroll = $(".code-scroll");
    if (!comparison) return;
    const saved = positions.get(activeKey);
    if (saved) {
      scroll.scrollTop = saved.top;
      lastAnchor = saved.anchor;
      comparison
        .querySelectorAll(".pane-source")
        .forEach((pane, index) => (pane.scrollLeft = saved.left[index] || 0));
    } else lastAnchor = null;
    $("#code-stage")?.addEventListener("change", (event) => {
      location.hash = hash({
        ...context.state,
        mode: event.target.value,
        section: null,
      });
    });
    $("#code-file-select")?.addEventListener("change", (event) => {
      location.hash = hash({
        ...context.state,
        pairId: event.target.value,
        section: null,
      });
    });
    $("#code-changes").addEventListener("click", () =>
      setDiff(!context.showSourceDiff),
    );
    comparison.querySelectorAll("[data-code-side]").forEach((button) =>
      button.addEventListener("click", () => {
        const anchor = captureAnchor();
        selection.side = button.dataset.codeSide;
        context.state.side = selection.side;
        comparison.dataset.side = selection.side;
        comparison
          .querySelectorAll("[data-code-side]")
          .forEach((item) =>
            item.setAttribute(
              "aria-pressed",
              String(item.dataset.codeSide === selection.side),
            ),
          );
        history.replaceState(
          null,
          "",
          hash({ ...context.state, section: null }),
        );
        context.sourceSelections.set(topic.id, { ...context.state });
        $("#permalink").href = location.hash;
        requestAnimationFrame(() => restoreAnchor(anchor));
      }),
    );
    comparison
      .querySelectorAll("[data-copy-source]")
      .forEach((button) =>
        button.addEventListener("click", () =>
          copySource(
            button,
            sourceFor(topic.guide, selection.pair[button.dataset.copySide])
              .code,
          ),
        ),
      );
    scroll.addEventListener(
      "scroll",
      () => {
        lastAnchor = captureAnchor();
      },
      { passive: true },
    );
    let syncing = false;
    comparison.querySelectorAll(".pane-source").forEach((pane) =>
      pane.addEventListener(
        "scroll",
        () => {
          if (syncing || !context.preferences.value.syncScroll) return;
          const other = comparison.querySelector(
            `[data-pane="${pane.dataset.pane === "before" ? "after" : "before"}"]`,
          );
          if (!other) return;
          syncing = true;
          const width = pane.scrollWidth - pane.clientWidth;
          other.scrollLeft =
            width > 0
              ? (pane.scrollLeft / width) *
                (other.scrollWidth - other.clientWidth)
              : 0;
          requestAnimationFrame(() => (syncing = false));
        },
        { passive: true },
      ),
    );
    if (typeof ResizeObserver === "function") {
      observer = new ResizeObserver(scheduleLayout);
      observer.observe($(".code-layout"));
      observer.observe(comparison);
    }
    scheduleLayout();
    if (saved?.anchor) requestAnimationFrame(() => restoreAnchor(saved.anchor));
    // Arrow keys move between meaningful files, not arbitrary source columns.
    $(".file-tree").addEventListener("keydown", (event) => {
      if (!["ArrowUp", "ArrowDown", "Home", "End"].includes(event.key)) return;
      const links = [...$(".file-tree").querySelectorAll("a")],
        index = links.indexOf(document.activeElement);
      if (index < 0) return;
      event.preventDefault();
      const next =
        event.key === "Home"
          ? 0
          : event.key === "End"
            ? links.length - 1
            : Math.max(
                0,
                Math.min(
                  links.length - 1,
                  index + (event.key === "ArrowDown" ? 1 : -1),
                ),
              );
      links[next].focus();
    });
  }
  document.fonts?.addEventListener("loadingdone", scheduleLayout);
  return { html, bind, prepareRender, setDiff, scheduleLayout };
}
