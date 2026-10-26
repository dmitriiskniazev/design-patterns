# Проверка удаления дополнительных страниц

- Дата: 2026-10-21.
- Резервная копия: `/private/tmp/design-patterns-remove-legacy-static-pages-20261021/before.tar.gz`; содержимое трёх удаляемых файлов сверено с оригиналами до удаления.
- `uv run --no-sync build-course`: 229 листингов, 25 тем; lessons/reference не созданы заново.
- `uv run --no-sync test-course`: инфраструктура и все 25 тем прошли.
- `openspec validate --all --strict`: 4 объекта прошли до архивации.
- Локальные href/src из web/index.html существуют; активных ссылок на удалённые материалы нет.
- Команды uv использовали внешний UV_CACHE_DIR, PYTHONDONTWRITEBYTECODE=1; pytest запускался без cacheprovider.
- Визуальная проверка в браузере не выполнялась. Из HTML изменён только текст noscript и удалена ссылка на дополнительный урок.
- Требования синхронизированы командой archive; изменение сохранено в `2026-10-21-remove-legacy-static-pages`.
