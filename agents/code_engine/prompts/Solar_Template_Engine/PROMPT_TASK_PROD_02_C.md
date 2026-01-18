// PROMPT_TASK_PROD_02_C.md
// FIXED: Added findFirst requirement (email is NOT globally unique)

ROLE: SENIOR BACKEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack:
- Next.js 14 (App Router)
- TypeScript
- Prisma ORM
- PostgreSQL
- Multi-tenant architecture

PRISMA SCHEMA CONTEXT (IMPORTANT):
model User {
  // ...
  @@unique([tenantId, email])  // email is unique PER TENANT, not globally!
}

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
  Import: '@/lib/auth/password'
- verifyPassword(password: string, hash: string): Promise<boolean>
  Import: '@/lib/auth/password'

TARGET FILE:
app/api/auth/login/route.ts

TASK:
Implement login API endpoint.

REQUIREMENTS:
1. HTTP method: POST
2. Path: /api/auth/login
3. Accept JSON body:
   - email: string
   - password: string
4. Validation:
   - Missing fields → return 400
5. Logic:
   - Find User by email using prisma.user.findFirst() 
   - IMPORTANT: Do NOT use findUnique — email is only unique per tenant!
   - If user not found → return 401
   - Verify password using verifyPassword utility
   - If invalid → return 401
6. Multi-tenant:
   - tenantId MUST come from User record (server-side)
   - Do NOT accept tenantId from request body
7. Response (200):
   - Return JSON with: id, email, tenantId
   - Do NOT return passwordHash
8. Error handling:
   - Invalid credentials → 401
   - Missing fields → 400
   - Server error → 500
9. Do NOT implement:
   - sessions
   - JWT
   - cookies
   - tokens
   - refresh logic
10. Do NOT touch Prisma schema
11. Do NOT modify existing utilities

TECHNICAL CONSTRAINTS:
- Use Next.js App Router convention
- Use NextResponse from 'next/server'
- Use async/await
- Use try/catch
- Import Prisma from '@/lib/prisma'

EXPECTED OUTPUT:
- Full source code of the API route file
- Correct imports
- Valid TypeScript
- No explanations
- No markdown
- Code ONLY

OUTPUT FORMAT:
<typescript code only>
