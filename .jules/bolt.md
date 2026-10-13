# Bolt's Journal

## 2025-05-20 - Avoid NumPy Overhead for Small Python Sequences
**Learning:** Calling `np.mean` on standard Python lists of small sizes (e.g. `[0.8, 0.9, 0.7]`) incurs significant overhead from NumPy array creation and scalar conversions compared to pure Python `sum(x) / len(x)`. In hot loops like candidate ranking in `solve_parallel_coding.py`, replacing `np.mean` provided a ~10x speedup. Additionally, checking pure Python type matches like `isinstance(x, list)` before entering `try/except` blocks or importing heavy libraries provides ~8x speedup in parsing functions like `_coerce_grid`.
**Action:** Prefer pure Python built-ins (`sum`, `len`, `isinstance`) for small collections and simple sequence transformations in hot paths.
