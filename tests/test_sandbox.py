import asyncio
from arc_agi.sandbox import run

def test_run_valid_grid():
    code = """
def transform(input_grid):
    return input_grid + 1
"""
    input_grid = [[1, 2], [3, 4]]
    ok, result = asyncio.run(run(code, input_grid))
    assert ok is True
    assert result == "[[2, 3], [4, 5]]"

def test_run_invalid_input_grid_type():
    code = """
def transform(input_grid):
    return input_grid
"""
    # Test non-list input_grid
    ok, result = asyncio.run(run(code, "not_a_list"))
    assert ok is False
    assert "invalid-input-grid" in result

    # Test list with non-list row
    ok, result = asyncio.run(run(code, [1, 2, 3]))
    assert ok is False
    assert "invalid-input-grid" in result

    # Test list of lists with non-int elements
    ok, result = asyncio.run(run(code, [["a", "b"]]))
    assert ok is False
    assert "invalid-input-grid" in result
