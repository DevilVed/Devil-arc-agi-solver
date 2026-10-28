## 2025-05-18 - Await Subprocess Termination on Timeout in Async Sandbox
**Vulnerability:** In `asyncio` subprocess execution, calling `proc.kill()` on timeout without `await proc.wait()` leaves killed processes unreaped as zombie (defunct) processes in the OS process table, risking process table exhaustion and Denial of Service (DoS) during large evaluation runs.
**Learning:** `proc.kill()` sends `SIGKILL` asynchronously but does not wait for or reap the process exit status in Python's `asyncio.subprocess` event loop.
**Prevention:** Always follow `proc.kill()` with `await proc.wait()` inside `asyncio.TimeoutError` exception handlers when executing subprocesses.
