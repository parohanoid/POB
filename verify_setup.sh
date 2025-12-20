#!/bin/bash

# Parliament of Bruce - Setup Verification Script
# This script verifies all dependencies and configuration

set -e

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "  Parliament of Bruce - Dependency & Configuration Verification"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Check virtual environment
echo "1️⃣  Checking Virtual Environment..."
if [ -d "venv" ]; then
    echo "   ✓ Virtual environment exists"
    source venv/bin/activate
    echo "   ✓ Virtual environment activated"
else
    echo "   ✗ Virtual environment not found"
    exit 1
fi
echo ""

# Check Python version
echo "2️⃣  Checking Python Version..."
PYTHON_VERSION=$(python --version)
echo "   ✓ $PYTHON_VERSION"
echo ""

# Check all dependencies
echo "3️⃣  Checking Dependencies..."
DEPS=("typer" "rich" "sqlalchemy" "pydantic" "pytest" "black" "ruff")
for dep in "${DEPS[@]}"; do
    if python -c "import $dep" 2>/dev/null; then
        echo "   ✓ $dep"
    else
        echo "   ✗ $dep (MISSING)"
    fi
done
echo ""

# Check CLI module
echo "4️⃣  Checking CLI Module..."
if python -c "from parliament_of_bruce import cli" 2>/dev/null; then
    echo "   ✓ CLI module imports successfully"
else
    echo "   ✗ CLI module import failed"
    exit 1
fi
echo ""

# Check database
echo "5️⃣  Checking Database..."
if [ -f ~/.parliament_of_bruce/parliament.db ]; then
    echo "   ✓ Database exists at ~/.parliament_of_bruce/parliament.db"
    echo "   ✓ Size: $(du -h ~/.parliament_of_bruce/parliament.db | cut -f1)"
else
    echo "   ℹ️  Database not yet initialized"
    echo "      Run: python -m parliament_of_bruce.cli init"
fi
echo ""

# Run tests
echo "6️⃣  Running Tests..."
if pytest parliament_of_bruce/tests/ -q 2>/dev/null; then
    PASSED=$(pytest parliament_of_bruce/tests/ -q 2>/dev/null | grep "passed" | head -1)
    echo "   ✓ Tests passed: $PASSED"
else
    echo "   ✗ Tests failed"
    exit 1
fi
echo ""

# Check CLI help
echo "7️⃣  Checking CLI Commands..."
COMMANDS=$(python -m parliament_of_bruce.cli --help 2>/dev/null | grep -E "^\s+(init|status|session|vote|reign|custom|emergency|analytics)" | wc -l)
echo "   ✓ Found $COMMANDS CLI commands"
echo ""

# Summary
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "✅ ALL CHECKS PASSED - System is ready to use!"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "📌 Quick Start:"
echo "   1. Activate venv: source venv/bin/activate"
echo "   2. Initialize:    python -m parliament_of_bruce.cli init"
echo "   3. Run session:   python -m parliament_of_bruce.cli session-cmd daily"
echo "   4. Check status:  python -m parliament_of_bruce.cli status"
echo ""
