import json
from typing import Callable, Any

from app.utils.cache import get_cached_result, set_cached_result


# Helper function that uses cache or computes and stores result
def cache_or_compute(
    operation: str,
    input_data: dict,
    compute_func: Callable[[], Any],
    ttl: int = 3600
) -> Any:
    cache_key = f"{operation}:{json.dumps(input_data, sort_keys=True)}"
    cached = get_cached_result(cache_key)
    if cached is not None:
        try:
            print(f"[CACHE HIT] Key: {cache_key}")
            return json.loads(cached)
        except json.JSONDecodeError:
            print(
                f"[CACHE HIT - JSON ERROR] "
                f"[Raw cached value used. "
                f"Key: {cache_key}"
            )
            return cached

    result = compute_func()
    set_cached_result(cache_key, json.dumps(result), ttl=ttl)
    return result


# Fibonacci number computation with caching
def calculate_fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")

    def compute():
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    return cache_or_compute("fibonacci", {"n": n}, compute)


# Factorial computation with caching
def calculate_factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")

    def compute():
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    return cache_or_compute("factorial", {"n": n}, compute)


# Power computation with caching
def calculate_power(base: float, exponent: float) -> float:
    def compute():
        return base ** exponent

    return cache_or_compute(
        "power",
        {"base": base, "exponent": exponent},
        compute
        )
