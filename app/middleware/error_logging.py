from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import publish_log


# Log structured error messages to a logging backend
def log_error(request: Request, status: int, detail: str):
    publish_log("logs", {
        "event": "operation_failed",
        "level": "ERROR",
        "input": {
            "path": str(request.url.path),
            "method": request.method
        },
        "result": f"{status} - {detail}"
    })


# Middleware that catches unhandled exceptions and logs them
class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            log_error(request, 500, str(exc))
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"}
            )


# Exception handler for HTTPException (e.g., 404, 403)
async def catch_http_exceptions(request: Request, exc: StarletteHTTPException):
    log_error(request, exc.status_code, str(exc.detail))
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# Exception handler for request validation errors (422)
async def catch_validation_errors(
        request: Request,
        exc: RequestValidationError
        ):
    log_error(request, 422, str(exc))
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error"}
    )
