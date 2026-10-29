# Sentinel Journal - Security Learnings

## 2025-10-29 - Subprocess Execution Environment Isolation in ARC Solver
**Vulnerability:** The code execution sandbox in `arc_agi/sandbox.py` inherited the process environment by default or omitted environment restrictions, allowing user code executed in subprocesses access to external executables via `PATH` and site packages or user python modules via `PYTHONPATH` or site-packages directories.
**Learning:** Subprocess execution of untrusted or LLM-generated code should explicitly constrain environment variables (setting `PYTHONPATH=""`, `PYTHONNOUSERSITE="1"`, `PYTHONSAFEPATH="1"`, and `PATH=""`) to prevent path traversal or untrusted binary execution.
**Prevention:** Always define explicit, minimal environment dictionaries when invoking `asyncio.create_subprocess_exec` for untrusted code execution.
