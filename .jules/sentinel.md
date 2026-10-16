## 2025-05-18 - Untrusted Subprocess Output Decoding & Zombie Process Reaping
**Vulnerability:** Subprocess stdout/stderr decoding used standard `.decode()`, which raised an unhandled `UnicodeDecodeError` when untrusted LLM-generated code emitted non-UTF-8 bytes to `stderr` or `stdout`, crashing the entire parent evaluation process. In addition, killing timed-out processes without `await proc.wait()` leaked zombie subprocesses.
**Learning:** Untrusted code execution in subprocesses must always decode output with `errors="replace"` (or `errors="ignore"`) to prevent unhandled decoding crashes.
**Prevention:** Always use `.decode("utf-8", errors="replace")` on stdout/stderr from untrusted subprocesses and ensure `await proc.wait()` is called after `proc.kill()`.
