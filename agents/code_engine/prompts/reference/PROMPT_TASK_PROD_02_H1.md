// PROMPT_TASK_PROD_02_H.md
// PURPOSE: Implement Project-by-ID GET endpoint with tenant isolation

ROLE: SENIOR BACKEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack:
- Next.js 14 (App Router)
- TypeScript (strict mode)
- Prisma ORM
- PostgreSQL
- Multi-tenant architecture

PROJECT IMPORT RULES:
- Use path alias "@/lib/*" for all lib imports
- Prisma client: import prisma from '@/lib/prisma'
- Auth guard: import { requireTenant } from '@/lib/auth/requireTenant'

GITKEEPER RULES (MANDATORY):
- This is NOT a solar/energy project
- Domain: task management system
- tenantId MUST exist on User
- tenantId MUST NOT come from client input
- tenantId MUST be resolved via requireTenant
- Do NOT invent new domain models
- Do NOT modify existing models or relations
- Only additive, backward-compatible code

EXISTING UTILITIES (ALREADY IMPLEMENTED):
- requireTenant(request: Request): Promise<{ userId: string, tenantId: string }>
  Import from: '@/lib/auth/requireTenant'
  Throws Response(401) if unauthorized

TARGET FILE:
app/api/projects/[id]/route.ts

REQUIRED IMPORTS:
import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';
import { requireTenant } from '@/lib/auth/requireTenant';

NEXT.JS 14 APP ROUTER PATTERN FOR DYNAMIC ROUTES:
```typescript
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const projectId = params.id;
  // ...
}
```

TASK:
Implement Project-by-ID API endpoint with tenant isolation.

FUNCTIONAL REQUIREMENTS:
1. HTTP method: GET only
2. Route param:
   - id: string (project id from URL)
3. Logic:
   a. Call requireTenant(request) to get tenantId
   b. Fetch Project by id using prisma.project.findUnique()
   c. If project not found → return 404 with JSON error
   d. If project.tenantId !== tenantId → return 403 (Forbidden)
   e. On success → return project JSON
4. Security:
   - Do NOT accept tenantId from client
   - Verify project belongs to tenant AFTER fetching
   - Enforce strict tenant isolation

ERROR RESPONSES:
- 401 Unauthorized: thrown by requireTenant (caught in try/catch)
- 404 Not Found: NextResponse.json({ error: 'Project not found' }, { status: 404 })
- 403 Forbidden: NextResponse.json({ error: 'Forbidden' }, { status: 403 })
- 500 Server Error: NextResponse.error() or NextResponse.json({ error: '...' }, { status: 500 })

SUCCESS RESPONSE:
- 200 OK: NextResponse.json(project, { status: 200 })

TECHNICAL CONSTRAINTS:
- Use Next.js App Router conventions
- Use NextRequest / NextResponse from 'next/server'
- Use { params } destructuring for route params
- Use async/await
- Use try/catch
- Use Prisma findUnique (id IS globally unique)

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript

OUTPUT FORMAT:
<complete app/api/projects/[id]/route.ts source code only>
