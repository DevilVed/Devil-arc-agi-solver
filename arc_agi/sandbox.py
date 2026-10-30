import asyncio
import json
import os
import sys
import tempfile
import textwrap

# Security: enforce resource limits on POSIX to prevent memory exhaustion DoS
# from untrusted generated code.
try:
    import resource
except ImportError:  # pragma: no cover
    resource = None  # type: ignore

# Maximum virtual memory (address space) allowed for subprocess: 1GB
_MAX_VIRTUAL_MEMORY_BYTES = 1024 * 1024 * 1024


def _limit_resources():
    """Apply resource constraints (e.g., memory limits) before subprocess exec."""
    if resource is not None and hasattr(resource, "RLIMIT_AS"):
        try:
            resource.setrlimit(
                resource.RLIMIT_AS,
                (_MAX_VIRTUAL_MEMORY_BYTES, _MAX_VIRTUAL_MEMORY_BYTES),
            )
        except (ValueError, OSError):
            pass


async def run(
    code: str, input_grid: list[list[int]], timeout_s: float = 1.5
) -> tuple[bool, str]:
    """Run user code in a subprocess asynchronously, returning (ok, result or error)."""
    script = _build_script(code)

    # Security: isolate subprocess environment to prevent leaking parent process
    # secrets (such as API keys like OPENAI_API_KEY, GEMINI_API_KEY, etc.).
    # Only expose minimal runtime variables required for python execution.
    sandbox_env = {
        "PYTHONHASHSEED": "0",
        "PATH": os.environ.get("PATH", ""),
    }

    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "u.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(textwrap.dedent(script))

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=td,
            env=sandbox_env,
            preexec_fn=_limit_resources if os.name == "posix" else None,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=json.dumps({"input": input_grid}).encode()),
                timeout=timeout_s,
            )
        except asyncio.TimeoutError:
            try:
                proc.kill()
                await proc.wait()
            except ProcessLookupError:
                pass
            return False, "timeout"

        if proc.returncode != 0:
            return False, (stderr.decode() or stdout.decode()).strip()

        try:
            payload = json.loads(stdout.decode())
            return bool(payload.get("ok")), json.dumps(payload.get("result"))
        except Exception as e:
            return False, f"bad-json: {e}"


def _build_script(code: str) -> str:
    return f"""
# generated file
{code}
if __name__ == '__main__':
    import json
    import numpy as np
    import scipy
    from sys import stdin
    data = json.load(stdin)
    res = transform(np.array(data['input']))
    print(json.dumps({{"ok": True, 'result': res.tolist()}}))
"""
