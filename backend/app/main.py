import secrets
import sys
from time import perf_counter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

from . import auth, db
from .routes.auth import router as auth_router
from .routes.projects import router as projects_router

# Configure loguru with defaults for extra fields
logger.remove()
logger = logger.bind(req="-", user="-", nick="-")
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
    "req={extra[req]} user={extra[user]} nick={extra[nick]} | {message}",
    enqueue=True,
    backtrace=False,
    diagnose=False,
)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = perf_counter()
        req_id = secrets.token_hex(4)
        request.state.req_id = req_id

        raw_cookie = request.cookies.get(auth.COOKIE_NAME)
        user_id = auth.verify_cookie_value(raw_cookie) if raw_cookie else None
        uid = str(user_id) if user_id else "-"

        bound = logger.bind(req=req_id, user=uid, nick="-")
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception:
            status_code = 500
            bound.exception(
                "unhandled_error method={method} path={path}",
                method=request.method,
                path=request.url.path,
            )
            raise
        finally:
            duration = perf_counter() - start
            bound.info(
                "request method={method} path={path} status={status} dur={duration:.3f}s",
                method=request.method,
                path=request.url.path,
                status=status_code,
                duration=duration,
            )


app = FastAPI(title="Project Manager API", version="0.1.0")

allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)


@app.on_event("startup")
async def on_startup() -> None:
    await db.connect_to_db()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await db.close_db()


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(projects_router)
