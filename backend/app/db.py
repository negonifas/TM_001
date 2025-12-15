from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

import asyncpg

from .config import settings


class Database:
    pool: Optional[asyncpg.Pool] = None


db = Database()


async def connect_to_db() -> None:
    """Открыть пул соединений и инициализировать схему."""
    db.pool = await asyncpg.create_pool(settings.database_url, min_size=1, max_size=5)
    await init_db()


async def close_db() -> None:
    """Закрыть пул при остановке приложения."""
    if db.pool:
        await db.pool.close()
        db.pool = None


async def init_db() -> None:
    """
    Минимальная схема: пользователи (auth) и проекты.
    Простая "миграция" через IF NOT EXISTS, чтобы не усложнять локальную разработку.
    """
    if not db.pool:
        raise RuntimeError("Connection pool is not initialized")

    async with db.pool.acquire() as conn:
        # Users: login + password hash + timestamps
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY,
                nickname TEXT UNIQUE NOT NULL,
                password_hash TEXT DEFAULT '',
                created_at TIMESTAMPTZ DEFAULT NOW(),
                last_seen TIMESTAMPTZ DEFAULT NOW()
            );
            """
        )
        await conn.execute(
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash TEXT DEFAULT '';"
        )
        await conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS users_nickname_lower_idx ON users (lower(nickname));"
        )

        # Projects: приватные записи, каждая привязана к owner_id
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                owner_id UUID REFERENCES users(id),
                name_ru TEXT NOT NULL,
                name_en TEXT DEFAULT '',
                organization_ru TEXT DEFAULT '',
                organization_en TEXT DEFAULT '',
                direction TEXT DEFAULT '',
                scope TEXT DEFAULT '',
                focus TEXT DEFAULT '',
                profile_type TEXT DEFAULT '',
                specialization TEXT DEFAULT '',
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );
            """
        )
        alter_queries = [
            "ALTER TABLE projects ADD COLUMN IF NOT EXISTS scope TEXT DEFAULT '';",
            "ALTER TABLE projects ADD COLUMN IF NOT EXISTS focus TEXT DEFAULT '';",
            "ALTER TABLE projects ADD COLUMN IF NOT EXISTS profile_type TEXT DEFAULT '';",
            "ALTER TABLE projects ADD COLUMN IF NOT EXISTS specialization TEXT DEFAULT '';",
            "ALTER TABLE projects ADD COLUMN IF NOT EXISTS owner_id UUID REFERENCES users(id);",
            "CREATE INDEX IF NOT EXISTS projects_owner_idx ON projects(owner_id);",
        ]
        for query in alter_queries:
            await conn.execute(query)


async def fetch_user(user_id: UUID) -> Optional[Dict[str, Any]]:
    """Получить пользователя по id."""
    if not db.pool:
        raise RuntimeError("Database is not connected")

    query = """
    SELECT id, nickname, created_at, last_seen
    FROM users
    WHERE id = $1;
    """

    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(query, user_id)
        return dict(row) if row else None


async def fetch_user_by_nickname(nickname: str) -> Optional[Dict[str, Any]]:
    """Найти пользователя по nickname (без учета регистра)."""
    if not db.pool:
        raise RuntimeError("Database is not connected")

    query = """
    SELECT id, nickname, password_hash, created_at, last_seen
    FROM users
    WHERE lower(nickname) = lower($1);
    """

    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(query, nickname)
        return dict(row) if row else None


async def create_user(nickname: str) -> Dict[str, Any]:
    """Создать пользователя без пароля (вспомогательная функция)."""
    if not db.pool:
        raise RuntimeError("Database is not connected")

    user_id = uuid4()
    query = """
    INSERT INTO users (id, nickname, password_hash)
    VALUES ($1, $2, $3)
    RETURNING id, nickname, password_hash, created_at, last_seen;
    """
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(query, user_id, nickname, "")
        return dict(row)


async def create_user_with_password(nickname: str, password_hash: str) -> Dict[str, Any]:
    """Создать пользователя с паролем (основной путь регистрации)."""
    if not db.pool:
        raise RuntimeError("Database is not connected")

    user_id = uuid4()
    query = """
    INSERT INTO users (id, nickname, password_hash)
    VALUES ($1, $2, $3)
    RETURNING id, nickname, password_hash, created_at, last_seen;
    """
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(query, user_id, nickname, password_hash)
        return dict(row)


async def touch_user(user_id: UUID, timestamp: datetime) -> None:
    """Обновить last_seen (скользящие сессии)."""
    if not db.pool:
        raise RuntimeError("Database is not connected")

    query = "UPDATE users SET last_seen = $2 WHERE id = $1;"
    async with db.pool.acquire() as conn:
        await conn.execute(query, user_id, timestamp)


async def fetch_projects(owner_id: UUID) -> List[Dict[str, Any]]:
    """Получить список проектов владельца."""
    if not db.pool:
        raise RuntimeError("Database is not connected")

    query = """
    SELECT id, name_ru, name_en, organization_ru, organization_en,
           direction, scope, focus, profile_type, specialization,
           created_at, updated_at
    FROM projects
    WHERE owner_id = $1
    ORDER BY id ASC;
    """

    async with db.pool.acquire() as conn:
        rows = await conn.fetch(query, owner_id)
        return [dict(row) for row in rows]


async def fetch_project(project_id: int, owner_id: UUID) -> Optional[Dict[str, Any]]:
    """Получить проект владельца по id."""
    if not db.pool:
        raise RuntimeError("Database is not connected")

    query = """
    SELECT id, name_ru, name_en, organization_ru, organization_en,
           direction, scope, focus, profile_type, specialization,
           created_at, updated_at
    FROM projects
    WHERE id = $1 AND owner_id = $2;
    """

    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(query, project_id, owner_id)
        return dict(row) if row else None


async def create_project(data: Dict[str, Any], owner_id: UUID) -> Dict[str, Any]:
    """Создать проект для владельца."""
    if not db.pool:
        raise RuntimeError("Database is not connected")

    query = """
    INSERT INTO projects (
        owner_id,
        name_ru,
        name_en,
        organization_ru,
        organization_en,
        direction,
        scope,
        focus,
        profile_type,
        specialization
    )
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
    RETURNING id, owner_id, name_ru, name_en, organization_ru, organization_en,
              direction, scope, focus, profile_type, specialization,
              created_at, updated_at;
    """

    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            query,
            owner_id,
            data.get("name_ru", ""),
            data.get("name_en", ""),
            data.get("organization_ru", ""),
            data.get("organization_en", ""),
            data.get("direction", ""),
            data.get("scope", ""),
            data.get("focus", ""),
            data.get("profile_type", ""),
            data.get("specialization", ""),
        )
        return dict(row)


async def update_project(project_id: int, data: Dict[str, Any], owner_id: UUID) -> Optional[Dict[str, Any]]:
    """Обновить проект владельца (перезапись полей)."""
    if not db.pool:
        raise RuntimeError("Database is not connected")

    existing = await fetch_project(project_id, owner_id)
    if not existing:
        return None

    updated = {
        "name_ru": data.get("name_ru", existing["name_ru"]),
        "name_en": data.get("name_en", existing["name_en"]),
        "organization_ru": data.get("organization_ru", existing["organization_ru"]),
        "organization_en": data.get("organization_en", existing["organization_en"]),
        "direction": data.get("direction", existing["direction"]),
        "scope": data.get("scope", existing.get("scope", "")),
        "focus": data.get("focus", existing.get("focus", "")),
        "profile_type": data.get("profile_type", existing.get("profile_type", "")),
        "specialization": data.get("specialization", existing.get("specialization", "")),
    }

    query = """
    UPDATE projects
    SET
        owner_id = $1,
        name_ru = $2,
        name_en = $3,
        organization_ru = $4,
        organization_en = $5,
        direction = $6,
        scope = $7,
        focus = $8,
        profile_type = $9,
        specialization = $10,
        updated_at = NOW()
    WHERE id = $11 AND owner_id = $1
    RETURNING id, owner_id, name_ru, name_en, organization_ru, organization_en,
              direction, scope, focus, profile_type, specialization,
              created_at, updated_at;
    """

    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            query,
            owner_id,
            updated["name_ru"],
            updated["name_en"],
            updated["organization_ru"],
            updated["organization_en"],
            updated["direction"],
            updated["scope"],
            updated["focus"],
            updated["profile_type"],
            updated["specialization"],
            project_id,
        )
        return dict(row) if row else None


async def delete_project(project_id: int, owner_id: UUID) -> bool:
    """Удалить проект владельца."""
    if not db.pool:
        raise RuntimeError("Database is not connected")

    query = "DELETE FROM projects WHERE id = $1 AND owner_id = $2;"

    async with db.pool.acquire() as conn:
        result = await conn.execute(query, project_id, owner_id)
        return result.endswith("DELETE 1")


async def delete_user_and_projects(user_id: UUID) -> bool:
    """Каскадно удалить пользователя и все его проекты (при удалении аккаунта)."""
    if not db.pool:
        raise RuntimeError("Database is not connected")

    async with db.pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute("DELETE FROM projects WHERE owner_id = $1;", user_id)
            result = await conn.execute("DELETE FROM users WHERE id = $1;", user_id)
            return result.endswith("DELETE 1")
