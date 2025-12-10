# OpenCode Agents Configuration

This is an Advent of Code 2025 solutions repository using Python.

## Project Structure

- `solutions/` - Daily puzzle solutions organized by day
- `specs/` - Puzzle specifications and problem descriptions
- `templates/` - Templates for creating new day solutions and specs
- `new-day.sh` - Script to scaffold a new day's solution

## Coding Patterns

### Python Solutions
- Each day has its own directory under `solutions/day-XX/`
- Solutions are in `solution.py` files
- Solutions typically include:
  - Input parsing functions
  - Part 1 and Part 2 solution functions
  - A `main()` function that runs both parts
  - File I/O to read puzzle input from `input.txt`

### Code Style
- Use clear, readable variable names
- Add comments for complex algorithms
- Break down problems into smaller helper functions
- Parse input data carefully according to puzzle requirements
- Handle both sample and actual puzzle inputs

## Agents

### Build
**Mode**: primary  
**Description**: Default agent for implementing puzzle solutions with full tool access.

Use this agent for:
- Implementing new day solutions
- Debugging and fixing errors
- Running tests and checking output
- Modifying existing solutions

### Plan
**Mode**: primary  
**Description**: Planning and analysis mode without making code changes.

Use this agent for:
- Analyzing puzzle requirements
- Planning solution approaches
- Reviewing code structure
- Discussing algorithm choices

### AoC Helper
**Mode**: subagent  
**Description**: Specialized assistant for Advent of Code puzzles.

This agent helps with:
- Understanding puzzle requirements from specs
- Suggesting algorithmic approaches
- Explaining common AoC patterns (BFS, DFS, dynamic programming, etc.)
- Identifying edge cases in puzzle inputs
- Optimizing solutions for performance

**Tools**:
- `write`: true (can create solution files)
- `edit`: true (can modify solutions)
- `bash`: true (can run solutions and tests)

### Test Runner
**Mode**: subagent  
**Description**: Runs and validates puzzle solutions.

This agent:
- Executes Python solutions
- Compares output against expected results
- Reports any errors or failures
- Suggests fixes for failing tests

**Tools**:
- `write`: false
- `edit`: false
- `bash`: true (limited to running Python scripts)

## Common Tasks

1. **Starting a new day**: Run `./new-day.sh XX` where XX is the day number
2. **Running a solution**: `python solutions/day-XX/solution.py`
3. **Testing with sample input**: Ensure `input.txt` contains sample data first
4. **Reading specs**: Check `specs/day-XX.md` for puzzle description

## Notes for AI Assistants

- Advent of Code puzzles often have two parts, with Part 2 building on Part 1
- Input data varies significantly between puzzles
- Performance optimization may be needed for larger inputs
- Edge cases are common and should be tested
- Many puzzles involve graph algorithms, grid traversal, or mathematical patterns
