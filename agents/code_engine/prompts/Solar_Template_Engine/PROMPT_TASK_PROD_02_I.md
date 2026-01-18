// PROMPT_TASK_PROD_02_I.md
// PURPOSE: Implement production health check endpoint
// VERSION: 1.1 — Fixed: include HealthResponse type definition

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
- Use path alias "@/lib/*"
- Do NOT use relative imports for core services
- Prisma client: import prisma from '@/lib/prisma'

PRISMA CONNECTION RULES (MANDATORY):
- Prisma client is a singleton — already configured in lib/prisma.ts
- Do NOT call prisma.$connect()
- Do NOT call prisma.$disconnect()
- Do NOT manage connection lifecycle manually
- Database check MUST use lightweight query:
  await prisma.$queryRaw`SELECT 1`

GITKEEPER RULES (MANDATORY):
- Domain: task management system
- This is NOT a solar/energy project
- Do NOT require authentication
- Do NOT require tenant
- Do NOT invent new domain models
- Do NOT modify Prisma schema

TARGET FILE:
app/api/health/route.ts

REQUIRED IMPORTS:
import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';

TASK:
Implement production health check endpoint.

REQUIRED TYPE DEFINITION (MUST BE INCLUDED IN OUTPUT):
```typescript
type HealthResponse = {
  status: 'ok';
  service: string;
  timestamp: string;
  db: 'ok' | 'error';
};
```
IMPORTANT: This type MUST be defined in the file, not imported!

FUNCTIONAL REQUIREMENTS:
1. HTTP method: GET only
2. Path: /api/health
3. Authentication: NONE required
4. Logic:
   a. Get current timestamp (ISO string)
   b. Try database connectivity check using prisma.$queryRaw`SELECT 1`
   c. Set db status based on result
5. Database check pattern:
   ```typescript
   let dbStatus: 'ok' | 'error' = 'error';
   try {
     await prisma.$queryRaw`SELECT 1`;
     dbStatus = 'ok';
   } catch (e) {
     // DB unreachable, keep dbStatus as 'error'
   }
   ```
6. Response (always 200):
   ```json
   {
     "status": "ok",
     "service": "solar-sprint",
     "timestamp": "2026-01-17T21:00:00.000Z",
     "db": "ok"
   }
   ```

COMPLETE CODE STRUCTURE (FOLLOW THIS EXACTLY):
```typescript
import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';

type HealthResponse = {
  status: 'ok';
  service: string;
  timestamp: string;
  db: 'ok' | 'error';
};

export async function GET(request: NextRequest) {
  // ... implementation
}
```

TECHNICAL CONSTRAINTS:
- Use NextRequest / NextResponse from 'next/server'
- Use async/await
- Use Prisma client singleton
- Handle DB error gracefully (try/catch around DB check only)
- Always return 200 — health endpoint should not fail
- Follow App Router conventions
- Define HealthResponse type INSIDE the file

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript
- MUST include type HealthResponse definition

OUTPUT FORMAT:
<complete app/api/health/route.ts source code only>
