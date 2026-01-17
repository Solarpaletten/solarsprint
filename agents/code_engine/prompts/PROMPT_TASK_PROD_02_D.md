// PROMPT_TASK_PROD_02_D.md

ROLE: SENIOR BACKEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack:
- Next.js 14 (App Router)
- Prisma ORM
- PostgreSQL
- Multi-tenant architecture

GITKEEPER RULES (MANDATORY):
- This is NOT a solar/energy project
- Domain: task management system
- tenantId MUST exist on User
- tenantId MUST NOT come from client input
- Do NOT invent new domain models
- Do NOT remove existing fields or relations
- Only additive, backward-compatible changes allowed

TARGET FILE:
app/api/auth/signup/route.ts

TASK:
Create a signup API endpoint.

FUNCTIONAL REQUIREMENTS:
1. HTTP method: POST
2. Input JSON body:
   - email: string
   - password: string
   - tenantName: string
3. Validation:
   - all fields required
   - return 400 on missing data
4. Logic:
   - create new Tenant
   - hash password using existing utility
   - create first User linked to Tenant
5. tenantId MUST be generated server-side
6. Do NOT implement sessions, cookies, JWT, or auth middleware
7. Do NOT return passwordHash
8. Use Prisma client
9. Follow Next.js App Router conventions

SECURITY REQUIREMENTS:
- tenantId MUST NOT come from request body
- password MUST be hashed
- return minimal safe response only

RESPONSE FORMAT (200):
{
  userId: string,
  email: string,
  tenantId: string
}

EXPECTED OUTPUT:
- FULL content of app/api/auth/signup/route.ts
- Valid TypeScript
- Valid Next.js App Router handler
- Code ONLY
- No markdown
- No explanations
- No comments outside code

IMPORTANT:
- Preserve existing project conventions
- Use existing Prisma models ONLY
- If something is missing, output:
  // CLARIFICATION_NEEDED: <question>

OUTPUT FORMAT:
<raw TypeScript source code only>
