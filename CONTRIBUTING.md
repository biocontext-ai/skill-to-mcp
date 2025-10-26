# Contributing to skill-to-mcp

Thank you for your interest in contributing to skill-to-mcp!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/biocontext-ai/skill-to-mcp.git
cd skill-to-mcp
```

2. Install in development mode with all dependencies:
```bash
uv venv --python 3.13
source .venv/bin/activate
uv sync --all-extras
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

## Running Tests

The test suite uses the included `skills/` directory for testing:

```bash
uv run pytest tests/ -v
```

With coverage:
```bash
uv run pytest tests/ --cov=src/skill_to_mcp --cov-report=html
```

## Code Style

This project uses:
- **ruff** for linting and formatting
- **pre-commit** for automated checks

Before committing, ensure your code passes all checks:
```bash
uv run pre-commit run --all-files
```

## Adding New Skills

To contribute example skills to the repository, place them in the `skills/` directory. Each skill:

1. Must have its own subdirectory
2. Must contain a `SKILL.md` file with valid YAML frontmatter
3. Should follow the naming convention: lowercase-with-hyphens

Example structure:
```
skills/
└── my-new-skill/
    ├── SKILL.md          # Required: Skill documentation with frontmatter
    ├── scripts/          # Optional: Implementation scripts
    │   └── main.py
    └── references/       # Optional: Reference materials
        └── docs.md
```

### SKILL.md Format

```markdown
---
name: my-new-skill
description: Brief description of what this skill does and when to use it
---

# Skill Title

Detailed documentation here...
```

## Project Structure

```
skill-to-mcp/
├── src/skill_to_mcp/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── mcp.py               # FastMCP server configuration
│   ├── skill_parser.py      # Skill parsing logic
│   └── tools/
│       ├── __init__.py
│       └── _skills.py       # MCP tool implementations
├── skills/                  # Skill directories
│   └── single-cell-rna-qc/
├── tests/
│   ├── test_app.py          # Integration tests
│   └── test_skill_parser.py # Unit tests
└── docs/                    # Documentation
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Ensure tests pass (`uv run pytest tests/`)
5. Ensure code style is correct (`pre-commit run --all-files`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Reporting Issues

When reporting issues, please include:

1. A clear description of the problem
2. Steps to reproduce
3. Expected vs actual behavior
4. Your environment (Python version, OS, etc.)
5. Relevant error messages or logs

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
