#!/bin/bash
# generate_frontend.sh — Generate entire Solar Sprint Frontend
# Usage: ./generate_frontend.sh

set -e

MODEL="qwen2.5-coder:14b"
PROMPTS_DIR="agents/code_engine/prompts/Solar_Template_Engine_FE"
PROJECT_DIR="projects/solarsprint"

# Color output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🚀 Solar Template Engine — Frontend Generator"
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
    sed '/^```typescriptreact$/d' | \
    sed '/^```tsx$/d' | \
    sed '/^```$/d' > "$PROJECT_DIR/$OUTPUT"
  
  echo -e "${GREEN}✅ Done:${NC} $OUTPUT"
}

# Pages (A → H)
generate "PROMPT_FRONTEND_01_A.md" "app/layout.tsx"
generate "PROMPT_FRONTEND_01_B.md" "app/page.tsx"
generate "PROMPT_FRONTEND_01_C.md" "app/(auth)/login/page.tsx"
generate "PROMPT_FRONTEND_01_D.md" "app/(auth)/signup/page.tsx"
generate "PROMPT_FRONTEND_01_E.md" "app/(dashboard)/layout.tsx"
generate "PROMPT_FRONTEND_01_F.md" "app/(dashboard)/page.tsx"
generate "PROMPT_FRONTEND_01_G.md" "app/(dashboard)/projects/page.tsx"
generate "PROMPT_FRONTEND_01_H.md" "app/(dashboard)/projects/[id]/page.tsx"

# Components (I → L)
generate "PROMPT_FRONTEND_01_I.md" "components/ui/Button.tsx"
generate "PROMPT_FRONTEND_01_J.md" "components/ui/Input.tsx"
generate "PROMPT_FRONTEND_01_K.md" "components/ui/Card.tsx"
generate "PROMPT_FRONTEND_01_L.md" "components/forms/AuthForm.tsx"

echo ""
echo "=============================================="
echo "🎉 Frontend generation complete!"
echo ""
echo "Files generated:"
echo "  - app/layout.tsx"
echo "  - app/page.tsx"
echo "  - app/(auth)/login/page.tsx"
echo "  - app/(auth)/signup/page.tsx"
echo "  - app/(dashboard)/layout.tsx"
echo "  - app/(dashboard)/page.tsx"
echo "  - app/(dashboard)/projects/page.tsx"
echo "  - app/(dashboard)/projects/[id]/page.tsx"
echo "  - components/ui/Button.tsx"
echo "  - components/ui/Input.tsx"
echo "  - components/ui/Card.tsx"
echo "  - components/forms/AuthForm.tsx"
echo ""
echo "Next: cd $PROJECT_DIR && pnpm build"
