# World-Scale Code LLM Setup for Solar AI

> **Document ID:** LLM-CODE-ENGINE-01  
> **Status:** APPROVED  
> **Author:** Claude (Lead Engineer)  
> **Date:** 2026-01-15

---

## Executive Summary

This document defines the architecture for a **production-grade Code Engine** capable of generating enterprise-quality code at scale. NOT a chatbot — a deterministic code generation pipeline.

---

## 1. Model Selection

### 1.1 Benchmark Analysis (January 2026)

| Model | HumanEval | MBPP | RAM (Q4) | Context | License |
|-------|-----------|------|----------|---------|---------|
| **Qwen2.5-Coder-7B** | 88.4% | 83.0% | ~5GB | 32K | Apache 2.0 |
| **Qwen2.5-Coder-14B** | 90.1% | 85.2% | ~9GB | 32K | Apache 2.0 |
| Qwen2.5-Coder-32B | 91.0% | 87.5% | ~20GB | 32K | Apache 2.0 |
| DeepSeek-Coder-V2-Lite | 81.1% | 78.0% | ~9GB | 128K | Permissive |
| Codestral 22B | 81.1% | 76.6% | ~14GB | 32K | Research |
| GPT-4o (reference) | 90.2% | 87.8% | API | 128K | Proprietary |

### 1.2 Selection Decision

**For MacBook Pro M5 (16GB unified memory):**

| Role | Model | Reason |
|------|-------|--------|
| **Junior Executor** | Qwen2.5-Coder-7B | ✅ Already installed, 88.4% HumanEval |
| **Senior Executor** | Qwen2.5-Coder-14B | 90.1% accuracy, fits in 16GB |
| **Complex Tasks** | External API | Claude API / DeepSeek API for 100k+ LOC |

**Key insight:** Qwen2.5-Coder-7B outperforms GPT-4 (87.1%) on HumanEval while running locally.

---

## 2. Architecture

### 2.1 Option A — Full Local (Privacy-First)

```
┌─────────────────────────────────────────────────────────────┐
│                      CODE ENGINE                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   ROUTER     │───▶│   JUNIOR     │    │   SENIOR     │  │
│  │              │    │ Qwen-7B      │    │ Qwen-14B     │  │
│  │ Complexity   │    │              │    │              │  │
│  │ Assessment   │───▶│ Simple tasks │    │ Medium tasks │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                   │           │
│         │                   ▼                   ▼           │
│         │            ┌─────────────────────────────┐        │
│         │            │      VALIDATOR              │        │
│         │            │  Syntax + Type + Lint       │        │
│         │            └─────────────────────────────┘        │
│         │                          │                        │
│         │                          ▼                        │
│         │            ┌─────────────────────────────┐        │
│         └───────────▶│      OUTPUT                 │        │
│                      │  Diff / Patch / Commit      │        │
│                      └─────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

**Pros:**
- 100% privacy
- Zero API costs
- Works offline
- Full control

**Cons:**
- Limited to ~14B model quality
- 10-20 sec latency per request
- Complex tasks may fail

---

### 2.2 Option B — Hybrid (Quality-First) ⭐ RECOMMENDED

```
┌─────────────────────────────────────────────────────────────┐
│                      CODE ENGINE                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    SMART ROUTER                       │   │
│  │                                                       │   │
│  │  Task Analysis:                                       │   │
│  │  • Lines affected: <50 → LOCAL                       │   │
│  │  • Single file edit → LOCAL                          │   │
│  │  • Multi-file refactor → API                         │   │
│  │  • Architecture change → API                         │   │
│  │  • New feature (complex) → API                       │   │
│  └──────────────────────────────────────────────────────┘   │
│              │                              │                │
│              ▼                              ▼                │
│  ┌──────────────────┐          ┌──────────────────────┐     │
│  │   LOCAL TIER     │          │    API TIER          │     │
│  │                  │          │                      │     │
│  │  Qwen2.5-7B      │          │  Claude API          │     │
│  │  Qwen2.5-14B     │          │  DeepSeek API        │     │
│  │                  │          │  OpenAI API          │     │
│  │  • Boilerplate   │          │                      │     │
│  │  • Simple CRUD   │          │  • Multi-file        │     │
│  │  • Tests         │          │  • Architecture      │     │
│  │  • Docs          │          │  • Complex logic     │     │
│  └──────────────────┘          └──────────────────────┘     │
│              │                              │                │
│              └──────────────┬───────────────┘                │
│                             ▼                                │
│              ┌──────────────────────────────┐                │
│              │        VALIDATOR             │                │
│              │  • TypeScript compile        │                │
│              │  • ESLint / Prettier         │                │
│              │  • Unit tests                │                │
│              │  • GitKeeper compliance      │                │
│              └──────────────────────────────┘                │
│                             │                                │
│                             ▼                                │
│              ┌──────────────────────────────┐                │
│              │        OUTPUT                │                │
│              │  • Git diff                  │                │
│              │  • PR description            │                │
│              │  • Commit message            │                │
│              └──────────────────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

**Routing Rules:**

| Criteria | Route |
|----------|-------|
| Lines < 50, single file | LOCAL (Qwen-7B) |
| Lines 50-200, single file | LOCAL (Qwen-14B) |
| Multi-file change | API |
| New feature | API |
| Refactoring > 3 files | API |
| Security-critical | API |

---

## 3. Installation Steps

### 3.1 Local Models (Ollama)

```bash
# Already installed: Qwen2.5-Coder-7B
ollama list | grep qwen

# Install Senior model (Qwen2.5-Coder-14B)
ollama pull qwen2.5-coder:14b

# Verify both models
ollama run qwen2.5-coder:7b "def hello(): pass"
ollama run qwen2.5-coder:14b "def hello(): pass"
```

### 3.2 Directory Structure

```bash
mkdir -p ~/AI-SERVER/agents/code-engine/{runtime,prompts,validators,output}

# Structure:
# AI-SERVER/
# └── agents/
#     ├── alama/          # Reasoning (existing)
#     └── code-engine/    # Code Generation (new)
#         ├── runtime/
#         │   ├── engine.py        # Main orchestrator
#         │   ├── router.py        # Task router
#         │   ├── local_client.py  # Ollama client
#         │   └── api_client.py    # External API client
#         ├── prompts/
#         │   ├── system.md        # System prompt
#         │   ├── typescript.md    # TS-specific rules
#         │   └── prisma.md        # Prisma-specific rules
#         ├── validators/
#         │   ├── syntax.py        # Syntax validation
#         │   └── gitkeeper.py     # Contract compliance
#         └── config.yaml          # Configuration
```

### 3.3 Configuration File

```yaml
# ~/AI-SERVER/agents/code-engine/config.yaml

models:
  local:
    junior:
      name: "qwen2.5-coder:7b"
      endpoint: "http://localhost:11434"
      max_tokens: 4096
      temperature: 0.1
    senior:
      name: "qwen2.5-coder:14b"
      endpoint: "http://localhost:11434"
      max_tokens: 8192
      temperature: 0.1
  api:
    claude:
      model: "claude-sonnet-4-20250514"
      max_tokens: 16384
    deepseek:
      model: "deepseek-coder"
      endpoint: "https://api.deepseek.com/v1"

routing:
  local_threshold_lines: 200
  local_threshold_files: 1
  prefer_local: true

validation:
  typescript: true
  eslint: true
  prettier: true
  tests: false  # Enable when test framework ready

output:
  format: "diff"  # diff | patch | full
  commit_message: true
  pr_description: false
```

### 3.4 Environment Variables

```bash
# Add to ~/.zshrc or ~/.bashrc

# Ollama (already configured)
export OLLAMA_HOST="http://localhost:11434"

# API Keys (for hybrid mode)
export ANTHROPIC_API_KEY="sk-ant-..."      # Optional
export DEEPSEEK_API_KEY="sk-..."           # Optional
export OPENAI_API_KEY="sk-..."             # Optional

# Code Engine
export CODE_ENGINE_MODE="hybrid"           # local | hybrid
export CODE_ENGINE_LOG_LEVEL="info"
```

---

## 4. Context Injection Strategy

### 4.1 Context Package Structure

Every code generation request includes:

```python
context_package = {
    # 1. Project metadata
    "project": {
        "name": "solar-sprint",
        "stack": "Next.js 14 + TypeScript + Prisma",
        "version": "0.2.0"
    },
    
    # 2. GitKeeper (source of truth)
    "gitkeeper": read_file("docs/gitkeeper.md"),
    
    # 3. Relevant files (auto-selected)
    "files": {
        "prisma/schema.prisma": "...",
        "lib/session.ts": "...",
        # ... only files relevant to task
    },
    
    # 4. Directory structure
    "tree": get_tree_structure(depth=3),
    
    # 5. Task specification
    "task": {
        "type": "implement",  # implement | refactor | fix | test
        "description": "Create /api/projects endpoint",
        "constraints": [
            "Use existing session.ts for auth",
            "Follow Prisma patterns from schema",
            "TypeScript strict mode"
        ]
    }
}
```

### 4.2 File Selection Algorithm

```python
def select_relevant_files(task: str, project_root: str) -> list[str]:
    """Select only files relevant to the task."""
    
    always_include = [
        "docs/gitkeeper.md",      # Source of truth
        "prisma/schema.prisma",   # Domain model
        "package.json",           # Dependencies
        "tsconfig.json"           # TypeScript config
    ]
    
    # Parse task to find references
    referenced = extract_file_references(task)
    
    # Find related files (imports, exports)
    related = find_related_files(referenced)
    
    # Limit total context
    MAX_FILES = 10
    MAX_TOKENS = 12000
    
    return prioritize_and_truncate(
        always_include + referenced + related,
        max_files=MAX_FILES,
        max_tokens=MAX_TOKENS
    )
```

### 4.3 Prompt Template

```markdown
# SYSTEM PROMPT FOR CODE ENGINE

You are a Senior TypeScript Engineer. Generate production-ready code.

## RULES (NON-NEGOTIABLE)
1. Output ONLY code — no explanations, no markdown
2. Follow existing patterns in the codebase
3. Use types from Prisma schema
4. Never invent new patterns
5. If unsure, output "CLARIFICATION_NEEDED: <question>"

## PROJECT CONTEXT
{gitkeeper_content}

## RELEVANT FILES
{file_contents}

## TASK
{task_description}

## OUTPUT FORMAT
Return ONLY the complete file content. No ```typescript``` markers.
```

---

## 5. Anti-Hallucination Rules

### 5.1 Prevention Layer

| Rule | Implementation |
|------|---------------|
| **No invented imports** | Validate against package.json |
| **No invented types** | Validate against Prisma schema |
| **No invented APIs** | Validate against existing routes |
| **No invented patterns** | Enforce codebase patterns via examples |
| **Temperature = 0.1** | Near-deterministic output |

### 5.2 Validation Pipeline

```python
def validate_generated_code(code: str, context: dict) -> ValidationResult:
    """Multi-stage validation pipeline."""
    
    checks = [
        # Stage 1: Syntax
        check_typescript_syntax(code),
        
        # Stage 2: Imports
        check_imports_exist(code, context["package.json"]),
        
        # Stage 3: Types
        check_types_exist(code, context["prisma_schema"]),
        
        # Stage 4: Patterns
        check_patterns_match(code, context["existing_files"]),
        
        # Stage 5: GitKeeper compliance
        check_gitkeeper_rules(code, context["gitkeeper"])
    ]
    
    return ValidationResult(
        passed=all(c.passed for c in checks),
        errors=[c.error for c in checks if not c.passed]
    )
```

### 5.3 Retry Strategy

```
Generate → Validate → FAIL?
    │                   │
    │                   ▼
    │         Append error to prompt
    │                   │
    │                   ▼
    │         Retry (max 3 times)
    │                   │
    ▼                   │
SUCCESS ◄───────────────┘
    │
    ▼
  OUTPUT
```

---

## 6. Recommended Default Configuration

### For Solar Sprint Project:

```yaml
# RECOMMENDED SETUP

mode: hybrid

primary_local_model: qwen2.5-coder:7b     # Fast, good enough for 80% tasks
secondary_local_model: qwen2.5-coder:14b  # Better quality, slower
fallback_api: claude                       # Complex tasks only

routing:
  use_local_for:
    - single_file_edits
    - boilerplate_generation
    - test_writing
    - documentation
    - simple_crud
    
  use_api_for:
    - multi_file_refactoring
    - architecture_changes
    - security_critical_code
    - complex_business_logic

validation:
  always_run:
    - typescript_compile
    - eslint
  run_on_api_results:
    - full_test_suite
```

---

## 7. Next Actions (TASKS)

### Immediate (Today)

| Task ID | Description | Owner | Priority |
|---------|-------------|-------|----------|
| **CODE-01** | Install Qwen2.5-Coder-14B | Junior | HIGH |
| **CODE-02** | Create code-engine directory structure | Junior | HIGH |
| **CODE-03** | Write config.yaml | Claude | HIGH |

### This Week

| Task ID | Description | Owner | Priority |
|---------|-------------|-------|----------|
| **CODE-04** | Implement engine.py (orchestrator) | Claude | HIGH |
| **CODE-05** | Implement router.py (task routing) | Claude | MEDIUM |
| **CODE-06** | Implement local_client.py | Junior | MEDIUM |
| **CODE-07** | Create system prompt templates | Claude | MEDIUM |

### Next Week

| Task ID | Description | Owner | Priority |
|---------|-------------|-------|----------|
| **CODE-08** | Implement validation pipeline | Claude | HIGH |
| **CODE-09** | Add API client (Claude/DeepSeek) | Claude | LOW |
| **CODE-10** | Integration tests | Junior | LOW |

---

## 8. Quick Start Commands

```bash
# 1. Install 14B model
ollama pull qwen2.5-coder:14b

# 2. Test both models
echo "def fib(n): return n if n<2 else fib(n-1)+fib(n-2)" | \
  ollama run qwen2.5-coder:7b "Optimize this function"

echo "def fib(n): return n if n<2 else fib(n-1)+fib(n-2)" | \
  ollama run qwen2.5-coder:14b "Optimize this function"

# 3. Create directory structure
cd ~/AI-SERVER
mkdir -p agents/code-engine/{runtime,prompts,validators,output}

# 4. Verify setup
ollama list
# Expected: qwen2.5-coder:7b, qwen2.5-coder:14b, llama3:8b
```

---

## Summary

```
╔══════════════════════════════════════════════════════════════╗
║  WORLD-SCALE CODE ENGINE — CONFIGURATION SUMMARY             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  LOCAL MODELS:                                               ║
║  • Junior: Qwen2.5-Coder-7B (88.4% HumanEval) ✅ INSTALLED  ║
║  • Senior: Qwen2.5-Coder-14B (90.1% HumanEval) → INSTALL    ║
║                                                              ║
║  API FALLBACK:                                               ║
║  • Claude API (complex tasks)                                ║
║  • DeepSeek API (alternative)                                ║
║                                                              ║
║  ARCHITECTURE: Hybrid (Option B) ⭐                          ║
║  • 80% tasks → Local (fast, free, private)                   ║
║  • 20% tasks → API (complex, multi-file)                     ║
║                                                              ║
║  ANTI-HALLUCINATION:                                         ║
║  • Temperature: 0.1                                          ║
║  • GitKeeper context injection                               ║
║  • 5-stage validation pipeline                               ║
║  • Retry with error feedback                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

**Document Status:** READY FOR REVIEW  
**Next Step:** D=>L for approval, then execute CODE-01 through CODE-03

