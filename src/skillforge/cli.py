"""
skillforge.cli - Command Line Interface for SkillForge
"""

from __future__ import annotations

import io
import os
import sys
import argparse
import json
from pathlib import Path

# UTF-8 stdout resilience
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from skillforge.scanner import SkillScanner
from skillforge.exporter import SkillExporter
from skillforge.recommender import SkillRecommender
from skillforge.models import SkillDomain, SkillLevel


def format_table_row(cols: list[str], widths: list[int]) -> str:
    parts = []
    for col, w in zip(cols, widths):
        parts.append(col.ljust(w)[:w])
    return " | ".join(parts)


def cmd_scan(args: argparse.Namespace) -> int:
    target_path = Path(args.path).resolve()
    print(f"\n🔍 Scanning skills at: {target_path} ...")

    scanner = SkillScanner()
    report = scanner.scan_path(target_path)

    print(f"\n>> SCAN COMPLETE: Found {report.total_skills} skills across {len([d for d, c in report.domain_distribution.items() if c > 0])} domains.")
    print(f">> Average Maturity Score: {report.average_xp:.1f} / 100 XP\n")

    print("=" * 85)
    print("MATURITY TIER DISTRIBUTION:")
    print("-" * 85)
    for lvl in [SkillLevel.L5_AUTONOMOUS, SkillLevel.L4_SELF_VERIFYING, SkillLevel.L3_TOOL_BACKED, SkillLevel.L2_STANDARD, SkillLevel.L1_PROMPTLET]:
        count = report.level_distribution.get(lvl.value, 0)
        bar = "█" * (count * 2)
        print(f"  {lvl.badge:20s} : {count:3d}  {bar}")
    print("=" * 85)

    widths = [26, 18, 8, 22]
    header = format_table_row(["SKILL NAME", "TIER", "XP", "DOMAIN"], widths)
    print("\n" + header)
    print("-" * len(header))

    for s in report.skills[:args.limit]:
        m = s.metadata
        sc = s.score
        row = format_table_row([m.name, sc.level.badge, f"{sc.xp_score} XP", m.domain.value], widths)
        print(row)

    if len(report.skills) > args.limit:
        print(f"\n[...and {len(report.skills) - args.limit} more skills. Use --limit 0 for full list.]")

    return 0


def cmd_rate(args: argparse.Namespace) -> int:
    target = Path(args.skill_path).resolve()
    scanner = SkillScanner()

    if target.is_dir():
        skill_file = target / "SKILL.md"
        if not skill_file.exists():
            skill_file = target / "prompt.md"
    else:
        skill_file = target

    if not skill_file.exists():
        # Try finding in .agents/skills/
        workspace_skill = Path(r"c:\Users\jaswa\Antigravity\.agents\skills") / args.skill_path / "SKILL.md"
        if workspace_skill.exists():
            skill_file = workspace_skill
        else:
            print(f"Error: Skill file not found at {target}")
            return 1

    analyzed = scanner.analyze_skill_file(skill_file)
    if not analyzed:
        print(f"Error: Unable to analyze skill at {skill_file}")
        return 1

    m = analyzed.metadata
    sc = analyzed.score

    print("\n" + "=" * 65)
    print(f"🛡️  SKILL EVALUATION REPORT: {m.name}")
    print("=" * 65)
    print(f"File Path    : {m.path}")
    print(f"Domain       : {m.domain.value}")
    print(f"Maturity     : {sc.level.badge} ({sc.level.display_name})")
    print(f"XP Score     : {sc.xp_score} / 100")
    print(f"Risk Profile : {m.risk.value.upper()}")
    print(f"Scripts      : {m.script_count} found | Tests: {m.test_count} found")
    print("-" * 65)
    print("CRITERIA SCORE BREAKDOWN:")
    for k, v in sc.criteria_breakdown.items():
        print(f"  • {k.replace('_', ' ').title():30s} : {v:2d} pts")
    print("-" * 65)

    if sc.passed_criteria:
        print("PASSED REQUIREMENTS:")
        for p in sc.passed_criteria:
            print(f"  [✓] {p}")
        print("-" * 65)

    if sc.missing_for_next_level:
        print("GAPS BLOCKING NEXT LEVEL:")
        for miss in sc.missing_for_next_level:
            print(f"  [!] {miss}")
        print("-" * 65)

    if sc.recommendations:
        print("ACTIONABLE LEVEL-UP RECOMMENDATIONS:")
        for rec in sc.recommendations:
            print(f"  -> {rec}")
    print("=" * 65 + "\n")
    return 0


def cmd_levelup(args: argparse.Namespace) -> int:
    target = Path(args.skill_path).resolve()
    scanner = SkillScanner()

    if target.is_dir():
        skill_file = target / "SKILL.md"
    else:
        skill_file = target

    if not skill_file.exists():
        workspace_skill = Path(r"c:\Users\jaswa\Antigravity\.agents\skills") / args.skill_path / "SKILL.md"
        if workspace_skill.exists():
            skill_file = workspace_skill
        else:
            print(f"Error: Skill file not found at {target}")
            return 1

    analyzed = scanner.analyze_skill_file(skill_file)
    if not analyzed:
        print(f"Error: Unable to analyze skill at {skill_file}")
        return 1

    recommender = SkillRecommender()
    plan = recommender.generate_upgrade_plan(analyzed)

    print("\n" + "=" * 70)
    print(f"🚀 SKILL LEVEL-UP BLUEPRINT: {plan['skill_name']}")
    print("=" * 70)
    print(f"Current Level : {plan['current_level']} ({plan['current_xp']} XP)")
    print(f"Target Level  : {plan['target_badge']}")
    print("-" * 70)
    print("ACTION ITEMS TO ADVANCE:")
    for item in plan["action_items"]:
        print(f"  * {item}")
    print("-" * 70)

    if plan["scaffolds"]:
        print("RECOMMENDED CODE SCAFFOLDING:")
        for filename, code in plan["scaffolds"].items():
            print(f"\n--- [{filename}] ---")
            print(code.strip())
    print("=" * 70 + "\n")
    return 0


def cmd_catalog(args: argparse.Namespace) -> int:
    target_path = Path(args.path).resolve()
    scanner = SkillScanner()
    report = scanner.scan_path(target_path)

    if args.json:
        out = SkillExporter.to_json(report)
        if args.output:
            Path(args.output).write_text(out, encoding="utf-8")
            print(f"JSON catalog written to {args.output}")
        else:
            print(out)
        return 0

    if args.html:
        out_html = SkillExporter.to_html_dashboard(report)
        Path(args.html).write_text(out_html, encoding="utf-8")
        print(f"Interactive HTML dashboard written to {args.html}")

    md_out = SkillExporter.to_markdown(report)
    out_file = Path(args.output) if args.output else target_path / "CATALOG.md"
    out_file.write_text(md_out, encoding="utf-8")
    print(f"Executive Markdown catalog written to {out_file}")
    return 0


def cmd_taxonomy(args: argparse.Namespace) -> int:
    print("\n" + "=" * 65)
    print("🗺️  SKILLFORGE 10-DOMAIN TAXONOMY ONTOLOGY")
    print("=" * 65)
    for dom in SkillDomain:
        print(f"• Domain: {dom.value}")
    print("=" * 65 + "\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="SkillForge - AI Agent Skill Leveling & Taxonomy Engine")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # scan
    p_scan = subparsers.add_parser("scan", help="Scan and summarize skills in a directory")
    p_scan.add_argument("path", nargs="?", default=r"c:\Users\jaswa\Antigravity\.agents\skills", help="Directory to scan")
    p_scan.add_argument("--limit", type=int, default=25, help="Number of skills to display in preview table")

    # rate
    p_rate = subparsers.add_parser("rate", help="Evaluate maturity level of a single skill")
    p_rate.add_argument("skill_path", help="Path to SKILL.md or folder name in .agents/skills")

    # levelup
    p_up = subparsers.add_parser("levelup", help="Generate upgrade roadmap and scaffolds for a skill")
    p_up.add_argument("skill_path", help="Path to SKILL.md or folder name in .agents/skills")

    # catalog
    p_cat = subparsers.add_parser("catalog", help="Export full catalog to Markdown/JSON/HTML")
    p_cat.add_argument("path", nargs="?", default=r"c:\Users\jaswa\Antigravity\.agents\skills", help="Directory to scan")
    p_cat.add_argument("--output", "-o", help="Output path for CATALOG.md or JSON")
    p_cat.add_argument("--html", help="Output path for interactive HTML dashboard")
    p_cat.add_argument("--json", action="store_true", help="Output raw JSON instead of Markdown")

    # taxonomy
    subparsers.add_parser("taxonomy", help="Show all 10 taxonomy domains")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    if args.command == "scan":
        return cmd_scan(args)
    elif args.command == "rate":
        return cmd_rate(args)
    elif args.command == "levelup":
        return cmd_levelup(args)
    elif args.command == "catalog":
        return cmd_catalog(args)
    elif args.command == "taxonomy":
        return cmd_taxonomy(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
