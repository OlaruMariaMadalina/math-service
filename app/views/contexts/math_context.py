from app.views.contexts.base import BasePageContext
from typing import Optional


# Context object for the math operations page
class MathPageContext(BasePageContext):
    fibonacci_result: Optional[int] = None
    power_result: Optional[float] = None
    factorial_result: Optional[int] = None

    fibonacci_error: Optional[str] = None
    power_error: Optional[str] = None
    factorial_error: Optional[str] = None
