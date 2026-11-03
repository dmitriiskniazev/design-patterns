import("./app.js").catch((error) => {
  console.error(error);
  document.body.classList.remove("app-loading");
  const message = document.createElement("p");
  message.setAttribute("role", "alert");
  message.textContent =
    "Не удалось загрузить интерфейс. Проверьте подключение при первом открытии и обновите страницу.";
  document.getElementById("lesson-body").replaceChildren(message);
});
