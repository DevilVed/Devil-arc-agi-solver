import asyncio
import unittest
from arc_agi.sandbox import run


class TestSandbox(unittest.IsolatedAsyncioTestCase):
    async def test_run_valid_code(self):
        code = """
def transform(grid):
    return grid + 1
"""
        ok, res = await run(code, [[1, 2], [3, 4]])
        self.assertTrue(ok)
        self.assertEqual(res, "[[2, 3], [4, 5]]")

    async def test_run_non_utf8_stderr(self):
        code = """
def transform(grid):
    import sys
    sys.stderr.buffer.write(bytes([0xff, 0xfe]))
    sys.exit(1)
"""
        ok, res = await run(code, [[1]])
        self.assertFalse(ok)
        self.assertIn("\ufffd", res)

    async def test_run_timeout(self):
        code = """
def transform(grid):
    import time
    time.sleep(2)
    return grid
"""
        ok, res = await run(code, [[1]], timeout_s=0.1)
        self.assertFalse(ok)
        self.assertEqual(res, "timeout")


if __name__ == "__main__":
    unittest.main()
