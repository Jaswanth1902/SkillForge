# 🗺️ SkillForge 10-Domain Taxonomy Ontology

**Ontology Version**: 1.0.0  
**Scope**: Universal Classification Schema for Premade & Custom AI Agent Skills  

---

## 1. Architecture Overview

SkillForge categorizes skills across **10 Primary Domains**. Classification uses multi-vector feature extraction:
1. **Keyword Dictionaries & Regex Matching**
2. **Tool Invocations & Permissions**
3. **Script Extensions & Environment Signatures**
4. **Contextual Triggers & Safety Hazard Profiling**

---

## 2. The 10 Primary Taxonomy Domains

### 1. `agent-architecture`
* **Focus**: Hypervisor scheduling, agent swarms, supervisor meshes, council deliberation, memory routing, subagent delegation.
* **Key Signatures**: `orchestration`, `swarm`, `supervisor`, `mesh`, `council`, `subagent`, `dispatch`, `blackboard`, `scheduler`.
* **Standard Tools**: `invoke_subagent`, `send_message`, `manage_subagents`, `agent-council`.

### 2. `software-engineering`
* **Focus**: Test-driven development, refactoring, pure-python decoupling, AST inspection, debugging, pull request reviews.
* **Key Signatures**: `refactoring`, `tdd`, `unit-test`, `architecture`, `clean-code`, `linting`, `ast-grep`, `debugging`, `git`, `pr`.
* **Standard Tools**: `replace_file_content`, `write_to_file`, `view_file`, `run_command`.

### 3. `security-sandbox`
* **Focus**: AST-grounded security linting, secret leak detection, Windows windowless isolation (`CREATE_NO_WINDOW`), privilege containment, safe exec.
* **Key Signatures**: `security`, `sandbox`, `audit`, `secrets`, `cve`, `vulnerability`, `isolation`, `firewall`, `oauth`, `token`.
* **Standard Tools**: `security-linting`, `safe_exec`, `security_audit`.

### 4. `web-harvesting`
* **Focus**: Undetectable web scraping, Playwright browser automation, Scrapling stealth fetchers, OpenGraph metadata extraction, social media dorks.
* **Key Signatures**: `scraping`, `crawler`, `scrapling`, `playwright`, `camoufox`, `stealth`, `dom`, `browser`, `html`, `parser`.
* **Standard Tools**: `scrapling`, `browser_navigate`, `crawl4ai`, `browser_snapshot`.

### 5. `data-knowledge`
* **Focus**: SQLite WAL storage, vector embeddings, FTS5 semantic search, graph memory, Obsidian vault synchronization, relational indexes.
* **Key Signatures**: `database`, `sqlite`, `vector`, `embedding`, `rag`, `fts5`, `wal`, `graph`, `knowledge-base`, `obsidian`, `vault`.
* **Standard Tools**: `sqlite-vec`, `omnia-memory-mcp`, `databank_engine`.

### 6. `ui-ux-craft`
* **Focus**: Emil Kowalski tactile physics, Atelier luxury aesthetics, anti-slop design filters, claymorphism, micro-spacing, typography, CSS.
* **Key Signatures**: `ui`, `ux`, `frontend`, `design`, `css`, `tailwind`, `react`, `emil-kowalski`, `tactile`, `physics`, `claymorphism`, `anti-slop`.
* **Standard Tools**: `ui-ux-pro-max`, `impeccable`, `anti-slop`, `generate_image`.

### 7. `devops-platform`
* **Focus**: Daemon orchestration, Windows/Linux process management, WSL, PowerShell profile debloating, package management (`uv`, `npm`, `cargo`).
* **Key Signatures**: `devops`, `docker`, `ci-cd`, `powershell`, `bash`, `linux`, `windows`, `daemon`, `service`, `wsl`, `uv`, `pip`.
* **Standard Tools**: `service-orchestration`, `service_manager`, `safe_exec`.

### 8. `research-analysis`
* **Focus**: ArXiv paper synthesis, academic ideation, literature reviews, ground truth harvesting, executive report compilation.
* **Key Signatures**: `research`, `arxiv`, `paper`, `literature`, `synthesis`, `benchmark`, `academic`, `analysis`, `report`, `dossier`.
* **Standard Tools**: `search_web`, `read_url_content`, `report-generator`, `notebooklm-bridge`.

### 9. `multimodal-sensory`
* **Focus**: Whisper speech-to-text, voice synthesis, image generation, vision models, camera/audio device interfacing.
* **Key Signatures**: `multimodal`, `audio`, `voice`, `whisper`, `speech`, `tts`, `stt`, `vision`, `image-generation`, `transcription`.
* **Standard Tools**: `generate_image`, `sensory-mcp`, `whisper`.

### 10. `workflow-productivity`
* **Focus**: Task observation, personal LinkedIn growth, Telegram remote bridges, sprint briefings, habit tracking, personal automation.
* **Key Signatures**: `workflow`, `productivity`, `linkedin`, `telegram`, `automation`, `email`, `kanban`, `sprint`, `task-observer`.
* **Standard Tools**: `linkedin-growth`, `telegram-bridge`, `task-observer`.
