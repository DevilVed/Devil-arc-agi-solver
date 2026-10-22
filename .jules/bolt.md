# Bolt's Journal - Critical Learnings

## 2025-05-20 - NumPy array item indexing in Python loops
**Learning:** Element-by-element scalar access on NumPy arrays in nested Python loops (e.g. `arr[i, j]`) introduces huge overhead due to scalar conversion and bounds checks. Converting to Python lists via `.tolist()` before iterating in Python loops improves iteration speed by ~3x.
**Action:** When generating text/string visual diffs or doing row/cell iterations in Python, convert 2D NumPy arrays to Python nested lists with `.tolist()` first.
