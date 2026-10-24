## 2026-10-24 - Process Environment Leakage in Code Sandbox

**Vulnerability:** Subprocesses spawned by `asyncio.create_subprocess_exec` in `arc_agi/sandbox.py` inherited all parent environment variables when `env` only specified `PYTHONHASHSEED`, exposing sensitive API keys (e.g., `OPENAI_API_KEY`, `GEMINI_API_KEY`) to untrusted LLM-generated code execution.
**Learning:** In Python's `asyncio.create_subprocess_exec` / `subprocess.Popen`, passing `env={"PYTHONHASHSEED": "0"}` replaces `os.environ` completely for the child process. However, if standard binaries require `PATH`, `PATH` should be explicitly passed while excluding sensitive environment keys.
**Prevention:** Always explicitly define a minimal, safe dictionary for `env` when spawning subprocesses to run untrusted code and verify environment isolation with unit tests.
