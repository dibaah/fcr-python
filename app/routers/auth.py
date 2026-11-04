"""
Development auth shim for the legacy Python app.

The real security boundary lives in the .NET host (cookie auth + RBAC).
This shim keeps the shared SPA's login flow working on the legacy server
with the demo credentials and enforces a session gate on every /api route
except the sign-in flow itself, the health probe and the OpenAPI schema.
It is a demonstration gate — NOT a production authentication mechanism
(see masterplan.md: real auth/RBAC replaces demo/demo later).
"""
from __future__ import annotations

import hmac

from fastapi import APIRouter, HTTPException, Request, Response, Cookie

router = APIRouter(prefix="/api/auth", tags=["Auth"])

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo"  # nosec B105 - local desktop demo gate, see module docstring

# Endpoints reachable without a session: the sign-in flow itself, the
# health probe (used by launcher/monitoring) and the OpenAPI schema.
PUBLIC_API_PATHS = frozenset({
    "/api/auth/login", "/api/auth/logout", "/api/auth/me",
    "/api/health", "/openapi.json",
})


def check_credentials(username: str, password: str) -> bool:
    """Constant-time comparison so the demo gate cannot be timing-probed."""
    u_ok = hmac.compare_digest(username, DEMO_USERNAME)
    p_ok = hmac.compare_digest(password, DEMO_PASSWORD)
    return u_ok and p_ok


def valid_session(cookie_value: str | None) -> bool:
    return bool(cookie_value) and hmac.compare_digest(cookie_value, DEMO_USERNAME)


@router.post("/login")
def login(body: dict, request: Request, response: Response) -> dict:
    username = str(body.get("username") or "").strip()
    password = str(body.get("password") or "")
    if not check_credentials(username, password):
        raise HTTPException(401, "Invalid username or password")
    # Secure flag only over HTTPS; http://127.0.0.1 is a secure context for
    # browsers but plain HTTP would drop a Secure cookie entirely.
    is_https = request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https"
    response.set_cookie(
        "fcr_auth", DEMO_USERNAME,
        httponly=True, samesite="lax", secure=is_https,
    )
    return {"username": DEMO_USERNAME, "roles": []}


@router.post("/logout")
def logout(response: Response) -> dict:
    response.delete_cookie("fcr_auth")
    return {"ok": True}


@router.get("/me")
def me(fcr_auth: str | None = Cookie(default=None)) -> dict:
    if not valid_session(fcr_auth):
        raise HTTPException(401, "Not authenticated")
    return {"id": "0", "username": DEMO_USERNAME, "roles": []}
