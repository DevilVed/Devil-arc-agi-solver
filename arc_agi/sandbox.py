import asyncio
import json
import os
import sys
import tempfile
import textwrap

async def run(
    code: str, input_grid: list[list[int]], timeout_s: float = 1.5
) -> tuple[bool, str]:
    """Run user code in a subprocess asynchronously, returning (ok, result or error)."""
    script = _build_script(code)

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
            env={"PYTHONHASHSEED": "0"},
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=json.dumps({"input": input_grid}).encode()),
                timeout=timeout_s,
            )
        except asyncio.TimeoutError:
            try:
                proc.kill()
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
import resource
import sys

# Limit virtual memory (1 GB) to protect against DoS memory exhaustion
try:
    resource.setrlimit(resource.RLIMIT_AS, (1024 * 1024 * 1024, 1024 * 1024 * 1024))
except Exception:
    pass

{code}

if __name__ == '__main__':
    import json
    import numpy as np
    import scipy
    from sys import stdin

    # Redirect stdout to stderr during transform execution to prevent user code prints
    # from corrupting the IPC JSON payload on stdout.
    _orig_stdout = sys.stdout
    sys.stdout = sys.stderr
    try:
        data = json.load(stdin)
        res = transform(np.array(data['input']))
        _result_str = json.dumps({{"ok": True, 'result': res.tolist()}})
    finally:
        sys.stdout = _orig_stdout

    print(_result_str)
"""
