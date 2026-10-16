import pytest
from arc_agi.utils import format_status_mark, canonical_test_key


def test_format_status_mark_success():
    assert format_status_mark(1.0, use_color=False) == "✓"
    assert format_status_mark(1.0, use_color=True) == "\033[92m✓\033[0m"


def test_format_status_mark_failure():
    assert format_status_mark(0.0, use_color=False) == "✗"
    assert format_status_mark(0.0, use_color=True) == "\033[91m✗\033[0m"
    assert format_status_mark(0.5, use_color=False) == "✗"


def test_canonical_test_key():
    results = [{"output": "[[1]]"}, {"output": "[[2]]"}]
    assert canonical_test_key(results) == "['[[1]]', '[[2]]']"
