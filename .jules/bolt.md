## 2025-05-18 - Avoid NumPy overhead on small list aggregations and element-by-element indexing

**Learning:**
- Using `np.mean()` on small Python lists (e.g. `len <= 10`) incurs significant overhead (~13x slower) compared to `sum(list) / len(list)` due to NumPy array creation.
- Indexing NumPy arrays element-by-element (`arr[i, j]`) in Python loops carries C-API wrapper overhead. Converting to standard Python lists via `arr.tolist()` before iterating in Python nested loops or list comprehensions yields ~3.1x faster execution.

**Action:**
- Prefer Python built-ins (`sum`, `len`) for aggregating standard Python lists over converting them to NumPy arrays with `np.mean`.
- Convert NumPy 2D arrays to Python lists (`.tolist()`) when performing element-level string formatting or nested iteration in Python.
