# SkillForge — Project Rules & Governance

1. **Standard Library Purity**: The core engine (`models`, `classifier`, `leveler`, `scanner`, `recommender`, `exporter`, `cli`) MUST run on the Python standard library with zero mandatory external package dependencies.
2. **Subprocess Isolation (Law 8)**: On Windows, any subprocess launched MUST include `creationflags=0x08000000` (`CREATE_NO_WINDOW`).
3. **AST & Syntax Gate (Gate 1)**: All code MUST pass static AST syntax parsing without errors.
4. **Isolated Test Harness (Gate 2)**: All test cases MUST reside in `tests/` and run cleanly via `pytest`.
5. **No Ad-Hoc Databases (Law 14)**: Shared state or vector telemetry must route to Central Blackboard (`.cache/blackboard.sqlite`), not ad-hoc `.db` files.
6. **Non-Destructive Scanning**: Scanners must be strictly read-only and never modify scanned skill files during `scan`, `rate`, or `catalog` execution.
