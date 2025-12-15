from __future__ import annotations

from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, Response, status, Depends
from loguru import logger
from passlib.context import CryptContext

from .. import db
from .. import auth as auth_utils
from ..schemas import AuthRequest, AuthResponse, LoginRequest, User

router = APIRouter(prefix="/api/auth", tags=["auth"])
# используем стойкий PBKDF2-SHA256, чтобы не зависеть от реализации bcrypt в ОС
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


@router.post("/register")
async def register(payload: AuthRequest, response: Response, request: Request) -> dict:
    nickname = payload.nickname.strip()
    if not nickname:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nickname is required")

    existing = await db.fetch_user_by_nickname(nickname)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    if not payload.create_if_missing:
        logger.bind(
            req=getattr(request.state, "req_id", "-"),
            user="-",
            nick=nickname,
        ).info("event=user_not_created nickname={nickname}", nickname=nickname)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Creation is not allowed")

    password = nickname
    password_hash = pwd_context.hash(password)
    user = await db.create_user_with_password(nickname, password_hash)
    logger.bind(
        req=getattr(request.state, "req_id", "-"),
        user=str(user["id"]),
        nick=user["nickname"],
    ).info("event=user_registered nickname={nickname}", nickname=user["nickname"])

    # Registration does not authenticate; just return credentials info
    return {"login": nickname, "password": password}


@router.get("/me", response_model=AuthResponse)
async def me(response: Response, request: Request) -> AuthResponse:
    raw_cookie = request.cookies.get(auth_utils.COOKIE_NAME)
    user_id = auth_utils.verify_cookie_value(raw_cookie) if raw_cookie else None
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user = await db.fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    await db.touch_user(user_id, datetime.utcnow())
    auth_utils.set_user_cookie(response, user_id)
    csrf = auth_utils.issue_csrf(response)
    logger.bind(
        req=getattr(request.state, "req_id", "-"),
        user=str(user["id"]),
        nick=user["nickname"],
    ).info("event=auth_me")
    return AuthResponse(user=User(**user), csrf_token=csrf)


@router.post("/logout")
async def logout(response: Response, request: Request) -> dict[str, str]:
    auth_utils.clear_cookies(response)
    logger.bind(
        req=getattr(request.state, "req_id", "-"),
        user="-",
        nick="-",
    ).info("event=logout")
    return {"status": "logged_out"}


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest, response: Response, request: Request) -> AuthResponse:
    nickname = payload.login.strip()
    if not nickname or not payload.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login and password are required")

    user = await db.fetch_user_by_nickname(nickname)
    if not user or not user.get("password_hash"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not pwd_context.verify(payload.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    auth_utils.set_user_cookie(response, user["id"])
    csrf = auth_utils.issue_csrf(response)

    logger.bind(
        req=getattr(request.state, "req_id", "-"),
        user=str(user["id"]),
        nick=user["nickname"],
    ).info("event=user_login nickname={nickname}", nickname=user["nickname"])

    return AuthResponse(user=User(**user), csrf_token=csrf)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(auth_utils.csrf_protect)])
async def delete_account(response: Response, request: Request) -> Response:
    raw_cookie = request.cookies.get(auth_utils.COOKIE_NAME)
    user_id = auth_utils.verify_cookie_value(raw_cookie) if raw_cookie else None
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user = await db.fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    await db.delete_user_and_projects(user_id)
    auth_utils.clear_cookies(response)
    logger.bind(
        req=getattr(request.state, "req_id", "-"),
        user=str(user["id"]),
        nick=user["nickname"],
    ).info("event=account_deleted")
    # return empty response for 204
    return Response(status_code=status.HTTP_204_NO_CONTENT)
