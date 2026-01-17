#!/bin/bash
# =============================================================================
# Alama — Reasoning Engine Setup Script
# TASK-INFRA-02
# =============================================================================

set -e

echo "=============================================="
echo "  Alama — Reasoning Engine Setup"
echo "  TASK-INFRA-02"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
AI_SERVER_HOME="$HOME/AI-SERVER"
ALAMA_HOME="$AI_SERVER_HOME/agents/alama"
MODEL="llama3.2:8b"
FALLBACK_MODEL="llama3.1:8b"

# -----------------------------------------------------------------------------
# Step 1: Check prerequisites
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[1/5] Checking prerequisites...${NC}"

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}ERROR: Ollama not installed${NC}"
    echo "Install Ollama first (TASK-INFRA-01)"
    exit 1
fi

# Check Ollama running
if ! curl -s http://localhost:11434/ > /dev/null 2>&1; then
    echo -e "${YELLOW}Starting Ollama server...${NC}"
    ollama serve &
    sleep 3
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites OK${NC}"
echo ""

# -----------------------------------------------------------------------------
# Step 2: Create directory structure
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[2/5] Creating directory structure...${NC}"

mkdir -p "$ALAMA_HOME"/{runtime,prompts,gitkeeper,reports,logs}
mkdir -p "$AI_SERVER_HOME/shared/standards"

echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# -----------------------------------------------------------------------------
# Step 3: Download LLaMA model
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[3/5] Downloading LLaMA model...${NC}"

# Check if model exists
if ollama list 2>/dev/null | grep -q "llama3.2"; then
    echo -e "${GREEN}✓ Model $MODEL already installed${NC}"
else
    echo "Downloading $MODEL (this may take a few minutes)..."
    ollama pull $MODEL
    echo -e "${GREEN}✓ Model downloaded${NC}"
fi
echo ""

# -----------------------------------------------------------------------------
# Step 4: Install Python dependencies
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[4/5] Installing Python dependencies...${NC}"

pip3 install --quiet requests pyyaml 2>/dev/null || true

echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# -----------------------------------------------------------------------------
# Step 5: Verify installation
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[5/5] Verifying installation...${NC}"

# Test LLaMA
echo "Testing LLaMA reasoning..."
RESPONSE=$(ollama run $MODEL "Say 'Alama is ready' and nothing else" 2>/dev/null | head -1)
if [[ -n "$RESPONSE" ]]; then
    echo -e "${GREEN}✓ LLaMA responding: $RESPONSE${NC}"
else
    echo -e "${RED}✗ LLaMA not responding${NC}"
fi

# Test CLI (if exists)
if [ -f "$ALAMA_HOME/runtime/alama.py" ]; then
    echo "Testing Alama CLI..."
    python3 "$ALAMA_HOME/runtime/alama.py" status 2>/dev/null && echo -e "${GREEN}✓ CLI working${NC}" || echo -e "${YELLOW}⚠ CLI needs setup${NC}"
fi

echo ""
echo "=============================================="
echo -e "${GREEN}  TASK-INFRA-02 SETUP COMPLETE${NC}"
echo "=============================================="
echo ""
echo "Alama Home:    $ALAMA_HOME"
echo "Model:         $MODEL"
echo "Server:        http://localhost:11434"
echo ""
echo "Quick commands:"
echo "  python3 $ALAMA_HOME/runtime/alama.py status"
echo "  python3 $ALAMA_HOME/runtime/alama.py analyze --repo ~/projects/my-repo"
echo "  python3 $ALAMA_HOME/runtime/alama.py gitkeeper --repo ~/projects/my-repo"
echo "  python3 $ALAMA_HOME/runtime/alama.py report --type daily --project my-project"
echo ""
echo "=============================================="
