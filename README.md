# Digital Innovation Management Platform

**Автор:** Afinogentov Nikita Yurievich  
**Репозиторий:** [GitLab – npcmr-mirr/digital-innovation-management-platform-310474](https://gitlab.npcmr.ru/npcmr-mirr/digital-innovation-management-platform-310474)

## 📘 О проекте
Прототип веб‑платформы для управления проектами цифровых инноваций. Текущая итерация: создание/редактирование/удаление проектов, работа с разделами.

## 🚀 Технологии
- Python 3.10
- FastAPI + psycopg2 (возможно позже SQLAlchemy)
- PostgreSQL
- React + Vite
- Node.js / npm
- Docker (позже)

## Структура репозитория

```
.
|-- backend/       # Сервис API на FastAPI (работа с данными и бизнес-логика)
|-- frontend/      # Пользовательский интерфейс на React (клиентская часть)
|-- dev.sh         # Скрипт для автоматизированного запуска окружения разработки
`-- README.md      # Описание проекта
```

## Как запустить проект (для разработки)

### Предварительные требования:
Убедитесь, что у вас установлены:
*   Python 3.10 и выше
*   Node.js (рекомендуется LTS версия) и npm
*   PostgreSQL (запущенный экземпляр)

### Настройка базы данных:
*   Создайте базу данных PostgreSQL (например, `telemedai_mvp`).
*   Убедитесь, что в `backend/.env` (скопируйте из `backend/.env.example`) указаны корректные параметры подключения к вашей БД.
*   *Миграции БД запускаются автоматически при первом старте бэкенда.*

### Шаги запуска

1. **Подготовка бэкенда (один раз, через uv):**
   Установите uv, если его ещё нет (например, `pipx install uv`).
   ```bash
   cd backend
   uv venv .wsl_venv
   source .wsl_venv/bin/activate
   uv pip install -r requirements.txt
   ```
   Убедитесь, что `backend/.env` содержит `database_url`, `auth_secret` и пр.

2. **Подготовка фронтенда (один раз):**
   ```bash
   cd frontend
   npm ci   # или npm install
   ```

3. **Запуск всего (рекомендуется, WSL/Linux):**
   ```bash
   # из корня репозитория
   npm run dev:full
   ```
   Скрипт `dev.sh` активирует `backend/.wsl_venv`, поднимает `uvicorn` и `npm start` для фронтенда.
   Остановка: `Ctrl+C`.

4. **Раздельный запуск (если нужно в разных терминалах):**
   *Backend*:
   ```bash
   cd backend
   source .wsl_venv/bin/activate
   uvicorn app.main:app --reload
   ```
   *Frontend*:
   ```bash
   cd frontend
   npm start
   ```
