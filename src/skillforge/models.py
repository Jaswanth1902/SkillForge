"""
skillforge.models - Data structures for Skill Leveling and Taxonomy Engine
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any


class SkillLevel(str, Enum):
    """5-Tier Maturity Hierarchy for Agent Skills."""
    L1_PROMPTLET = "L1_PROMPTLET"       # Raw unstructured markdown / prompt snippet
    L2_STANDARD = "L2_STANDARD"         # Standard SKILL.md with YAML frontmatter & instructions
    L3_TOOL_BACKED = "L3_TOOL_BACKED"   # Backed by executable scripts or CLI tools
    L4_SELF_VERIFYING = "L4_SELF_VERIFYING"  # Includes automated tests, linting & blast-radius gating
    L5_AUTONOMOUS = "L5_AUTONOMOUS"     # Closed-loop self-healing, multi-agent protocol & telemetry

    @property
    def rank(self) -> int:
        order = {
            SkillLevel.L1_PROMPTLET: 1,
            SkillLevel.L2_STANDARD: 2,
            SkillLevel.L3_TOOL_BACKED: 3,
            SkillLevel.L4_SELF_VERIFYING: 4,
            SkillLevel.L5_AUTONOMOUS: 5,
        }
        return order[self]

    @property
    def display_name(self) -> str:
        names = {
            SkillLevel.L1_PROMPTLET: "Level 1: Novice Promptlet",
            SkillLevel.L2_STANDARD: "Level 2: Structured Standard",
            SkillLevel.L3_TOOL_BACKED: "Level 3: Tool-Backed Adept",
            SkillLevel.L4_SELF_VERIFYING: "Level 4: Self-Verifying Expert",
            SkillLevel.L5_AUTONOMOUS: "Level 5: Autonomous Master",
        }
        return names[self]

    @property
    def badge(self) -> str:
        badges = {
            SkillLevel.L1_PROMPTLET: "🥉 L1-PROMPTLET",
            SkillLevel.L2_STANDARD: "🥈 L2-STANDARD",
            SkillLevel.L3_TOOL_BACKED: "🥇 L3-TOOL-BACKED",
            SkillLevel.L4_SELF_VERIFYING: "💎 L4-VERIFIED",
            SkillLevel.L5_AUTONOMOUS: "👑 L5-AUTONOMOUS",
        }
        return badges[self]


class RiskProfile(str, Enum):
    """Blast radius and operational safety risk profile."""
    SAFE = "safe"             # Pure read-only or reasoning
    LOW = "low"               # Minor file creation in local sandbox
    MEDIUM = "medium"         # Subprocess commands, non-destructive external calls
    HIGH = "high"             # System edits, file deletes, active network writes
    CRITICAL = "critical"     # Shell execution with elevated privileges, external credentials


class SkillDomain(str, Enum):
    """10 Primary Taxonomy Domains for AI Agent Skills."""
    AGENT_ARCHITECTURE = "agent-architecture"
    SOFTWARE_ENGINEERING = "software-engineering"
    SECURITY_SANDBOX = "security-sandbox"
    WEB_HARVESTING = "web-harvesting"
    DATA_KNOWLEDGE = "data-knowledge"
    UI_UX_CRAFT = "ui-ux-craft"
    DEVOPS_PLATFORM = "devops-platform"
    RESEARCH_ANALYSIS = "research-analysis"
    MULTIMODAL_SENSORY = "multimodal-sensory"
    WORKFLOW_PRODUCTIVITY = "workflow-productivity"


@dataclass
class SkillMetadata:
    """Parsed representation of an agent skill."""
    name: str
    path: str
    description: str = ""
    domain: SkillDomain = SkillDomain.SOFTWARE_ENGINEERING
    subdomains: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    allowed_tools: List[str] = field(default_factory=list)
    risk: RiskProfile = RiskProfile.LOW
    has_frontmatter: bool = False
    has_scripts: bool = False
    has_references: bool = False
    has_tests: bool = False
    script_count: int = 0
    test_count: int = 0
    reference_count: int = 0
    asset_count: int = 0
    token_estimate: int = 0
    source_format: str = "antigravity"  # 'antigravity', 'claude_code', 'cursor', 'generic'
    extra_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["domain"] = self.domain.value
        d["risk"] = self.risk.value
        return d


@dataclass
class LevelScore:
    """Comprehensive maturity score and level grading."""
    level: SkillLevel
    xp_score: int                           # 0 to 100
    criteria_breakdown: Dict[str, int]     # category -> points awarded
    passed_criteria: List[str]             # List of fulfilled requirements
    missing_for_next_level: List[str]      # Gaps blocking the next level tier
    recommendations: List[str]             # Actionable instructions to level up

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level.value,
            "rank": self.level.rank,
            "display_name": self.level.display_name,
            "badge": self.level.badge,
            "xp_score": self.xp_score,
            "criteria_breakdown": self.criteria_breakdown,
            "passed_criteria": self.passed_criteria,
            "missing_for_next_level": self.missing_for_next_level,
            "recommendations": self.recommendations,
        }


@dataclass
class AnalyzedSkill:
    """Full unified analysis of a single skill."""
    metadata: SkillMetadata
    score: LevelScore

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata.to_dict(),
            "score": self.score.to_dict(),
        }


@dataclass
class SkillCatalogReport:
    """Aggregate taxonomy and leveling census across a collection of skills."""
    total_skills: int
    level_distribution: Dict[str, int]
    domain_distribution: Dict[str, int]
    risk_distribution: Dict[str, int]
    average_xp: float
    skills: List[AnalyzedSkill] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_skills": self.total_skills,
            "average_xp": round(self.average_xp, 1),
            "level_distribution": self.level_distribution,
            "domain_distribution": self.domain_distribution,
            "risk_distribution": self.risk_distribution,
            "skills": [s.to_dict() for s in self.skills],
        }
