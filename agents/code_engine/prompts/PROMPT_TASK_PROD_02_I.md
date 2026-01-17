// PROMPT_TASK_PROD_02_I.md

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
- Use existing helpers ONLY

TARGET FILE:
app/api/projects/[id]/route.ts

EXISTING UTILITIES:
- requireTenant(request): returns { userId, tenantId }

TASK:
Add DELETE endpoint for Project.

FUNCTIONAL REQUIREMENTS:
1. HTTP method: DELETE
2. Path: /api/projects/[id]
3. Logic:
   - Resolve tenant using requireTenant
   - Find Project by id
   - If not found → return 404
   - If project.tenantId !== tenantId → return 403
   - Delete project
4. Security:
   - Do NOT accept tenantId from request
   - Enforce tenant isolation
5. Response:
   - On success return status 204 OR JSON { success: true }

TECHNICAL CONSTRAINTS:
- Use NextRequest / NextResponse
- Use async/await
- Use try/catch
- Use Prisma client
- Follow App Router conventions

IMPORTANT:
- Preserve existing GET handler if present
- Add DELETE handler in the same file
- Do NOT remove existing code

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript

OUTPUT FORMAT:
<complete updated route.ts source code only>
