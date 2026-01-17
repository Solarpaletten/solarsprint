# Changelog

All notable changes to this project are documented here.

This project follows an **Engine-driven development pipeline**:
each milestone is a reproducible step of the backend assembly line.

---

## [0.1.0] — 2026-01-17

### 🚀 Initial MVP Release (Engine-built)

First production-ready MVP of **Solar Sprint** — a multi-tenant task management backend,
implemented entirely via an AI-assisted code engine pipeline (A → K).

---

### ✨ Features

#### Multi-Tenant Core
- Tenant as top-level isolation boundary
- Strict tenant separation enforced server-side
- `tenantId` never accepted from client input

#### Authentication (MVP)
- Password-based authentication
- Secure password hashing (bcrypt, 12 rounds)
- No sessions, JWT, cookies, or middleware
- API-first authentication model

#### Auth API
- `POST /api/auth/signup`
  - Creates Tenant
  - Creates first User
- `POST /api/auth/login`
  - Validates credentials
  - Returns minimal auth context

#### Auth Context Utilities
- `getCurrentUser(request)`
- `requireTenant(request)`
- Auth context resolved via request header:
  - `x-user-id: <userId>`

---

### 📦 Projects API (Tenant-aware)

- `GET /api/projects`
- `POST /api/projects`
- `GET /api/projects/{id}`
- `PATCH /api/projects/{id}`
- `DELETE /api/projects/{id}`

All endpoints enforce:
- Tenant isolation
- No cross-tenant access
- No client-provided tenant identifiers

---

### 🩺 Operations

- `GET /api/health`
  - Service status
  - Timestamp
  - Database connectivity check
  - Lightweight Prisma query

---

### 🧠 Architecture Decisions

- Next.js 14 App Router
- Prisma ORM (PostgreSQL)
- Prisma client as singleton
- No manual DB connection management
- API-only backend (frontend-agnostic)

---

### 📚 Documentation

- Full README including:
  - Architecture overview
  - API contracts
  - Security principles
  - Multi-tenant rules

---

### 🛠️ Development Pipeline

- Engine-driven prompts (A → K)
- Deterministic file generation
- Additive-only changes
- Patch-based updates
- Designed for automated audits

---

### 🔒 Security Principles

- Zero trust in client input
- Strict tenant enforcement
- Minimal API responses
- No sensitive data leakage

---

### 🧪 Status

- MVP backend complete
- Ready for:
  - GitHub release
  - External audit
  - Frontend integration
  - Feature extension (tasks, roles, permissions)

---

[0.1.0]: https://github.com/<ORG>/<REPO>/releases/tag/v0.1.0
