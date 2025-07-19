from pydantic import BaseModel, Field
from typing import Union, Dict


# Request schema for Fibonacci operation
class FibonacciRequest(BaseModel):
    n: int = Field(..., ge=0, description="Input number should be >= 0")


# Request schema for power operation
class PowRequest(BaseModel):
    base: float
    exponent: float


# Request schema for factorial operation
class FactorialRequest(BaseModel):
    n: int = Field(..., ge=0, description="Input number should be >= 0")


# Standardized response schema for math operations
class MathOperationResponse(BaseModel):
    operation: str
    input: Union[int, Dict[str, float]]
    result: Union[int, float]
    user: str
