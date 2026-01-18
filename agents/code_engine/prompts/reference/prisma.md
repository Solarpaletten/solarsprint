# Prisma Code Generation Rules

## Client Singleton

Always use the singleton pattern:

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient()

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}
```

## Query Patterns

### Find One
```typescript
// ✅ Good
const user = await prisma.user.findUnique({
  where: { id: userId }
})

// ✅ Good with relations
const user = await prisma.user.findUnique({
  where: { id: userId },
  include: { tenant: true }
})
```

### Find Many with Filters
```typescript
// ✅ Good
const projects = await prisma.project.findMany({
  where: { tenantId },
  orderBy: { createdAt: 'desc' },
  take: 10
})
```

### Create with Relations
```typescript
// ✅ Good - Transaction for related records
const result = await prisma.$transaction(async (tx) => {
  const tenant = await tx.tenant.create({
    data: { name: tenantName }
  })
  
  const user = await tx.user.create({
    data: {
      email,
      tenantId: tenant.id
    }
  })
  
  return { tenant, user }
})
```

### Update
```typescript
// ✅ Good
const updated = await prisma.user.update({
  where: { id: userId },
  data: { name: newName }
})
```

### Delete
```typescript
// ✅ Good
await prisma.session.delete({
  where: { id: sessionId }
})

// ✅ Good - Delete many
await prisma.session.deleteMany({
  where: { userId }
})
```

## Multi-Tenant Patterns

### CRITICAL: Always filter by tenantId

```typescript
// ✅ Good - tenantId from session, not from request
export async function getProjects(tenantId: string) {
  return prisma.project.findMany({
    where: { tenantId }  // Server-controlled
  })
}

// ❌ NEVER do this - tenantId from client
export async function getProjects(request: Request) {
  const { tenantId } = await request.json()  // SECURITY RISK
  return prisma.project.findMany({
    where: { tenantId }
  })
}
```

### Session-Based Tenant Access
```typescript
// ✅ Good
export async function GET() {
  const session = await getCurrentSession()
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }
  
  const projects = await prisma.project.findMany({
    where: { tenantId: session.user.tenantId }
  })
  
  return NextResponse.json(projects)
}
```

## Type Usage

Use generated Prisma types:

```typescript
import { User, Project, Tenant } from '@prisma/client'

// Type with relations
type UserWithTenant = User & {
  tenant: Tenant
}

// Or use Prisma's generated types
import { Prisma } from '@prisma/client'

type UserWithTenant = Prisma.UserGetPayload<{
  include: { tenant: true }
}>
```

## Error Handling

```typescript
import { Prisma } from '@prisma/client'

try {
  await prisma.user.create({ data: userData })
} catch (error) {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    if (error.code === 'P2002') {
      // Unique constraint violation
      throw new Error('User already exists')
    }
  }
  throw error
}
```

## Solar Sprint Schema Reference

```prisma
model Tenant {
  id        String   @id @default(cuid())
  name      String
  projects  Project[]
  users     User[]
}

model Project {
  id          String   @id @default(cuid())
  name        String
  description String?
  tenantId    String
  tenant      Tenant   @relation(...)
}

model User {
  id        String   @id @default(cuid())
  email     String
  password  String
  name      String?
  tenantId  String
  tenant    Tenant   @relation(...)
  sessions  Session[]
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  expiresAt    DateTime
  userId       String
  user         User     @relation(...)
}
```