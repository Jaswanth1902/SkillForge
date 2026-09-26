"""
tests/test_scanner.py - Unit tests for universal skill scanning
"""

from pathlib import Path
import pytest
from skillforge.scanner import SkillScanner


def test_scan_single_skill_file(tmp_path: Path):
    skill_dir = tmp_path / "sample-skill"
    skill_dir.mkdir()
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(
        "---\n"
        "name: sample-skill\n"
        "description: Sample skill for scanner unit test.\n"
        "---\n\n"
        "# Sample Skill\n\n## Instructions\nDo task.\n",
        encoding="utf-8"
    )

    scanner = SkillScanner()
    analyzed = scanner.analyze_skill_file(skill_file)

    assert analyzed is not None
    assert analyzed.metadata.name == "sample-skill"
    assert analyzed.score.xp_score > 0


def test_scan_directory(tmp_path: Path):
    for i in range(3):
        s_dir = tmp_path / f"skill-{i}"
        s_dir.mkdir()
        (s_dir / "SKILL.md").write_text(
            f"---\nname: skill-{i}\ndescription: Skill {i} description.\n---\n# Skill {i}\n",
            encoding="utf-8"
        )

    scanner = SkillScanner()
    report = scanner.scan_path(tmp_path)

    assert report.total_skills == 3
    assert report.average_xp > 0
