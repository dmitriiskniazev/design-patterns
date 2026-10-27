# Why
Плоский каталог python скрывает четыре учебных варианта; базовые файлы уже содержат часть расширений. Пользователь согласовал этапы base/extended, автономные without_pattern/with_pattern, main.py и ролевые модули для всех 25 тем.

# What Changes
Перенести 100 вариантов, убрать импорты соседних вариантов, отделить расширение от базы, разделить проверки поведения. Обновить сборщик, discovery тестов, фрагменты и совместимость ссылок сайта.

# Capabilities
## New Capabilities
- autonomous-examples: четыре самостоятельных каталога на тему.
## Modified Capabilities
- learning-interface: понятные имена, полные снимки и main.py.
- project-workflow: изолированная проверка каждого варианта.

# Impact
examples/, web/lessons.json, src/, tests/, README, AGENTS и OpenSpec. Предыдущая очистка остаётся локальной; публикация не входит в это согласование.
