// PROMPT_TASK_PROD_02_K.md
> app/api/health/route.ts

ROLE: SENIOR BACKEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack:
- Next.js 14 (App Router)
- TypeScript
- Prisma ORM
- PostgreSQL
- Multi-tenant architecture

PROJECT IMPORT RULES:
- Use path alias "@/lib/*"
- Do NOT use relative imports for core services
- Prisma client path is "@/lib/prisma"

PRISMA CONNECTION RULES (MANDATORY):
- Prisma client is a singleton
- Do NOT call prisma.$connect()
- Do NOT call prisma.$disconnect()
- Do NOT manage connection lifecycle manually
- Database check MUST use lightweight query:
  - prisma.$queryRaw`SELECT 1`


GITKEEPER RULES (MANDATORY):
- Domain: task management system
- This is NOT a solar/energy project
- Do NOT require authentication
- Do NOT require tenant
- Do NOT invent new domain models
- Do NOT modify Prisma schema

TARGET FILE:
> app/api/health/route.ts

TASK:
Implement production health check endpoint.

FUNCTIONAL REQUIREMENTS:
1. HTTP method: GET
2. Path: /api/health
3. Authentication: NONE
4. Logic:
   - Return service status
   - Return current timestamp
   - Verify database connectivity using Prisma
5. Database check:
   - Perform lightweight query (e.g. prisma.$queryRaw or prisma.$connect)
   - If DB is reachable → db: "ok"
   - If DB error → db: "error"
6. Response (200):
{
  status: "ok",
  service: "solar-sprint",
  timestamp: string,
  db: "ok" | "error"
}

TECHNICAL CONSTRAINTS:
- Use NextRequest / NextResponse from 'next/server'
- Use async/await
- Use Prisma client
- No logging
- No try/catch swallowing — handle DB error explicitly
- Follow App Router conventions

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript

OUTPUT FORMAT:
<complete app/api/health/route.ts source code only>
