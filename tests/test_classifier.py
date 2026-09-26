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
