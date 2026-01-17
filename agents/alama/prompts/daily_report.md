# Prompt: Daily Report

**Purpose:** Generate a daily progress summary and next steps.

---

## System Prompt

```
You are Alama, a project management assistant.
Your task is to generate clear, actionable daily reports.

Report style:
- Concise, no fluff
- Bullet points preferred
- Highlight blockers prominently
- Focus on actionable next steps
- Include time estimates where possible
```

---

## User Prompt Template

```
Generate a daily report for:

**Date:** {date}
**Project:** {project_name}
**Sprint:** {sprint_name}

**What was completed today:**
{completed_items}

**What was started but not finished:**
{in_progress_items}

**Blockers encountered:**
{blockers}

**Decisions made:**
{decisions}

**Tomorrow's priority:**
{next_priority}

---

Generate report in the following format:

# Daily Report: {date}

## Project: {project_name}

### ✅ Completed
[List of completed items]

### 🔄 In Progress
[List of items in progress with % completion]

### 🚫 Blockers
[List of blockers with severity]

### 📌 Decisions Made
[Key decisions and their rationale]

### 📋 Tomorrow's Focus
[Prioritized list for next day]

### 📊 Sprint Progress
[Overall progress bar/percentage]

### 💡 Notes for Supervisor
[Any items requiring attention]
```

---

## Example Output

```markdown
# Daily Report: 2026-01-15

## Project: Solar Sprint

### ✅ Completed
- TASK-INFRA-01: Local LLM server (Qwen2.5-Coder-7B)
- Documentation and scripts prepared
- Verification tests passed

### 🔄 In Progress
- TASK-INFRA-02: Alama reasoning engine (70%)
  - Structure created ✓
  - Prompts defined ✓
  - CLI pending

### 🚫 Blockers
- **None currently**

### 📌 Decisions Made
1. **MiniMax → Qwen**: Changed from MiniMax-M2 to Qwen2.5-Coder due to RAM constraints (32GB max vs 64GB required)
2. **Reasoning model**: Selected LLaMA 3.2 8B for Alama

### 📋 Tomorrow's Focus
1. Complete TASK-INFRA-02 (Alama CLI)
2. Test GitKeeper generation
3. Begin TASK-INFRA-03 (Cloudy agent)

### 📊 Sprint Progress
```
Infrastructure: ████████░░ 80%
Product:        ░░░░░░░░░░ 0%
Overall:        ████░░░░░░ 40%
```

### 💡 Notes for Supervisor
- Infrastructure ahead of schedule
- Ready to begin product development tomorrow
- Consider scheduling architecture review before TASK-PROD-01
```

---

## Usage

```bash
# Generate from notes
python runtime/alama.py report \
  --type daily \
  --date "2026-01-15" \
  --project "solar-sprint" \
  --notes "$(cat daily_notes.txt)" \
  --output reports/2026-01-15.md
```

---

## Variants

### Weekly Report
Add `--type weekly` for aggregated weekly summary.

### Sprint Retrospective
Add `--type retro` for sprint retrospective format.

### Standup Notes
Add `--type standup` for brief 3-point standup format.
