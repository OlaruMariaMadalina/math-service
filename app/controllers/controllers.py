from fastapi import APIRouter, Depends

from app.schemas.schemas import (
    MathOperationResponse,
    FibonacciRequest,
    PowRequest,
    FactorialRequest,
)
from app.services.services import (
    calculate_fibonacci,
    calculate_power,
    calculate_factorial,
)
from app.auth.jwt_utils import get_current_user
from app.db.models.user_model import User
from app.utils.logger import publish_log, build_log_message


router = APIRouter()


@router.post("/fibonacci", response_model=MathOperationResponse)
def compute_fibonacci(
    req: FibonacciRequest,
    current_user: User = Depends(get_current_user),
):
    # Compute Fibonacci sequence
    result = calculate_fibonacci(req.n)

    # Build and publish log message
    log_message = build_log_message(
        operation="fib",
        input_data={"n": req.n},
        result=result,
        user=current_user.username,
    )
    publish_log("logs", log_message)

    # Return structured response
    return MathOperationResponse(
        operation="fib",
        input={"n": req.n},
        result=result,
        user=current_user.username,
    )


@router.post("/power", response_model=MathOperationResponse)
def compute_power(
    req: PowRequest,
    current_user: User = Depends(get_current_user),
):
    # Compute power: base ^ exponent
    result = calculate_power(req.base, req.exponent)

    # Build and publish log message
    log_message = build_log_message(
        operation="pow",
        input_data={"base": req.base, "exponent": req.exponent},
        result=result,
        user=current_user.username,
    )
    publish_log("logs", log_message)

    # Return structured response
    return MathOperationResponse(
        operation="pow",
        input={"base": req.base, "exponent": req.exponent},
        result=result,
        user=current_user.username,
    )


@router.post("/factorial", response_model=MathOperationResponse)
def compute_factorial(
    req: FactorialRequest,
    current_user: User = Depends(get_current_user),
):
    # Compute factorial of a number
    result = calculate_factorial(req.n)

    # Build and publish log message
    log_message = build_log_message(
        operation="factorial",
        input_data={"n": req.n},
        result=result,
        user=current_user.username,
    )
    publish_log("logs", log_message)

    # Return structured response
    return MathOperationResponse(
        operation="factorial",
        input={"n": req.n},
        result=result,
        user=current_user.username,
    )
