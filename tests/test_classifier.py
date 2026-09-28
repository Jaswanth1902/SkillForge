"""
tests/test_classifier.py - Unit tests for taxonomy classification and risk profiling
"""

import pytest
from skillforge.classifier import SkillClassifier
from skillforge.models import SkillDomain, RiskProfile


def test_classify_security_domain():
    classifier = SkillClassifier()
    domain, subdomains, risk = classifier.classify(
        name="security-linting",
        description="Scans codebase for dangerous calls, injection vectors, and hardcoded secrets.",
        content="Runs AST inspection to detect secrets and verify sandbox execution.",
        tags=["security", "audit", "sandbox"],
        tools=["security_audit"],
    )
    assert domain == SkillDomain.SECURITY_SANDBOX
    assert risk in (RiskProfile.LOW, RiskProfile.MEDIUM, RiskProfile.SAFE)


def test_classify_web_harvesting():
    classifier = SkillClassifier()
    domain, subdomains, risk = classifier.classify(
        name="scrapling",
        description="Autonomous undetectable web scraping and data harvesting engine powered by Scrapling.",
        content="Bypasses Cloudflare, WAFs, and anti-bot defenses using adaptive fetchers and Playwright.",
        tags=["scraping", "web", "crawler"],
        tools=["browser_navigate"],
    )
    assert domain == SkillDomain.WEB_HARVESTING


def test_classify_critical_risk():
    classifier = SkillClassifier()
    domain, subdomains, risk = classifier.classify(
        name="nuclear-cleanup",
        description="Force cleans directories",
        content="Execute rm -rf / or rmdir /s on targets with sudo privileges.",
        tags=["cleanup"],
        tools=["run_command"],
    )
    assert risk == RiskProfile.CRITICAL


@pytest.mark.parametrize(
    "keyword",
    [
        "GitHub Actions", "github-actions", "CI/CD", "ci-cd", "Docker",
        "Dockerfile", "Kubernetes", "k8s", "Terraform", "Helm", "ArgoCD",
        "Argo CD", "continuous integration", "continuous delivery",
        "continuous deployment", "infrastructure as code",
    ],
)
def test_classify_devops_keywords(keyword):
    domain, subdomains, risk = SkillClassifier().classify(
        name="example", description=keyword, content="", tags=[], tools=[],
    )
    assert domain == SkillDomain.DEVOPS_PLATFORM
    assert keyword.lower() in subdomains
    assert risk == RiskProfile.LOW


@pytest.mark.parametrize(
    "keyword",
    [
        "SQLite WAL", "Postgres", "PostgreSQL", "Redis", "pgvector",
        "vector store", "vector stores", "Alembic migrations",
        "write-ahead log", "write-ahead logging",
    ],
)
def test_classify_database_keywords(keyword):
    domain, _, risk = SkillClassifier().classify(
        name="example", description=keyword, content="", tags=[], tools=[],
    )
    assert domain == SkillDomain.DATA_KNOWLEDGE
    assert risk == RiskProfile.LOW


@pytest.mark.parametrize(
    "description, content, expected_domain",
    [
        ("GitHub Actions workflow", "Continuous integration for Python.",
         SkillDomain.DEVOPS_PLATFORM),
        ("Build Docker containers", "Use a Dockerfile for reproducible builds.",
         SkillDomain.DEVOPS_PLATFORM),
        ("Kubernetes releases", "Manage Helm charts with ArgoCD.",
         SkillDomain.DEVOPS_PLATFORM),
        ("Terraform plans", "Review infrastructure as code changes.",
         SkillDomain.DEVOPS_PLATFORM),
        ("SQLite WAL tuning", "Configure write-ahead logging for persistence.",
         SkillDomain.DATA_KNOWLEDGE),
        ("PostgreSQL schema changes", "Apply Alembic migrations.",
         SkillDomain.DATA_KNOWLEDGE),
        ("Redis persistence", "Inspect snapshots and expiration settings.",
         SkillDomain.DATA_KNOWLEDGE),
        ("Semantic retrieval", "Manage vector stores with pgvector.",
         SkillDomain.DATA_KNOWLEDGE),
    ],
)
def test_classify_infrastructure_descriptions(description, content, expected_domain):
    domain, _, _ = SkillClassifier().classify(
        name="example", description=description, content=content, tags=[], tools=[],
    )
    assert domain == expected_domain


@pytest.mark.parametrize("field", ["name", "description", "content", "tags", "tools"])
@pytest.mark.parametrize(
    "keyword, expected_domain",
    [("Terraform", SkillDomain.DEVOPS_PLATFORM), ("Redis", SkillDomain.DATA_KNOWLEDGE)],
)
def test_classify_infrastructure_across_input_fields(field, keyword, expected_domain):
    inputs = dict(name="", description="", content="", tags=[], tools=[])
    inputs[field] = [keyword] if field in ("tags", "tools") else keyword
    domain, _, _ = SkillClassifier().classify(**inputs)
    assert domain == expected_domain


@pytest.mark.parametrize(
    "description, expected_domain",
    [
        ("Multi-agent orchestration with a supervisor", SkillDomain.AGENT_ARCHITECTURE),
        ("Python refactoring and unit-test debugging", SkillDomain.SOFTWARE_ENGINEERING),
        ("Security audit of encryption and secrets", SkillDomain.SECURITY_SANDBOX),
        ("Web scraping with a browser crawler", SkillDomain.WEB_HARVESTING),
        ("Knowledge-base retrieval with embeddings", SkillDomain.DATA_KNOWLEDGE),
        ("React frontend design with CSS", SkillDomain.UI_UX_CRAFT),
        ("Linux systemd service deployment", SkillDomain.DEVOPS_PLATFORM),
        ("Academic research and literature synthesis", SkillDomain.RESEARCH_ANALYSIS),
        ("Audio transcription and speech synthesis", SkillDomain.MULTIMODAL_SENSORY),
        ("Calendar automation and email workflow", SkillDomain.WORKFLOW_PRODUCTIVITY),
    ],
)
def test_classify_existing_domains(description, expected_domain):
    domain, _, _ = SkillClassifier().classify(
        name="example", description=description, content="", tags=[], tools=[],
    )
    assert domain == expected_domain


@pytest.mark.parametrize(
    "description",
    ["redistribute", "helmsman", "terraforming", "argocds", "postgresqlish", "alembics"],
)
def test_infrastructure_keywords_do_not_match_inside_words(description):
    domain, subdomains, _ = SkillClassifier().classify(
        name="example", description=description, content="", tags=[], tools=[],
    )
    assert domain == SkillDomain.SOFTWARE_ENGINEERING
    assert subdomains == []
