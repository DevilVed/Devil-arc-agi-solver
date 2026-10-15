## 2025-02-28 - Grid Diff and Soft Score Vectorization in ARC Evaluation

**Learning:** Iterating over 2D NumPy arrays element-by-element (`arr[i, j]`) in Python loops incurs high scalar indexing overhead compared to `.tolist()`. Additionally, calling `np.mean` and `np.nan_to_num` on small Python lists of floats introduces unnecessary NumPy array conversion overhead (~20x to 50x slower than `sum(lst) / len(lst)`).
**Action:** Convert 2D NumPy arrays to nested lists via `.tolist()` before string/diff formatting in Python loops, and use pure Python `sum/len` for mean calculations over small Python float lists.
