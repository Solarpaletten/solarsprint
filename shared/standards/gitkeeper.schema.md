# GitKeeper Schema v1.0

**Standard:** Solar Sprint Project
**Purpose:** Define the canonical structure for GitKeeper documents

---

## What is GitKeeper?

GitKeeper is the **single source of truth** for a project sprint.
It is a machine-readable and human-readable contract that defines:

- What we're building
- How we're building it
- What's in scope
- What's explicitly out
- How to verify completion

---

## GitKeeper vs Other Documents

| Document | Purpose | Audience | Update Frequency |
|----------|---------|----------|------------------|
| **GitKeeper** | Sprint contract | Engineers | Per sprint |
| README | Project intro | Users/Developers | Rarely |
| CHANGELOG | Version history | Users | Per release |
| TODO | Daily tasks | Individual | Daily |
| ADR | Architecture decisions | Team | Per decision |

---

## Required Sections

### 0) Meta (Required)

```markdown
## 0) Meta
- Owner: [Name] (Role)
- Supervisor: [Name] (Role)
- Engineer: [Name] (Role)
- Status: FREEZE v{version} | DRAFT | IN PROGRESS
- Last Updated: YYYY-MM-DD
```

### 1) Mission (Required)

```markdown
## 1) Mission
[One paragraph, max 3 sentences describing the project goal]
```

### 2) Non-Negotiable Principles (Required)

```markdown
## 2) Non-Negotiable Principles (FREEZE)
1. [Principle that CANNOT change]
2. [Principle that CANNOT change]
...
```

**Rules:**
- Use numbered list
- Each principle must be verifiable
- Mark with (FREEZE) to indicate locked

### 3) Current Sprint Scope (Required)

```markdown
## 3) Current Sprint Scope

### Included
- [Feature/Task that IS in this sprint]
- [Feature/Task that IS in this sprint]

### Excluded
- [Feature/Task that is explicitly OUT]
- [Feature/Task that is explicitly OUT]
```

**Rules:**
- Be explicit about what's OUT
- Prevents scope creep

### 4) Domain Model (Required)

```markdown
## 4) Domain Model

[ASCII diagram or structured text showing entity relationships]

Entity1
  ├── Entity2 (relationship)
  │    └── Entity3
  └── Entity4
```

### 5) Technical Stack (Required)

```markdown
## 5) Technical Stack (FREEZE)
- Framework: [Name] [Version]
- Database: [Name] [Version]
- Language: [Name] [Version]
...
```

### 6) API Contracts (Conditional)

```markdown
## 6) API Contracts (FREEZE)

### Endpoint: GET /api/resource
- Response: { field: type }

### Endpoint: POST /api/resource
- Request: { field: type }
- Response: { field: type }
```

**Required if:** Project has API

### 7) Acceptance Criteria (Required)

```markdown
## 7) Acceptance Criteria
1. [Verifiable condition for "done"]
2. [Verifiable condition for "done"]
...
```

**Rules:**
- Each criterion must be testable
- Binary: pass/fail

### 8) Engineering Checklist (Required)

```markdown
## 8) Engineering Checklist
1. [ ] Task description
2. [ ] Task description
3. [x] Completed task
...
```

**Rules:**
- Numbered list
- Checkbox format
- Order = execution order

### 9) Change Control (Required)

```markdown
## 9) Change Control

❌ NOT allowed:
- [Change that breaks contract]

✅ Allowed:
- [Change that extends without breaking]
```

### 10) Next Releases (Optional)

```markdown
## 10) Next Releases (Future)
- v{next}: [Brief description]
- v{next+1}: [Brief description]
```

---

## FREEZE Rules

| Marker | Meaning |
|--------|---------|
| `(FREEZE)` | Section is locked, no changes |
| `(DRAFT)` | Section is work in progress |
| `(DEPRECATED)` | Section will be removed |

---

## Versioning

- **v0.x** — Development, may change
- **v1.x** — Stable, additive changes only
- **v2.x** — Breaking changes from v1

---

## Validation

A valid GitKeeper must have:

- [ ] All required sections present
- [ ] Meta section complete
- [ ] At least 3 acceptance criteria
- [ ] At least 5 checklist items
- [ ] Clear included/excluded scope
- [ ] Version number

---

## File Naming

```
{project_name}_gitkeeper_v{version}.md

Examples:
- solar_sprint_gitkeeper_v0.1.md
- alama_gitkeeper_v1.0.md
```

---

## Example Minimal GitKeeper

```markdown
# PROJECT NAME — GitKeeper v0.1

## 0) Meta
- Owner: Name (Architect)
- Supervisor: Name (Senior)
- Engineer: Name
- Status: FREEZE v0.1
- Last Updated: 2026-01-15

## 1) Mission
Build [what] that [does what] for [whom].

## 2) Non-Negotiable Principles (FREEZE)
1. Principle one
2. Principle two

## 3) Current Sprint Scope
### Included
- Feature A
- Feature B

### Excluded
- Feature C (future)

## 4) Domain Model
EntityA → EntityB → EntityC

## 5) Technical Stack (FREEZE)
- Tech: Version

## 7) Acceptance Criteria
1. User can do X
2. System does Y

## 8) Engineering Checklist
1. [ ] Task 1
2. [ ] Task 2

## 9) Change Control
❌ NOT allowed: breaking changes
✅ Allowed: additive changes
```

---

**GitKeeper Schema v1.0** | Solar Sprint Standards
