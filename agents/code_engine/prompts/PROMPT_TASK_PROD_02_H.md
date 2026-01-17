// PROMPT_TASK_PROD_02_H.md

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
- This is NOT a solar/energy project
- Domain: task management system
- tenantId MUST exist on User
- tenantId MUST NOT come from client input
- tenantId MUST be resolved via requireTenant
- Do NOT invent new domain models
- Do NOT modify existing models or relations
- Only additive, backward-compatible code

TARGET FILE:
app/api/projects/[id]/route.ts

EXISTING UTILITIES (ALREADY IMPLEMENTED):
- requireTenant(request): Promise<{ userId: string, tenantId: string }>
- Prisma client at '@/lib/prisma'

TASK:
Implement Project-by-ID API endpoint with tenant isolation.

FUNCTIONAL REQUIREMENTS:
1. HTTP method: GET
2. Route param:
   - id: string (project id)
3. Logic:
   - Resolve tenantId via requireTenant(request)
   - Fetch Project by id
   - If project not found → return 404
   - If project.tenantId !== tenantId → return 403
4. Response:
   - On success → return Project JSON
5. Security:
   - Do NOT accept tenantId from client
   - Enforce strict tenant isolation
6. Error handling:
   - Unauthorized → 401 (from requireTenant)
   - Not found → 404
   - Forbidden → 403
7. Do NOT implement:
   - sessions
   - tokens
   - middleware
   - mutations (GET only)

TECHNICAL CONSTRAINTS:
- Use Next.js App Router conventions
- Use NextRequest / NextResponse
- Use async/await
- Use try/catch
- Use Prisma findUnique

EXPECTED OUTPUT:
- FULL content of app/api/projects/[id]/route.ts
- Valid TypeScript
- Correct imports
- Code ONLY
- No markdown
- No explanations
- No comments outside code

IMPORTANT:
If something is missing or ambiguous, output:
  // CLARIFICATION_NEEDED: <question>

OUTPUT FORMAT:
<raw TypeScript source code only>
