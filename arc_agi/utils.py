import sys
from arc_agi.types import RunResult


def canonical_test_key(results: list[RunResult]) -> str:
    return str([r["output"] for r in results])


def format_status_mark(score: float, use_color: bool | None = None) -> str:
    """Format status mark with optional ANSI color for CLI output."""
    if use_color is None:
        use_color = sys.stdout.isatty()
    if score == 1.0:
        return "\033[92m✓\033[0m" if use_color else "✓"
    return "\033[91m✗\033[0m" if use_color else "✗"
