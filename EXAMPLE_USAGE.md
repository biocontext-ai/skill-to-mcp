# Example Usage

This document demonstrates how to use the skill-to-mcp server with different configurations.

## Quick Start

### 1. Using uvx (Recommended)

Run directly without installation:

```bash
# Using command-line option
uvx skill_to_mcp --skills-dir /path/to/your/skills

# Using environment variable
SKILLS_DIR=/path/to/your/skills uvx skill_to_mcp
```

### 2. Using pip

Install and run:

```bash
pip install skill_to_mcp

# Run with skills directory
skill_to_mcp --skills-dir /path/to/your/skills
```

## MCP Client Configuration

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "biomedical-skills": {
      "command": "uvx",
      "args": [
        "skill_to_mcp",
        "--skills-dir",
        "/Users/yourname/biomedical-skills"
      ],
      "env": {
        "UV_PYTHON": "3.12"
      }
    }
  }
}
```

### Using Environment Variables

```json
{
  "mcpServers": {
    "biomedical-skills": {
      "command": "uvx",
      "args": ["skill_to_mcp"],
      "env": {
        "UV_PYTHON": "3.12",
        "SKILLS_DIR": "/Users/yourname/biomedical-skills"
      }
    }
  }
}
```

### Multiple Skill Collections

You can run multiple instances with different skill directories:

```json
{
  "mcpServers": {
    "biomedical-skills": {
      "command": "uvx",
      "args": ["skill_to_mcp", "--skills-dir", "/path/to/biomedical-skills"]
    },
    "data-science-skills": {
      "command": "uvx",
      "args": ["skill_to_mcp", "--skills-dir", "/path/to/data-science-skills"]
    }
  }
}
```

## Creating Your Own Skills Directory

### 1. Create the directory structure

```bash
mkdir -p ~/my-skills/my-first-skill
cd ~/my-skills/my-first-skill
```

### 2. Create a SKILL.md file

```bash
cat > SKILL.md << 'EOF'
---
name: my-first-skill
description: A simple example skill demonstrating the basic structure
---

# My First Skill

This is an example skill.

## Usage

Describe how to use this skill here.

## Examples

Provide examples of when to use this skill.
EOF
```

### 3. (Optional) Add supporting files

```bash
mkdir scripts
echo "print('Hello from my skill!')" > scripts/example.py
```

### 4. Use with skill-to-mcp

```bash
skill_to_mcp --skills-dir ~/my-skills
```

## Testing the Server

You can test the server works by listing available tools:

```python
from fastmcp import Client
from skill_to_mcp.mcp import initialize_mcp
import asyncio

async def test():
    mcp = initialize_mcp("/path/to/your/skills")
    async with Client(mcp) as client:
        # List available skills
        skills = await client.call_tool("get_available_skills", {})
        print(skills.content[0].text)

asyncio.run(test())
```

## HTTP Transport (Advanced)

For HTTP-based access:

```bash
skill_to_mcp \
  --skills-dir /path/to/skills \
  --transport http \
  --port 8080 \
  --host 0.0.0.0
```

Then configure your MCP client to connect via HTTP:

```json
{
  "mcpServers": {
    "remote-skills": {
      "url": "http://localhost:8080"
    }
  }
}
```

## Troubleshooting

### Error: "Skills directory is required"

Make sure you've specified the skills directory either via:
- `--skills-dir` command-line option, or
- `SKILLS_DIR` environment variable

### Error: "Skills directory does not exist"

Verify the path exists and is accessible:

```bash
ls -la /path/to/your/skills
```

### No skills found

Check that your skills directory contains subdirectories with `SKILL.md` files:

```bash
find /path/to/your/skills -name "SKILL.md"
```

Each SKILL.md must have valid YAML frontmatter with `name` and `description` fields.
