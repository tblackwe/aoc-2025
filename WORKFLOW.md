# Agentic Workflow Script - Quick Reference

## Usage

```bash
./solve-day.py <day> <model>
```

## Examples

```bash
# Solve day 5 using GPT-4o
./solve-day.py 5 gpt-4o

# Solve day 12 using Claude 3.5 Sonnet
./solve-day.py 12 claude-3.5-sonnet

# Solve day 25 using Gemini 2.0 Flash
./solve-day.py 25 gemini-2.0-flash --year 2025
```

## Workflow Stages

The script orchestrates three AI agents in sequence:

### Stage 1: Architect
**Purpose**: Create comprehensive specification

**Input**: Puzzle URL (fetched automatically)

**Output**: `specs/day-XX.md`

**What it does**:
- Fetches puzzle description from adventofcode.com
- Analyzes problem requirements
- Identifies algorithm patterns
- Creates detailed specification with:
  - Problem description and examples
  - Input/output format specifications
  - Algorithm analysis (2-3 approaches)
  - Data structure recommendations
  - Comprehensive test plan
  - Implementation guidance

### Stage 2: SDET
**Purpose**: Create comprehensive unit tests (TDD - tests first!)

**Input**: `specs/day-XX.md`

**Output**: `solutions/day-XX/test_solution.py`

**What it does**:
- Reviews specification thoroughly
- Extracts example test cases with expected outputs
- Identifies edge cases:
  - Empty inputs
  - Single element inputs
  - Boundary conditions
  - Maximum/minimum values
- Creates test suite with:
  - Parsing tests
  - Part 1 example tests
  - Part 2 example tests (if available)
  - Edge case tests
- Runs tests to verify they FAIL (no implementation yet - RED phase)

### Stage 3: Implementer
**Purpose**: Implement solution to make tests pass

**Input**: 
- `specs/day-XX.md`
- `solutions/day-XX/test_solution.py`

**Output**: `solutions/day-XX/solution.py`

**What it does**:
- Reviews spec and test requirements
- Implements `parse_input()` function (foundation!)
- Implements `solve_part1()` following spec algorithms
- Runs tests frequently (Red-Green-Refactor)
- Makes all Part 1 tests pass (GREEN phase)
- Refactors code for quality
- Verifies final test suite passes

### Stage 4: Git Commit
**Purpose**: Commit changes to version control

**What it does**:
- Stages spec, tests, and solution files
- Creates descriptive commit message
- Commits to the day's branch

### Stage 5: Pull Request
**Purpose**: Create PR for code review

**What it does**:
- Pushes branch to remote
- Creates PR with comprehensive description
- Includes workflow summary and test results
- Ready for review and merge

## Models Available

Based on [GitHub Copilot supported models](https://docs.github.com/en/copilot/reference/ai-models/supported-models):

### OpenAI Models
- `gpt-5.1-codex` - **Recommended for AoC** - Latest coding-focused model
- `gpt-5.1-codex-max` - Maximum capability for complex problems
- `gpt-5.1-codex-mini` - Fast, low-cost option
- `gpt-5.1` - Latest general model
- `gpt-5` - Stable general model
- `gpt-5-mini` - Fast, economical choice

### Anthropic Models
- `claude-sonnet-4.5` - **Recommended for reasoning** - Best balance
- `claude-opus-4.5` - Maximum capability (higher cost)
- `claude-sonnet-4` - Reliable performance
- `claude-haiku-4.5` - Fast, economical choice

### Google Models
- `gemini-2.5-pro` - Solid all-around performance
- `gemini-3-pro` - Latest (public preview)

### Other Models
- `grok-code-fast-1` - xAI's fast coding model (complimentary)
- `raptor-mini` - Fine-tuned GPT-5 mini (free)

## Prerequisites

### 1. OpenCode Configuration
Ensure `.opencode/` directory has:
- `opencode.json` - Agent configurations
- `prompts/architect.txt` - Architect prompt
- `prompts/sdet.txt` - SDET prompt
- `prompts/implementer.txt` - Implementer prompt

### 2. AoC Session Cookie (Optional)
For automatic input fetching:

```bash
# Get your session cookie from adventofcode.com
# In browser: F12 > Application > Cookies > session value

# Save it to your home directory
echo "your_session_cookie_here" > ~/.adventofcode.session
```

Without the session cookie, you'll need to manually download `input.txt`.

## Output Files

After successful workflow:

```
specs/day-05.md                 # Comprehensive specification
solutions/day-05/
  ├── solution.py               # Part 1 implementation
  ├── test_solution.py          # Comprehensive test suite
  ├── input.txt                 # Your puzzle input
  └── README.md                 # Solution notes
.workflow-day-05.json           # Workflow metadata
```

## Workflow Results

The script saves metadata to `.workflow-day-XX.json`:

```json
{
  "day": 5,
  "model": "gpt-4o",
  "stages": {
    "architect": {
      "status": "success",
      "duration": 45.2,
      "output": "specs/day-05.md"
    },
    "sdet": {
      "status": "success",
      "duration": 32.8,
      "output": "solutions/day-05/test_solution.py"
    },
    "implementer": {
      "status": "success",
      "duration": 58.6,
      "output": "solutions/day-05/solution.py"
    }
  },
  "total_duration": 136.6,
  "completed_at": "2025-12-10T10:30:00"
}
```

## Running Tests

```bash
# Run tests for a specific day
cd solutions/day-05
python3 -m unittest test_solution.py

# Run with verbose output
python3 -m unittest test_solution.py -v
```

## Running Solution

```bash
# Run the solution (requires input.txt)
cd solutions/day-05
python3 solution.py
```

## Manual Intervention

The script currently requires manual agent invocation. When prompted:

1. Copy the displayed command
2. Run it in OpenCode (or your AI interface)
3. Wait for the agent to complete
4. Press Enter to continue to next stage

### Example Flow

```
Manual Step Required:
Run this command in OpenCode:
@architect Analyze day 5 puzzle at https://adventofcode.com/2025/day/5...

Press Enter when architect has created the spec (or 'skip' to continue):
[Press Enter after reviewing specs/day-05.md]
```

## Troubleshooting

### Tests Don't Fail in Stage 2
This is unusual. Tests should fail because no implementation exists yet. Check:
- Is there an existing `solution.py` file?
- Are the tests actually calling the solution functions?

### Architect Can't Fetch Puzzle
- Check the puzzle URL is correct
- Ensure the day has been released (midnight EST)
- Verify internet connection

### Input File Not Downloaded
- Check `~/.adventofcode.session` exists and has valid cookie
- Cookie expires - get a fresh one from browser
- Manually download: Save input from `https://adventofcode.com/2025/day/X/input`

### Agent Doesn't Follow Instructions
- Try a different model
- Review the agent prompts in `.opencode/prompts/`
- Check agent configuration in `opencode.json`

## Tips for Best Results

1. **Use Architect First**: Always start with a good spec
2. **Review the Spec**: Check that examples and expected outputs are correct
3. **Verify Tests Fail**: Tests should fail initially (TDD principle)
4. **Check Test Pass After Implementation**: All Part 1 tests should pass
5. **Run Solution Manually**: Verify it produces correct output
6. **Try Different Models**: Some models are better at certain problem types

## What About Part 2?

Part 2 is unlocked after solving Part 1. To handle Part 2:

1. Update the spec with Part 2 requirements
2. Run SDET again to add Part 2 tests
3. Run Implementer to implement Part 2 solution
4. Or run the full workflow again with the updated puzzle

## Advanced Usage

### Custom Year
```bash
./solve-day.py 5 gpt-4o --year 2024
```

### Skip Stages
During execution, type `skip` when prompted to skip a stage:
```
Press Enter when architect has created the spec (or 'skip' to continue): skip
```

## Integration with Git

Suggested workflow:

```bash
# Create a branch for the day
git checkout -b day-05

# Run the workflow
./solve-day.py 5 gpt-4o

# Review and test
cd solutions/day-05
python3 -m unittest test_solution.py
python3 solution.py

# Commit the results
git add specs/day-05.md solutions/day-05/
git commit -m "Add day 5 solution using TDD workflow"

# Create PR
gh pr create --title "Day 5 solution" --body "Solved using TDD workflow with gpt-4o"
```

## See Also

- [AGENTS.md](AGENTS.md) - Detailed agent documentation
- [PROJECT.md](PROJECT.md) - Project overview and architecture
- [templates/](templates/) - Templates for specs and solutions
