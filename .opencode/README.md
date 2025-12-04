# Opencode Configuration

This directory contains configuration for the Opencode agent manager.

## What is Opencode?

Opencode is an agent manager that helps coordinate AI agents working on coding tasks. It's particularly useful for spec-driven development where you want to delegate implementation to AI agents.

## Configuration File

The `config.yaml` file defines:

- **Project Settings**: Name, description
- **Agent Configuration**: Which model to use, temperature, token limits
- **Workflow**: Directories for specs, solutions, templates
- **Instructions**: Default instructions given to agents
- **Validation**: How to test generated solutions

## Using Opencode

### Assigning a Spec to an Agent

```bash
opencode assign specs/day-01.md --output solutions/day-01/
```

This will:
1. Read the specification
2. Provide it to an AI agent with context
3. Generate solution and tests in the output directory
4. Optionally run validation tests

### Customizing Agent Behavior

Edit `config.yaml` to customize:

```yaml
agents:
  default:
    model: "gpt-4"           # Change model
    temperature: 0.2         # Adjust creativity (0-1)
    max_tokens: 4000         # Adjust response length
```

### Adding Custom Instructions

Modify the `instructions` field in `config.yaml` to add project-specific guidance:

```yaml
workflow:
  assignment:
    instructions: |
      Additional instructions here...
      - Follow PEP 8 style guide
      - Optimize for readability
      - Add type hints
```

## Alternative Agent Managers

If you're not using Opencode, you can still use this project structure with:

- **GitHub Copilot**: Use the specs as comments/documentation
- **ChatGPT/Claude**: Copy-paste specs into conversation
- **Custom Scripts**: Write your own automation using the structure

The key is the spec-driven approach, not the specific tool.

## Learn More

- Opencode Documentation: Check your agent manager's documentation for specific setup instructions
- See [../CONTRIBUTING.md](../CONTRIBUTING.md) for workflow details
- Check [../QUICKSTART.md](../QUICKSTART.md) for quick start guide
