## 2025-05-18 - NumPy Indexing Overhead in Iterative String Generation
**Learning:** Iterating element-by-element over 2D NumPy arrays in Python loops (e.g. `arr[i, j]`) introduces significant scalar conversion overhead compared to converting to native lists via `.tolist()` first.
**Action:** When building custom grid string formatting or diff visualizations over 2D NumPy arrays, call `.tolist()` before nested loops or list comprehensions for a ~3x performance boost.
