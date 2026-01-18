// PROMPT_TASK_PROD_02_H.md
// PURPOSE: Add PATCH endpoint to existing Project-by-ID route

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
- Only additive, backward-compatible code allowed
- PRESERVE all existing handlers

EXISTING UTILITIES:
- requireTenant(request: Request): Promise<{ userId: string, tenantId: string }>
  Import from: '@/lib/auth/requireTenant'

TARGET FILE:
app/api/projects/[id]/route.ts

EXISTING CODE (MUST PRESERVE — DO NOT MODIFY):
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

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { tenantId } = await requireTenant(request);
    const projectId = params.id;

    const project = await prisma.project.findUnique({
      where: { id: projectId },
    });

    if (!project) {
      return NextResponse.json({ message: 'Project not found' }, { status: 404 });
    }

    if (project.tenantId !== tenantId) {
      return NextResponse.json({ message: 'Forbidden' }, { status: 403 });
    }

    await prisma.project.delete({
      where: { id: projectId },
    });

    return new NextResponse(null, { status: 204 });
  } catch (error) {
    console.error('Error deleting project:', error);
    return NextResponse.json({ message: 'Internal Server Error' }, { status: 500 });
  }
}
```

TASK:
Add PATCH handler to the SAME file. Keep GET and DELETE handlers unchanged.

FUNCTIONAL REQUIREMENTS:
1. HTTP method: PATCH
2. Path: /api/projects/[id]
3. Route params pattern (same as GET/DELETE):
   ```typescript
   export async function PATCH(
     request: NextRequest,
     { params }: { params: { id: string } }
   ) {
   ```
4. Input JSON body (all optional):
   - name?: string
   - description?: string
5. Validation:
   - If body has NEITHER name NOR description → return 400
6. Logic:
   a. Call requireTenant(request) to get tenantId
   b. Parse JSON body
   c. Validate at least one field provided
   d. Find Project by id using prisma.project.findUnique()
   e. If not found → return 404
   f. If project.tenantId !== tenantId → return 403
   g. Update project with ONLY provided fields
   h. Return updated project
7. Security:
   - Do NOT accept tenantId from request body
   - Do NOT update tenantId even if provided
   - Enforce strict tenant isolation

PRISMA UPDATE PATTERN:
```typescript
const updatedProject = await prisma.project.update({
  where: { id: projectId },
  data: {
    ...(body.name && { name: body.name }),
    ...(body.description !== undefined && { description: body.description }),
  },
});
```

ERROR RESPONSES:
- 400: NextResponse.json({ error: 'No fields provided' }, { status: 400 })
- 404: NextResponse.json({ error: 'Project not found' }, { status: 404 })
- 403: NextResponse.json({ error: 'Forbidden' }, { status: 403 })
- 500: NextResponse.json({ error: 'Internal Server Error' }, { status: 500 })

SUCCESS RESPONSE:
- 200: NextResponse.json(updatedProject)

TECHNICAL CONSTRAINTS:
- Use NextRequest / NextResponse
- Use { params } destructuring
- Use async/await
- Use try/catch
- Use Prisma client

CRITICAL:
- Output the COMPLETE file with GET, DELETE, and PATCH handlers
- Do NOT remove or modify the existing GET and DELETE handlers
- Keep the same imports

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO triple backticks
- Valid TypeScript

OUTPUT FORMAT:
<complete route.ts with GET + DELETE + PATCH handlers>
