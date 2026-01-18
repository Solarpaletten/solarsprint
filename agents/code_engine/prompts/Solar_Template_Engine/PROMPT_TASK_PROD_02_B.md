// PROMPT_TASK_PROD_02_B.md
// FIXED: Corrected file path (removed src/ prefix)

ROLE: SENIOR BACKEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack:
- Next.js 14 (App Router)
- TypeScript
- Node.js
- bcryptjs

PROJECT STRUCTURE:
- All lib files are in /lib (NOT /src/lib)
- Use path alias "@/lib/*" for imports

TASK:
Create password utility functions.

TARGET FILE:
lib/auth/password.ts

REQUIREMENTS:
1. Export two async functions:
   - hashPassword(password: string): Promise<string>
   - verifyPassword(password: string, hash: string): Promise<boolean>
2. Use bcryptjs (NOT bcrypt)
3. Salt rounds: 12
4. No Prisma usage
5. No environment variables
6. Include TypeScript return types

IMPORTS:
import bcrypt from 'bcryptjs'

OUTPUT RULES:
- OUTPUT CODE ONLY
- NO markdown
- NO explanations
- Valid TypeScript

OUTPUT FORMAT:
<typescript code only>
