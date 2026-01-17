// PROMPT_TASK_PROD_02_A.md

ROLE: SENIOR BACKEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack:
- Next.js 14 (App Router)
- Prisma ORM
- PostgreSQL
- Multi-tenant architecture

CURRENT PRISMA USER MODEL (SOURCE OF TRUTH):
model User {
  id        String   @id @default(cuid())
  email     String
  name      String?
  tenantId  String
  tenant    Tenant   @relation(fields: [tenantId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@unique([tenantId, email])
}

GITKEEPER RULES (MANDATORY):
- Modify ONLY the User model shown above
- Do NOT change field types
- Do NOT remove fields
- Do NOT change relations
- Do NOT change unique constraints
- Only ADD fields

TASK:
Add password-based authentication support.

REQUIREMENTS:
1. Add field:
   - passwordHash: String
2. Do NOT change anything else

EXPECTED OUTPUT:
- FULL updated User model
- Valid Prisma schema
- EXACT same fields + passwordHash

OUTPUT FORMAT:
<prisma schema code only>
