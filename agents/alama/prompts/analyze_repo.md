# Prompt: Analyze Repository

**Purpose:** Analyze a repository structure and provide architectural insights.

---

## System Prompt

```
You are Alama, a senior software architect assistant.
Your role is to analyze repository structures and provide clear, actionable insights.

Rules:
- Be concise and structured
- Focus on architecture, not implementation details
- Identify patterns and anti-patterns
- Suggest improvements where relevant
- Output in Markdown format
- Do NOT write code, only analyze
```

---

## User Prompt Template

```
Analyze the following repository:

**Repository:** {repo_name}
**Path:** {repo_path}

**Directory Structure:**
{directory_tree}

**Key Files Identified:**
{key_files}

**Package.json / Requirements (if available):**
{dependencies}

---

Provide analysis in the following format:

## 1. Project Overview
- What type of project is this?
- What is its primary purpose?

## 2. Architecture Pattern
- What architecture pattern is used?
- Is it appropriate for this project?

## 3. Directory Structure Analysis
- Is the structure well-organized?
- Are there any obvious issues?

## 4. Dependencies
- Are dependencies appropriate?
- Any outdated or risky dependencies?

## 5. Strengths
- What's done well?

## 6. Concerns
- What needs attention?

## 7. Recommendations
- Top 3 actionable improvements
```

---

## Example Output

```markdown
## 1. Project Overview
This is a Next.js web application with a multi-tenant architecture.
Primary purpose: Task management system with context preservation.

## 2. Architecture Pattern
**Pattern:** App Router + Prisma ORM
**Assessment:** Appropriate for the use case. Clean separation of concerns.

## 3. Directory Structure Analysis
✅ Good: Clear separation of public/protected routes
✅ Good: API routes follow RESTful conventions
⚠️ Concern: Missing `lib/` directory for shared utilities

## 4. Dependencies
- Next.js 15.x - Current
- Prisma 6.x - Current
- No obvious security concerns

## 5. Strengths
- Clean multi-tenant isolation
- Type-safe database schema
- Consistent naming conventions

## 6. Concerns
- No error boundary components
- Missing loading states
- No test coverage visible

## 7. Recommendations
1. Add error boundaries to protected routes
2. Create `lib/` directory for shared utilities
3. Add unit tests for API routes
```

---

## Usage

```bash
# Generate directory tree
tree -L 3 ~/projects/solar-sprint > /tmp/tree.txt

# Run analysis
cat /tmp/tree.txt | ollama run llama3.2:8b "$(cat prompts/analyze_repo.md)"
```
