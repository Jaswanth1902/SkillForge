"""
tests/test_cli.py - Unit tests for SkillForge CLI subcommands
"""

import sys
from pathlib import Path
import pytest
from skillforge.cli import main


def test_cli_taxonomy(capsys):
    sys.argv = ["skillforge", "taxonomy"]
    code = main()
    assert code == 0
    captured = capsys.readouterr()
    assert "agent-architecture" in captured.out
    assert "software-engineering" in captured.out


def test_cli_scan(capsys):
    skills_dir = str(Path(r"c:\Users\jaswa\Antigravity\.agents\skills"))
    sys.argv = ["skillforge", "scan", skills_dir, "--limit", "5"]
    code = main()
    assert code == 0
    captured = capsys.readouterr()
    assert "SCAN COMPLETE" in captured.out
    assert "MATURITY TIER DISTRIBUTION" in captured.out


def test_cli_rate(capsys):
    sys.argv = ["skillforge", "rate", "task-observer"]
    code = main()
    assert code == 0
    captured = capsys.readouterr()
    assert "SKILL EVALUATION REPORT" in captured.out
    assert "task-observer" in captured.out


def test_cli_levelup(capsys):
    sys.argv = ["skillforge", "levelup", "anti-slop"]
    code = main()
    assert code == 0
    captured = capsys.readouterr()
    assert "SKILL LEVEL-UP BLUEPRINT" in captured.out
