## 2025-05-18 - Concurrent Sandbox Evaluation & NumPy List Conversion

**Learning:** Running independent sandbox subprocesses (`asyncio.create_subprocess_exec`) sequentially for each training/test input grid created significant latency in code evaluation per LLM iteration. Parallelizing grid evaluations with `asyncio.gather` reduced evaluation wall-clock time from `sum(t_i)` to `max(t_i)`, yielding a 2x-5x speedup per iteration. Additionally, element-wise indexing of 2D NumPy arrays in Python loops (`arr[i, j]`) introduces large scalar creation/boxing overheads compared to calling `arr.tolist()` first.

**Action:** Always batch independent subprocess tasks with `asyncio.gather`, and convert NumPy arrays to native Python lists via `.tolist()` before element-wise loop iterations.
