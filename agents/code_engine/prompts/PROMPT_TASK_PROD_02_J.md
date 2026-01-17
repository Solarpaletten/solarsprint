// PROMPT_TASK_PROD_02_J.md

ROLE: SENIOR BACKEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack:
- Next.js 14 (App Router)
- TypeScript
- Prisma ORM
- PostgreSQL
- Multi-tenant architecture

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- tenantId MUST be resolved server-side
- tenantId MUST NOT come from client input
- Do NOT invent new domain models
- Do NOT modify Prisma schema
- Only additive, backward-compatible code allowed
- Preserve existing handlers

TARGET FILE:
app/api/projects/[id]/route.ts

EXISTING HANDLERS:
- GET
- DELETE

EXISTING UTILITIES:
- requireTenant(request): returns { userId, tenantId }
- Prisma client at '@/lib/prisma'

TASK:
Add UPDATE endpoint for Project.

FUNCTIONAL REQUIREMENTS:
1. HTTP method: PATCH
2. Path: /api/projects/[id]
3. Input JSON body:
   - name?: string
   - description?: string
4. Logic:
   - Resolve tenant using requireTenant(request)
   - Find Project by id
   - If not found → return 404
   - If project.tenantId !== tenantId → return 403
   - Update ONLY provided fields (name, description)
5. Security:
   - Do NOT accept tenantId from request
   - Enforce strict tenant isolation
6. Response:
   - Return updated project JSON

TECHNICAL CONSTRAINTS:
- Use NextRequest / NextResponse
- Use async/await
- Use try/catch
- Use Prisma client
- Follow App Router conventions

IMPORTANT:
- Do NOT remove or modify existing GET or DELETE handlers
- Add PATCH handler in the SAME file
- If no fields provided → return 400

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript

OUTPUT FORMAT:
<complete updated route.ts source code only>
