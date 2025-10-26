from pathlib import Path

from fastmcp import FastMCP


def initialize_mcp(skills_dir: str | Path) -> FastMCP:
    """Initialize the FastMCP server with a specific skills directory.

    Parameters
    ----------
    skills_dir : str | Path
        Path to the directory containing skill subdirectories with SKILL.md files.

    Returns
    -------
    FastMCP
        Initialized MCP server with skill tools registered.
    """
    mcp_server = FastMCP(
        name="skill-to-mcp",
        instructions=(
            "Convert AI Skills (following Claude Skills format) into MCP server resources. "
            "This server provides access to skills stored in SKILL.md files, allowing LLMs to "
            "discover and use specialized knowledge and workflows. Use get_available_skills to "
            "see what's available, then get_skill_details to access specific skills."
        ),
        on_duplicate_tools="error",
    )

    # Register tools with the configured skills directory
    from skill_to_mcp.tools._skills import register_skill_tools

    register_skill_tools(mcp_server, skills_dir)

    return mcp_server


# Default instance for testing (uses package's skills directory)
mcp: FastMCP | None = None
