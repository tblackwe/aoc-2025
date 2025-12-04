# Project Architecture

This document describes the architecture and design decisions for the spec-driven development approach used in this Advent of Code 2025 project.

## Philosophy

Traditional coding workflow:
```
Problem → Code → Test → Debug → Submit
```

Spec-driven workflow:
```
Problem → Spec → Review Spec → AI Agent → Review Solution → Submit
```

The key insight: **A well-written specification is easier to review and refine than code**, and can be delegated to AI agents for implementation.

## Project Structure

```
aoc-2025/
├── .opencode/              # Agent manager configuration
│   ├── README.md           # Opencode documentation
│   └── config.yaml         # Agent settings and workflow config
│
├── specs/                  # Problem specifications
│   ├── README.md           # Spec writing guidelines
│   ├── day-01-example.md   # Example spec format
│   └── day-XX.md           # Daily puzzle specs (created as needed)
│
├── solutions/              # Generated solutions
│   ├── README.md           # Solution directory guide
│   └── day-XX/             # Per-day solution directories
│       ├── solution.py     # Main solution implementation
│       ├── test_solution.py # Unit tests
│       ├── input.txt       # Puzzle input (gitignored)
│       └── README.md       # Solution notes
│
├── templates/              # Reusable templates
│   ├── spec-template.md    # Blank spec template
│   ├── solution-template.py # Python solution skeleton
│   └── test-template.py    # Test suite skeleton
│
├── README.md               # Project overview and quick start
├── CONTRIBUTING.md         # Detailed contribution workflow
├── QUICKSTART.md           # 5-minute getting started guide
└── new-day.sh              # Script to set up a new day
```

## Component Details

### Specifications (`specs/`)

**Purpose**: Define "what" needs to be solved, not "how" to solve it.

**Key Elements**:
- Problem description (from AoC, paraphrased)
- Input/output format specification
- Multiple worked examples
- Edge cases to handle
- Specific test cases
- Performance constraints

**Benefits**:
- Easier to review than code
- Clear communication with AI agents
- Serves as documentation
- Can be refined iteratively

### Solutions (`solutions/`)

**Purpose**: Contain AI-generated (or manual) implementations.

**Structure**: Each day gets its own directory with:
- `solution.py` - Main implementation
- `test_solution.py` - Test suite based on spec
- `input.txt` - User's puzzle input (not committed)
- `README.md` - Notes and insights

**Philosophy**: Solutions should be **generated**, not written. Write specs instead.

### Templates (`templates/`)

**Purpose**: Provide consistent structure for specs and solutions.

**Templates**:
1. **spec-template.md**: Structured format for writing problem specs
2. **solution-template.py**: Python solution skeleton with clear sections
3. **test-template.py**: Test suite template with unittest framework

**Customization**: Templates can be modified for different languages or styles.

### Agent Configuration (`.opencode/`)

**Purpose**: Configure how AI agents interact with the project.

**Configuration** (`config.yaml`):
- Model selection (GPT-4, Claude, etc.)
- Temperature and token limits
- Directory locations
- Default instructions for agents
- Validation commands

**Flexibility**: Can work with Opencode or other agent managers.

## Automation

### `new-day.sh` Script

**Purpose**: Set up a new day's files in seconds.

**Usage**:
```bash
./new-day.sh 1   # Creates specs/day-01.md and solutions/day-01/
```

**What it does**:
1. Creates spec from template with day number filled in
2. Creates solution directory
3. Populates solution templates
4. Creates solution README
5. Shows next steps

## Workflow

### Standard Flow

1. **Prepare**: Run `./new-day.sh <day>`
2. **Specify**: Edit `specs/day-XX.md` with puzzle details
3. **Assign**: `opencode assign specs/day-XX.md` (or manual)
4. **Test**: `cd solutions/day-XX && python3 -m unittest test_solution.py`
5. **Run**: `python3 solution.py` with your puzzle input
6. **Submit**: Submit answer to Advent of Code

### Iteration Flow

If the solution is incorrect:
1. **Debug**: Identify what went wrong
2. **Refine Spec**: Add missing details, edge cases, or examples
3. **Reassign**: Give updated spec to agent
4. **Repeat**: Test again

## Design Decisions

### Why Python?

- Default in templates, but **not required**
- Fast to write and test
- Good for AoC problems (parsing, algorithms)
- Widely supported by AI models

**Note**: Any language can be specified in the spec's implementation notes.

### Why Separate Specs from Solutions?

- **Separation of concerns**: What vs. How
- **Reviewability**: Easier to review a spec than code
- **Reusability**: Same spec can generate solutions in different languages
- **Documentation**: Specs serve as permanent documentation

### Why Directory-per-Day?

- **Isolation**: Each day is self-contained
- **Flexibility**: Different languages/approaches per day
- **Organization**: Easy to find specific solutions
- **Independence**: Can work on multiple days in parallel

### Why Templates?

- **Consistency**: All specs and solutions follow same structure
- **Speed**: Quick setup for new days
- **Quality**: Ensures important sections aren't forgotten
- **Guidance**: Shows what information is needed

## Customization

### Using Different Languages

Edit the spec's implementation notes:
```markdown
## Implementation Notes
- **Language**: JavaScript (Node.js)
- **Style**: ESLint standard
```

Then provide appropriate templates or modify the AI agent's instructions.

### Adding More Templates

Create new files in `templates/`:
- `solution-template.js` for JavaScript
- `solution-template.go` for Go
- `spec-template-detailed.md` for complex problems

### Using Different Agent Managers

The project structure works with any agent manager:
- **GitHub Copilot**: Use specs as context in comments
- **ChatGPT**: Copy-paste spec into conversation
- **Custom Scripts**: Write your own automation
- **Manual**: Implement solutions yourself using specs as guide

## Best Practices

### Writing Specs

1. **Be Specific**: Ambiguity leads to incorrect solutions
2. **Include Examples**: Multiple examples > lengthy descriptions
3. **Think Edge Cases**: Empty, single, max, duplicates, invalid
4. **Define Tests**: Concrete inputs and expected outputs
5. **Iterate**: Refine spec if agent misunderstands

### Reviewing Solutions

1. **Run Tests First**: Does it pass spec examples?
2. **Check Edge Cases**: Try boundary conditions
3. **Read the Code**: Does it make sense?
4. **Test with Real Input**: Try your puzzle input
5. **Don't Trust Blindly**: AI agents make mistakes

### Managing the Repository

1. **Commit Specs Early**: Before generating solutions
2. **Gitignore Inputs**: Puzzle inputs are user-specific
3. **Document Insights**: Add notes to solution READMEs
4. **Keep Templates Updated**: Improve based on experience

## Future Enhancements

Possible additions to this project structure:

- [ ] Support for multiple languages
- [ ] Automated testing CI/CD pipeline
- [ ] Performance benchmarking
- [ ] Solution comparison (different approaches)
- [ ] Visualization of solutions
- [ ] Shared test suite across languages
- [ ] Web interface for spec creation
- [ ] Integration with Advent of Code API

## Conclusion

This spec-driven approach transforms solving AoC from:
- Writing code → Writing specifications
- Debugging → Refining specs
- Implementation details → Problem understanding

The goal is to **think clearly about problems** and **delegate implementation** to AI agents, while maintaining quality through good specifications and testing.

Happy spec writing! 🎄⭐
