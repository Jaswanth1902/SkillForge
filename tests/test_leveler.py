"""
tests/test_leveler.py - Unit tests for 5-tier leveling rubric and scoring
"""

import pytest
from skillforge.leveler import SkillLeveler
from skillforge.models import SkillMetadata, SkillLevel


def test_level_1_promptlet():
    leveler = SkillLeveler()
    meta = SkillMetadata(
        name="raw-prompt",
        path="prompt.md",
        description="",
        has_frontmatter=False,
        has_scripts=False,
        has_tests=False,
    )
    content = "Just do something quickly without rules."
    score = leveler.evaluate(meta, content)

    assert score.level == SkillLevel.L1_PROMPTLET
    assert score.xp_score < 25
    assert len(score.missing_for_next_level) > 0


def test_level_2_standard():
    leveler = SkillLeveler()
    meta = SkillMetadata(
        name="standard-skill",
        path="SKILL.md",
        description="Comprehensive guidelines for code formatting and standard conventions.",
        has_frontmatter=True,
        has_scripts=False,
        has_tests=False,
        triggers=["format code", "standard style"],
    )
    content = (
        "---\nname: standard-skill\ndescription: A standard skill.\n---\n"
        "# Standard Skill\n\n"
        "## Instructions\nFollow these guidelines carefully.\n\n"
        "## Guidelines\n1. Do not break syntax.\n\n"
        "## Examples\nUsage: run format.\n"
    )
    score = leveler.evaluate(meta, content)

    assert score.level == SkillLevel.L2_STANDARD
    assert score.xp_score >= 25


def test_level_3_tool_backed():
    leveler = SkillLeveler()
    meta = SkillMetadata(
        name="tool-skill",
        path="SKILL.md",
        description="A tool-backed skill executing deterministic Python scripts.",
        has_frontmatter=True,
        has_scripts=True,
        script_count=2,
        has_tests=False,
        triggers=["run tool"],
    )
    content = (
        "---\nname: tool-skill\ndescription: Tool backed.\n---\n"
        "# Tool Skill\n\n## Instructions\nRuns scripts/tool.py\n\n## Examples\n```python\nimport sys\n```\n"
    )
    score = leveler.evaluate(meta, content)

    assert score.level == SkillLevel.L3_TOOL_BACKED
    assert score.xp_score >= 35


def test_level_4_self_verifying():
    leveler = SkillLeveler()
    meta = SkillMetadata(
        name="verified-skill",
        path="SKILL.md",
        description="A fully verified skill with pytest suite and error handling.",
        has_frontmatter=True,
        has_scripts=True,
        script_count=1,
        has_tests=True,
        test_count=3,
        triggers=["verify"],
    )
    content = (
        "---\nname: verified-skill\ndescription: Verified.\n---\n"
        "# Verified Skill\n\n"
        "## Instructions\nExecute with creationflags=0x08000000 CREATE_NO_WINDOW\n\n"
        "try:\n    run()\nexcept Exception:\n    pass\n\n"
        "## Examples\nUsage example here.\n"
    )
    score = leveler.evaluate(meta, content)

    assert score.level in (SkillLevel.L4_SELF_VERIFYING, SkillLevel.L5_AUTONOMOUS)
    assert score.xp_score >= 65
