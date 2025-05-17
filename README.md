# Парсер рассписаний
## Описание
Проект автоматически собирает данные из Airtable c использованием библиотеки Selenium, сохраняя в формате JSON и предоставляет API через DJango. Используется Docker-окружение.

### Требования
- Docker 20.10+
- Docker Compose 2.0+

### Запуск
```bash
docker-compose build
docker-compose up
```
### Выполнение задач по рассписанию с библиотекой celery
Для работы с celery требуется redis  
Настройки сelery и redis находятся в конце файла /navigator/settings.py
