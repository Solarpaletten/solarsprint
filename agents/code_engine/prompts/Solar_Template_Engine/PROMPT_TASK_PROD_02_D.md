// PROMPT_TASK_PROD_02_D.md
// FIXED: Added EXISTING UTILITIES section with hashPassword import path

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
- Use path alias "@/lib/*" for all lib imports
- Prisma client: '@/lib/prisma'
- Password utils: '@/lib/auth/password'

GITKEEPER RULES (MANDATORY):
- This is NOT a solar/energy project
- Domain: task management system
- tenantId MUST exist on User
- tenantId MUST NOT come from client input
- Do NOT invent new domain models
- Do NOT remove existing fields or relations
- Only additive, backward-compatible changes allowed

EXISTING UTILITIES (ALREADY IMPLEMENTED — USE THESE):
- hashPassword(password: string): Promise<string>
  Import from: '@/lib/auth/password'
- verifyPassword(password: string, hash: string): Promise<boolean>
  Import from: '@/lib/auth/password'

FORBIDDEN:
- Do NOT import bcrypt or bcryptjs directly
- Do NOT call bcrypt.hash() directly
- MUST use hashPassword() utility

TARGET FILE:
app/api/auth/signup/route.ts

TASK:
Create a signup API endpoint.

FUNCTIONAL REQUIREMENTS:
1. HTTP method: POST
2. Path: /api/auth/signup
3. Input JSON body:
   - email: string
   - password: string
   - tenantName: string
4. Validation:
   - All fields required
   - Return 400 on missing data
5. Logic (in order):
   a. Create new Tenant
   b. Hash password using hashPassword() utility (NOT bcrypt directly!)
   c. Create first User linked to Tenant
6. tenantId MUST be generated server-side from new Tenant
7. Do NOT implement sessions, cookies, JWT, or auth middleware
8. Do NOT return passwordHash in response
9. Use Prisma client
10. Follow Next.js App Router conventions

SECURITY REQUIREMENTS:
- tenantId MUST NOT come from request body
- password MUST be hashed using hashPassword() utility
- Return minimal safe response only

RESPONSE FORMAT (200):
{
  userId: string,
  email: string,
  tenantId: string
}

REQUIRED IMPORTS:
import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';
import { hashPassword } from '@/lib/auth/password';

EXPECTED OUTPUT:
- FULL content of app/api/auth/signup/route.ts
- Valid TypeScript
- Valid Next.js App Router handler
- Code ONLY
- No markdown
- No explanations
- No comments outside code

IMPORTANT:
- Use hashPassword() utility — do NOT use bcrypt directly
- If something is missing, output:
  // CLARIFICATION_NEEDED: <question>

OUTPUT FORMAT:
<raw TypeScript source code only>
