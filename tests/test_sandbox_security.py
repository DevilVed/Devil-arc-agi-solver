import asyncio
import os
import pytest

from arc_agi.sandbox import run


def test_sandbox_does_not_leak_environment_secrets(monkeypatch):
    """Ensure sensitive environment variables in parent process are not exposed in the sandbox."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-secret-12345")
    monkeypatch.setenv("GEMINI_API_KEY", "gemini-secret-67890")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "aws-secret-test")

    code = """
def transform(grid):
    import os
    leaked = []
    for key in ['OPENAI_API_KEY', 'GEMINI_API_KEY', 'AWS_SECRET_ACCESS_KEY']:
        if key in os.environ:
            leaked.append(key)
    if leaked:
        raise RuntimeError(f"Leaked secrets found: {leaked}")
    return grid
"""
    input_grid = [[1, 2], [3, 4]]
    ok, result = asyncio.run(run(code, input_grid))
    assert ok is True, f"Expected successful run without secret leakage, got error: {result}"
    assert result == "[[1, 2], [3, 4]]"


def test_sandbox_normal_execution():
    """Ensure normal ARC transformations with numpy / scipy work properly."""
    code = """
def transform(grid):
    import numpy as np
    return grid * 2
"""
    input_grid = [[1, 2], [3, 4]]
    ok, result = asyncio.run(run(code, input_grid))
    assert ok is True
    assert result == "[[2, 4], [6, 8]]"


def test_sandbox_memory_limit_enforced():
    """Ensure excessive memory allocations fail safely without crashing host process."""
    code = """
def transform(grid):
    # Try to allocate huge amount of memory (> 1GB)
    _ = [0] * (500 * 1024 * 1024)
    return grid
"""
    input_grid = [[1]]
    ok, error_msg = asyncio.run(run(code, input_grid, timeout_s=5.0))
    assert ok is False
    assert "MemoryError" in error_msg or "memory" in error_msg.lower() or error_msg == "timeout"


def test_sandbox_timeout():
    """Ensure infinite loops or long executions are terminated safely."""
    code = """
def transform(grid):
    import time
    while True:
        time.sleep(0.1)
    return grid
"""
    input_grid = [[1]]
    ok, error_msg = asyncio.run(run(code, input_grid, timeout_s=0.5))
    assert ok is False
    assert error_msg == "timeout"
