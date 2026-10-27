## 2026-03-31 - Sandbox IPC Corruption and Unbounded Memory Execution

**Vulnerability:** Untrusted LLM-generated Python code executing in `arc_agi/sandbox.py` could corrupt IPC JSON output if the code called `print()` and could cause host DoS via unbounded memory allocation.
**Learning:** In subprocess-based execution where `stdout` is used for JSON IPC, untrusted user/LLM print statements interleave with stdout, causing `json.loads` parsing failures. Furthermore, subprocesses without virtual memory limits (`RLIMIT_AS`) can exhaust system RAM.
**Prevention:** Always redirect `sys.stdout` to `sys.stderr` during untrusted code execution block so user output does not contaminate IPC, and set `resource.RLIMIT_AS` bounds on sandbox subprocesses.
