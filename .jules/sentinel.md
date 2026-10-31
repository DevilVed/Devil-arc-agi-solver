# Sentinel's Journal

## 2025-05-18 - AST Validation for Subprocess Sandbox
**Vulnerability:** LLM-generated code was piped directly into Python subprocesses in `arc_agi/sandbox.py` with access to host imports (`os`, `sys`, `subprocess`, `socket`) and file manipulation functions (`open`).
**Learning:** In ARC-AGI problem solvers, generated code only needs array transformations (such as `numpy` and `scipy`). Validating the AST before writing temporary files and spawning subprocesses catches malicious or prompt-injected payload attempts instantly with zero subprocess execution overhead.
**Prevention:** Always perform static AST inspection on untrusted dynamic code prior to subprocess invocation to block dangerous imports and dangerous built-ins.
