#!/bin/bash
# generate_all.sh — Generate entire Solar Sprint project (Backend + Frontend)
# Usage: ./generate_all.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║   🚀 SOLAR TEMPLATE ENGINE v1.0                               ║"
echo "║                                                               ║"
echo "║   One-click project generation                                ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check ollama is running
if ! command -v ollama &> /dev/null; then
  echo "❌ Error: ollama not found. Please install ollama first."
  exit 1
fi

# Check model is available
if ! ollama list | grep -q "qwen2.5-coder:14b"; then
  echo "⚠️  Model qwen2.5-coder:14b not found. Pulling..."
  ollama pull qwen2.5-coder:14b
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "PHASE 1: BACKEND"
echo "═══════════════════════════════════════════════════════════════"
echo ""

bash "$SCRIPT_DIR/generate_backend.sh"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "PHASE 2: FRONTEND"
echo "═══════════════════════════════════════════════════════════════"
echo ""

bash "$SCRIPT_DIR/generate_frontend.sh"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "PHASE 3: BUILD"
echo "═══════════════════════════════════════════════════════════════"
echo ""

cd projects/solarsprint

echo "📦 Installing dependencies..."
pnpm install

echo "🗄️  Generating Prisma client..."
npx prisma generate

echo "🔨 Building project..."
pnpm build

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║   ✅ SOLAR SPRINT GENERATED SUCCESSFULLY!                     ║"
echo "║                                                               ║"
echo "║   Backend:  9 files                                           ║"
echo "║   Frontend: 12 files                                          ║"
echo "║   Total:    21 files                                          ║"
echo "║                                                               ║"
echo "║   Run: cd projects/solarsprint && pnpm dev                    ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
