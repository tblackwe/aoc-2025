#!/bin/bash
# Script to set up a new day for Advent of Code 2025

set -e

# Helper function for cross-platform sed replacement
sed_inplace() {
    local pattern=$1
    local file=$2
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "$pattern" "$file"
    else
        sed -i "$pattern" "$file"
    fi
}

# Check if day number is provided
if [ -z "$1" ]; then
    echo "Usage: ./new-day.sh <day-number>"
    echo "Example: ./new-day.sh 1"
    exit 1
fi

DAY=$1
# Format day with leading zero
DAY_FORMATTED=$(printf "%02d" $DAY)

echo "Setting up Day $DAY_FORMATTED..."

# Create spec from template
SPEC_FILE="specs/day-${DAY_FORMATTED}.md"
if [ -f "$SPEC_FILE" ]; then
    echo "❌ Spec already exists: $SPEC_FILE"
else
    cp templates/spec-template.md "$SPEC_FILE"
    # Replace XX with the day number
    sed_inplace "s/XX/$DAY_FORMATTED/g" "$SPEC_FILE"
    echo "✅ Created spec: $SPEC_FILE"
fi

# Create solution directory
SOLUTION_DIR="solutions/day-${DAY_FORMATTED}"
if [ -d "$SOLUTION_DIR" ]; then
    echo "❌ Solution directory already exists: $SOLUTION_DIR"
else
    mkdir -p "$SOLUTION_DIR"
    
    # Copy templates
    cp templates/solution-template.py "$SOLUTION_DIR/solution.py"
    cp templates/test-template.py "$SOLUTION_DIR/test_solution.py"
    
    # Replace XX with the day number
    sed_inplace "s/XX/$DAY_FORMATTED/g" "$SOLUTION_DIR/solution.py"
    sed_inplace "s/XX/$DAY_FORMATTED/g" "$SOLUTION_DIR/test_solution.py"
    
    # Create README
    cat > "$SOLUTION_DIR/README.md" << EOF
# Day ${DAY_FORMATTED} Solution

This solution is generated based on the specification in \`specs/day-${DAY_FORMATTED}.md\`.

## Running the Solution

\`\`\`bash
python3 solution.py
\`\`\`

## Running Tests

\`\`\`bash
python3 -m unittest test_solution.py
\`\`\`

## Input

Place your puzzle input in \`input.txt\` (not committed to git).

## Notes

[Add any notes about the implementation, challenges, or insights]
EOF
    
    echo "✅ Created solution directory: $SOLUTION_DIR"
fi

echo ""
echo "🎄 Day $DAY_FORMATTED is ready!"
echo ""
echo "Next steps:"
echo "1. Edit $SPEC_FILE with the puzzle details"
echo "2. Assign to an AI agent: opencode assign $SPEC_FILE"
echo "3. Or implement manually in $SOLUTION_DIR"
