## 2025-05-20 - Avoid NumPy Overhead on Small Python Lists and Grid Iteration

**Learning:** In ARC-AGI grid evaluation, repeatedly converting small Python lists of floats or 2D grid outputs to NumPy arrays (and vice versa, or using `np.mean` and `np.nan_to_num` on small scalar collections) introduces up to 39x execution overhead compared to pure Python `sum/len` operations. Furthermore, elementwise scalar indexing on 2D NumPy arrays (`arr[i, j]`) in Python loops is ~2.9x slower than converting the array to Python lists (`arr.tolist()`) before iterating.

**Action:** Prefer pure Python list operations (`sum(list) / len(list)`) for calculating averages on small collections of floats, convert NumPy arrays to Python lists before elementwise grid iteration, and fast-path list type checks before attempting imports or string coercions.
