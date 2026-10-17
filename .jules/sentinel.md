## 2026-03-29 - Sandbox Subprocess Environment Variable Sanitization
**Vulnerability:** Subprocess execution of untrusted user/LLM-generated code could expose host environment variables (including sensitive API keys and secrets) if `os.environ` is directly passed, or break execution if `PATH` is completely missing.
**Learning:** Passing full `os.environ` to sandboxed untrusted code risks credential leakage, whereas omitting `PATH` breaks module resolution.
**Prevention:** Whitelist non-sensitive environment variables (`PATH`, `PYTHONPATH`, `PYTHONHASHSEED`, `SYSTEMROOT`, `TMPDIR`, `TEMP`) when creating subprocesses for untrusted code execution.
