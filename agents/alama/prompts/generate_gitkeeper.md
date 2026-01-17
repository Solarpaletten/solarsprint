# Prompt: Generate GitKeeper

**Purpose:** Create a GitKeeper document — the single source of truth for a project.

---

## System Prompt

```
You are Alama, a documentation specialist for software projects.
Your task is to generate a GitKeeper document that serves as the canonical source of truth.

GitKeeper is NOT:
- A README (that's for users)
- A changelog (that's for releases)
- A todo list (that's for daily work)

GitKeeper IS:
- The architectural contract
- The sprint scope definition
- The acceptance criteria
- The engineering checklist

Rules:
- Be precise and unambiguous
- Use FREEZE markers for locked decisions
- Structure for machine and human readability
- Include only actionable, verifiable items
```

---

## User Prompt Template

```
Generate a GitKeeper document for:

**Project:** {project_name}
**Current Phase:** {phase}
**Sprint:** {sprint_name}

**Context:**
{project_context}

**Architecture Decisions (if known):**
{architecture_notes}

**Scope (what's included):**
{scope_included}

**Out of Scope (explicitly excluded):**
{scope_excluded}

---

Generate GitKeeper in the following format:

# {PROJECT_NAME} — GitKeeper v{version}

## 0) Meta
- Owner:
- Supervisor:
- Engineer:
- Status:
- Last Updated:

## 1) Mission
[One paragraph describing the project goal]

## 2) Non-Negotiable Principles (FREEZE)
[List of architectural decisions that CANNOT change]

## 3) Current Sprint Scope
### Included
[Bullet list of what's IN this sprint]

### Excluded
[Bullet list of what's explicitly OUT]

## 4) Domain Model
[Entity relationships in text/ASCII format]

## 5) Technical Stack (FREEZE)
[Technologies locked for this project]

## 6) API Contracts (FREEZE)
[Key endpoints with request/response shapes]

## 7) Acceptance Criteria
[Verifiable conditions for "done"]

## 8) Engineering Checklist
[Numbered task list for implementation]

## 9) Change Control
[Rules for what can/cannot be changed]

## 10) Next Releases (Future)
[What comes after this sprint]
```

---

## Example Output

```markdown
# SOLAR SPRINT — GitKeeper v0.1

## 0) Meta
- Owner: Leanid (Architect)
- Supervisor: Dashka (Super-Senior)
- Engineer: Claude
- Status: FREEZE v0.1
- Last Updated: 2026-01-15

## 1) Mission
Build a web-first, multi-tenant task management system that stores full context 
and allows returning to work after days/weeks without losing anything.

## 2) Non-Negotiable Principles (FREEZE)
1. Web-first (Next.js App Router)
2. Multi-tenant: Account → Users → Projects → Task Capsules
3. Account isolation: accountId from session ONLY
4. Task Capsule is the core: one screen = all context
5. API-first: mobile client consumes same API

## 3) Current Sprint Scope
### Included
- Auth + session
- Account context
- Projects CRUD
- Task Capsules CRUD
- Attachments (URL-based)
- Reminders (manual)
- Dashboard
- Share payload

### Excluded
- Mobile app
- AI assistant
- Auto-planning
- External integrations

## 4) Domain Model
Account
  ├── Users (OWNER/ADMIN/MEMBER)
  ├── Projects
  │    ├── ProjectMembers
  │    └── Tasks
  │         ├── Attachments
  │         ├── ContactActions
  │         ├── Reminders
  │         └── TaskHistory

## 5) Technical Stack (FREEZE)
- Next.js 15 (App Router)
- Prisma 6
- PostgreSQL
- TypeScript

## 6) API Contracts (FREEZE)
- GET /api/auth/session
- POST /api/auth/login
- GET /api/projects
- POST /api/projects
- GET /api/tasks?projectId=...
- POST /api/tasks
- GET /api/tasks/{id}
- PATCH /api/tasks/{id}

## 7) Acceptance Criteria
1. User can sign up / log in
2. User sees dashboard with grouped tasks
3. User can create project
4. User can create task and open Task Capsule
5. User can add attachments, contacts, reminders
6. User can mark task DONE
7. User can generate share payload
8. Multi-tenant isolation enforced

## 8) Engineering Checklist
1. [ ] Bootstrap Next.js + Prisma + Postgres
2. [ ] Implement auth/session
3. [ ] Implement multi-tenant guards
4. [ ] Implement Projects endpoints + UI
5. [ ] Implement Tasks endpoints + UI
6. [ ] Implement attachments/contacts/reminders
7. [ ] Implement dashboard queries
8. [ ] Implement share endpoint
9. [ ] Add TaskHistory logging
10. [ ] Final polish
11. [ ] Push to GitHub, tag v0.1.0

## 9) Change Control
❌ NOT allowed: modify URLs, remove fields, rename models
✅ Allowed: add new fields, add new endpoints

## 10) Next Releases (Future)
- v0.2: File upload + signed URLs
- v0.3: Mobile client
- v0.4: AI summaries
- v0.5: Auto-planning
```

---

## Usage

```bash
# Provide context and generate
python runtime/alama.py gitkeeper \
  --project "solar-sprint" \
  --phase "MVP v0.1" \
  --context "$(cat project_notes.txt)" \
  --output gitkeeper/solar-sprint.md
```
