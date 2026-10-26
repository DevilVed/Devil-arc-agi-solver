## 2026-03-08 - Optimize `_mean_soft` ranking calculation
**Learning:** For small list collections (like `train_results` per ARC-AGI candidate solution), calling `np.mean` introduces unnecessary array conversion and NumPy C-API call overhead compared to native Python `sum(...) / len(...)`.
**Action:** Use native Python arithmetic (`sum(x) / len(x)`) for lightweight sequence operations on small lists instead of converting to NumPy arrays.
