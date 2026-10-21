import asyncio
import json
import os
import sys
import tempfile
import textwrap

def validate_input_grid(input_grid: list[list[int]]) -> bool:
    """Validate that input_grid is a 2D list of integers within expected ARC-AGI bounds (0-9)."""
    if not isinstance(input_grid, list):
        return False
    if len(input_grid) == 0:
        return False
    for row in input_grid:
        if not isinstance(row, list):
            return False
        for cell in row:
            # Check for boolean explicitly because bool is a subclass of int in Python
            if isinstance(cell, bool) or not isinstance(cell, int):
                return False
            if cell < 0 or cell > 9:
                return False
    return True

async def run(
    code: str, input_grid: list[list[int]], timeout_s: float = 1.5
) -> tuple[bool, str]:
    """Run user code in a subprocess asynchronously, returning (ok, result or error)."""
    if not validate_input_grid(input_grid):
        return False, "invalid input grid"

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
