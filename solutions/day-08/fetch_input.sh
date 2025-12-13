#!/bin/bash
# Download Advent of Code 2025 Day 8 input
# Run this script to fetch your puzzle input

SESSION=$(cat ~/.adventofcode.session)

curl -s \
  -H "Cookie: session=${SESSION}" \
  -H "User-Agent: Mozilla/5.0" \
  https://adventofcode.com/2025/day/8/input \
  -o input.txt

if [ -f input.txt ]; then
    echo "✅ Downloaded input.txt"
    echo "   Size: $(wc -c < input.txt) bytes"
    echo "   Lines: $(wc -l < input.txt)"
else
    echo "❌ Failed to download input.txt"
    exit 1
fi
