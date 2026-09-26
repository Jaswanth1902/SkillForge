# 💻 SkillForge CLI Reference

Command line interface reference for `skillforge`.

---

## Commands

### `skillforge scan [path]`
Recursively inspects a directory or workspace for skills, parses metadata, grades maturity tiers, and outputs a colorized ASCII summary table.
```bash
# Scan default .agents/skills
python -m skillforge.cli scan

# Scan a custom directory with a display limit
python -m skillforge.cli scan path/to/skills --limit 10
```

### `skillforge rate <skill_path_or_name>`
Performs a deep-dive evaluation of a specific skill file or folder. Outputs XP score (0–100), criteria breakdown, fulfilled requirements, blocking gaps, and recommendations.
```bash
# Rate by skill folder name (looks in .agents/skills/)
python -m skillforge.cli rate task-observer

# Rate by direct file path
python -m skillforge.cli rate path/to/my-skill/SKILL.md
```

### `skillforge levelup <skill_path_or_name>`
Generates actionable steps and drop-in code scaffolds to advance the skill to the immediate next maturity tier.
```bash
python -m skillforge.cli levelup anti-slop
```

### `skillforge catalog [path]`
Compiles and exports an executive catalog report in Markdown, JSON, and/or interactive HTML dashboard.
```bash
# Export Markdown catalog
python -m skillforge.cli catalog .agents/skills --output CATALOG.md

# Export JSON catalog
python -m skillforge.cli catalog .agents/skills --output skills_index.json --json

# Export dark-mode HTML dashboard
python -m skillforge.cli catalog .agents/skills --html DASHBOARD.html
```

### `skillforge taxonomy`
Prints all 10 standard taxonomy domains.
```bash
python -m skillforge.cli taxonomy
```
