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

        env = {
            "PYTHONHASHSEED": "0",
            "PYTHONPATH": os.pathsep.join(sys.path),
        }

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=td,
            env=env,
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
            return False, (
                stderr.decode(errors="replace") or stdout.decode(errors="replace")
            ).strip()

        try:
            payload = json.loads(stdout.decode(errors="replace"))
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
    res_arr = np.asarray(res)
    print(json.dumps({{"ok": True, 'result': res_arr.tolist()}}))
"""
