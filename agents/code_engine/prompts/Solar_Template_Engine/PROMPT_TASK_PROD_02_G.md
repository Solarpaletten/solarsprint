// PROMPT_TASK_PROD_02_G.md
// PURPOSE: Implement Projects API (GET/POST) with tenant isolation

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
- This is NOT a solar/energy project
- Domain: task management system
- tenantId MUST exist on all business entities
- tenantId MUST NOT come from client input
- tenantId MUST be resolved via requireTenant(request)
- Do NOT invent new domain models
- Do NOT modify Prisma schema
- Only additive, backward-compatible code allowed

EXISTING UTILITIES (ALREADY IMPLEMENTED):
- requireTenant(request: Request): Promise<{ userId: string; tenantId: string }>
  Import from: '@/lib/auth/requireTenant'
  Throws Response(401) if unauthorized

TARGET FILE:
app/api/projects/route.ts

TASK:
Implement Projects API (tenant-aware).

REQUIRED IMPORTS:
import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';
import { requireTenant } from '@/lib/auth/requireTenant';

FUNCTIONAL REQUIREMENTS:

1. HTTP Methods:
   - GET
   - POST

2. Authentication:
   - MUST use requireTenant(request) at the start of each handler
   - If unauthorized → requireTenant throws, handler catches in try/catch

3. GET /api/projects:
   - Call requireTenant(request) to get tenantId
   - Return list of projects WHERE tenantId matches
   - Order by createdAt DESC
   - Response: NextResponse.json(projects, { status: 200 })

4. POST /api/projects:
   - Call requireTenant(request) to get tenantId
   - Parse JSON body
   - Accept fields:
     - name: string (REQUIRED)
     - description?: string (optional)
   - Validate: if !name → return 400
   - Create project with tenantId from requireTenant (NOT from body)
   - Response: NextResponse.json(project, { status: 201 })

5. Error handling:
   - Missing name → NextResponse.json({ error: 'Name is required' }, { status: 400 })
   - Auth failure → caught from requireTenant, return NextResponse.error()
   - Other errors → NextResponse.error() or 500

RESPONSE EXAMPLES:
GET 200: [{ id, name, description, tenantId, createdAt, updatedAt }, ...]
POST 201: { id, name, description, tenantId, createdAt, updatedAt }
POST 400: { error: "Name is required" }

TECHNICAL CONSTRAINTS:
- Use Next.js App Router convention (export async function GET/POST)
- Use NextRequest / NextResponse from 'next/server'
- Use async/await
- Use try/catch around each handler
- Use Prisma client
- No sessions, cookies, JWT, middleware

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- NO comments outside code
- NO triple backticks
- Valid TypeScript

OUTPUT FORMAT:
<complete app/api/projects/route.ts source code only>
