# Bolt's Performance Journal

## 2026-03-31 - Concurrent ARC Grid Evaluation
**Learning:** Evaluating candidate ARC code sequentially against each train and test grid in `solve_coding.py` bottlenecked on subprocess spawning and evaluation overhead (3.4 train grids + 1.1 test grids per iteration). Using `asyncio.gather` across independent candidate evaluations overlaps subprocess execution and cuts per-iteration evaluation time by ~63%.
**Action:** Always check loop-based `await run(...)` calls in solver iterations for opportunities to evaluate independent sample inputs concurrently.
