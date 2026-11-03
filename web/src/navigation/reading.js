import { loadReading, saveReading } from "../settings/storage.js";
export function restoreReading() {
  let savedPosition = null;
  try {
    savedPosition = JSON.parse(loadReading() || "null");
  } catch {}
  const resume =
    !location.hash &&
    savedPosition &&
    typeof savedPosition.hash === "string" &&
    savedPosition.hash.startsWith("#");
  if (resume) history.replaceState(null, "", savedPosition.hash);
  const rememberPosition = () =>
    saveReading({ hash: location.hash, y: window.scrollY });
  window.addEventListener("pagehide", rememberPosition);
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) rememberPosition();
  });
  let scrollTimer;
  window.addEventListener(
    "scroll",
    () => {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(rememberPosition, 250);
    },
    { passive: true },
  );

  return { resume, savedPosition, rememberPosition };
}
