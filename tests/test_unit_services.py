import pytest
from unittest.mock import patch
from app.services.math_service import (
    calculate_fibonacci,
    calculate_factorial,
    calculate_power,
    cache_or_compute,
)


# Tests that fibonacci(5) returns 5 and result is cached
@patch("app.services.math_service.set_cached_result")
@patch("app.services.math_service.get_cached_result", return_value=None)
def test_calculate_fibonacci_returns_correct_result(mock_get, mock_set):
    result = calculate_fibonacci(5)
    assert result == 5
    mock_get.assert_called_once()
    mock_set.assert_called_once()


# Tests that negative input raises ValueError in fibonacci()
@patch("app.services.math_service.set_cached_result")
@patch("app.services.math_service.get_cached_result", return_value=None)
def test_calculate_fibonacci_negative_raises(mock_get, mock_set):
    with pytest.raises(ValueError):
        calculate_fibonacci(-3)


# Tests correct results for factorial of 0, 1, 5
@patch("app.services.math_service.set_cached_result")
@patch("app.services.math_service.get_cached_result", return_value=None)
def test_calculate_factorial_returns_correct_result(mock_get, mock_set):
    assert calculate_factorial(0) == 1
    assert calculate_factorial(1) == 1
    assert calculate_factorial(5) == 120


# Tests that negative input raises ValueError in factorial()
@patch("app.services.math_service.set_cached_result")
@patch("app.services.math_service.get_cached_result", return_value=None)
def test_calculate_factorial_negative_raises(mock_get, mock_set):
    with pytest.raises(ValueError):
        calculate_factorial(-10)


# Tests power function for int and float exponents
@patch("app.services.math_service.set_cached_result")
@patch("app.services.math_service.get_cached_result", return_value=None)
def test_calculate_power_returns_correct_result(mock_get, mock_set):
    assert calculate_power(2, 3) == 8
    assert calculate_power(5, 0) == 1
    assert calculate_power(9, 0.5) == 3


# Tests cache_or_compute calls compute and stores result
@patch("app.services.math_service.set_cached_result")
@patch("app.services.math_service.get_cached_result", return_value=None)
def test_cache_or_compute_computes_and_caches(mock_get, mock_set):
    def dummy_func():
        return 123

    result = cache_or_compute("test_op", {"x": 1}, dummy_func)
    assert result == 123
    mock_get.assert_called_once()
    mock_set.assert_called_once()


# Tests cache_or_compute returns cached value without computing
@patch("app.services.math_service.set_cached_result")
@patch("app.services.math_service.get_cached_result", return_value="456")
def test_cache_or_compute_uses_cache(mock_get, mock_set):
    def dummy_func():
        return 999

    result = cache_or_compute("test_op", {"x": 1}, dummy_func)
    assert result == 456
    mock_get.assert_called_once()
    mock_set.assert_not_called()
