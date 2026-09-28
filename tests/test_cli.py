"""
tests/test_cli.py - Unit tests for SkillForge CLI subcommands
"""

import sys
from pathlib import Path
from skillforge.cli import main


def _write_skill(skill_dir: Path, name: str) -> Path:
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(
        "---\n"
        f"name: {name}\n"
        f"description: {name} skill for portable CLI tests.\n"
        "---\n\n"
        f"# {name}\n\n## Instructions\nDo the task.\n",
        encoding="utf-8",
    )
    return skill_file


def test_cli_taxonomy(capsys):
    sys.argv = ["skillforge", "taxonomy"]
    code = main()
    assert code == 0
    captured = capsys.readouterr()
    assert "agent-architecture" in captured.out
    assert "software-engineering" in captured.out


def test_cli_scan(tmp_path: Path, capsys):
    skills_dir = tmp_path / "skills"
    for name in ("scan-skill-one", "scan-skill-two", "scan-skill-three"):
        _write_skill(skills_dir / name, name)

    sys.argv = ["skillforge", "scan", str(skills_dir), "--limit", "5"]
    code = main()
    assert code == 0
    captured = capsys.readouterr()
    assert "SCAN COMPLETE" in captured.out
    assert "MATURITY TIER DISTRIBUTION" in captured.out


def test_cli_rate(tmp_path: Path, capsys):
    skill_file = _write_skill(tmp_path / "task-observer", "task-observer")
    sys.argv = ["skillforge", "rate", str(skill_file)]
    code = main()
    assert code == 0
    captured = capsys.readouterr()
    assert "SKILL EVALUATION REPORT" in captured.out
    assert "task-observer" in captured.out


def test_cli_levelup(tmp_path: Path, capsys):
    skill_file = _write_skill(tmp_path / "anti-slop", "anti-slop")
    sys.argv = ["skillforge", "levelup", str(skill_file)]
    code = main()
    assert code == 0
    captured = capsys.readouterr()
    assert "SKILL LEVEL-UP BLUEPRINT" in captured.out
