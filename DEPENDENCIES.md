# SkillForge — Dependencies & Runtime Manifest

## Runtime Dependencies
- **Python**: `>= 3.10`
- **Standard Library Modules Used**:
  - `pathlib`, `dataclasses`, `enum`, `typing`, `json`, `re`, `argparse`, `io`, `os`, `sys`, `datetime`, `shutil`
- **Zero External Runtime Dependencies**: SkillForge is engineered to run cleanly without requiring `pip install` on standard environments.

## Development & Test Dependencies
- `pytest >= 8.0.0` (for running automated test suite in `tests/`)
- `ruff >= 0.3.0` (fast static linting)
- `ast-grep / sg` (optional structural searching)

## Known Pitfalls & Safe Invariants
- **Windows UTF-8 Console**: Handled via `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` in `cli.py`.
- **Windows Windowless Execution**: All subprocess calls comply with `creationflags=0x08000000`.
