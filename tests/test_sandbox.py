import asyncio
import pytest
from arc_agi.sandbox import run, validate_input_grid

def test_validate_input_grid_valid():
    assert validate_input_grid([[0, 1, 2], [3, 4, 9]]) is True
    assert validate_input_grid([[0]]) is True

def test_validate_input_grid_invalid():
    # Not a list
    assert validate_input_grid("invalid") is False
    # Empty list
    assert validate_input_grid([]) is False
    # 1D list or non-list row
    assert validate_input_grid([1, 2, 3]) is False
    # Out of range color values
    assert validate_input_grid([[-1, 0]]) is False
    assert validate_input_grid([[10, 0]]) is False
    # Non-integer cell values (strings, floats, bools)
    assert validate_input_grid([["0", "1"]]) is False
    assert validate_input_grid([[1.5, 2.0]]) is False
    assert validate_input_grid([[True, False]]) is False

def test_run_with_invalid_input_grid():
    code = "def transform(grid):\n    return grid"
    ok, err = asyncio.run(run(code, [["invalid"]]))
    assert ok is False
    assert err == "invalid input grid"

def test_run_with_valid_input_grid():
    code = "def transform(grid):\n    return grid"
    ok, result = asyncio.run(run(code, [[1, 2], [3, 4]]))
    assert ok is True
    assert result == "[[1, 2], [3, 4]]"
