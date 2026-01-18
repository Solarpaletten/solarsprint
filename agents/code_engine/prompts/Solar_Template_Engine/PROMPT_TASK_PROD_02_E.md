// PROMPT_TASK_PROD_02_E.md
// PURPOSE: Implement getCurrentUser resolver
// VERSION: 1.1 — Fixed: include AuthUser type definition

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

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- Do NOT return passwordHash in any response
- Do NOT invent new domain models
- Do NOT modify Prisma schema

TARGET FILE:
lib/auth/getCurrentUser.ts

REQUIRED IMPORTS:
import prisma from '@/lib/prisma';

TASK:
Implement getCurrentUser resolver that reads x-user-id header and returns user data.

REQUIRED TYPE DEFINITION (MUST BE INCLUDED IN OUTPUT):
```typescript
type AuthUser = {
  id: string;
  email: string;
  tenantId: string;
} | null;
```
IMPORTANT: This type MUST be defined in the file, not imported!

FUNCTIONAL REQUIREMENTS:
1. Function signature:
   ```typescript
   export async function getCurrentUser(request: Request): Promise<AuthUser>
   ```
2. Logic:
   a. Read header: request.headers.get('x-user-id')
   b. If no header → return null
   c. Find user by id using prisma.user.findUnique()
   d. Use select to return ONLY: id, email, tenantId
   e. If user not found → return null
   f. Return user object
3. Security:
   - Do NOT return passwordHash
   - Use Prisma select to limit fields

COMPLETE CODE STRUCTURE (FOLLOW THIS EXACTLY):
```typescript
import prisma from '@/lib/prisma';

type AuthUser = {
  id: string;
  email: string;
  tenantId: string;
} | null;

export async function getCurrentUser(request: Request): Promise<AuthUser> {
  // ... implementation
}
```

TECHNICAL CONSTRAINTS:
- Use Web Fetch API Request type (NOT NextRequest)
- Use async/await
- Use try/catch — return null on any failure
- Use Prisma select for minimal data exposure
- No console.log or logging
- Define AuthUser type INSIDE the file

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript
- MUST include type AuthUser definition

OUTPUT FORMAT:
<complete lib/auth/getCurrentUser.ts source code only>
