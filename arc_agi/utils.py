import sys
from typing import Optional
from arc_agi.types import RunResult


def canonical_test_key(results: list[RunResult]) -> str:
    return str([r["output"] for r in results])


def format_status_mark(score: float, use_color: Optional[bool] = None) -> str:
    """Format status mark with symbols and optional ANSI color coding."""
    if use_color is None:
        use_color = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    if score == 1.0:
        return "\033[92m✓\033[0m" if use_color else "✓"
    elif score > 0.0:
        return "\033[93m◐\033[0m" if use_color else "◐"
    return "\033[91m✗\033[0m" if use_color else "✗"


def format_score(val: float | int) -> str:
    """Format a score value cleanly as integer if whole or float with 1 decimal."""
    if isinstance(val, float):
        return f"{int(val)}" if val.is_integer() else f"{val:.1f}"
    return str(val)
