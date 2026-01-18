// PROMPT_TASK_PROD_02_A.md
// PURPOSE: Add passwordHash field to User model

ROLE: SENIOR BACKEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack:
- Next.js 14 (App Router)
- Prisma ORM
- PostgreSQL
- Multi-tenant architecture

FULL PRISMA SCHEMA (SOURCE OF TRUTH):

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Tenant {
  id        String   @id @default(cuid())
  name      String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  projects Project[]
  users    User[]

  @@map("tenants")
}

model Project {
  id          String   @id @default(cuid())
  name        String
  description String?
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  tenantId String
  tenant   Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)

  @@index([tenantId])
  @@map("projects")
}

model User {
  id        String   @id @default(cuid())
  email     String
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  tenantId String
  tenant   Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)

  @@unique([tenantId, email])
  @@index([tenantId])
  @@map("users")
}
```

GITKEEPER RULES (MANDATORY):
- Modify ONLY the User model
- Do NOT change field types
- Do NOT remove fields
- Do NOT change relations
- Do NOT change unique constraints
- Do NOT change @@map or @@index
- Only ADD new fields

TASK:
Add password-based authentication support to User model.

REQUIREMENTS:
1. Add ONE field to User model:
   - passwordHash: String
2. Place the new field after email
3. Do NOT change anything else in the schema
4. Output the COMPLETE updated schema (all models)

EXPECTED OUTPUT:
- FULL Prisma schema with all models
- User model now includes passwordHash field
- Valid Prisma syntax
- No explanations

OUTPUT FORMAT:
<complete prisma schema code only>
