# 🛡️ SkillForge Leveling Specification (5-Tier Maturity Standard)

**Standard Version**: 1.0.0  
**Domain**: Agentic AI Skill Governance, Maturity Assessment & Lifecycle Verification  
**Maintainer**: Antigravity Core Architecture  

---

## 1. Executive Summary

As AI agent frameworks (Antigravity, Claude Code, Cursor, Windsurf, Codex) scale, agent capabilities are increasingly authored as modular "skills". However, the quality of these skills varies wildly—from raw text prompt snippets that hallucinate and leak secrets, to production-grade, AST-grounded, self-healing execution modules.

The **SkillForge 5-Tier Leveling Standard** establishes an objective, measurable maturity rubric. Every skill is assigned an **XP Score (0–100)** and graded into one of five maturity levels:

```
[Level 1: Novice Promptlet]   (0 - 24 XP)   🥉 Raw instructions, unverified, high hallucination risk
          │
          ▼
[Level 2: Structured Standard] (25 - 39 XP)  🥈 YAML frontmatter, markdown sections, clear triggers
          │
          ▼
[Level 3: Tool-Backed Adept]   (40 - 64 XP)  🥇 Dedicated deterministic scripts, parameters, CLI
          │
          ▼
[Level 4: Self-Verifying]      (65 - 84 XP)  💎 Automated pytest harness, AST linting, blast-radius gating
          │
          ▼
[Level 5: Autonomous Master]   (85 - 100 XP) 👑 Closed-loop recovery, multi-agent protocol, telemetry
```

---

## 2. The 5 Maturity Tiers

### 🥉 Level 1: Novice Promptlet (0–24 XP)
* **Definition**: A free-form prompt snippet or unstructured markdown document.
* **Characteristics**:
  - Missing YAML frontmatter (`---`).
  - No deterministic tool backing.
  - Vague activation conditions.
* **Operational Risk**: High risk of silent drift, hallucinated parameters, and inconsistent invocation.

### 🥈 Level 2: Structured Standard (25–39 XP)
* **Definition**: A standard AI agent skill adhering to modern specification formats (`SKILL.md`).
* **Characteristics**:
  - Valid YAML frontmatter containing `name`, `description`, `domain`, and optional `tags`/`triggers`.
  - Structured Markdown with H2 headings (`## Instructions`, `## Guidelines`, `## Examples`).
  - Explicit contextual trigger criteria ("Use when the user...").
* **Operational Risk**: Low reasoning risk, but execution relies purely on LLM in-context code generation.

### 🥇 Level 3: Tool-Backed Adept (40–64 XP)
* **Definition**: A skill backed by dedicated, deterministic executable code.
* **Characteristics**:
  - Sibling `scripts/` or `tools/` containing standalone Python, Shell, or TypeScript utilities.
  - Well-defined CLI arguments and parameter schemas.
  - Zero global side effects (isolated execution).
  - Explicit tool dependencies declared in metadata.
* **Operational Risk**: Predictable execution; requires manual user verification if bugs arise.

### 💎 Level 4: Self-Verifying Expert (65–84 XP)
* **Definition**: A production-grade skill capable of self-testing and blast-radius safety enforcement.
* **Characteristics**:
  - Automated test suite in `tests/` or `verification/` (e.g. pytest suite).
  - Strict OS isolation: Windows subprocesses pass `creationflags=0x08000000` (`CREATE_NO_WINDOW`).
  - Static AST and syntax verification prior to deployment.
  - Comprehensive error handling and non-zero exit codes on failure.
* **Operational Risk**: Minimal. Failures are caught immediately by automated gates.

### 👑 Level 5: Autonomous Master (85–100 XP)
* **Definition**: An elite, self-healing, multi-agent capable capability.
* **Characteristics**:
  - Closed-loop feedback: capable of self-correcting after unexpected tool errors.
  - Multi-agent coordination: supports council deliberation, supervisory review, and delegation handoffs.
  - Central Blackboard state persistence (`.cache/blackboard.sqlite` WAL).
  - Token telemetry: records token burnage, latency profiles, and enforces token-bounded distillation.
* **Operational Risk**: Production zero-entropy standard.

---

## 3. Rubric Scoring Matrix (100 Total Points)

| Dimension | Max Points | Evaluation Criteria |
| :--- | :--- | :--- |
| **Structure & Frontmatter** | **20 pts** | Valid YAML (10), substantive description (5), structured H2 sections (5) |
| **Executable Tooling** | **25 pts** | Sibling scripts in `scripts/` (15), explicit tools declared (5), auxiliary assets/references (5) |
| **Safety & Verification** | **25 pts** | Automated tests in `tests/` (15), `CREATE_NO_WINDOW` isolation (5), error handling/fallbacks (5) |
| **Trigger & Guidance** | **15 pts** | Explicit trigger list (8), input/output code examples (7) |
| **Autonomy & Resilience** | **15 pts** | Performance/token telemetry (5), persistent state/Blackboard (5), closed-loop/multi-agent contracts (5) |

---

## 4. How to Level Up a Skill

Run `skillforge levelup <skill_name>` to automatically generate required scaffolds:
1. **L1 ➔ L2**: Add YAML frontmatter and structured headers using `skillforge levelup`.
2. **L2 ➔ L3**: Generate a deterministic CLI script in `scripts/<skill_name>_runner.py`.
3. **L3 ➔ L4**: Generate an automated pytest harness in `tests/test_<skill_name>.py`.
4. **L4 ➔ L5**: Wire telemetry and state persistence into Central Blackboard WAL.
