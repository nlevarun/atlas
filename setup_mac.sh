#!/bin/bash
# Atlas Automated Setup for Mac
# Run this once after copying Atlas to your Mac

set -e  # Exit on error

echo "========================================"
echo "Atlas Setup for Mac"
echo "========================================"
echo ""

# Check prerequisites
echo "[1/8] Checking prerequisites..."

if ! command -v python3.12 &> /dev/null; then
    echo "❌ Python 3.12 not found"
    echo "Install: brew install python@3.12"
    exit 1
fi
echo "✅ Python 3.12 found"

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found"
    echo "Install: brew install node@20"
    exit 1
fi
echo "✅ Node.js found"

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found"
    echo "Install: brew install --cask docker"
    echo "Then start Docker Desktop"
    exit 1
fi
echo "✅ Docker found"

# Create virtual environment
echo ""
echo "[2/8] Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  venv already exists, skipping..."
else
    python3.12 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate venv
echo ""
echo "[3/8] Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo ""
echo "[4/8] Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ pip upgraded"

# Install Python dependencies
echo ""
echo "[5/8] Installing Python dependencies..."
cd apps/api
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi
cd ../..

# Install Node dependencies
echo ""
echo "[6/8] Installing Node.js dependencies..."
echo "    (This may take 2-3 minutes...)"
cd apps/web
npm install --silent
if [ $? -eq 0 ]; then
    echo "✅ Node.js dependencies installed"
else
    echo "❌ Failed to install Node.js dependencies"
    exit 1
fi
cd ../..

# Make helper scripts executable
echo ""
echo "[7/8] Setting up helper scripts..."
chmod +x *.sh
echo "✅ Helper scripts ready"

# Create .env from example if it doesn't exist
echo ""
echo "[8/8] Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ .env file created (edit to add API keys)"
else
    echo "⚠️  .env already exists, skipping..."
fi

echo ""
echo "========================================"
echo "Setup Complete! 🎉"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Start Docker Desktop (if not running)"
echo "2. Run: ./start_all.sh"
echo "3. Open: http://localhost:3000"
echo "4. Search: Anthropic"
echo ""
echo "Optional: Edit .env to add API keys"
echo "  - TAVILY_API_KEY for real news"
echo "  - OPENAI_API_KEY for real synthesis"
echo "  - GITHUB_TOKEN for better rate limits"
echo ""
echo "Documentation:"
echo "  - MAC_SETUP.md - Setup details"
echo "  - OPERATIONS_MANUAL.md - How to use"
echo "  - USER_GUIDE.md - Research tips"
echo ""
echo "Happy researching! 📊"
echo ""
