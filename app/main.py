from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from prometheus_fastapi_instrumentator import Instrumentator

from app.controllers.math_controller import router
from app.controllers.auth_controller import router as auth_router
from app.middleware.error_logging import (
    ErrorLoggingMiddleware,
    catch_http_exceptions,
    catch_validation_errors,
)
from fastapi.templating import Jinja2Templates
from app.controllers import ui_controller

# app = FastAPI(title=settings.app_name)
app = FastAPI(debug=True)

templates = Jinja2Templates(directory="app/views")

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
app.include_router(ui_controller.router)
