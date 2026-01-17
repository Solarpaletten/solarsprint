Solar Sprint — Backend Architecture

This document describes the runtime and domain architecture of the Solar Sprint backend.

The architecture prioritizes:

Determinism

Tenant isolation

Auditability

Backend-first correctness

🎯 Architectural Goals

Strict multi-tenancy

Zero trust in client input

API-only backend

Deterministic build process

Minimal moving parts

Future extensibility without refactor

🧱 High-Level Overview
Client
  |
  |  (HTTP / JSON)
  v
Next.js App Router (API-only)
  |
  |  Auth / Tenant Resolution
  v
Domain APIs (Projects, Health, Auth)
  |
  |  Prisma ORM
  v
PostgreSQL


There is no frontend coupling and no session layer in the MVP.

🧠 Core Architectural Decisions
1. API-Only Backend

No UI rendering

No server components

No cookies or sessions

No middleware auth layer

All logic lives inside API route handlers.

This allows:

Frontend independence

Easy integration (web, mobile, CLI)

Clean audit surface

2. Multi-Tenant by Construction

Multi-tenancy is not a feature — it is the default execution model.

Rules:

Every business entity belongs to a Tenant

tenantId is never accepted from client input

tenantId is resolved server-side only

Cross-tenant access is explicitly forbidden

Tenant resolution flow:

Request
  ↓
getCurrentUser()
  ↓
requireTenant()
  ↓
tenantId injected into domain logic

3. Authentication Model (MVP)

Authentication is intentionally minimal.

What exists:

Password-based auth

Secure password hashing (bcrypt, 12 rounds)

Stateless API calls

What does NOT exist:

Sessions

JWT

Cookies

Refresh tokens

Middleware auth

Auth context is resolved via request header:

x-user-id: <userId>


This is explicitly intentional for MVP and internal tooling.

🔐 Security Model

Security is enforced structurally.

See ENGINE.md for enforcement rules.

Core Principles

Zero trust in client input

Minimal response payloads

No sensitive fields returned

Explicit authorization checks in every route

Enforcement Points

requireTenant() throws on unauthorized access

Tenant ownership verified before:

Read

Update

Delete

Prisma queries scoped by tenantId

🗂️ Project Structure
projects/solar-sprint/
├── app/
│   └── api/
│       ├── auth/
│       │   ├── signup/route.ts
│       │   └── login/route.ts
│       ├── projects/
│       │   ├── route.ts
│       │   └── [id]/route.ts
│       └── health/route.ts
│
├── lib/
│   └── auth/
│       ├── password.ts
│       ├── getCurrentUser.ts
│       └── requireTenant.ts
│
├── prisma/
│   └── schema.prisma
│
├── README.md
├── CHANGELOG.md
├── ENGINE.md
└── ARCHITECTURE.md

🧬 Domain Model
Tenant

Top-level isolation boundary

Owns Users and Projects

User

Belongs to exactly one Tenant

Identified by id

Authenticated via passwordHash

Project

Belongs to exactly one Tenant

All access validated against tenant ownership

🛠️ Prisma & Database

PostgreSQL backend

Prisma ORM

Prisma client as singleton

No manual $connect() / $disconnect()

Health checks use:

await prisma.$queryRaw`SELECT 1`


This avoids connection lifecycle issues in serverless environments.

🧪 Operational Endpoints
Health Check
GET /api/health


Returns:

Service status

Timestamp

Database connectivity state

No authentication required.

🔁 Architecture Evolution & Constraints


Each architectural layer corresponds to Engine prompts

Changes are additive and auditable

Architecture is therefore:

Reproducible

Reviewable

Evolvable without refactor

🚀 Evolution Path (v0.2.0+)

Planned extensions without breaking architecture:

Roles (OWNER / ADMIN / MEMBER)

Tasks domain

Role-based access control

Validation helpers

Audit logging

Policy enforcement layer

All future work continues via alphabet-based Engine prompts (L → …).

📌 Summary

Solar Sprint uses a clean, minimal backend architecture

Multi-tenancy is enforced at every layer

Security is structural, not optional

The Engine is the primary builder

Architecture is deterministic and auditable

High-level diagram

Tenant resolution flow

Domain model

Project structure

Evolution path