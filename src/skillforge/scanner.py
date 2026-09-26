"""
skillforge.scanner - Universal File-System Skill Scanner & Parser
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from skillforge.models import (
    SkillMetadata,
    AnalyzedSkill,
    SkillCatalogReport,
    SkillLevel,
    SkillDomain,
    RiskProfile,
)
from skillforge.classifier import SkillClassifier
from skillforge.leveler import SkillLeveler


class SkillScanner:
    """Universal scanner for AI agent skills across directories and frameworks."""

    def __init__(self):
        self.classifier = SkillClassifier()
        self.leveler = SkillLeveler()

    def scan_path(self, target_path: Path | str) -> SkillCatalogReport:
        """
        Scans a file or directory tree for skills and returns a complete catalog report.
        """
        path = Path(target_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Target path does not exist: {path}")

        found_skills: List[AnalyzedSkill] = []

        if path.is_file():
            analyzed = self.analyze_skill_file(path)
            if analyzed:
                found_skills.append(analyzed)
        else:
            found_skills = self._scan_directory(path)

        # Aggregate report
        level_dist: Dict[str, int] = {lvl.value: 0 for lvl in SkillLevel}
        domain_dist: Dict[str, int] = {dom.value: 0 for dom in SkillDomain}
        risk_dist: Dict[str, int] = {r.value: 0 for r in RiskProfile}
        total_xp = 0

        for s in found_skills:
            level_dist[s.score.level.value] += 1
            domain_dist[s.metadata.domain.value] += 1
            risk_dist[s.metadata.risk.value] += 1
            total_xp += s.score.xp_score

        avg_xp = (total_xp / len(found_skills)) if found_skills else 0.0

        return SkillCatalogReport(
            total_skills=len(found_skills),
            level_distribution=level_dist,
            domain_distribution=domain_dist,
            risk_distribution=risk_dist,
            average_xp=avg_xp,
            skills=sorted(found_skills, key=lambda x: x.score.xp_score, reverse=True),
        )

    def _scan_directory(self, root_dir: Path) -> List[AnalyzedSkill]:
        """Discovers all SKILL.md and skill files in directory tree."""
        skills: List[AnalyzedSkill] = []
        visited_dirs = set()

        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Skip hidden git and build folders
            dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", ".venv", "__pycache__", ".pytest_cache")]
            current_path = Path(dirpath)

            # Check if this folder has a SKILL.md
            for f in filenames:
                if f.upper() in ("SKILL.MD", "PROMPT.MD"):
                    skill_file = current_path / f
                    if current_path not in visited_dirs:
                        analyzed = self.analyze_skill_file(skill_file)
                        if analyzed:
                            skills.append(analyzed)
                            visited_dirs.add(current_path)
                    break

        return skills

    def analyze_skill_file(self, skill_file: Path) -> Optional[AnalyzedSkill]:
        """Parses, classifies, and levels a single skill file and its surrounding assets."""
        try:
            content = skill_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return None

        parent_dir = skill_file.parent
        name = parent_dir.name
        if name in ("skills", "plugins", ".agents", "skills_library") or name == "":
            name = skill_file.stem

        frontmatter, body = self._parse_frontmatter(content)
        parsed_name = frontmatter.get("name") or name
        description = frontmatter.get("description") or ""

        # Scan surrounding folders (scripts/, tests/, references/, assets/)
        scripts, tests, refs, assets = self._inspect_sibling_folders(parent_dir)

        # Estimate tokens
        token_estimate = max(1, len(content) // 4)

        # Triggers and allowed tools
        triggers = frontmatter.get("triggers", [])
        if isinstance(triggers, str):
            triggers = [t.strip() for t in triggers.split(",") if t.strip()]

        allowed_tools = frontmatter.get("tools", [])
        if isinstance(allowed_tools, str):
            allowed_tools = [t.strip() for t in allowed_tools.split(",") if t.strip()]

        tags = frontmatter.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        # Classify
        domain, subdomains, risk = self.classifier.classify(
            name=parsed_name,
            description=description,
            content=body,
            tags=tags,
            tools=allowed_tools,
        )

        metadata = SkillMetadata(
            name=parsed_name,
            path=str(skill_file),
            description=description,
            domain=domain,
            subdomains=subdomains,
            tags=tags,
            triggers=triggers,
            allowed_tools=allowed_tools,
            risk=risk,
            has_frontmatter=bool(frontmatter),
            has_scripts=len(scripts) > 0,
            has_references=len(refs) > 0,
            has_tests=len(tests) > 0,
            script_count=len(scripts),
            test_count=len(tests),
            reference_count=len(refs),
            asset_count=len(assets),
            token_estimate=token_estimate,
            source_format="antigravity" if ".agents" in str(skill_file) else "generic",
            extra_metadata=frontmatter,
        )

        # Grade Level
        score = self.leveler.evaluate(metadata, content)

        return AnalyzedSkill(metadata=metadata, score=score)

    def _parse_frontmatter(self, text: str) -> Tuple[Dict[str, Any], str]:
        """Standard-library YAML frontmatter extractor (avoids heavy PyYAML dependency)."""
        fm_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", text, re.DOTALL)
        if not fm_match:
            return {}, text

        fm_text = fm_match.group(1)
        body = fm_match.group(2)
        parsed = {}

        current_key = None
        for line in fm_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip().strip("'\"")

                if val.startswith("[") and val.endswith("]"):
                    items = [x.strip().strip("'\"") for x in val[1:-1].split(",") if x.strip()]
                    parsed[key] = items
                elif not val:
                    parsed[key] = []
                    current_key = key
                else:
                    parsed[key] = val
                    current_key = None
            elif current_key and line.startswith("-"):
                val = line[1:].strip().strip("'\"")
                if isinstance(parsed[current_key], list):
                    parsed[current_key].append(val)

        return parsed, body

    def _inspect_sibling_folders(self, skill_dir: Path) -> Tuple[List[str], List[str], List[str], List[str]]:
        """Finds scripts, tests, references, and assets in a skill's directory."""
        scripts = []
        tests = []
        refs = []
        assets = []

        if not skill_dir.is_dir():
            return scripts, tests, refs, assets

        # Subfolders
        subfolders = {
            "scripts": (scripts, (".py", ".sh", ".ps1", ".js", ".ts")),
            "tools": (scripts, (".py", ".sh", ".ps1", ".js", ".ts")),
            "tests": (tests, (".py", ".js", ".ts")),
            "evals": (tests, (".py", ".json", ".md")),
            "verification": (tests, (".py", ".sh")),
            "references": (refs, (".md", ".json", ".txt")),
            "docs": (refs, (".md", ".txt")),
            "assets": (assets, (".json", ".png", ".jpg", ".svg", ".template")),
        }

        for folder_name, (target_list, extensions) in subfolders.items():
            sub = skill_dir / folder_name
            if sub.is_dir():
                for f in sub.rglob("*"):
                    if f.is_file() and f.suffix.lower() in extensions:
                        target_list.append(f.name)

        return scripts, tests, refs, assets
