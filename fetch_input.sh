#!/bin/bash
# Download Advent of Code 2025 input
# Usage: ./fetch_input.sh <day>
# Example: ./fetch_input.sh 8

if [ -z "$1" ]; then
    echo "Usage: ./fetch_input.sh <day>"
    echo "Example: ./fetch_input.sh 8"
    exit 1
fi

DAY=$1

# Validate day is a number between 1-25
if ! [[ "$DAY" =~ ^[0-9]+$ ]] || [ "$DAY" -lt 1 ] || [ "$DAY" -gt 25 ]; then
    echo "❌ Day must be a number between 1 and 25"
    exit 1
fi

# Format day with leading zero
DAY_FORMATTED=$(printf "%02d" $DAY)

# Check for session cookie
if [ ! -f ~/.adventofcode.session ]; then
    echo "❌ Session cookie file not found: ~/.adventofcode.session"
    echo "   Create this file with your AoC session cookie."
    exit 1
fi

SESSION=$(cat ~/.adventofcode.session)

# Create output directory if it doesn't exist
OUTPUT_DIR="solutions/day-${DAY_FORMATTED}"
mkdir -p "$OUTPUT_DIR"

# Download input
curl -s \
  -H "Cookie: session=${SESSION}" \
  -H "User-Agent: Mozilla/5.0" \
  "https://adventofcode.com/2025/day/${DAY}/input" \
  -o "${OUTPUT_DIR}/input.txt"

if [ -f "${OUTPUT_DIR}/input.txt" ]; then
    echo "✅ Downloaded ${OUTPUT_DIR}/input.txt"
    echo "   Size: $(wc -c < ${OUTPUT_DIR}/input.txt) bytes"
    echo "   Lines: $(wc -l < ${OUTPUT_DIR}/input.txt)"
else
    echo "❌ Failed to download input.txt"
    exit 1
fi
