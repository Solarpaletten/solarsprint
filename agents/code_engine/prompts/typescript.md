# TypeScript Code Generation Rules

## Type Safety

- NEVER use `any` type
- Prefer `unknown` over `any` when type is truly unknown
- Use strict null checks
- Define explicit return types for all functions

## Patterns

### Function Signatures
```typescript
// ✅ Good
export function processUser(user: User): ProcessedUser {
  // ...
}

// ❌ Bad
export function processUser(user: any) {
  // ...
}
```

### Async/Await
```typescript
// ✅ Good
export async function fetchData(): Promise<Data> {
  try {
    const response = await fetch(url)
    return response.json()
  } catch (error) {
    throw new Error('Failed to fetch data')
  }
}

// ❌ Bad
export function fetchData() {
  return fetch(url).then(r => r.json())
}
```

### Error Handling
```typescript
// ✅ Good
if (!user) {
  throw new Error('User not found')
}

// ❌ Bad
if (!user) {
  return null // Silent failure
}
```

## Next.js App Router Specifics

### API Routes
```typescript
// ✅ Good - app/api/example/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  return NextResponse.json({ data: 'value' })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  return NextResponse.json({ success: true }, { status: 201 })
}
```

### Server Components
```typescript
// ✅ Good - No "use client" needed for server components
export default async function Page() {
  const data = await fetchData()
  return <div>{data.title}</div>
}
```

### Client Components
```typescript
// ✅ Good - Explicit "use client" directive
'use client'

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

## Import Organization

```typescript
// 1. Node.js built-ins
import { readFile } from 'fs/promises'

// 2. External packages
import { NextResponse } from 'next/server'
import { z } from 'zod'

// 3. Internal absolute imports
import { prisma } from '@/lib/prisma'
import { validateUser } from '@/lib/validators'

// 4. Relative imports
import { UserCard } from './UserCard'
import type { User } from './types'
```

## Validation with Zod

```typescript
import { z } from 'zod'

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().positive().optional()
})

type User = z.infer<typeof UserSchema>

export function validateUser(data: unknown): User {
  return UserSchema.parse(data)
}
```