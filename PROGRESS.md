# Digital Innovation Management Platform (PROGRESS / README-черновик)

Автор: Afinogentov Nikita Yurievich
Репозиторий (оригинал): https://gitlab.npcmr.ru/npcmr-mirr/digital-innovation-management-platform-310474

Дата (черновик): 2025-11-28T14:07:04.841Z
Просмотр выполнил: Copilot CLI (ассистент)

---

Кратко: проект — веб-платформа для управления цифровыми инновациями: backend на FastAPI, frontend на React; цель — управление проектами, обработка заявок и управление ролями/доступами.

## Технологии
- Python 3.10, FastAPI (uvicorn), psycopg2 (в перспективе возможно SQLAlchemy)
- PostgreSQL
- React (Create React App, react-scripts) — текущая реализация
- Node.js (LTS) и npm
- Docker / docker-compose (опционально)

> Важно: README в репозитории упоминает Vite; текущая реализация фронтенда использует Create React App (react-scripts). Рекомендуется синхронизовать документацию со стеком или выполнить миграцию фронтенда на Vite.

## Структура репозитория
.
|-- backend/       # FastAPI сервис (API, модели, миграции, env)
|-- frontend/      # React-приложение (Create React App)
|-- dev.sh         # вспомогательный скрипт для запуска разработки (локально)
`-- README.md      # основное описание проекта

## Быстрый старт (локально)
Требования: Python 3.10, Node.js LTS, npm, PostgreSQL.

1) База данных
- Создайте базу (например: telemedai_mvp) и пользователя PostgreSQL.
- Подготовьте `backend/.env` на основе `backend/.env.example` и укажите параметры подключения.

2) Backend (локально)
- cd backend/
- python3 -m venv .linux_venv
- source .linux_venv/bin/activate
- pip install -r requirements.txt
- uvicorn app.main:app --reload
API по умолчанию: http://localhost:8000

3) Frontend
- cd frontend/
- npm install
- npm start
Фронтенд ожидает API по `REACT_APP_API_URL` или по умолчанию http://localhost:8000.

4) Скрипт dev:full
- В `frontend/package.json` есть скрипт `dev:full`, который запускает backend и frontend параллельно через `concurrently` и предполагает WSL/Linux-окружение (виртуальное окружение `.linux_venv`). Проверьте и адаптируйте под вашу среду.

## Переменные окружения
- `backend/.env` — DB connection, секреты и т.п. (добавьте `backend/.env.example`)
- `frontend`: `REACT_APP_API_URL` — базовый URL API

## Найденные проблемы / замечания
- Фронтенд: Create React App (react-scripts) — README упоминает Vite (несоответствие).
- В коде: хардкод русских строк, alert-ы, повторяющаяся логика форм, ручные fetch-запросы без общего API-слоя.
- package.json: дубли `devDependencies`, скрипт `dev:full` привязан к WSL-паттерну.

## Рекомендации (пошагово)
Короткие (низкий порог):
- Актуализировать README — указать реальный стек (CRA или Vite).
- Добавить `backend/.env.example`.
- Создать `PROGRESS.md` (этот файл) и краткий roadmap в Issue/PROJECT.

Средние:
- Вынести повторяющуюся логику форм в хуки/компоненты.
- Сделать единый API-wrapper (fetch/axios) с централизованной обработкой ошибок и credentials.
- Заменить `alert` на систему уведомлений (toasts) и вынести тексты в i18n/константы.
- Упростить CSS: CSS-модули или utility-классы.

Долгие:
- Рассмотреть миграцию фронтенда на Vite (опционально) для более быстрой разработки.
- Добавить docker-compose для локальной среды (backend + frontend + postgres).
- Ввести тесты (pytest для backend, RTL для frontend), ESLint/Prettier и CI.

## Предлагаемые следующие шаги (на ваш выбор)
- Оставить этот файл как PROGRESS.md и закоммитить его — вы коммитите и пушите.
- Или дать разрешение — подготовлю PR с заменой README.md и/или обновлением PROGRESS.md и других вспомогательных файлов.

---

Исходный осмотр (коротко): просмотрен frontend (App.js, RegistrationForm, RoleSelection, стили), package.json, public; рекомендации записаны выше.

Файл создан локально: ничего не менял в других файлах репозитория.
