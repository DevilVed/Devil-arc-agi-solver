# Bolt Journal - Critical Learnings

## 2025-05-20 - NumPy Scalar Indexing Overhead in Loop Formatting
**Learning:** Scalar indexing on NumPy 2D arrays (`arr[i, j]`) in Python loops carries significant overhead due to Python-C bridge conversions and scalar wrapping. Converting 2D NumPy arrays to standard Python nested lists using `.tolist()` before iterating/formatting yields a ~3x speedup.
**Action:** When constructing string formatting or grid diffs from NumPy 2D arrays, convert to standard Python lists via `.tolist()` first.
