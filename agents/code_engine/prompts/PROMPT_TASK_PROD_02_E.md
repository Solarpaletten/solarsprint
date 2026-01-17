// PROMPT_TASK_PROD_02_E.md

ROLE: SENIOR BACKEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack:
- Next.js 14
- TypeScript
- Prisma ORM
- PostgreSQL
- Multi-tenant architecture

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- tenantId MUST exist on User
- tenantId MUST NOT come from client input
- Do NOT invent new domain models
- Do NOT modify Prisma schema

TASK:
Implement current user resolver utility.

FILE TO GENERATE:
lib/auth/getCurrentUser.ts

REQUIREMENTS:
1. Export async function:
   - getCurrentUser(request: Request)
2. Logic:
   - Read header: "x-user-id"
   - If header missing → return null
   - Find User by id using Prisma
   - If not found → return null
3. Return object:
   - id
   - email
   - tenantId
4. Do NOT implement:
   - sessions
   - JWT
   - cookies
   - tokens
5. Do NOT throw — return null on failure
6. Use Prisma client
7. Use async/await
8. No logging

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript

OUTPUT:
<complete getCurrentUser.ts source code only>
