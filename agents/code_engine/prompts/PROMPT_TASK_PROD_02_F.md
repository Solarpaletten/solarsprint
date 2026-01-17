// PROMPT_TASK_PROD_02_F.md

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
- tenantId MUST be resolved server-side
- Do NOT invent new domain models
- Do NOT modify Prisma schema
- Only additive, backward-compatible code

EXISTING UTILITIES (ALREADY IMPLEMENTED):
- getCurrentUser(request: Request): Promise<{ id, email, tenantId } | null>

TARGET FILE:
lib/auth/requireTenant.ts

TASK:
Implement tenant guard helper.

FUNCTIONAL REQUIREMENTS:
1. Export async function:
   - requireTenant(request: Request)
2. Logic:
   - Call getCurrentUser(request)
   - If user is null → throw Response with status 401
   - If tenantId missing → throw Response with status 401
3. Return object:
   {
     userId: string,
     tenantId: string
   }
4. Do NOT read tenantId from headers or body
5. Do NOT create sessions or tokens
6. Do NOT log anything
7. Do NOT catch errors silently

TECHNICAL CONSTRAINTS:
- Use Web Fetch API Request
- Throw new Response(...) on auth failure
- Keep function minimal and reusable

EXPECTED OUTPUT:
- Full source code of lib/auth/requireTenant.ts
- Valid TypeScript
- No explanations
- No markdown
- Code ONLY

IMPORTANT:
If something required is missing, output:
CLARIFICATION_NEEDED: <question>

OUTPUT FORMAT:
<raw TypeScript source code only>
