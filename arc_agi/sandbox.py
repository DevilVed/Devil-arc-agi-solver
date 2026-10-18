import asyncio
import json
import os
import sys
import tempfile


def _set_limits():
    """Limit subprocess resources on POSIX systems to prevent DoS/OOM attacks."""
    if os.name == "posix":
        try:
            import resource

            # Limit virtual memory to 2 GB
            mem_limit = 2 * 1024 * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (mem_limit, mem_limit))
        except Exception:
            pass


async def run(
    code: str, input_grid: list[list[int]], timeout_s: float = 1.5
) -> tuple[bool, str]:
    """Run user code in a subprocess asynchronously, returning (ok, result or error)."""
    script = _build_script(code)

    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "u.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(script)

        env = {**os.environ, "PYTHONHASHSEED": "0"}
        kwargs = {}
        if os.name == "posix":
            kwargs["preexec_fn"] = _set_limits

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=td,
            env=env,
            **kwargs,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=json.dumps({"input": input_grid}).encode()),
                timeout=timeout_s,
            )
        except asyncio.TimeoutError:
            try:
                proc.kill()
                await proc.wait()  # Ensure process is reaped to avoid zombie leak
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
    return f"""# generated file
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
