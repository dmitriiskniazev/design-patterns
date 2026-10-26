# Proposal

## Why
Пользователь выбрал полноценный uv-проект со структурой src и tests. Makefile и отдельный скрипт сборки заменяются устанавливаемым пакетом и командами uv run.

## What Changes
- **BREAKING**: удалить Makefile; оформить pyproject.toml, uv.lock и пакет src/design_patterns.
- Перенести сборщик в пакет с командой build-course; добавить test-course и tests для инфраструктуры курса.
- Обновить README, AGENTS и контекст OpenSpec.
- Сохранить автоматическое обнаружение тем и отдельный процесс pytest для каждой темы. Учебные комплекты остаются в examples.

## Capabilities
### New Capabilities
Нет.

### Modified Capabilities
- `project-workflow`: полноценный uv-проект без Makefile.

## Impact
Makefile, scripts/build_course.py, src, tests, pyproject.toml, uv.lock, README.md, AGENTS.md, openspec/config.yaml и требования project-workflow.
