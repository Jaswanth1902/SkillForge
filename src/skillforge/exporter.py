"""
skillforge.exporter - Catalog Exporter (Markdown, JSON, SVG Badges, and HTML Dashboard)
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from skillforge.models import SkillCatalogReport, SkillLevel, SkillDomain


class SkillExporter:
    """Exports skill analysis into standard markdown catalogs, JSON schemas, and HTML dashboards."""

    @staticmethod
    def to_markdown(report: SkillCatalogReport, title: str = "SkillForge Catalog & Leveling Index") -> str:
        """Renders an executive Markdown document summarizing all scanned skills."""
        now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = [
            f"# 🛡️ {title}",
            "",
            f"> **Generated**: {now_iso} • **Total Skills**: `{report.total_skills}` • **Average XP**: `{report.average_xp}/100`",
            "",
            "---",
            "",
            "## 📊 Executive Census & Maturity Distribution",
            "",
            "| Maturity Tier | Count | Share (%) | Badge | Criteria Summary |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]

        tier_summaries = {
            "L5_AUTONOMOUS": "Closed-loop, multi-agent contracts, telemetry, state persistence",
            "L4_SELF_VERIFYING": "Automated pytest suite, AST linting, blast-radius safety rating",
            "L3_TOOL_BACKED": "Dedicated executable CLI scripts, deterministic arguments",
            "L2_STANDARD": "YAML frontmatter, structured Markdown sections, clear triggers",
            "L1_PROMPTLET": "Unstructured prompt snippet or basic text instructions",
        }

        for lvl in [SkillLevel.L5_AUTONOMOUS, SkillLevel.L4_SELF_VERIFYING, SkillLevel.L3_TOOL_BACKED, SkillLevel.L2_STANDARD, SkillLevel.L1_PROMPTLET]:
            count = report.level_distribution.get(lvl.value, 0)
            share = (count / report.total_skills * 100) if report.total_skills else 0.0
            lines.append(f"| **{lvl.display_name}** | `{count}` | `{share:.1f}%` | {lvl.badge} | {tier_summaries[lvl.value]} |")

        lines.extend([
            "",
            "---",
            "",
            "## 🗺️ Taxonomy Domain Breakdown",
            "",
            "| Domain | Skill Count | Share (%) |",
            "| :--- | :--- | :--- |",
        ])

        for dom in SkillDomain:
            count = report.domain_distribution.get(dom.value, 0)
            if count > 0:
                share = (count / report.total_skills * 100) if report.total_skills else 0.0
                lines.append(f"| **`{dom.value}`** | `{count}` | `{share:.1f}%` |")

        lines.extend([
            "",
            "---",
            "",
            "## 📜 Comprehensive Skill Registry",
            "",
            "| Skill Name | Tier | XP | Domain | Risk | Scripts | Tests | Description |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        for s in report.skills:
            m = s.metadata
            sc = s.score
            desc = (m.description[:95] + "...") if len(m.description) > 95 else m.description
            lines.append(
                f"| **`{m.name}`** | {sc.level.badge} | `{sc.xp_score}` | `{m.domain.value}` | `{m.risk.value}` | `{m.script_count}` | `{m.test_count}` | {desc or '*No description*'} |"
            )

        lines.append("")
        return "\n".join(lines)

    @staticmethod
    def to_json(report: SkillCatalogReport, indent: int = 2) -> str:
        """Serializes report into JSON."""
        return json.dumps(report.to_dict(), indent=indent)

    @staticmethod
    def to_html_dashboard(report: SkillCatalogReport) -> str:
        """Renders an interactive dark-mode HTML dashboard conforming to Emil Kowalski tactile aesthetics."""
        skills_json = json.dumps([s.to_dict() for s in report.skills])
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SkillForge Dashboard</title>
  <style>
    :root {{
      --bg: #0B0B0D;
      --card-bg: #141418;
      --border: #22222A;
      --text: #EDEDED;
      --text-muted: #8E8D96;
      --gold: #C5A059;
      --cyan: #38BDF8;
      --emerald: #10B981;
    }}
    body {{
      margin: 0;
      padding: 32px;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border);
      padding-bottom: 20px;
      margin-bottom: 28px;
    }}
    .title h1 {{ margin: 0; font-size: 26px; font-weight: 700; color: #FFF; }}
    .title p {{ margin: 6px 0 0 0; color: var(--text-muted); font-size: 14px; }}
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 32px;
    }}
    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 18px;
      transition: transform 0.15s ease;
    }}
    .stat-card:hover {{ transform: translateY(-2px); }}
    .stat-val {{ font-size: 32px; font-weight: 700; color: var(--gold); }}
    .stat-label {{ font-size: 13px; color: var(--text-muted); margin-top: 4px; }}
    .skill-table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--card-bg);
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid var(--border);
    }}
    th, td {{
      padding: 14px 18px;
      text-align: left;
      border-bottom: 1px solid var(--border);
      font-size: 14px;
    }}
    th {{ background: #18181E; color: var(--text-muted); font-weight: 600; }}
    tr:hover td {{ background: #1B1B22; }}
    .badge {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      border: 1px solid var(--border);
    }}
  </style>
</head>
<body>
  <div class="header">
    <div class="title">
      <h1>🛡️ SkillForge Intelligence Dashboard</h1>
      <p>Autonomous AI Agent Skill Leveling & Taxonomy Engine</p>
    </div>
  </div>

  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-val">{report.total_skills}</div>
      <div class="stat-label">Total Skills Indexed</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">{report.average_xp:.1f}</div>
      <div class="stat-label">Average Maturity XP (0-100)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">{report.level_distribution.get("L5_AUTONOMOUS", 0) + report.level_distribution.get("L4_SELF_VERIFYING", 0)}</div>
      <div class="stat-label">Production Grade (L4 & L5)</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">{len([d for d, c in report.domain_distribution.items() if c > 0])}</div>
      <div class="stat-label">Active Taxonomy Domains</div>
    </div>
  </div>

  <table class="skill-table">
    <thead>
      <tr>
        <th>Skill Name</th>
        <th>Maturity Tier</th>
        <th>XP Score</th>
        <th>Domain</th>
        <th>Risk Profile</th>
        <th>Scripts</th>
        <th>Tests</th>
      </tr>
    </thead>
    <tbody>
      {"".join(f"<tr><td><strong>{s.metadata.name}</strong></td><td><span class='badge'>{s.score.level.badge}</span></td><td>{s.score.xp_score} XP</td><td><code>{s.metadata.domain.value}</code></td><td>{s.metadata.risk.value.upper()}</td><td>{s.metadata.script_count}</td><td>{s.metadata.test_count}</td></tr>" for s in report.skills)}
    </tbody>
  </table>
</body>
</html>"""
