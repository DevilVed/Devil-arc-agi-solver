import asyncio
import json
import os
import sys
import tempfile
import textwrap
from typing import Any

def _is_valid_input_grid(input_grid: Any) -> bool:
    """Validate that input_grid is a 2D list of integers or numeric values."""
    if not isinstance(input_grid, list):
        return False
    for row in input_grid:
        if not isinstance(row, list):
            return False
        for val in row:
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                return False
    return True


async def run(
    code: str, input_grid: list[list[int]], timeout_s: float = 1.5
) -> tuple[bool, str]:
    """Run user code in a subprocess asynchronously, returning (ok, result or error)."""
    if not _is_valid_input_grid(input_grid):
        return False, "invalid-input-grid: input_grid must be a 2D list of integers"

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
