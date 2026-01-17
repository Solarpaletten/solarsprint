// PROMPT_TASK_PROD_02_C.md

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
- tenantId MUST be resolved from User record
- Do NOT invent new domain models
- Do NOT remove or modify existing fields or relations
- Only additive, backward-compatible changes allowed

EXISTING UTILITIES (ALREADY IMPLEMENTED):
- hashPassword(password: string): Promise<string>
- verifyPassword(password: string, hash: string): Promise<boolean>

TASK:
Implement login API endpoint.

REQUIREMENTS:
1. Create API route:
   - POST /api/auth/login
2. Accept JSON body:
   - email: string
   - password: string
3. Logic:
   - Find User by email
   - If user not found → return 401
   - Verify password using verifyPassword
   - If invalid → return 401
4. Multi-tenant:
   - tenantId MUST come from User record
   - Do NOT accept tenantId from request body
5. Response:
   - On success: return JSON with user id, email, tenantId
   - Do NOT return passwordHash
6. Error handling:
   - Invalid credentials → 401
   - Missing fields → 400
7. Do NOT implement:
   - sessions
   - JWT
   - cookies
   - tokens
   - refresh logic
8. Do NOT touch Prisma schema
9. Do NOT modify existing utilities

TECHNICAL CONSTRAINTS:
- Use Next.js App Router convention
- Use NextResponse from 'next/server'
- Use async/await
- Use try/catch

EXPECTED OUTPUT:
- Full source code of the API route file
- Correct imports
- Valid TypeScript
- No explanations
- No markdown
- Code ONLY

OUTPUT FORMAT:
<typescript code only>
