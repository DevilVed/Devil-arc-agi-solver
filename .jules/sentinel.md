# Sentinel Security Journal

## 2025-05-18 - Async Subprocess Cleanup and Environment Preservation in Execution Sandboxes

**Vulnerability:** In `arc_agi/sandbox.py`, timing out subprocess execution called `proc.kill()` without awaiting `proc.wait()`, leading to zombie child processes and unclosed pipe file descriptors (resource leak / DoS risk). Additionally, overriding `env={"PYTHONHASHSEED": "0"}` completely stripped `os.environ` (e.g., `PATH`, `PYTHONPATH`), breaking subprocess package resolution, while tracebacks leaked internal server temporary directory paths.

**Learning:** `asyncio.create_subprocess_exec` requires `await proc.wait()` after `proc.kill()` to properly reap subprocesses in the event loop. Passing a custom `env` dictionary replaces `os.environ` unless explicitly merged. Unsanitized stderr outputs in dynamic execution environments leak filesystem structure.

**Prevention:** Always await process termination (`await proc.wait()`) when killing subprocesses in asyncio loops, merge `os.environ` when customizing environment variables (`{**os.environ, ...}`), and sanitize temporary file paths from error messages before returning them to callers.
