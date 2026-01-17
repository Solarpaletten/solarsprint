// PROMPT_TASK_PROD_02_B.md

ROLE: SENIOR BACKEND ENGINEER

PROJECT CONTEXT:
Project: Solar Sprint
Stack:
- Next.js 14
- TypeScript
- Node.js
- bcrypt

TASK:
Create password utility functions.

REQUIREMENTS:
1. Create file: src/lib/auth/password.ts
2. Export functions:
   - hashPassword(password: string): Promise<string>
   - verifyPassword(password: string, hash: string): Promise<boolean>
3. Use bcrypt
4. Salt rounds: 12
5. No Prisma usage
6. No environment variables
7. No comments, no explanations

OUTPUT FORMAT:
<typescript code only>
