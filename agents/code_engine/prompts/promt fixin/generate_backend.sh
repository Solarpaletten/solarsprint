#!/bin/bash
# generate_backend.sh — Generate entire Solar Sprint Backend
# Usage: ./generate_backend.sh

set -e

MODEL="qwen2.5-coder:14b"
PROMPTS_DIR="agents/code_engine/prompts/Solar_Template_Engine"
PROJECT_DIR="projects/solarsprint"

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🚀 Solar Template Engine — Backend Generator"
echo "=============================================="

# Function to generate file from prompt
generate() {
  local PROMPT="$1"
  local OUTPUT="$2"
  
  echo -e "${YELLOW}🔄 Generating:${NC} $OUTPUT"
  
  # Create directory if needed
  mkdir -p "$(dirname "$PROJECT_DIR/$OUTPUT")"
  
  # Generate and clean
  ollama run "$MODEL" < "$PROMPTS_DIR/$PROMPT" | \
    sed '/^```typescript$/d' | \
    sed '/^```prisma$/d' | \
    sed '/^```$/d' > "$PROJECT_DIR/$OUTPUT"
  
  echo -e "${GREEN}✅ Done:${NC} $OUTPUT"
}

# Backend files (A → I)
generate "PROMPT_TASK_PROD_02_A.md" "prisma/schema.prisma"
generate "PROMPT_TASK_PROD_02_B.md" "lib/auth/password.ts"
generate "PROMPT_TASK_PROD_02_C.md" "app/api/auth/login/route.ts"
generate "PROMPT_TASK_PROD_02_D.md" "app/api/auth/signup/route.ts"
generate "PROMPT_TASK_PROD_02_E.md" "lib/auth/getCurrentUser.ts"
generate "PROMPT_TASK_PROD_02_F.md" "lib/auth/requireTenant.ts"
generate "PROMPT_TASK_PROD_02_G.md" "app/api/projects/route.ts"
generate "PROMPT_TASK_PROD_02_H.md" "app/api/projects/[id]/route.ts"
generate "PROMPT_TASK_PROD_02_I.md" "app/api/health/route.ts"

echo ""
echo "=============================================="
echo "🎉 Backend generation complete!"
echo ""
echo "Files generated:"
echo "  - prisma/schema.prisma"
echo "  - lib/auth/password.ts"
echo "  - lib/auth/getCurrentUser.ts"
echo "  - lib/auth/requireTenant.ts"
echo "  - app/api/auth/login/route.ts"
echo "  - app/api/auth/signup/route.ts"
echo "  - app/api/projects/route.ts"
echo "  - app/api/projects/[id]/route.ts"
echo "  - app/api/health/route.ts"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_DIR"
echo "  npx prisma generate"
echo "  pnpm build"
