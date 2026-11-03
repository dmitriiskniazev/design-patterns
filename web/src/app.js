import "../course-data.js";
import { $, escape } from "./dom.js";
import { hash, parseHash } from "./navigation/router.js";
import { restoreReading } from "./navigation/reading.js";
import { createNavigation } from "./navigation/view.js";
import { createCodeViewer } from "./code_viewer/view.js";
import { createLesson } from "./lesson/view.js";
import { createPreferences } from "./settings/preferences.js";
import * as storage from "./settings/storage.js";
import { createSettingsPanel } from "./settings/panel.js";

const topics = window.COURSE_TOPICS;
const context = {
  topics,
  state: null,
  sourceSelections: new Map(),
  showSourceDiff: true,
  render,
};
const { resume, savedPosition, rememberPosition } = restoreReading();
const navigation = createNavigation(context),
  viewer = createCodeViewer(context),
  lesson = createLesson(context);
const preferences = createPreferences(
  () => viewer.setDiff(preferences.value.diff),
  storage,
);
context.preferences = preferences;
context.showSourceDiff = preferences.value.diff;
preferences.subscribe(() => viewer.scheduleLayout());
createSettingsPanel(preferences);
function render(initial = false) {
  const previous = context.state;
  const focused = document.activeElement;
  viewer.prepareRender();
  context.state = parseHash(topics, context.sourceSelections);
  if (location.hash !== hash(context.state))
    history.replaceState(null, "", hash(context.state));
  const state = context.state,
    topic = topics.find((topic) => topic.id === state.topic),
    code = state.view === "code";
  context.sourceSelections.set(topic.id, {
    mode: state.mode,
    pairId: state.pairId,
    side: state.side,
  });
  document.body.classList.toggle("code-mode", code);
  document.title = `${topic.name} · Python — patterns`;
  $("#topic-title").textContent = topic.name;
  $("#topic-subtitle").textContent = topic.ru;
  $("#permalink").href = hash(state);
  $("#mode-tabs").innerHTML = lesson.tabs();
  $("#lesson-body").setAttribute("role", "tabpanel");
  $("#lesson-body").setAttribute(
    "aria-labelledby",
    `chapter-tab-${state.view}`,
  );
  $("#lesson-body").innerHTML = code
    ? viewer.html(topic)
    : topic.ready
      ? lesson.read(topic) + navigation.readingNavigation(topic)
      : `<section><h2>Материал готовится</h2><p>${escape(topic.name)}</p><a href="#strategy/read">Начать со Strategy</a></section>`;
  navigation.renderCatalog();
  navigation.renderOutline();
  lesson.bind(topic);
  preferences.refresh();
  if (code) viewer.bind(topic);
  if (!initial && previous?.topic !== state.topic) {
    navigation.closeCatalog();
    $("#topic-title").focus({ preventScroll: true });
    window.scrollTo(0, 0);
  } else if (!initial && previous?.view !== state.view)
    $(`#chapter-tab-${state.view}`).focus({ preventScroll: true });
  else if (code && focused?.id === "code-stage") $("#code-stage")?.focus();
  else if (code && focused?.id === "code-file-select")
    $("#code-file-select")?.focus();
  else if (code && focused?.dataset.pair)
    document
      .querySelector(`[data-pair="${state.pairId}"]`)
      ?.focus({ preventScroll: true });
  navigation.focusSection();
}
$("#lesson-count").textContent = `${topics.length} тем`;
$(".skip-link").addEventListener("click", (event) => {
  event.preventDefault();
  $("#content").focus();
});
$("#topic-search").addEventListener("input", navigation.renderCatalog);
$("#catalog-toggle").addEventListener("click", () => {
  const open = document.body.classList.toggle("catalog-open");
  $("#catalog-toggle").setAttribute("aria-expanded", String(open));
  $(".backdrop").hidden = !open;
  $(".workspace").inert = open;
  if (open) $("#topic-search").focus();
});
$(".backdrop").addEventListener("click", () => navigation.closeCatalog(true));
document.addEventListener("keydown", (event) => {
  if (!document.body.classList.contains("catalog-open")) return;
  if (event.key === "Escape") {
    navigation.closeCatalog(true);
    return;
  }
  if (event.key !== "Tab") return;
  const controls = [...$("#catalog").querySelectorAll("a,button,input")].filter(
    (el) => !el.disabled,
  );
  if (event.shiftKey && document.activeElement === controls[0]) {
    event.preventDefault();
    controls.at(-1).focus();
  } else if (!event.shiftKey && document.activeElement === controls.at(-1)) {
    event.preventDefault();
    controls[0].focus();
  }
});
window.addEventListener("hashchange", () => {
  render();
  rememberPosition();
});
window.matchMedia("(min-width: 960px)").addEventListener("change", (event) => {
  if (event.matches) navigation.closeCatalog();
});
render(true);
document.body.classList.remove("app-loading");
if (resume && Number.isFinite(savedPosition.y) && context.state.view === "read")
  requestAnimationFrame(() => window.scrollTo(0, Math.max(0, savedPosition.y)));
