## 2026-03-31 - Accessible Status Indicators in Terminal CLI

**Learning:** Terminal outputs relying solely on color (such as green vs red text) fail accessibility for users with color vision deficiencies and in non-interactive/redirected pipe environments. Using distinct Unicode glyphs (✓ for complete pass, ◐ for partial pass, ✗ for fail) provides clear status comprehension even without ANSI color codes or TTY support.
**Action:** Always combine semantic Unicode symbols with optional ANSI colors, and detect `sys.stdout.isatty()` before emitting color escape codes in CLI utilities.
