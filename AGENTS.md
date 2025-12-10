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

### Architect
**Mode**: subagent  
**Description**: Solution architect for Advent of Code puzzles - creates comprehensive specs and test plans.

This agent's primary responsibility is to:
1. **Analyze the puzzle**: Read and deeply understand the problem requirements
2. **Create detailed specs**: Write comprehensive specifications in `specs/day-XX.md` including:
   - Clear problem description with examples
   - Input/output format specifications
   - Step-by-step explanation of the solution approach
   - Part 1 and Part 2 requirements
3. **Identify algorithms**: Analyze and document possible algorithmic approaches:
   - Time and space complexity analysis
   - Data structure recommendations
   - Trade-offs between different approaches
   - Common AoC patterns (BFS, DFS, DP, graph algorithms, etc.)
4. **Design test plan**: Create comprehensive unit test strategy:
   - Example test cases from the puzzle
   - Edge cases and boundary conditions
   - Simple cases for validation
   - Test data with expected outputs

**Output**: A complete specification document that includes:
- Problem statement and examples
- Algorithm analysis and recommendations
- Detailed test plan with test cases
- Implementation guidance and gotchas

**Tools**:
- `write`: true (creates spec files)
- `edit`: true (updates specs)
- `bash`: false (read-only analysis)

Use this agent at the start of each new puzzle to create a solid foundation before implementation.

### Implementer
**Mode**: subagent  
**Description**: Solution implementer for Advent of Code puzzles - writes code based on specs and makes tests pass.

This agent helps with:
- Understanding puzzle requirements from specs
- Implementing solutions based on architect specs and test cases
- Following TDD by making failing tests pass
- Writing clean, well-commented Python code
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

### Optimizer
**Mode**: subagent  
**Description**: Analyzes and optimizes solution performance for time and space complexity.

This agent:
- Reviews existing solutions for performance bottlenecks
- Analyzes time and space complexity
- Suggests algorithmic improvements
- Implements optimizations while maintaining correctness
- Benchmarks performance improvements
- Documents trade-offs and optimization strategies

**Tools**:
- `write`: true (can optimize solution files)
- `edit`: true (can refactor code)
- `bash`: true (runs benchmarks and tests)

### SDET
**Mode**: subagent  
**Description**: Software Development Engineer in Test - implements comprehensive unit tests following TDD principles.

This agent's primary responsibility is to:
1. **Review specifications**: Read and analyze the spec file in `specs/day-XX.md` to understand:
   - Problem requirements and constraints
   - Expected inputs and outputs
   - Example test cases provided in the puzzle
   - Part 1 and Part 2 requirements
2. **Implement unit tests**: Create comprehensive test suites in `solutions/day-XX/test_solution.py` including:
   - Tests for example inputs from the spec (with expected outputs)
   - Tests for parsing functions
   - Tests for Part 1 and Part 2 solution functions
   - Parameterized tests for multiple test cases
   - Clear test names and documentation
3. **Identify edge cases**: Think critically about boundary conditions and edge cases:
   - Empty inputs or zero values
   - Single element inputs
   - Maximum/minimum values
   - Invalid or malformed inputs
   - Special patterns or corner cases specific to the puzzle
4. **Design test data**: Create meaningful test inputs that cover:
   - Happy path scenarios
   - Boundary conditions
   - Edge cases and error conditions
   - Performance stress tests (if applicable)
5. **Verify test coverage**: Ensure all critical paths and functions are tested

**Output**: A complete test file (`test_solution.py`) that:
- Contains all example test cases from the spec with correct expected values
- Includes comprehensive edge case tests
- Is ready to run before implementation (TDD approach)
- Uses clear assertions and helpful error messages
- Follows Python unittest best practices

**Tools**:
- `write`: true (creates test files)
- `edit`: true (updates tests)
- `bash`: true (can run tests to verify they fail before implementation)

Use this agent after the Architect creates the spec and before implementing the solution to follow test-driven development practices.

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
