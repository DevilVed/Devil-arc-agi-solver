import asyncio
import os
import pytest
from arc_agi.sandbox import run

def test_sandbox_run_success_numpy():
    code = """
import numpy as np
def transform(grid):
    return grid + 1
"""
    input_grid = [[1, 2], [3, 4]]
    ok, result = asyncio.run(run(code, input_grid))
    assert ok is True
    assert result == "[[2, 3], [4, 5]]"

def test_sandbox_run_success_list():
    code = """
def transform(grid):
    return [[val + 1 for val in row] for row in grid]
"""
    input_grid = [[1, 2], [3, 4]]
    ok, result = asyncio.run(run(code, input_grid))
    assert ok is True
    assert result == "[[2, 3], [4, 5]]"

def test_sandbox_run_timeout():
    code = """
import time
def transform(grid):
    time.sleep(10)
    return grid
"""
    input_grid = [[1, 2]]
    ok, result = asyncio.run(run(code, input_grid, timeout_s=0.2))
    assert ok is False
    assert result == "timeout"

def test_sandbox_run_error():
    code = """
def transform(grid):
    raise ValueError("custom error")
"""
    input_grid = [[1, 2]]
    ok, result = asyncio.run(run(code, input_grid))
    assert ok is False
    assert "ValueError: custom error" in result

def test_sandbox_environment_isolation(monkeypatch):
    monkeypatch.setenv("SECRET_API_KEY", "super_secret_value_123")
    code = """
import os
def transform(grid):
    secret = os.environ.get("SECRET_API_KEY", "NOT_FOUND")
    if secret != "NOT_FOUND":
        raise RuntimeError(f"Secret leaked: {secret}")
    return grid
"""
    input_grid = [[1]]
    ok, result = asyncio.run(run(code, input_grid))
    assert ok is True
    assert result == "[[1]]"
