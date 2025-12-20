#!/bin/bash

# Parliament of Bruce - Quick Activation Helper
# Add this to your ~/.bashrc or ~/.zshrc for easy access

# Function to quickly navigate to and activate POB
pob() {
    if [ "$1" == "activate" ] || [ "$1" == "on" ]; then
        cd /home/parohanoid/Documents/projects/POB
        source venv/bin/activate
        echo "✅ Parliament of Bruce environment activated"
        echo "📍 Location: $(pwd)"
        echo "🐍 Python: $(python --version)"
        echo ""
        echo "Quick commands:"
        echo "  pob status     - Show current status"
        echo "  pob help       - Show all commands"
        echo "  pob init       - Initialize system"
        echo ""
    elif [ "$1" == "status" ]; then
        python -m parliament_of_bruce.cli status
    elif [ "$1" == "help" ]; then
        python -m parliament_of_bruce.cli --help
    elif [ "$1" == "init" ]; then
        python -m parliament_of_bruce.cli init
    elif [ "$1" == "off" ]; then
        deactivate 2>/dev/null && echo "✅ Virtual environment deactivated" || echo "⚠️  No virtual environment active"
    else
        # Forward to CLI if not a special command
        python -m parliament_of_bruce.cli "$@"
    fi
}

# Export the function
export -f pob

echo "✅ Parliament of Bruce shell functions loaded"
echo ""
echo "Usage:"
echo "  pob activate          - Activate the environment"
echo "  pob status            - Show system status"
echo "  pob help              - Show all commands"
echo "  pob <command> [args]  - Run parliament_of_bruce command"
echo "  pob off               - Deactivate environment"
