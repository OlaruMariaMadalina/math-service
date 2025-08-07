from typing import Union, Dict

from pydantic import BaseModel, Field


# Request schema for Fibonacci operation.
class FibonacciRequest(BaseModel):
    n: int = Field(
        ...,
        ge=0,
        le=10000,
        description="Input number must be between 0 and 10,000"
    )


# Request schema for Power operation.
class PowRequest(BaseModel):
    base: float = Field(
        ...,
        ge=-1e6,
        le=1e6,
        description="Base must be between -1e6 and 1e6"
    )
    exponent: float = Field(
        ...,
        ge=-1000,
        le=1000,
        description="Exponent must be between -1000 and 1000"
    )


# Request schema for Factorial operation.
class FactorialRequest(BaseModel):
    n: int = Field(
        ...,
        ge=0,
        le=1000,
        description="Input number must be between 0 and 1,000"
    )


# Response schema for all math operations.
class MathOperationResponse(BaseModel):
    operation: str
    input: Union[int, Dict[str, float]]
    result: Union[int, float]
    user: str
