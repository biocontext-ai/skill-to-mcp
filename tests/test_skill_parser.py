"""Tests for skill parser module."""

from pathlib import Path

import pytest

from skill_to_mcp.skill_parser import SkillMetadata, SkillParser


@pytest.fixture
def skills_dir():
    """Get the skills directory path."""
    return Path(__file__).parent.parent / "skills"


@pytest.fixture
def parser(skills_dir):
    """Create a SkillParser instance."""
    return SkillParser(skills_dir)


def test_skills_directory_exists(skills_dir):
    """Test that skills directory exists."""
    assert skills_dir.exists()
    assert skills_dir.is_dir()


def test_parser_initialization(skills_dir):
    """Test SkillParser initialization."""
    parser = SkillParser(skills_dir)
    assert parser.skills_directory == skills_dir


def test_parser_invalid_directory():
    """Test SkillParser with invalid directory."""
    with pytest.raises(ValueError, match="Skills directory does not exist"):
        SkillParser("/nonexistent/path")


def test_find_all_skills(parser):
    """Test finding all skills."""
    skills = parser.find_all_skills()
    assert len(skills) > 0
    assert all(isinstance(skill, SkillMetadata) for skill in skills)


def test_skill_metadata_structure(parser):
    """Test that skill metadata has required fields."""
    skills = parser.find_all_skills()
    for skill in skills:
        assert hasattr(skill, "name")
        assert hasattr(skill, "description")
        assert hasattr(skill, "skill_path")
        assert isinstance(skill.name, str)
        assert isinstance(skill.description, str)
        assert isinstance(skill.skill_path, Path)


def test_skill_metadata_to_dict(parser):
    """Test converting skill metadata to dictionary."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_dict = skills[0].to_dict()
        assert "name" in skill_dict
        assert "description" in skill_dict
        assert "path" in skill_dict


def test_get_skill_content(parser):
    """Test getting skill content with return_type='content'."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        content = parser.get_skill_content(skill_name, return_type="content")
        assert isinstance(content, str)
        assert len(content) > 0
        # Should contain frontmatter
        assert "---" in content
        assert f"name: {skill_name}" in content


def test_get_skill_content_both(parser):
    """Test getting skill content with return_type='both' (default)."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        result = parser.get_skill_content(skill_name, return_type="both")
        assert isinstance(result, dict)
        assert "content" in result
        assert "file_path" in result
        assert isinstance(result["content"], str)
        assert isinstance(result["file_path"], str)
        assert len(result["content"]) > 0
        assert result["file_path"].endswith("SKILL.md")


def test_get_skill_content_file_path(parser):
    """Test getting skill content with return_type='file_path'."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        file_path = parser.get_skill_content(skill_name, return_type="file_path")
        assert isinstance(file_path, str)
        assert file_path.endswith("SKILL.md")
        assert Path(file_path).exists()


def test_get_skill_content_invalid_return_type(parser):
    """Test getting skill content with invalid return_type."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        with pytest.raises(ValueError, match="Invalid return_type"):
            parser.get_skill_content(skill_name, return_type="invalid")


def test_get_skill_content_not_found(parser):
    """Test getting content for non-existent skill."""
    with pytest.raises(ValueError, match="Skill .* not found"):
        parser.get_skill_content("nonexistent-skill")


def test_list_skill_files(parser):
    """Test listing files in a skill directory."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        files = parser.list_skill_files(skill_name, relative=True)
        assert isinstance(files, list)
        assert len(files) > 0
        # Should include SKILL.md
        assert "SKILL.md" in files
        # All paths should be strings
        assert all(isinstance(f, str) for f in files)


def test_list_skill_files_absolute(parser):
    """Test listing files with absolute paths."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        files = parser.list_skill_files(skill_name, relative=False)
        assert isinstance(files, list)
        # Should be absolute paths
        assert all(Path(f).is_absolute() for f in files)


def test_list_skill_files_not_found(parser):
    """Test listing files for non-existent skill."""
    with pytest.raises(ValueError, match="Skill .* not found"):
        parser.list_skill_files("nonexistent-skill")


def test_get_skill_file(parser):
    """Test getting content of a skill file with return_type='content'."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        # Get SKILL.md content
        content = parser.get_skill_file(skill_name, "SKILL.md", return_type="content")
        assert isinstance(content, str)
        assert len(content) > 0


def test_get_skill_file_both(parser):
    """Test getting skill file with return_type='both' (default)."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        result = parser.get_skill_file(skill_name, "SKILL.md", return_type="both")
        assert isinstance(result, dict)
        assert "content" in result
        assert "file_path" in result
        assert isinstance(result["content"], str)
        assert isinstance(result["file_path"], str)
        assert len(result["content"]) > 0
        assert result["file_path"].endswith("SKILL.md")


def test_get_skill_file_file_path(parser):
    """Test getting skill file with return_type='file_path'."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        file_path = parser.get_skill_file(skill_name, "SKILL.md", return_type="file_path")
        assert isinstance(file_path, str)
        assert file_path.endswith("SKILL.md")
        assert Path(file_path).exists()


def test_get_skill_file_invalid_return_type(parser):
    """Test getting skill file with invalid return_type."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        with pytest.raises(ValueError, match="Invalid return_type"):
            parser.get_skill_file(skill_name, "SKILL.md", return_type="invalid")


def test_get_skill_file_not_found(parser):
    """Test getting non-existent file."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        with pytest.raises(ValueError, match="File not found"):
            parser.get_skill_file(skill_name, "nonexistent.txt")


def test_get_skill_file_directory_traversal(parser):
    """Test that directory traversal is prevented."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        with pytest.raises(ValueError, match="Invalid path"):
            parser.get_skill_file(skill_name, "../../../etc/passwd")


def test_get_skill_file_is_directory(parser):
    """Test getting a directory instead of a file."""
    skills = parser.find_all_skills()
    if len(skills) > 0:
        skill_name = skills[0].name
        # Find a directory if one exists
        skill_path = skills[0].skill_path
        subdirs = [d for d in skill_path.iterdir() if d.is_dir()]
        if subdirs:
            subdir_name = subdirs[0].name
            with pytest.raises(ValueError, match="Path is not a file"):
                parser.get_skill_file(skill_name, subdir_name)


def test_parse_skill_metadata_single_cell_rna_qc(parser, skills_dir):
    """Test parsing the single-cell-rna-qc skill specifically."""
    skill_md = skills_dir / "single-cell-rna-qc" / "SKILL.md"
    if skill_md.exists():
        metadata = parser.parse_skill_metadata(skill_md)
        assert metadata.name == "single-cell-rna-qc"
        assert len(metadata.description) > 0
        assert metadata.skill_path == skill_md.parent


def test_frontmatter_validation(parser, tmp_path):
    """Test frontmatter validation with invalid SKILL.md files."""
    # Create a temporary skill directory
    temp_skill = tmp_path / "test-skill"
    temp_skill.mkdir()

    # Test missing frontmatter
    skill_md = temp_skill / "SKILL.md"
    skill_md.write_text("# No frontmatter here")
    with pytest.raises(ValueError, match="No valid YAML frontmatter found"):
        parser.parse_skill_metadata(skill_md)

    # Test missing name field
    skill_md.write_text("---\ndescription: Test\n---\n# Content")
    with pytest.raises(ValueError, match="Missing 'name' field"):
        parser.parse_skill_metadata(skill_md)

    # Test missing description field
    skill_md.write_text("---\nname: test\n---\n# Content")
    with pytest.raises(ValueError, match="Missing 'description' field"):
        parser.parse_skill_metadata(skill_md)

    # Test invalid YAML syntax (tabs in YAML are not allowed)
    skill_md.write_text("---\nname: test\ndescription: test\n\tinvalid: yaml\n---\n# Content")
    with pytest.raises(ValueError, match="Invalid YAML"):
        parser.parse_skill_metadata(skill_md)
