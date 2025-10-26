"""Skill parser module for processing SKILL.md files and skill directories."""

import re
from pathlib import Path
from typing import Any

import yaml


class SkillMetadata:
    """Represents metadata from a SKILL.md file."""

    def __init__(self, name: str, description: str, skill_path: Path):
        """Initialize skill metadata.

        Parameters
        ----------
        name : str
            Skill name from frontmatter.
        description : str
            Skill description from frontmatter.
        skill_path : Path
            Path to the directory containing the SKILL.md file.
        """
        self.name = name
        self.description = description
        self.skill_path = skill_path

    def to_dict(self) -> dict[str, str]:
        """Convert metadata to dictionary.

        Returns
        -------
        dict[str, str]
            Dictionary with name, description, and path.
        """
        return {
            "name": self.name,
            "description": self.description,
            "path": str(self.skill_path),
        }


class SkillParser:
    """Parser for Claude Skills following the SKILL.md format."""

    def __init__(self, skills_directory: Path | str = "skills"):
        """Initialize the skill parser.

        Parameters
        ----------
        skills_directory : Path | str
            Path to the directory containing skill subdirectories.
        """
        self.skills_directory = Path(skills_directory)
        if not self.skills_directory.exists():
            raise ValueError(f"Skills directory does not exist: {self.skills_directory}")

    def find_all_skills(self) -> list[SkillMetadata]:
        """Find all SKILL.md files and parse their metadata.

        Returns
        -------
        list[SkillMetadata]
            List of skill metadata objects.
        """
        skills = []
        for skill_md in self.skills_directory.rglob("SKILL.md"):
            try:
                metadata = self.parse_skill_metadata(skill_md)
                skills.append(metadata)
            except (ValueError, OSError) as e:
                # Log error but continue processing other skills
                print(f"Error parsing {skill_md}: {e}")
                continue
        return skills

    def parse_skill_metadata(self, skill_md_path: Path) -> SkillMetadata:
        """Parse frontmatter from a SKILL.md file.

        Parameters
        ----------
        skill_md_path : Path
            Path to the SKILL.md file.

        Returns
        -------
        SkillMetadata
            Parsed skill metadata.

        Raises
        ------
        ValueError
            If frontmatter is missing or invalid.
        """
        content = skill_md_path.read_text(encoding="utf-8")
        frontmatter = self._extract_frontmatter(content)

        # Validate required fields
        if "name" not in frontmatter:
            raise ValueError(f"Missing 'name' field in {skill_md_path}")
        if "description" not in frontmatter:
            raise ValueError(f"Missing 'description' field in {skill_md_path}")

        return SkillMetadata(
            name=frontmatter["name"],
            description=frontmatter["description"],
            skill_path=skill_md_path.parent,
        )

    def _extract_frontmatter(self, content: str) -> dict[str, Any]:
        """Extract YAML frontmatter from SKILL.md content.

        Parameters
        ----------
        content : str
            Full content of SKILL.md file.

        Returns
        -------
        dict[str, Any]
            Parsed frontmatter as dictionary.

        Raises
        ------
        ValueError
            If frontmatter is not found or invalid.
        """
        # Match frontmatter between --- delimiters at start of file
        pattern = r"^---\s*\n(.*?)\n---\s*\n"
        match = re.match(pattern, content, re.DOTALL)

        if not match:
            raise ValueError("No valid YAML frontmatter found")

        yaml_content = match.group(1)
        try:
            return yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in frontmatter: {e}") from e

    def get_skill_content(
        self, skill_name: str, return_type: str = "both"
    ) -> "str | dict[str, str]":
        """Get the full content of a SKILL.md file by skill name.

        Parameters
        ----------
        skill_name : str
            Name of the skill.
        return_type : str
            Type of data to return: "content", "file_path", or "both" (default).

        Returns
        -------
        str | dict[str, str]
            If return_type is "content": Full content of the SKILL.md file.
            If return_type is "file_path": Absolute path to the SKILL.md file.
            If return_type is "both": Dictionary with "content" and "file_path" keys.

        Raises
        ------
        ValueError
            If skill is not found or return_type is invalid.
        """
        if return_type not in ("content", "file_path", "both"):
            raise ValueError(f"Invalid return_type: {return_type}. Must be 'content', 'file_path', or 'both'")

        skills = self.find_all_skills()
        for skill in skills:
            if skill.name == skill_name:
                skill_md_path = skill.skill_path / "SKILL.md"

                if return_type == "content":
                    return skill_md_path.read_text(encoding="utf-8")
                elif return_type == "file_path":
                    return str(skill_md_path.resolve())
                else:  # both
                    return {
                        "content": skill_md_path.read_text(encoding="utf-8"),
                        "file_path": str(skill_md_path.resolve()),
                    }

        raise ValueError(f"Skill '{skill_name}' not found")

    def list_skill_files(self, skill_name: str, relative: bool = True) -> "list[str]":
        """List all files in a skill directory recursively.

        Parameters
        ----------
        skill_name : str
            Name of the skill.
        relative : bool
            If True, return paths relative to skill directory. Default: True.

        Returns
        -------
        list[str]
            List of file paths in the skill directory.

        Raises
        ------
        ValueError
            If skill is not found.
        """
        skills = self.find_all_skills()
        for skill in skills:
            if skill.name == skill_name:
                files = []
                for file_path in skill.skill_path.rglob("*"):
                    if file_path.is_file():
                        if relative:
                            rel_path = file_path.relative_to(skill.skill_path)
                            files.append(str(rel_path))
                        else:
                            files.append(str(file_path))
                return sorted(files)

        raise ValueError(f"Skill '{skill_name}' not found")

    def get_skill_file(
        self, skill_name: str, relative_path: str, return_type: str = "both"
    ) -> "str | dict[str, str]":
        """Get content of a specific file within a skill directory.

        Parameters
        ----------
        skill_name : str
            Name of the skill.
        relative_path : str
            Path relative to the skill directory.
        return_type : str
            Type of data to return: "content", "file_path", or "both" (default).

        Returns
        -------
        str | dict[str, str]
            If return_type is "content": Content of the requested file.
            If return_type is "file_path": Absolute path to the file.
            If return_type is "both": Dictionary with "content" and "file_path" keys.

        Raises
        ------
        ValueError
            If skill or file is not found, if path is invalid, or if return_type is invalid.
        """
        if return_type not in ("content", "file_path", "both"):
            raise ValueError(f"Invalid return_type: {return_type}. Must be 'content', 'file_path', or 'both'")

        skills = self.find_all_skills()
        for skill in skills:
            if skill.name == skill_name:
                # Validate path to prevent directory traversal
                file_path = (skill.skill_path / relative_path).resolve()
                if not file_path.is_relative_to(skill.skill_path.resolve()):
                    raise ValueError("Invalid path: attempting to access files outside skill directory")

                if not file_path.exists():
                    raise ValueError(f"File not found: {relative_path}")

                if not file_path.is_file():
                    raise ValueError(f"Path is not a file: {relative_path}")

                if return_type == "content":
                    return file_path.read_text(encoding="utf-8")
                elif return_type == "file_path":
                    return str(file_path)
                else:  # both
                    return {
                        "content": file_path.read_text(encoding="utf-8"),
                        "file_path": str(file_path),
                    }

        raise ValueError(f"Skill '{skill_name}' not found")
