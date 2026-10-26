from arc_agi.solve_parallel_coding import _mean_soft
from arc_agi.types import ARCAGIResult, RunResult

def test_mean_soft_empty():
    res = ARCAGIResult(
        train_results=[],
        results=[],
        iteration=1,
        prompt_tokens=0,
        completion_tokens=0,
    )
    assert _mean_soft(res) == 0.0

def test_mean_soft_values():
    tr1 = RunResult(success=True, output="[]", soft_score=0.5, error=None, code="")
    tr2 = RunResult(success=True, output="[]", soft_score=1.0, error=None, code="")
    res = ARCAGIResult(
        train_results=[tr1, tr2],
        results=[],
        iteration=1,
        prompt_tokens=0,
        completion_tokens=0,
    )
    assert _mean_soft(res) == 0.75
