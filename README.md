# Skill-to-MCP

[![BioContextAI - Registry](https://img.shields.io/badge/Registry-package?style=flat&label=BioContextAI&labelColor=%23fff&color=%233555a1&link=https%3A%2F%2Fbiocontext.ai%2Fregistry)](https://biocontext.ai/registry)
[![Tests][badge-tests]][tests]
[![Documentation][badge-docs]][documentation]
[![PyPI](https://img.shields.io/pypi/v/skill-to-mcp)][pypi]
[![Python Version](https://img.shields.io/pypi/pyversions/skill-to-mcp)][pypi]

[badge-tests]: https://img.shields.io/github/actions/workflow/status/biocontext-ai/skill-to-mcp/test.yaml?branch=main
[badge-docs]: https://img.shields.io/readthedocs/skill-to-mcp

Convert AI Skills (following Claude Skills format) into MCP server resources, making them accessible through the Model Context Protocol.

> **Part of [BioContextAI](https://biocontext.ai)** - A community-driven initiative connecting agentic AI with biomedical resources through standardized MCP servers. While this package is domain-agnostic and can be used for any skill collection, it was developed to support the biomedical research community.

## Overview

This MCP server exposes Claude Skills as resources that can be accessed by LLM applications through the Model Context Protocol. Skills are self-contained directories containing a `SKILL.md` file with YAML frontmatter, along with supporting files like scripts, references, and examples.

### Features

- **Automatic skill discovery**: Recursively finds all `SKILL.md` files in the `skills/` directory
- **Frontmatter parsing**: Extracts skill metadata (name, description) from YAML frontmatter
- **Three core tools**:
  - `get_available_skills`: Lists all available skills with descriptions
  - `get_skill_details`: Returns SKILL.md content and file listing for a specific skill
  - `get_skill_related_file`: Reads any file within a skill directory (with directory traversal protection)
- **Security**: Path validation prevents access outside skill directories

## Getting Started

Please refer to the [documentation][] for comprehensive guides, or jump to:
- [Configuration](#configuration) - Set up your skills directory
- [Usage](#usage) - Learn about the three core tools
- [Creating Skills](#creating-skills) - Build your own skills
- [Installation](#installation) - Multiple installation options

### Quick Links

- **Documentation**: [skill-to-mcp.readthedocs.io][documentation]
- **BioContextAI Registry**: [biocontext.ai/registry][registry]
- **API Reference**: [API documentation][]
- **Source Code**: [GitHub][source]
- **Issue Tracker**: [GitHub Issues][issue tracker]

## Configuration

The MCP server requires a skills directory to be specified. This allows you to:
- Install the package separately from your skills
- Edit skills without modifying the package
- Use different skill collections for different projects

Set the skills directory using either:
- Command-line option: `--skills-dir /path/to/skills`
- Environment variable: `SKILLS_DIR=/path/to/skills`

### Example Configuration for MCP Clients

```json
{
  "mcpServers": {
    "skill-to-mcp": {
      "command": "uvx",
      "args": ["skill_to_mcp", "--skills-dir", "/path/to/your/skills"],
      "env": {
        "UV_PYTHON": "3.12"
      }
    }
  }
}
```

Or using environment variables:

```json
{
  "mcpServers": {
    "skill-to-mcp": {
      "command": "uvx",
      "args": ["skill_to_mcp"],
      "env": {
        "UV_PYTHON": "3.12",
        "SKILLS_DIR": "/path/to/your/skills"
      }
    }
  }
}
```

## Usage

Once configured in your MCP client, the server provides three tools:

### get_available_skills

Returns a list of all available skills with metadata:
```json
[
  {
    "name": "single-cell-rna-qc",
    "description": "Performs quality control on single-cell RNA-seq data...",
    "path": "/path/to/skills/single-cell-rna-qc"
  }
]
```

### get_skill_details

Returns the full SKILL.md content and list of files for a specific skill:
```json
{
  "skill_content": "---\nname: single-cell-rna-qc\n...",
  "files": ["SKILL.md", "scripts/qc_analysis.py", "references/guidelines.md"]
}
```

The `return_type` parameter controls what data is returned:
- `"content"`: Returns only the SKILL.md content as text
- `"file_path"`: Returns only the absolute path to SKILL.md
- `"both"` (default): Returns both content and file path in a dict

### get_skill_related_file

Reads a specific file within a skill directory:
```python
get_skill_related_file(
    skill_name="single-cell-rna-qc",
    relative_path="scripts/qc_analysis.py",
    return_type="content"  # "content", "file_path", or "both" (default)
)
```

### Example Configurations

#### Claude Desktop Configuration

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

#### Multiple Skill Collections

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

## Creating Skills

Skills should be placed in your configured skills directory. Each skill must:

1. Have its own subdirectory
2. Contain a `SKILL.md` file with YAML frontmatter
3. Follow the frontmatter format:

```markdown
---
name: my-skill-name
description: Brief description of what this skill does and when to use it
---

# Skill Content

Instructions and documentation go here...
```

### Skill Naming Requirements

- Use lowercase letters, numbers, and hyphens only
- Maximum 64 characters
- No XML tags or reserved words

See the included example `skills/single-cell-rna-qc/SKILL.md` for a complete reference.

### Example Skills Directory Structure

```
my-skills/
├── skill-1/
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
├── skill-2/
│   ├── SKILL.md
│   └── data/
└── skill-3/
    └── SKILL.md
```

## Installation

You need to have Python 3.11 or newer installed on your system.
If you don't have Python installed, we recommend installing [uv][].

There are several alternative options to install skill-to-mcp:

1. Use `uvx` to run it immediately (requires SKILLS_DIR environment variable):

```bash
SKILLS_DIR=/path/to/skills uvx skill_to_mcp
```

Or with the command-line option:

```bash
uvx skill_to_mcp --skills-dir /path/to/skills
```

2. Include it in various MCP clients that support the `mcp.json` standard:

```json
{
  "mcpServers": {
    "skill-to-mcp": {
      "command": "uvx",
      "args": ["skill_to_mcp", "--skills-dir", "/path/to/your/skills"],
      "env": {
        "UV_PYTHON": "3.12"
      }
    }
  }
}
```

3. Install it through `pip`:

```bash
pip install --user skill_to_mcp
```

4. Install the latest development version:

```bash
pip install git+https://github.com/biocontext-ai/skill-to-mcp.git@main
```

## Deployment Options

### Local Development

For development and testing:

```bash
# Using uvx (recommended)
SKILLS_DIR=/path/to/skills uvx skill_to_mcp

# Using pip
pip install skill_to_mcp
skill_to_mcp --skills-dir /path/to/skills
```

### Production Deployment

For production environments with HTTP transport:

```bash
export MCP_ENVIRONMENT=PRODUCTION
export SKILLS_DIR=/path/to/skills
export MCP_TRANSPORT=http
export MCP_PORT=8000

skill_to_mcp
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN pip install skill_to_mcp

COPY skills /app/skills

ENV SKILLS_DIR=/app/skills
ENV MCP_TRANSPORT=http
ENV MCP_PORT=8000

CMD ["skill_to_mcp"]
```

Build and run:

```bash
docker build -t skill-to-mcp .
docker run -p 8000:8000 skill-to-mcp
```

## About BioContextAI

[BioContextAI](https://biocontext.ai) is a community effort to connect agentic artificial intelligence with biomedical resources using the Model Context Protocol. The [Registry](https://biocontext.ai/registry) is a community-driven catalog of MCP servers for biomedical research, enabling researchers and developers to discover, access, and contribute specialized tools and databases.

**Key Principles:**
- **FAIR4RS Compliant**: Findable, Accessible, Interoperable, Reusable for Research Software
- **Community-Driven**: Open-source and collaborative development
- **Standardized**: Built on the Model Context Protocol specification

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Development setup
- Code style requirements
- Testing procedures
- Pull request process

To contribute skills to the biomedical community, consider adding them to the [BioContextAI Registry](https://biocontext.ai/registry).

## Contact

If you found a bug, please use the [issue tracker][].

For questions about BioContextAI or the registry, visit [biocontext.ai](https://biocontext.ai).

## Citation

If you use this software in your research, please cite the BioContextAI paper:

```bibtex
@article{BioContext_AI_Kuehl_Schaub_2025,
  title={BioContextAI is a community hub for agentic biomedical systems},
  url={http://dx.doi.org/10.1038/s41587-025-02900-9},
  urldate = {2025-11-06},
  doi={10.1038/s41587-025-02900-9},
  year = {2025},
  month = nov,
  journal={Nature Biotechnology},
  publisher={Springer Science and Business Media LLC},
  author={Kuehl, Malte and Schaub, Darius P. and Carli, Francesco and Heumos, Lukas and Hellmig, Malte and Fernández-Zapata, Camila and Kaiser, Nico and Schaul, Jonathan and Kulaga, Anton and Usanov, Nikolay and Koutrouli, Mikaela and Ergen, Can and Palla, Giovanni and Krebs, Christian F. and Panzer, Ulf and Bonn, Stefan and Lobentanzer, Sebastian and Saez-Rodriguez, Julio and Puelles, Victor G.},
  year={2025},
  month=nov,
  language={en},
}
```

## Acknowledgments

- **Example Skill**: The included `single-cell-rna-qc` skill is adapted from [Anthropic's Life Sciences repository](https://github.com/anthropics/life-sciences)
- **Anthropic**: For developing Claude Skills and the Model Context Protocol
- **scverse®**: The scverse community ([scverse.org](https://scverse.org)) for best practices in single-cell analysis
- **BioContextAI Community**: For fostering open-source biomedical AI infrastructure

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

**Note**: While this software is open-source, individual skills may have their own licenses. Users are responsible for compliance with the licenses of any skills they use or distribute.

[uv]: https://github.com/astral-sh/uv
[issue tracker]: https://github.com/biocontext-ai/skill-to-mcp/issues
[tests]: https://github.com/biocontext-ai/skill-to-mcp/actions/workflows/test.yaml
[documentation]: https://skill-to-mcp.readthedocs.io
[changelog]: https://skill-to-mcp.readthedocs.io/en/latest/changelog.html
[api documentation]: https://skill-to-mcp.readthedocs.io/en/latest/api.html
[pypi]: https://pypi.org/project/skill-to-mcp
[registry]: https://biocontext.ai/registry
[source]: https://github.com/biocontext-ai/skill-to-mcp
