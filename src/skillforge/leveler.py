"""
skillforge.leveler - 5-Tier Maturity Leveling & Scoring Rubric Engine
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple
from skillforge.models import SkillLevel, LevelScore, SkillMetadata


class SkillLeveler:
    """
    Evaluates agent skills against an empirical 5-tier maturity rubric.
    Assigns XP points (0-100), determines SkillLevel, and outputs actionable gaps.
    """

    def evaluate(self, meta: SkillMetadata, content: str) -> LevelScore:
        """
        Grades skill maturity and returns LevelScore with detailed criteria breakdown.
        """
        breakdown: Dict[str, int] = {
            "structure_and_frontmatter": 0,  # Max 20
            "executable_tooling": 0,          # Max 25
            "safety_and_verification": 0,    # Max 25
            "trigger_and_guidance": 0,       # Max 15
            "autonomy_and_resilience": 0,    # Max 15
        }
        passed: List[str] = []
        missing: List[str] = []
        recommendations: List[str] = []

        content_lower = content.lower()

        # -------------------------------------------------------------
        # 1. Structure & Frontmatter (Max 20 pts)
        # -------------------------------------------------------------
        if meta.has_frontmatter:
            breakdown["structure_and_frontmatter"] += 10
            passed.append("YAML frontmatter header present")
        else:
            missing.append("Missing standard YAML frontmatter (---\\nname: ...\\ndescription: ...\\n---)")
            recommendations.append("Add YAML frontmatter with 'name' and 'description' fields.")

        if meta.description and len(meta.description.strip()) > 20:
            breakdown["structure_and_frontmatter"] += 5
            passed.append("Substantive skill description provided")
        else:
            missing.append("Brief or missing description")
            recommendations.append("Expand description to explain exact purpose and activation context.")

        if len(content.splitlines()) >= 15 and re.search(r"^##\s+", content, re.MULTILINE):
            breakdown["structure_and_frontmatter"] += 5
            passed.append("Structured markdown sections with H2 headings")
        else:
            missing.append("Unstructured or brief prose")
            recommendations.append("Organize content into clear ## Instructions, ## Guidelines, and ## Examples.")

        # -------------------------------------------------------------
        # 2. Executable Tooling & Determinism (Max 25 pts)
        # -------------------------------------------------------------
        if meta.has_scripts or meta.script_count > 0:
            breakdown["executable_tooling"] += 15
            passed.append(f"Dedicated executable script(s) found ({meta.script_count} scripts)")
        elif re.search(r"```(python|bash|sh|powershell|js|ts)", content):
            breakdown["executable_tooling"] += 8
            passed.append("Embedded executable code blocks present")
        else:
            missing.append("No executable scripts or code blocks")
            recommendations.append("Back prompt instructions with deterministic scripts in a scripts/ folder.")

        if meta.allowed_tools or len(meta.allowed_tools) > 0:
            breakdown["executable_tooling"] += 5
            passed.append(f"Explicit tool dependencies declared ({len(meta.allowed_tools)} tools)")
        elif re.search(r"\b(run_command|view_file|replace_file_content|write_to_file)\b", content):
            breakdown["executable_tooling"] += 3
            passed.append("References standard tool primitives")

        if meta.reference_count > 0 or meta.asset_count > 0:
            breakdown["executable_tooling"] += 5
            passed.append(f"Auxiliary assets/references attached ({meta.reference_count + meta.asset_count} files)")

        # -------------------------------------------------------------
        # 3. Safety & Verification (Max 25 pts)
        # -------------------------------------------------------------
        if meta.has_tests or meta.test_count > 0:
            breakdown["safety_and_verification"] += 15
            passed.append(f"Automated test harness / verification suite present ({meta.test_count} tests)")
        else:
            missing.append("No automated test suite (tests/ or verification/)")
            recommendations.append("Create automated unit/integration tests to verify deterministic behavior.")

        if "create_no_window" in content_lower or "0x08000000" in content_lower:
            breakdown["safety_and_verification"] += 5
            passed.append("Strict Windows windowless subprocess isolation enforced (Law 8)")
        elif "subprocess" in content_lower:
            missing.append("Subprocess call without explicit CREATE_NO_WINDOW flag")
            recommendations.append("Add creationflags=0x08000000 to all Windows subprocess calls.")

        if any(w in content_lower for w in ["try:", "catch", "error handling", "fallback", "exit code"]):
            breakdown["safety_and_verification"] += 5
            passed.append("Explicit error handling and failure modes documented")
        else:
            missing.append("Missing error handling or fallback strategies")
            recommendations.append("Document explicit error categories and fallback behavior.")

        # -------------------------------------------------------------
        # 4. Trigger & Guidance Precision (Max 15 pts)
        # -------------------------------------------------------------
        if meta.triggers and len(meta.triggers) >= 2:
            breakdown["trigger_and_guidance"] += 8
            passed.append(f"Explicit trigger keywords declared ({len(meta.triggers)} triggers)")
        elif "use when" in content_lower or "activate when" in content_lower or "trigger:" in content_lower:
            breakdown["trigger_and_guidance"] += 5
            passed.append("Contextual activation condition specified in prose")
        else:
            missing.append("Vague or missing activation triggers")
            recommendations.append("Add explicit 'Use when the user...' activation phrases in frontmatter or intro.")

        if "example" in content_lower or "usage:" in content_lower:
            breakdown["trigger_and_guidance"] += 7
            passed.append("Concrete invocation examples provided")
        else:
            missing.append("No practical usage examples")
            recommendations.append("Include input/output code examples and CLI invocation patterns.")

        # -------------------------------------------------------------
        # 5. Autonomy & Closed-Loop Resilience (Max 15 pts)
        # -------------------------------------------------------------
        if any(w in content_lower for w in ["telemetry", "token_bounded", "benchmark", "profil"]):
            breakdown["autonomy_and_resilience"] += 5
            passed.append("Performance profiling or token telemetry telemetry integrated")

        if any(w in content_lower for w in ["blackboard", "sqlite", "wal", "state machine", "datastore", "memory"]):
            breakdown["autonomy_and_resilience"] += 5
            passed.append("Persistent state management / blackboard integration")

        if any(w in content_lower for w in ["council", "multi-agent", "closed-loop", "self-healing", "retry"]):
            breakdown["autonomy_and_resilience"] += 5
            passed.append("Closed-loop feedback or multi-agent delegation contracts")

        # -------------------------------------------------------------
        # Compute Total XP and Level
        # -------------------------------------------------------------
        total_xp = sum(breakdown.values())

        if total_xp >= 85 and (meta.has_tests or meta.test_count > 0) and (meta.has_scripts or meta.script_count > 0):
            level = SkillLevel.L5_AUTONOMOUS
        elif total_xp >= 60 and (meta.has_tests or meta.test_count > 0):
            level = SkillLevel.L4_SELF_VERIFYING
        elif (total_xp >= 35 and (meta.has_scripts or meta.script_count > 0)) or total_xp >= 45:
            level = SkillLevel.L3_TOOL_BACKED
        elif total_xp >= 25 and meta.has_frontmatter:
            level = SkillLevel.L2_STANDARD
        else:
            level = SkillLevel.L1_PROMPTLET

        # Filter missing list based on next level target
        next_level_targets = self._get_next_level_gaps(level, breakdown, meta)
        if next_level_targets:
            missing = next_level_targets

        return LevelScore(
            level=level,
            xp_score=total_xp,
            criteria_breakdown=breakdown,
            passed_criteria=passed,
            missing_for_next_level=missing,
            recommendations=recommendations,
        )

    def _get_next_level_gaps(
        self,
        current_level: SkillLevel,
        breakdown: Dict[str, int],
        meta: SkillMetadata,
    ) -> List[str]:
        """Identifies exact barriers preventing advancement to the immediate next tier."""
        gaps: List[str] = []

        if current_level == SkillLevel.L1_PROMPTLET:
            gaps.append("Missing standard YAML frontmatter with 'name' and 'description'")
            gaps.append("Structured sections (## Instructions, ## Examples) needed for Level 2")

        elif current_level == SkillLevel.L2_STANDARD:
            if not meta.has_scripts and meta.script_count == 0:
                gaps.append("Must add standalone executable scripts in scripts/ or tools/ to reach Level 3")
            if breakdown["executable_tooling"] < 15:
                gaps.append("Must declare explicit tool dependencies or executable parameters")

        elif current_level == SkillLevel.L3_TOOL_BACKED:
            if not meta.has_tests and meta.test_count == 0:
                gaps.append("Must create automated test suite (pytest in tests/) to reach Level 4")
            gaps.append("Must document error handling, input validation, and blast-radius safety")

        elif current_level == SkillLevel.L4_SELF_VERIFYING:
            gaps.append("Must integrate closed-loop feedback, state persistence (Blackboard), or token telemetry to reach Level 5")
            gaps.append("Must establish multi-agent protocol or autonomous error recovery")

        elif current_level == SkillLevel.L5_AUTONOMOUS:
            gaps = ["Maximum maturity level achieved (Autonomous Master)"]

        return gaps
