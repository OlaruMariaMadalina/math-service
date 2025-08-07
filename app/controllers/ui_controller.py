from typing import Optional

from fastapi import (
    APIRouter, Request, Form, Depends, status
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import httpx

from app.utils.config import settings
from app.auth.ui_auth_guard import require_user_auth
from app.db.database import get_db
from app.db.repositories.log_repository import get_paginated_logs
from app.views.contexts.auth_context import AuthPageContext
from app.views.contexts.base import BasePageContext
from app.views.contexts.math_context import MathPageContext

router = APIRouter()
templates = Jinja2Templates(directory="app/views")
API_BASE = settings.API_BASE


# Render login + register page
@router.get("/login", response_class=HTMLResponse)
def show_auth_form(request: Request):
    context = AuthPageContext(request=request)
    return templates.TemplateResponse(request, "auth.html", context.to_dict())


# Handle login form submission
@router.post("/login")
async def handle_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    data = {"username": username, "password": password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE}/auth/login", data=data, headers=headers
        )

    if response.status_code == 200:
        token = response.json()["access_token"]
        resp = RedirectResponse(url="/math", status_code=status.HTTP_302_FOUND)
        resp.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax"
        )
        return resp

    context = AuthPageContext(
        request=request,
        login_error="Invalid username or password."
    )
    return templates.TemplateResponse(request, "auth.html", context.to_dict())


# Handle registration form submission
@router.post("/register", response_class=HTMLResponse)
async def handle_register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    data = {"username": username, "password": password}

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_BASE}/auth/register", json=data)

    if response.status_code == 200:
        context = AuthPageContext(
            request=request,
            register_success="User registered successfully."
        )
    else:
        context = AuthPageContext(
            request=request,
            register_error="Username already taken."
        )

    return templates.TemplateResponse(request, "auth.html", context.to_dict())


# Handle logout: delete cookie
@router.post("/logout")
def logout():
    response = RedirectResponse(
        url="/login",
        status_code=status.HTTP_302_FOUND
        )
    response.delete_cookie("access_token")
    return response


# Render math operations page
@router.get("/math", response_class=HTMLResponse)
def show_math_page(request: Request):
    auth = require_user_auth(request)
    if not auth:
        return RedirectResponse("/login")

    username, role = auth
    context = MathPageContext(
        request=request,
        is_authenticated=True,
        username=username,
        role=role
    )
    return templates.TemplateResponse(request, "math.html", context.to_dict())


# Handle math operation forms
@router.post("/math", response_class=HTMLResponse)
async def handle_math_forms(
    request: Request,
    operation: str = Form(...),
    n: Optional[int] = Form(None),
    base: Optional[float] = Form(None),
    exponent: Optional[float] = Form(None),
):
    auth = require_user_auth(request)
    if not auth:
        return RedirectResponse("/login")

    username, role = auth
    token = request.cookies.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    context = MathPageContext(
        request=request,
        is_authenticated=True,
        username=username,
        role=role
    )

    async with httpx.AsyncClient() as client:
        if operation == "fibonacci":
            if n is None or not (0 <= n <= 10000):
                context.fibonacci_error = "n must be between 0 and 10,000."
            else:
                response = await client.post(
                    f"{API_BASE}/fibonacci", json={"n": n}, headers=headers
                )
                if response.status_code == 200:
                    context.fibonacci_result = response.json()["result"]

        elif operation == "factorial":
            if n is None or not (0 <= n <= 1000):
                context.factorial_error = "n must be between 0 and 1,000."
            else:
                response = await client.post(
                    f"{API_BASE}/factorial", json={"n": n}, headers=headers
                )
                if response.status_code == 200:
                    context.factorial_result = response.json()["result"]

        elif operation == "power":
            if base is None or exponent is None:
                context.power_error = "Base and exponent are required."
            elif abs(base) > 1e6 or abs(exponent) > 1000:
                context.power_error = (
                    "Base must be [-1e6, 1e6] and exponent [-1000, 1000]."
                )
            else:
                response = await client.post(
                    f"{API_BASE}/power",
                    json={"base": base, "exponent": exponent},
                    headers=headers
                )
                if response.status_code == 200:
                    context.power_result = response.json()["result"]

    return templates.TemplateResponse(request, "math.html", context.to_dict())


# Render logs page (admin only)
@router.get("/logs", response_class=HTMLResponse)
def view_logs(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1
):
    auth = require_user_auth(request)
    if not auth:
        return RedirectResponse("/login")

    username, role = auth
    if role != "admin":
        return HTMLResponse(content="Access Denied", status_code=403)

    logs = get_paginated_logs(db, page=page)
    log_entries = [
        {
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "event": log.event,
            "level": log.level,
            "operation": log.operation,
            "input": log.input,
            "result": log.result,
            "user": log.user
        }
        for log in logs
    ]

    context = BasePageContext(
        request=request,
        username=username,
        is_authenticated=True,
        role=role
    ).model_dump()

    context["logs"] = log_entries
    context["page"] = page

    return templates.TemplateResponse(request, "logs.html", context)
