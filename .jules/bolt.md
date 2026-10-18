## 2026-03-31 - NumPy Scalar Indexing in Python Loops

**Learning:** Indexing NumPy 2D arrays scalar-by-scalar (`arr[i, j]`) inside standard Python loops creates significant overhead due to NumPy scalar object instantiations on every access.
**Action:** When iterating cell-by-cell over NumPy arrays in Python loops (e.g., for string formatting or visual diffs), convert the array to a native Python list first using `.tolist()`. This provides a ~3x speedup.
