import { $, escape, categories } from "../dom.js";
import { hash } from "./router.js";
export function createNavigation(context) {
  const topics = context.topics;
  let outlineObserver;
  function readingPosition(topic) {
    const ready = topics.filter((item) => item.ready),
      index = ready.indexOf(topic);
    return {
      index,
      total: ready.length,
      previous:
        index > 0
          ? { topic: ready[index - 1].id, view: "read", step: 0 }
          : null,
      next:
        index < ready.length - 1
          ? { topic: ready[index + 1].id, view: "read", step: 0 }
          : null,
    };
  }

  function readingNavigation(topic) {
    const position = readingPosition(topic);
    const next = position.next;
    const label = !next
      ? ""
      : next.topic !== topic.id
        ? `Следующая тема: ${topics.find((item) => item.id === next.topic).name}`
        : next.view !== context.state.view
          ? {
              code: "Перейти к решению",
              practice: "Попробовать самостоятельно",
              extension: "Разобрать расширение",
            }[next.view]
          : "Следующий шаг";
    return `<nav class="step-actions" aria-label="Порядок чтения">${position.previous ? `<a class="subtle-button" href="${hash(position.previous)}">← Назад</a>` : "<span></span>"}${next ? `<a class="next-button" href="${hash(next)}">${escape(label)} →</a>` : '<p class="course-complete" role="status">Последняя тема курса.</p>'}</nav>`;
  }

  function closeCatalog(restoreFocus = false) {
    const focusInside = $("#catalog").contains(document.activeElement);
    document.body.classList.remove("catalog-open");
    $("#catalog-toggle").setAttribute("aria-expanded", "false");
    $(".backdrop").hidden = true;
    $(".workspace").inert = false;
    if (restoreFocus) $("#catalog-toggle").focus();
    else if (focusInside) $("#topic-title").focus({ preventScroll: true });
  }

  function renderCatalog() {
    const query = $("#topic-search").value.trim().toLocaleLowerCase("ru");
    const matches = topics.filter((t) =>
      `${t.name} ${t.ru}`.toLocaleLowerCase("ru").includes(query),
    );
    $("#search-status").textContent = `Найдено тем: ${matches.length}`;
    $("#topic-list").innerHTML =
      Object.entries(categories)
        .map(([category, label]) => {
          const group = matches.filter((t) => t.category === category);
          if (!group.length) return "";
          return `<section class="topic-group"><h2>${label}</h2>${group.map((t) => `<a class="topic-link" href="${hash({ ...context.state, topic: t.id, section: null, step: 0, view: "read" })}" ${context.state.topic === t.id ? 'aria-current="page"' : ""} title="${escape(t.ru)}"><span class="number">${String(topics.indexOf(t) + 1).padStart(2, "0")}</span><span class="topic-name">${escape(t.name)}</span>${t.ready ? "" : '<span class="planned-marker">В плане</span>'}</a>`).join("")}</section>`;
        })
        .join("") ||
      '<div class="empty-state"><p>Тем с таким названием нет.</p><button class="text-button" id="clear-search">Очистить поиск</button></div>';
    $("#clear-search")?.addEventListener("click", () => {
      $("#topic-search").value = "";
      renderCatalog();
      $("#topic-search").focus();
    });
    $("#topic-list")
      .querySelectorAll("a")
      .forEach((a) => a.addEventListener("click", () => closeCatalog()));
  }

  function focusSection() {
    const heading = context.state.section
      ? document.getElementById(`lesson-${context.state.section}`) ||
        document.querySelector(
          `[data-section-target="${context.state.section}"]`,
        )
      : null;
    if (!heading) return;
    const disclosure = heading.closest("details");
    if (disclosure) disclosure.open = true;
    heading.scrollIntoView({ block: "start" });
    heading.focus({ preventScroll: true });
    $(".mobile-toc").open = false;
    markSection(context.state.section);
  }

  function markSection(section) {
    document.querySelectorAll("[data-section]").forEach((link) => {
      if (link.dataset.section === section)
        link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  }

  function renderOutline() {
    outlineObserver?.disconnect();
    const headings = [
      ...$("#lesson-body").querySelectorAll("[data-section-target] h2"),
    ];
    headings.forEach((heading, i) => {
      heading.dataset.sectionTarget = heading.closest(
        "[data-section-target]",
      ).dataset.sectionTarget;
      heading.id = `lesson-${heading.dataset.sectionTarget}`;
      heading.tabIndex = -1;
    });
    const markup = headings
      .map(
        (heading, i) =>
          `<a data-section="${heading.dataset.sectionTarget}" href="${hash({ ...context.state, section: heading.dataset.sectionTarget })}">${escape(heading.textContent)}</a>`,
      )
      .join("");
    $("#page-toc").innerHTML = markup;
    $("#mobile-page-toc").innerHTML = markup;
    document.querySelectorAll("[data-section]").forEach((link) =>
      link.addEventListener("click", (event) => {
        if (link.getAttribute("href") === location.hash) {
          event.preventDefault();
          focusSection();
        }
      }),
    );
    $(".page-outline").hidden = true;
    $(".mobile-toc").hidden = !headings.length;
    if (typeof IntersectionObserver === "function") {
      const visibleHeadings = new Set();
      outlineObserver = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) visibleHeadings.add(entry.target);
            else visibleHeadings.delete(entry.target);
          });
          const visible = [...visibleHeadings].sort(
            (a, b) =>
              a.getBoundingClientRect().top - b.getBoundingClientRect().top,
          );
          const current =
            visible[0] ||
            [...headings]
              .reverse()
              .find((heading) => heading.getBoundingClientRect().top <= 80);
          if (current)
            markSection(
              current.dataset.sectionTarget ||
                current.id.replace("lesson-", ""),
            );
        },
        { rootMargin: "-80px 0px -55% 0px", threshold: 0 },
      );
      headings.forEach((heading) => outlineObserver.observe(heading));
    }
    markSection(context.state.section || "s1");
  }

  return {
    readingNavigation,
    closeCatalog,
    renderCatalog,
    focusSection,
    renderOutline,
  };
}
