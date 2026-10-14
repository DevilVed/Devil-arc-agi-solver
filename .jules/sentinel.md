# Sentinel Security Journal

## 2025-02-17 - Subprocess Environment Stripping and Output Serialization in Sandbox
**Vulnerability:** In `arc_agi/sandbox.py`, passing `env={"PYTHONHASHSEED": "0"}` replaced the entire environment dictionary for spawned Python processes, stripping `PATH`, `PYTHONPATH`, and system libraries required by C-extensions. In addition, `_build_script` assumed `transform` returns a NumPy array with `.tolist()`, causing `AttributeError` when Python lists were returned.
**Learning:** Overriding `env` completely in `asyncio.create_subprocess_exec` without inheriting `os.environ.copy()` can break module resolution and dynamic library loading in subprocesses. Additionally, LLM-generated code may return standard Python lists or tuples.
**Prevention:** Always use `env = os.environ.copy()` before modifying environment variables for subprocess execution. Safely inspect and convert outputs in script runners before serialization.
