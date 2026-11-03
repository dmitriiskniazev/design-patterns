# Why
У проекта лишние каталоги и сохранённые результаты генерации. ZIP-комплекты больше не нужны.

# What Changes
Объединить интерфейс и материалы в web/, убрать assets/ и content/, ZIP и отслеживаемый course-data.js. Одна команда build-course создаёт только .build/site. Сохранить главы, Python-исходники, совместимость ссылок и офлайн-чтение.

# Capabilities
## New Capabilities
- compact-site: компактные исходники и чистая публикация.
## Modified Capabilities
- project-workflow: отказаться от ZIP-комплектов.
- learning-interface: читать собранный сайт из корня, сохранять прежние ссылки.

# Impact
web/, src/, tests/, workflow, README, AGENTS, конфигурация OpenSpec.
