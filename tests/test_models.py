"""
tests/test_models.py - Unit tests for SkillForge data models
"""

import pytest
from skillforge.models import (
    SkillLevel,
    RiskProfile,
    SkillDomain,
    SkillMetadata,
    LevelScore,
    AnalyzedSkill,
    SkillCatalogReport,
)


def test_skill_level_properties():
    assert SkillLevel.L1_PROMPTLET.rank == 1
    assert SkillLevel.L5_AUTONOMOUS.rank == 5
    assert "Novice" in SkillLevel.L1_PROMPTLET.display_name
    assert "Master" in SkillLevel.L5_AUTONOMOUS.display_name
    assert "🥉" in SkillLevel.L1_PROMPTLET.badge
    assert "👑" in SkillLevel.L5_AUTONOMOUS.badge


def test_skill_metadata_serialization():
    meta = SkillMetadata(
        name="test-skill",
        path="/tmp/test/SKILL.md",
        description="A test skill for unit testing",
        domain=SkillDomain.SOFTWARE_ENGINEERING,
        risk=RiskProfile.SAFE,
        has_frontmatter=True,
    )
    d = meta.to_dict()
    assert d["name"] == "test-skill"
    assert d["domain"] == "software-engineering"
    assert d["risk"] == "safe"
    assert d["has_frontmatter"] is True


def test_level_score_serialization():
    score = LevelScore(
        level=SkillLevel.L3_TOOL_BACKED,
        xp_score=65,
        criteria_breakdown={"executable_tooling": 20},
        passed_criteria=["Dedicated scripts"],
        missing_for_next_level=["Automated tests"],
        recommendations=["Add tests"],
    )
    d = score.to_dict()
    assert d["level"] == "L3_TOOL_BACKED"
    assert d["rank"] == 3
    assert d["xp_score"] == 65
    assert len(d["passed_criteria"]) == 1


def test_catalog_report_serialization():
    meta = SkillMetadata(name="test", path="SKILL.md")
    score = LevelScore(
        level=SkillLevel.L2_STANDARD,
        xp_score=35,
        criteria_breakdown={},
        passed_criteria=[],
        missing_for_next_level=[],
        recommendations=[],
    )
    report = SkillCatalogReport(
        total_skills=1,
        level_distribution={"L2_STANDARD": 1},
        domain_distribution={"software-engineering": 1},
        risk_distribution={"low": 1},
        average_xp=35.0,
        skills=[AnalyzedSkill(metadata=meta, score=score)],
    )
    d = report.to_dict()
    assert d["total_skills"] == 1
    assert d["average_xp"] == 35.0
