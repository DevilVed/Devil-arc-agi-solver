## 2025-02-23 - Subprocess Environment Sanitization
**Vulnerability:** Subprocess sandbox inherited all host environment variables, potentially exposing sensitive secrets (such as API keys) to untrusted LLM-generated code executed via `asyncio.create_subprocess_exec`.
**Learning:** Default subprocess creation inherits `os.environ` completely if `env` dictionary is only partially populated or left default. Passing `env={"PYTHONHASHSEED": "0"}` was previously used, but explicit white-listing of essential environment keys (`PATH`, `PYTHONPATH`, `SYSTEMROOT`) ensures both isolation of host env secrets and functional execution across environments.
**Prevention:** Always sanitize and filter environment variables passed to sandbox subprocesses.
