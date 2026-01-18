// PROMPT_TASK_PROD_02_F.md
// PURPOSE: Implement requireTenant guard helper
// VERSION: 1.1 — Fixed: include TenantContext type definition

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
- Use relative imports for same-directory modules
- getCurrentUser: import { getCurrentUser } from './getCurrentUser'

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- tenantId MUST be resolved server-side
- tenantId MUST NOT come from client input
- Do NOT invent new domain models

EXISTING UTILITIES (ALREADY IMPLEMENTED):
- getCurrentUser(request: Request): Promise<AuthUser>
  Import from: './getCurrentUser' (relative, same directory)
  Returns: { id, email, tenantId } | null

TARGET FILE:
lib/auth/requireTenant.ts

REQUIRED IMPORTS:
import { getCurrentUser } from './getCurrentUser';

TASK:
Implement requireTenant guard that ensures user is authenticated and has tenantId.

REQUIRED TYPE DEFINITION (MUST BE INCLUDED IN OUTPUT):
```typescript
type TenantContext = {
  userId: string;
  tenantId: string;
};
```
IMPORTANT: This type MUST be defined in the file, not imported!

FUNCTIONAL REQUIREMENTS:
1. Function signature:
   ```typescript
   export async function requireTenant(request: Request): Promise<TenantContext>
   ```
2. Logic:
   a. Call getCurrentUser(request)
   b. If no user OR no tenantId → throw Response(401)
   c. Return { userId, tenantId }
3. Error handling:
   - Unauthorized: throw new Response('Unauthorized', { status: 401 })

COMPLETE CODE STRUCTURE (FOLLOW THIS EXACTLY):
```typescript
import { getCurrentUser } from './getCurrentUser';

type TenantContext = {
  userId: string;
  tenantId: string;
};

export async function requireTenant(request: Request): Promise<TenantContext> {
  // ... implementation
}
```

TECHNICAL CONSTRAINTS:
- Use Web Fetch API Request type (NOT NextRequest)
- Use async/await
- Throw Response object for auth failures (NOT return)
- Define TenantContext type INSIDE the file

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript
- MUST include type TenantContext definition

OUTPUT FORMAT:
<complete lib/auth/requireTenant.ts source code only>
