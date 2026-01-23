Solar Sprint — Multi-tenant Backend (MVP)

What it is
- API-only backend for multi-tenant task management

Stack
- Next.js 14 (App Router)
- TypeScript
- Prisma (PostgreSQL)

Quick Rules
- tenantId is never accepted from client
- All auth context resolved server-side

API Overview
- /api/health
- /api/auth/signup
- /api/auth/login
- /api/projects
- /api/projects/{id}

Auth Model (MVP)
- Password-based
- Auth via x-user-id header

Documentation
- ARCHITECTURE.md — system design
- CHANGELOG.md — releases

add text.txt