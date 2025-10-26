"""MCP tools for accessing Claude Skills from the skills directory."""

from pathlib import Path

from fastmcp import FastMCP

from skill_to_mcp.skill_parser import SkillParser


def register_skill_tools(mcp_server: FastMCP, skills_dir: str | Path) -> None:
    """Register skill tools with the MCP server.

    Parameters
    ----------
    mcp_server : FastMCP
        The FastMCP server instance to register tools with.
    skills_dir : str | Path
        Path to the directory containing skill subdirectories.
    """
    # Initialize the skill parser with the provided skills directory
    skill_parser = SkillParser(skills_dir)

    @mcp_server.tool()
    def get_available_skills() -> list[dict[str, str]]:
        """Get an overview of all available skills.

        This tool provides LLMs with a list of available skills and their use cases by parsing
        the frontmatter (YAML metadata) at the start of each SKILL.md file.

        LLMs should rely on this tool to discover what skills are available before requesting
        detailed skill information.

        Returns
        -------
        list[dict[str, str]]
            List of skill metadata dictionaries, each containing:
            - name: The skill identifier (lowercase, hyphens only)
            - description: When and how to use this skill
            - path: Location of the skill directory

        Examples
        --------
        >>> skills = get_available_skills()
        >>> print(skills[0]["name"])
        'single-cell-rna-qc'
        """
        skills = skill_parser.find_all_skills()
        return [skill.to_dict() for skill in skills]

    @mcp_server.tool()
    def get_skill_details(skill_name: str) -> dict[str, any]:
        """Get detailed information about a specific skill.

        This tool provides the full SKILL.md content and a recursive list of all files
        contained within the skill's directory. LLMs should use get_skill_related_file()
        to read the content of specific files.

        Parameters
        ----------
        skill_name : str
            The name of the skill (from get_available_skills).

        Returns
        -------
        dict[str, any]
            Dictionary containing:
            - skill_content: Full text of the SKILL.md file
            - files: List of relative file paths in the skill directory

        Raises
        ------
        ValueError
            If the skill is not found.

        Examples
        --------
        >>> details = get_skill_details("single-cell-rna-qc")
        >>> print(details["files"])
        ['SKILL.md', 'scripts/qc_analysis.py', ...]
        """
        try:
            skill_content = skill_parser.get_skill_content(skill_name)
            files = skill_parser.list_skill_files(skill_name, relative=True)

            return {
                "skill_content": skill_content,
                "files": files,
            }
        except ValueError as e:
            raise ValueError(f"Error getting skill details: {e}") from e

    @mcp_server.tool()
    def get_skill_related_file(skill_name: str, relative_path: str) -> str:
        """Read the content of a specific file within a skill directory.

        This tool returns the requested file based on a path relative to the skill's
        SKILL.md location. Use get_skill_details() first to see the list of available files.

        Parameters
        ----------
        skill_name : str
            The name of the skill.
        relative_path : str
            Path to the file relative to the skill directory (e.g., "scripts/qc_core.py").

        Returns
        -------
        str
            The content of the requested file.

        Raises
        ------
        ValueError
            If the skill or file is not found, or if the path is invalid.

        Examples
        --------
        >>> content = get_skill_related_file("single-cell-rna-qc", "scripts/qc_core.py")
        >>> print(len(content) > 0)
        True
        """
        try:
            return skill_parser.get_skill_file(skill_name, relative_path)
        except ValueError as e:
            raise ValueError(f"Error reading skill file: {e}") from e
