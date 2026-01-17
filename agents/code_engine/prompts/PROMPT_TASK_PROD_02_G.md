// PROMPT_TASK_PROD_02_G.md

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
- tenantId MUST exist on all business entities
- tenantId MUST NOT come from client input
- tenantId MUST be resolved via requireTenant(request)
- Do NOT invent new domain models
- Do NOT modify Prisma schema
- Only additive, backward-compatible code allowed

EXISTING UTILITIES (ALREADY IMPLEMENTED):
- requireTenant(request): Promise<{ userId: string; tenantId: string }>

TARGET FILE:
app/api/projects/route.ts

TASK:
Implement Projects API (tenant-aware).

FUNCTIONAL REQUIREMENTS:

1. HTTP Methods:
   - GET
   - POST

2. Authentication:
   - MUST use requireTenant(request)
   - If unauthorized → let requireTenant throw

3. GET /api/projects:
   - Return list of projects for current tenant only
   - Order by createdAt DESC

4. POST /api/projects:
   - Accept JSON body:
     - name: string
     - description?: string
   - Validate required fields
   - Create project linked to tenantId
   - tenantId MUST come from requireTenant
   - Do NOT accept tenantId from request body

5. Response format:
   - GET: array of projects
   - POST: created project
   - Do NOT include sensitive data

6. Error handling:
   - Missing required fields → 400
   - Other errors → 500

TECHNICAL CONSTRAINTS:
- Use Next.js App Router convention
- Use NextRequest / NextResponse from 'next/server'
- Use async / await
- Use Prisma client
- No sessions
- No cookies
- No JWT
- No middleware

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript

IMPORTANT:
- Follow existing project conventions
- If something is missing, output:
  // CLARIFICATION_NEEDED: <question>

OUTPUT FORMAT:
<complete app/api/projects/route.ts source code only>
