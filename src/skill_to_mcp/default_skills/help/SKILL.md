---
name: help
description: Provides information about using the skill-to-mcp server and how to install additional skills
---

# Help Skill

This is the default skill loaded by the skill-to-mcp server when no skills directory is specified.

## Purpose

The skill-to-mcp server converts AI Skills (following Claude Skills format) into MCP server resources. This help skill provides basic information about using the server.

## Available Tools

The server provides three core tools:

1. **get_available_skills**: Lists all available skills with their descriptions
2. **get_skill_details**: Returns the full SKILL.md content and file listing for a specific skill
3. **get_skill_related_file**: Reads any file within a skill directory

## Installing Additional Skills

To use custom skills with this server, you need to:

1. **Create or obtain a skills directory** containing skill subdirectories
2. **Configure the server** to use your skills directory

### Option 1: Using Command-Line Option

```bash
skill_to_mcp --skills-dir /path/to/your/skills
```

Or with uvx:

```bash
uvx skill_to_mcp --skills-dir /path/to/your/skills
```

### Option 2: Using Environment Variable

Set the `SKILLS_DIR` environment variable:

```bash
export SKILLS_DIR=/path/to/your/skills
skill_to_mcp
```

### Option 3: MCP Client Configuration

Configure your MCP client (e.g., Claude Desktop) to pass the skills directory:

```json
{
  "mcpServers": {
    "my-skills": {
      "command": "uvx",
      "args": ["skill_to_mcp", "--skills-dir", "/path/to/your/skills"],
      "env": {
        "UV_PYTHON": "3.12"
      }
    }
  }
}
```

## Creating Your Own Skills

Each skill must:

1. Have its own subdirectory
2. Contain a `SKILL.md` file with YAML frontmatter
3. Follow this frontmatter format:

```markdown
---
name: my-skill-name
description: Brief description of what this skill does and when to use it
---

# Skill Content

Your skill instructions and documentation go here...
```

### Example Skill Structure

```
my-skills/
├── skill-1/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── example.py
│   └── references/
│       └── guidelines.md
└── skill-2/
    └── SKILL.md
```

## Finding More Skills

- **BioContextAI Registry**: [biocontext.ai/registry](https://biocontext.ai/registry) - Community catalog of biomedical MCP servers and skills
- **GitHub**: Search for repositories tagged with "claude-skills" or "mcp-skills"
- **Community Resources**: Check the skill-to-mcp documentation for links to skill collections

## Next Steps

1. Identify or create skills relevant to your use case
2. Configure the server with your skills directory
3. Use the `get_available_skills` tool to discover what's available
4. Start using the skills with `get_skill_details` and `get_skill_related_file`

## Documentation

For more information, visit:
- Documentation: [skill-to-mcp.readthedocs.io](https://skill-to-mcp.readthedocs.io)
- Source Code: [github.com/biocontext-ai/skill-to-mcp](https://github.com/biocontext-ai/skill-to-mcp)
- Issues: [github.com/biocontext-ai/skill-to-mcp/issues](https://github.com/biocontext-ai/skill-to-mcp/issues)
