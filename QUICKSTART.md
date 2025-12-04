# Quick Start Guide

Get started with spec-driven development for Advent of Code 2025 in 5 minutes.

## Prerequisites

- Python 3.x (for running examples)
- An AI agent tool (e.g., Opencode, GitHub Copilot, ChatGPT)
- Access to [Advent of Code 2025](https://adventofcode.com/2025)

## Step-by-Step

### 1. Wait for a Puzzle Release

Advent of Code releases puzzles daily from December 1-25. Go to [adventofcode.com/2025](https://adventofcode.com/2025) when a puzzle is available.

### 2. Create a Spec (5 minutes)

```bash
# Copy the template
cp templates/spec-template.md specs/day-01.md

# Edit specs/day-01.md
```

Fill in:
- Problem description (from AoC website)
- Input/output format
- At least 2 examples from the puzzle
- Edge cases you can think of
- Test cases

### 3. Assign to AI Agent

**Option A: Using Opencode**
```bash
opencode assign specs/day-01.md --output solutions/day-01/
```

**Option B: Manual Assignment**
1. Copy the content of `specs/day-01.md`
2. Provide it to your AI agent with instructions:
   ```
   Please implement a solution for this Advent of Code puzzle spec.
   Follow the structure in templates/solution-template.py.
   Include tests based on the spec examples.
   ```

### 4. Test the Solution

```bash
cd solutions/day-01

# Run tests
python3 -m unittest test_solution.py

# Run with your puzzle input
# (Download from AoC and save as input.txt)
python3 solution.py
```

### 5. Submit Answer

Copy the output and submit it on the Advent of Code website!

## Example Workflow

Here's a real example of the process:

1. **Read Puzzle**: Day 1 asks you to sum all numbers in a list
2. **Write Spec** (2 min):
   ```markdown
   # Day 01: Sum Numbers
   Parse input as integers, one per line, and return their sum.
   Example: "1\n2\n3" → 6
   ```
3. **Assign to Agent** (1 min): Provide spec to AI
4. **Review Solution** (2 min): Check generated code and tests
5. **Run & Submit** (1 min): Execute and submit answer

Total: ~6 minutes per puzzle!

## Tips

- **Start Simple**: Your first spec doesn't need to be perfect
- **Iterate**: If the agent misunderstands, clarify the spec and retry
- **Keep Examples**: Good examples are worth 1000 words of description
- **Test First**: Always run the example tests before trying your puzzle input

## What If It Doesn't Work?

1. **Agent confused?** → Add more examples to your spec
2. **Wrong answer?** → Check edge cases in your spec
3. **Code error?** → Review the error and clarify constraints in spec
4. **Too slow?** → Add performance requirements to spec

## Next Steps

- Read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed workflow
- Check [specs/day-01-example.md](specs/day-01-example.md) for a spec example
- Review templates in `templates/` directory

Happy coding! 🎄⭐
