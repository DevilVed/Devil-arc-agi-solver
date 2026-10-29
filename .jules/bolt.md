
## 2026-03-30 - Python scalar indexing vs list indexing on 2D NumPy arrays
**Learning:** Element-by-element 2D indexing on NumPy arrays (`arr[i, j]`) in Python loops introduces significant overhead due to scalar object wrapping and C-level array indexing checks. Converting NumPy arrays to native Python nested lists (`.tolist()`) prior to standard `zip` iteration yielded a ~4x speedup for element-level processing functions (e.g., diagram rendering and array diffing).
**Action:** When iterating over individual elements of a NumPy array in Python loops (such as formatting or string diff rendering), convert the array with `.tolist()` first to eliminate NumPy scalar indexing overhead.
