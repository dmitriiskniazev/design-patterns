# Proposal

## Why
Команды примеров, тестов и сервера должны запускаться через uv, как попросил пользователь.

## What Changes
- Единый запуск Python 3.15 через uv во всех целях Makefile.
- Прямые uv-команды для базовых и расширенных примеров в курсе и руководстве.

## Capabilities
### New Capabilities
Нет.

### Modified Capabilities
- `project-workflow`: единый способ запуска Python-команд.

## Impact
Makefile, сборщик данных курса, README, AGENTS и контекст OpenSpec. Учебный код сохраняется.
