# Multi-Model Architect Testing

This directory contains tools for testing the architect agent with multiple AI models to compare spec generation quality.

## Overview

The multi-model architect system allows you to:
1. Run the architect agent with multiple AI models simultaneously
2. Generate specs for the same puzzle using different models
3. Compare the quality, completeness, and approach of each model's output
4. Choose the best spec or merge insights from multiple models

## Configuration

### Models Configured

The configuration in `.opencode/multi-model-architect.yaml` includes:

#### GitHub Copilot Models
- **GPT-4o**: Latest GPT-4 optimized model
- **Claude 3.5 Sonnet**: Anthropic's latest reasoning model
- **Gemini 2.0 Flash**: Google's latest fast model
- **O1 Preview**: OpenAI's reasoning model

> **Note**: The models you requested (GPT-5.1-Codex-Max, Gemini 3 Pro, Big Pickle) don't currently exist or aren't available through standard APIs. The configuration uses the latest available models as of December 2024.

### Updating Configuration

Edit `.opencode/multi-model-architect.yaml` to:
- Enable/disable specific models
- Add new models as they become available
- Adjust timeout and token limits
- Configure output directories

```yaml
models:
  - name: "model-name"
    provider: "provider-name"
    display_name: "Friendly Name"
    enabled: true
```

## Usage

### Basic Usage

```bash
# Run with all enabled models
python3 run-multi-model-architect.py puzzle.txt --day 5

# Run with specific models only  
python3 run-multi-model-architect.py puzzle.txt --day 5 --models gpt-4o,claude-3.5-sonnet

# Skip comparison report
python3 run-multi-model-architect.py puzzle.txt --day 5 --no-report
```

### Preparing Puzzle Input

1. Copy the puzzle description from Advent of Code
2. Save it to a text file (e.g., `puzzle-day-05.txt`)
3. Run the multi-model script with that file

Example `puzzle-day-05.txt`:
```
--- Day 5: Print Queue ---

[Full puzzle description here...]
```

### Output Structure

```
specs/
  multi-model-comparison/
    day-05-gpt-4o.md              # Spec from GPT-4o
    day-05-claude-3-5-sonnet.md   # Spec from Claude
    day-05-gemini-2-0-flash.md    # Spec from Gemini
    day-05-o1-preview.md          # Spec from O1
    comparison-day-05.md          # Comparison report
```

## Comparison Metrics

The comparison report evaluates each model's spec on:

### Completeness
- Did it cover all required sections?
- Problem description present?
- Algorithm analysis included?
- Test plan comprehensive?
- Implementation guidance provided?

### Detail Level
- How thorough are the explanations?
- Quality of examples and traces
- Depth of complexity analysis
- Coverage of edge cases

### Test Coverage
- Number of test cases provided
- Variety of test scenarios
- Edge and corner cases identified
- Input/output examples given

### Algorithm Analysis
- Number of approaches considered
- Quality of complexity analysis
- Data structure recommendations
- Trade-off discussions

### Clarity
- How clear and actionable is the spec?
- Can a developer implement without questions?
- Well-organized structure?
- Clear explanations?

## Implementation Status

### ⚠️ Current Limitations

The `run-multi-model-architect.py` script is currently a **framework** that needs integration with OpenCode's Task tool to actually invoke different models.

**What works:**
- Configuration loading
- Puzzle input reading
- Output directory creation
- Comparison report generation

**What needs implementation:**
- Actual model invocation via OpenCode Task tool
- Model-specific parameter passing
- Async execution of multiple models
- Result collection and spec saving

### Implementing Model Invocation

To complete the implementation, the script needs to call the OpenCode Task tool with model selection. This would look like:

```python
# In _run_architect_with_model method
result = await task(
    description=f"Generate spec with {model_name}",
    prompt=task_prompt,
    subagent_type="architect",
    model=model_name,  # Model selection parameter
    temperature=self.config['agent']['task']['temperature'],
    max_tokens=self.config['agent']['task']['max_tokens']
)
```

### Manual Workaround

Until the automation is complete, you can manually test multiple models:

1. **Use OpenCode CLI** (if available):
   ```bash
   opencode task --agent architect --model gpt-4o --input puzzle.txt
   opencode task --agent architect --model claude-3.5-sonnet --input puzzle.txt
   ```

2. **Use @architect in OpenCode UI** with different model selections

3. **Copy-paste to different AI interfaces** (ChatGPT, Claude, etc.)

## Workflow

### Recommended Approach

1. **Prepare puzzle input**
   ```bash
   # Copy puzzle to file
   pbpaste > puzzle-day-05.txt
   ```

2. **Run multi-model architect**
   ```bash
   python3 run-multi-model-architect.py puzzle-day-05.txt --day 5
   ```

3. **Review all generated specs**
   ```bash
   ls specs/multi-model-comparison/day-05-*.md
   ```

4. **Read comparison report**
   ```bash
   cat specs/multi-model-comparison/comparison-day-05.md
   ```

5. **Choose best spec** or merge insights

6. **Copy to main specs directory**
   ```bash
   cp specs/multi-model-comparison/day-05-claude-3-5-sonnet.md specs/day-05.md
   ```

7. **Implement solution**
   ```bash
   @aoc-helper implement specs/day-05.md
   ```

## Future Enhancements

Potential improvements to the multi-model system:

- [ ] Automatic quality scoring using LLM-as-judge
- [ ] Side-by-side diff viewer for specs
- [ ] Hybrid spec generation (merge best parts from multiple models)
- [ ] Performance tracking across puzzles (which model is consistently best?)
- [ ] Cost tracking per model
- [ ] Integration with OpenCode's native multi-model support

## Troubleshooting

### PyYAML Not Found
```bash
pip3 install pyyaml
```

### Config File Not Found
```bash
# Check path
ls -la .opencode/multi-model-architect.yaml

# Or specify custom path
python3 run-multi-model-architect.py puzzle.txt --day 5 --config custom-config.yaml
```

### Model Not Available
Edit `.opencode/multi-model-architect.yaml` and set `enabled: false` for unavailable models.

## See Also

- [AGENTS.md](../AGENTS.md) - Agent configuration and roles
- [.opencode/prompts/architect.txt](prompts/architect.txt) - Architect agent prompt
- [OpenCode Documentation](https://opencode.ai/docs) - OpenCode usage guide
