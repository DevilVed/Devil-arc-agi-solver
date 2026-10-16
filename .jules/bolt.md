## 2026-03-31 - Async Subprocess Concurrency in ARC Evaluation
**Learning:** In ARC-AGI code evaluation, candidate solutions need to be evaluated against multiple train examples and test examples in the sandbox. Running subprocess executions sequentially in a loop blocks on process spawn and subprocess I/O sequentially. Executing them concurrently with `asyncio.gather` reduces evaluation time from ~1.0s to ~0.43s (a ~2.3x speedup).
**Action:** Always use `asyncio.gather` for independent subprocess executions or I/O-bound tasks in async code.
