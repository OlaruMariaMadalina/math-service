from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from prometheus_fastapi_instrumentator import Instrumentator

from app.controllers.controllers import router
from app.auth.auth_router import router as auth_router
from app.utils.config import settings
from app.middleware.error_logging import (
    ErrorLoggingMiddleware,
    catch_http_exceptions,
    catch_validation_errors,
)
print("RUN_MAIN ENTRYPOINT")  # debug
app = FastAPI(title=settings.app_name)

# Enable Prometheus metrics instrumentation
Instrumentator().instrument(app).expose(app)

# Middleware for logging uncaught runtime errors
app.add_middleware(ErrorLoggingMiddleware)

# Custom handler for HTTP exceptions (e.g. 404, 403)
app.add_exception_handler(StarletteHTTPException, catch_http_exceptions)

# Custom handler for request validation errors
app.add_exception_handler(RequestValidationError, catch_validation_errors)

# Register application routers
app.include_router(router)
app.include_router(auth_router)
