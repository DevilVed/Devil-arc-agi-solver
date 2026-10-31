import asyncio
from arc_agi.sandbox import run, validate_code_safety


def test_validate_safe_code():
    safe_code = """
import numpy as np

def transform(grid):
    return grid * 2
"""
    is_safe, err = validate_code_safety(safe_code)
    assert is_safe is True
    assert err is None


def test_validate_blocks_disallowed_modules():
    bad_codes = [
        "import os\ndef transform(grid):\n    os.system('whoami')\n    return grid",
        "import subprocess\ndef transform(grid):\n    return grid",
        "import sys\ndef transform(grid):\n    return grid",
        "from os import path\ndef transform(grid):\n    return grid",
        "from urllib.request import urlopen\ndef transform(grid):\n    return grid",
        "import socket\ndef transform(grid):\n    return grid",
    ]
    for code in bad_codes:
        is_safe, err = validate_code_safety(code)
        assert is_safe is False
        assert err is not None
        assert "Disallowed module import" in err


def test_validate_blocks_dangerous_builtins():
    bad_codes = [
        "def transform(grid):\n    eval('1 + 1')\n    return grid",
        "def transform(grid):\n    exec('x = 1')\n    return grid",
        "def transform(grid):\n    with open('/etc/passwd') as f:\n        pass\n    return grid",
        "def transform(grid):\n    m = __import__('os')\n    return grid",
    ]
    for code in bad_codes:
        is_safe, err = validate_code_safety(code)
        assert is_safe is False
        assert err is not None
        assert "Disallowed built-in" in err


def test_validate_syntax_error():
    syntax_error_code = "def transform(grid): return ("
    is_safe, err = validate_code_safety(syntax_error_code)
    assert is_safe is False
    assert err is not None
    assert "Syntax error" in err


def test_run_rejects_malicious_code():
    malicious_code = "import os\ndef transform(grid):\n    return grid"
    ok, res = asyncio.run(run(malicious_code, [[1, 2], [3, 4]]))
    assert ok is False
    assert res.startswith("Security error:")
    assert "Disallowed module import: os" in res


def test_run_executes_safe_code():
    safe_code = "def transform(grid):\n    return grid + 1"
    ok, res = asyncio.run(run(safe_code, [[1, 2], [3, 4]]))
    assert ok is True
    assert res == "[[2, 3], [4, 5]]"
