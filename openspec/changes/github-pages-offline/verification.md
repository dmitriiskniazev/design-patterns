# Проверки 2026-10-26

- uv run test-course: 150 инфраструктурных тестов и проверки всех 25 тем прошли до добавления тестов сборки.
- uv run pytest -q: 152 passed после добавления двух тестов сборки.
- uv run build-site: собраны 25 тем, 50 листингов и полный офлайн-набор.
- openspec validate --all --strict: 4 passed, 0 failed.
- node --check: app.js, offline.js, сгенерированный sw.js.
- Внешний Playwright/Chromium: экран 390×844, отсутствие горизонтального переполнения страницы, тема, каталог/Escape, восстановление раздела и scroll, офлайн-перезагрузка, переход между темами, ZIP HTTP 200, отсутствие pageerror.
- Отдельно проверены ожидание новой версии, её активация после закрытия окна, удаление прежнего кеша и повторное офлайн-открытие. Исправлена гонка сообщения о готовности обновления.

## Осталось
Не проверена установка на физический iPhone/iPad. Изменение остаётся открытым для этой проверки. Пользователь явно разрешил публичный репозиторий; публикация выполнена.

## Опубликовано

- Репозиторий: https://github.com/dmitriiskniazev/design-patterns
- Сайт: https://dmitriiskniazev.github.io/design-patterns/ (HTTPS включён).
- Исправление cef6a2c: исключён .nojekyll из кеша, так как Pages отвечает 404 на служебный файл; добавлена регрессионная проверка.
- GitHub Actions: https://github.com/dmitriiskniazev/design-patterns/actions/runs/40375229267 — success, включая test-course, build-site и deploy.
- Внешний Chromium проверил опубликованный HTTPS-адрес: экран 390×844, тема, каталог/Escape, восстановление позиции, офлайн-перезагрузка, переход Adapter → Observer, 25 тем, ZIP HTTP 200 без сети, отсутствие ошибок JavaScript.

## Состав опубликованного репозитория
.github/workflows/pages.yml, .gitignore, .python-version, AGENTS.md, README.md, assets/, content/, examples/, openspec/, pyproject.toml, src/, tests/, uv.lock, web/. Исключены .venv, .build и локальные кеши. Pages публикует только .build/site: HTML, CSS, JavaScript, manifest, иконки, Python-примеры и ZIP-комплекты.
