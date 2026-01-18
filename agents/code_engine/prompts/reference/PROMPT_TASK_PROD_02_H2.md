// PROMPT_TASK_PROD_02_I.md
// PURPOSE: Add DELETE endpoint to existing Project-by-ID route

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
- Domain: task management system
- tenantId MUST be resolved server-side
- tenantId MUST NOT come from client input
- Do NOT invent new domain models
- Do NOT modify Prisma schema
- Use existing helpers ONLY
- PRESERVE all existing handlers

EXISTING UTILITIES:
- requireTenant(request: Request): Promise<{ userId: string, tenantId: string }>
  Import from: '@/lib/auth/requireTenant'

TARGET FILE:
app/api/projects/[id]/route.ts

EXISTING CODE (MUST PRESERVE):
```typescript
import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';
import { requireTenant } from '@/lib/auth/requireTenant';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { tenantId } = await requireTenant(request);

    const project = await prisma.project.findUnique({
      where: { id: params.id },
    });

    if (!project) {
      return NextResponse.json({ error: 'Project not found' }, { status: 404 });
    }

    if (project.tenantId !== tenantId) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    return NextResponse.json(project, { status: 200 });
  } catch (error) {
    return NextResponse.error();
  }
}
```

TASK:
Add DELETE handler to the SAME file. Keep GET handler unchanged.

FUNCTIONAL REQUIREMENTS:
1. HTTP method: DELETE
2. Path: /api/projects/[id]
3. Route params pattern (same as GET):
   ```typescript
   export async function DELETE(
     request: NextRequest,
     { params }: { params: { id: string } }
   ) {
   ```
4. Logic:
   a. Call requireTenant(request) to get tenantId
   b. Find Project by id using prisma.project.findUnique()
   c. If not found → return 404
   d. If project.tenantId !== tenantId → return 403
   e. Delete project using prisma.project.delete()
   f. Return 204 No Content
5. Security:
   - Do NOT accept tenantId from request
   - Enforce tenant isolation

ERROR RESPONSES:
- 404: NextResponse.json({ message: 'Project not found' }, { status: 404 })
- 403: NextResponse.json({ message: 'Forbidden' }, { status: 403 })
- 500: NextResponse.json({ message: 'Internal Server Error' }, { status: 500 })

SUCCESS RESPONSE:
- 204: new NextResponse(null, { status: 204 })

TECHNICAL CONSTRAINTS:
- Use NextRequest / NextResponse
- Use { params } destructuring
- Use async/await
- Use try/catch
- Use Prisma client

CRITICAL:
- Output the COMPLETE file with BOTH GET and DELETE handlers
- Do NOT remove or modify the existing GET handler
- Keep the same imports

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO triple backticks
- Valid TypeScript

OUTPUT FORMAT:
<complete route.ts with GET + DELETE handlers>
