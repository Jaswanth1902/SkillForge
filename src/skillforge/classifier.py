"""
skillforge.classifier - Multi-Vector Taxonomy Classifier & Risk Profiler
"""

from __future__ import annotations

import re
from typing import Dict, List, Set, Tuple
from skillforge.models import SkillDomain, RiskProfile


# Domain Taxonomy Signature Dictionaries
DOMAIN_SIGNATURES: Dict[SkillDomain, Dict[str, List[str]]] = {
    SkillDomain.AGENT_ARCHITECTURE: {
        "keywords": [
            "agent", "orchestration", "multi-agent", "swarm", "supervisor", "mesh",
            "council", "deliberation", "subagent", "dispatch", "delegation", "hypervisor",
            "scheduler", "blackboard", "handoff", "router", "kernel", "autonomous",
        ],
        "tools": ["invoke_subagent", "send_message", "manage_subagents", "agent-council"],
    },
    SkillDomain.SOFTWARE_ENGINEERING: {
        "keywords": [
            "refactoring", "tdd", "unit-test", "architecture", "decoupling", "python",
            "typescript", "javascript", "rust", "go", "code-review", "clean-code",
            "linting", "ast-grep", "debugging", "algorithm", "git", "pr", "diff",
        ],
        "tools": ["run_command", "replace_file_content", "write_to_file", "view_file"],
    },
    SkillDomain.SECURITY_SANDBOX: {
        "keywords": [
            "security", "sandbox", "audit", "secrets", "cve", "penetration", "warden",
            "vulnerability", "injection", "privilege", "isolation", "firewall", "auth",
            "token", "oauth", "encryption", "hashing", "signature", "create_no_window",
        ],
        "tools": ["security-linting", "safe_exec", "security_audit"],
    },
    SkillDomain.WEB_HARVESTING: {
        "keywords": [
            "scraping", "crawler", "scrapling", "playwright", "camoufox", "stealth",
            "dom", "browser", "html", "parser", "beautifulsoup", "selenium", "dork",
            "instagram", "reddit", "twitter", "api-gateway", "webhook", "fetcher",
        ],
        "tools": ["browser_navigate", "browser_snapshot", "crawl4ai", "scrapling"],
    },
    SkillDomain.DATA_KNOWLEDGE: {
        "keywords": [
            "database", "sqlite", "postgres", "vector", "embedding", "rag", "fts5",
            "wal", "graph", "knowledge-base", "obsidian", "vault", "memory", "schema",
            "retrieval", "semantic", "cosine", "fnv", "datastore",
        ],
        "tools": ["sqlite-vec", "omnia-memory-mcp", "databank_engine"],
    },
    SkillDomain.UI_UX_CRAFT: {
        "keywords": [
            "ui", "ux", "frontend", "design", "css", "tailwind", "react", "vue",
            "emil-kowalski", "tactile", "physics", "animation", "claymorphism", "glass",
            "atelier", "typography", "palette", "component", "anti-slop", "impeccable",
        ],
        "tools": ["generate_image", "ui-ux-pro-max", "impeccable", "anti-slop"],
    },
    SkillDomain.DEVOPS_PLATFORM: {
        "keywords": [
            "devops", "docker", "ci-cd", "kubernetes", "powershell", "bash", "linux",
            "windows", "daemon", "service", "systemd", "wsl", "process", "deploy",
            "package-manager", "uv", "pip", "npm", "cargo", "cloud",
        ],
        "tools": ["service-orchestration", "service_manager", "safe_exec"],
    },
    SkillDomain.RESEARCH_ANALYSIS: {
        "keywords": [
            "research", "arxiv", "paper", "literature", "synthesis", "benchmark",
            "academic", "analysis", "report", "evaluation", "dossier", "survey",
            "ground-truth", "study", "metrics", "deep-dive",
        ],
        "tools": ["search_web", "read_url_content", "report-generator", "notebooklm-bridge"],
    },
    SkillDomain.MULTIMODAL_SENSORY: {
        "keywords": [
            "multimodal", "audio", "voice", "whisper", "speech", "tts", "stt",
            "vision", "image-generation", "ocr", "camera", "microphone", "sensory",
            "transcription", "synthetic-voice", "sound",
        ],
        "tools": ["generate_image", "sensory-mcp", "whisper"],
    },
    SkillDomain.WORKFLOW_PRODUCTIVITY: {
        "keywords": [
            "workflow", "productivity", "linkedin", "telegram", "automation", "email",
            "notion", "kanban", "sprint", "roadmap", "task-observer", "habit", "calendar",
            "social-media", "outreach", "resume", "growth",
        ],
        "tools": ["linkedin-growth", "telegram-bridge", "task-observer"],
    },
}

# High-Risk Signatures
RISK_RULES = [
    (re.compile(r"\b(rm\s+-rf|del\s+/[sS]|rmdir\s+/[sS]|drop\s+database|format\s+[a-zA-Z]:)\b", re.IGNORECASE), RiskProfile.CRITICAL),
    (re.compile(r"\b(chmod\s+777|sudo|runas|elevate|admin|bypass-executionpolicy)\b", re.IGNORECASE), RiskProfile.CRITICAL),
    (re.compile(r"\b(api_key|secret|password|credential|private_key|token|auth_token)\b", re.IGNORECASE), RiskProfile.HIGH),
    (re.compile(r"\b(subprocess\.Popen|subprocess\.run|os\.system|exec\(|eval\()\b", re.IGNORECASE), RiskProfile.HIGH),
    (re.compile(r"\b(write_to_file|replace_file_content|edit|patch|modify)\b", re.IGNORECASE), RiskProfile.MEDIUM),
    (re.compile(r"\b(view_file|read|list_dir|search|query|analyze|audit)\b", re.IGNORECASE), RiskProfile.SAFE),
]


class SkillClassifier:
    """Classifies skills into taxonomy domains and calculates operational risk profiles."""

    def classify(
        self,
        name: str,
        description: str,
        content: str,
        tags: List[str],
        tools: List[str],
    ) -> Tuple[SkillDomain, List[str], RiskProfile]:
        """
        Calculates primary domain, matched subdomains, and risk profile.
        """
        combined_text = f"{name} {description} {' '.join(tags)} {' '.join(tools)} {content[:2000]}".lower()

        domain_scores: Dict[SkillDomain, int] = {domain: 0 for domain in SkillDomain}
        matched_tags: Dict[SkillDomain, Set[str]] = {domain: set() for domain in SkillDomain}

        # 1. Score against domain dictionary
        for domain, sigs in DOMAIN_SIGNATURES.items():
            for kw in sigs["keywords"]:
                pattern = rf"\b{re.escape(kw)}\b"
                matches = len(re.findall(pattern, combined_text))
                if matches > 0:
                    domain_scores[domain] += matches * 2
                    matched_tags[domain].add(kw)

            for tool in sigs["tools"]:
                if tool.lower() in combined_text or tool in tools:
                    domain_scores[domain] += 5
                    matched_tags[domain].add(tool)

        # 2. Pick Primary Domain (Default to Software Engineering if tied at 0)
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        primary_domain = sorted_domains[0][0] if sorted_domains[0][1] > 0 else SkillDomain.SOFTWARE_ENGINEERING

        # 3. Derive Subdomains / Secondary Tags
        subdomains = list(matched_tags[primary_domain])[:5]
        if not subdomains and tags:
            subdomains = tags[:3]

        # 4. Assess Risk Profile
        risk = self._assess_risk(content, tools, tags)

        return primary_domain, subdomains, risk

    def _assess_risk(self, content: str, tools: List[str], tags: List[str]) -> RiskProfile:
        """Evaluates potential execution hazard based on commands and tool capabilities."""
        content_sample = content[:4000]

        # Check explicit rules
        for pattern, risk_level in RISK_RULES:
            if pattern.search(content_sample):
                return risk_level

        # Check tool hazard
        tool_hazard = "safe"
        for t in tools:
            tl = t.lower()
            if any(k in tl for k in ["kill", "delete", "drop", "sudo"]):
                return RiskProfile.CRITICAL
            if any(k in tl for k in ["exec", "command", "bash", "powershell", "subshell"]):
                tool_hazard = "high"
            elif any(k in tl for k in ["write", "modify", "edit"]) and tool_hazard != "high":
                tool_hazard = "medium"

        if tool_hazard == "high":
            return RiskProfile.HIGH
        elif tool_hazard == "medium":
            return RiskProfile.MEDIUM

        return RiskProfile.LOW
