# Contributing to AoC 2025 Spec-Driven Development

This project follows a spec-driven development approach where AI agents implement solutions based on detailed specifications.

## Workflow

### 1. Create a Specification

When a new Advent of Code puzzle is released:

```bash
# Copy the template
cp templates/spec-template.md specs/day-XX.md

# Edit the spec with problem details
# Include: description, examples, edge cases, test cases
```

### 2. Write a Complete Spec

A good spec includes:

- **Problem Description**: Clear explanation of what needs to be solved
- **Input/Output Format**: Exact format specifications
- **Examples**: Multiple worked examples with explanations
- **Edge Cases**: Boundary conditions and special cases
- **Test Cases**: Specific inputs and expected outputs
- **Constraints**: Performance and implementation requirements

### 3. Assign to AI Agent

Use Opencode to assign the spec to an AI agent:

```bash
opencode assign specs/day-XX.md --output solutions/day-XX/
```

Or manually provide the spec to your AI agent of choice.

### 4. Review Generated Solution

Check the generated solution:

```bash
cd solutions/day-XX
python3 -m unittest test_solution.py  # Run tests
python3 solution.py                    # Run the solution
```

### 5. Iterate if Needed

If the solution doesn't meet requirements:
- Refine the spec to be more precise
- Add missing edge cases or examples
- Reassign to the agent with the updated spec

## Tips for Writing Good Specs

### Be Specific

❌ Bad: "Process the input and find the answer"
✅ Good: "Parse each line as a pair of integers separated by whitespace, then sum all first integers"

### Include Examples

Always provide at least 2-3 examples with step-by-step explanations:

```markdown
**Input:**
1 2
3 4

**Expected Output:**
4

**Explanation:**
Sum of first integers: 1 + 3 = 4
```

### Think Through Edge Cases

- What if input is empty?
- What about single elements?
- Maximum/minimum values?
- Duplicate values?
- Invalid input?

### Define Test Cases

```markdown
1. **Empty Input**: `""` → `0`
2. **Single Line**: `"5 10"` → `5`
3. **Multiple Lines**: `"1 2\n3 4\n5 6"` → `9`
```

## Project Structure

```
aoc-2025/
├── specs/              # Write specs here
├── solutions/          # Generated solutions go here
├── templates/          # Templates for specs and solutions
└── .opencode/          # Opencode configuration
```

## Language Choices

While templates use Python, you can specify any language in your spec:

```markdown
## Implementation Notes
- **Language**: JavaScript (Node.js)
- **Style**: Standard.js
```

## Questions?

For issues with:
- **Specs**: Review examples in `specs/day-01-example.md`
- **Templates**: Check files in `templates/`
- **Opencode**: See `.opencode/config.yaml`
