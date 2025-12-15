from __future__ import annotations

import hmac
import hashlib
import secrets
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, Request, Response, status

from . import db
from .config import settings

COOKIE_NAME = "user_id"
CSRF_COOKIE = "csrf_token"
CSRF_HEADER = "X-CSRF-Token"
MAX_AGE_SECONDS = settings.cookie_max_age_days * 24 * 60 * 60
COOKIE_EXPIRE_NOW = 0


def _sign_user_id(user_id: str) -> str:
    return hmac.new(settings.auth_secret.encode(), user_id.encode(), hashlib.sha256).hexdigest()


def build_cookie_value(user_id: UUID) -> str:
    uid_str = str(user_id)
    signature = _sign_user_id(uid_str)
    return f"{uid_str}.{signature}"


def verify_cookie_value(raw: str) -> Optional[UUID]:
    try:
        uid_part, sig_part = raw.split(".", 1)
        UUID(uid_part)
    except Exception:
        return None

    expected_sig = _sign_user_id(uid_part)
    if not hmac.compare_digest(expected_sig, sig_part):
        return None

    return UUID(uid_part)


def set_user_cookie(response: Response, user_id: UUID) -> None:
    response.set_cookie(
        COOKIE_NAME,
        build_cookie_value(user_id),
        max_age=MAX_AGE_SECONDS,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
    )


def issue_csrf(response: Response) -> str:
    token = secrets.token_urlsafe(32)
    response.set_cookie(
        CSRF_COOKIE,
        token,
        max_age=MAX_AGE_SECONDS,
        httponly=False,
        samesite="lax",
        secure=settings.cookie_secure,
    )
    return token


def clear_cookies(response: Response) -> None:
    response.delete_cookie(
        COOKIE_NAME,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
    )
    response.delete_cookie(
        CSRF_COOKIE,
        httponly=False,
        samesite="lax",
        secure=settings.cookie_secure,
    )


def verify_csrf(request: Request) -> None:
    header_token = request.headers.get(CSRF_HEADER)
    cookie_token = request.cookies.get(CSRF_COOKIE)
    if not header_token or not cookie_token or not hmac.compare_digest(header_token, cookie_token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token")


async def get_current_user(request: Request, response: Response) -> dict:
    raw_cookie = request.cookies.get(COOKIE_NAME)
    user_id = verify_cookie_value(raw_cookie) if raw_cookie else None
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user = await db.fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Sliding expiration
    set_user_cookie(response, user_id)
    await db.touch_user(user_id, datetime.utcnow())
    # keep in request state for logging convenience
    request.state.user = user
    return user


def csrf_protect(request: Request) -> None:
    verify_csrf(request)
