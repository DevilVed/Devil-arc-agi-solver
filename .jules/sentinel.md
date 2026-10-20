## 2025-05-15 - Process Group Termination in Async Subprocess Sandbox
**Vulnerability:** Untrusted LLM code executed in `sandbox.py` could leak zombie processes or orphaned child processes upon timeout, causing process table exhaustion and resource leaks.
**Learning:** `proc.kill()` in `asyncio.create_subprocess_exec` only sends SIGKILL to the top-level subprocess and leaves defunct zombie processes if `proc.wait()` is not awaited.
**Prevention:** Always spawn untrusted subprocesses with `start_new_session=True` (on POSIX) and kill the entire process group using `os.killpg(os.getpgid(proc.pid), signal.SIGKILL)` followed by `await proc.wait()` on timeout.
