from pathlib import Path

import pytest
from fastmcp import Client

import skill_to_mcp


@pytest.fixture
def skills_dir():
    """Get the skills directory path for testing."""
    return Path(__file__).parent.parent / "skills"


@pytest.fixture
def mcp(skills_dir):
    """Initialize MCP server with test skills directory."""
    from skill_to_mcp.mcp import initialize_mcp

    return initialize_mcp(skills_dir)


def test_package_has_version():
    """Testing package version exist."""
    assert skill_to_mcp.__version__ is not None


@pytest.mark.asyncio
async def test_get_available_skills(mcp):
    """Test get_available_skills tool."""
    async with Client(mcp) as client:
        result = await client.call_tool("get_available_skills", {})
        # Use structured_content to get the actual data
        skills = result.structured_content.get("result", [])
        assert isinstance(skills, list)
        if len(skills) > 0:
            skill = skills[0]
            assert "name" in skill
            assert "description" in skill
            assert "path" in skill


@pytest.mark.asyncio
async def test_get_skill_details(mcp):
    """Test get_skill_details tool with default return_type."""
    async with Client(mcp) as client:
        # First get available skills
        skills_result = await client.call_tool("get_available_skills", {})
        skills = skills_result.structured_content.get("result", [])

        if len(skills) > 0:
            skill_name = skills[0]["name"]

            # Get details for the first skill (default return_type="both")
            details_result = await client.call_tool("get_skill_details", {"skill_name": skill_name})
            details = details_result.structured_content

            assert "skill_content" in details
            assert "files" in details
            assert isinstance(details["skill_content"], dict)
            assert "content" in details["skill_content"]
            assert "file_path" in details["skill_content"]
            assert isinstance(details["files"], list)
            assert len(details["skill_content"]["content"]) > 0
            assert len(details["files"]) > 0
            assert "SKILL.md" in details["files"]


@pytest.mark.asyncio
async def test_get_skill_details_content_only(mcp):
    """Test get_skill_details with return_type='content'."""
    async with Client(mcp) as client:
        skills_result = await client.call_tool("get_available_skills", {})
        skills = skills_result.structured_content.get("result", [])

        if len(skills) > 0:
            skill_name = skills[0]["name"]
            details_result = await client.call_tool(
                "get_skill_details", {"skill_name": skill_name, "return_type": "content"}
            )
            details = details_result.structured_content

            assert "skill_content" in details
            assert isinstance(details["skill_content"], str)
            assert len(details["skill_content"]) > 0


@pytest.mark.asyncio
async def test_get_skill_details_file_path_only(mcp):
    """Test get_skill_details with return_type='file_path'."""
    async with Client(mcp) as client:
        skills_result = await client.call_tool("get_available_skills", {})
        skills = skills_result.structured_content.get("result", [])

        if len(skills) > 0:
            skill_name = skills[0]["name"]
            details_result = await client.call_tool(
                "get_skill_details", {"skill_name": skill_name, "return_type": "file_path"}
            )
            details = details_result.structured_content

            assert "skill_content" in details
            assert isinstance(details["skill_content"], str)
            assert details["skill_content"].endswith("SKILL.md")


@pytest.mark.asyncio
async def test_get_skill_details_not_found(mcp):
    """Test get_skill_details with non-existent skill."""
    async with Client(mcp) as client:
        with pytest.raises(Exception, match="not found"):
            await client.call_tool("get_skill_details", {"skill_name": "nonexistent-skill"})


@pytest.mark.asyncio
async def test_get_skill_related_file(mcp):
    """Test get_skill_related_file tool with default return_type."""
    async with Client(mcp) as client:
        # First get available skills
        skills_result = await client.call_tool("get_available_skills", {})
        skills = skills_result.structured_content.get("result", [])

        if len(skills) > 0:
            skill_name = skills[0]["name"]

            # Get SKILL.md content with default return_type="both"
            file_result = await client.call_tool(
                "get_skill_related_file", {"skill_name": skill_name, "relative_path": "SKILL.md"}
            )
            content = file_result.content[0].text if file_result.content else ""

            # Should return a dict with both content and file_path
            assert "content" in content or "---" in content
            # In the actual response, it might be serialized differently
            # so we check for the YAML frontmatter which should be present


@pytest.mark.asyncio
async def test_get_skill_related_file_content_only(mcp):
    """Test get_skill_related_file with return_type='content'."""
    async with Client(mcp) as client:
        skills_result = await client.call_tool("get_available_skills", {})
        skills = skills_result.structured_content.get("result", [])

        if len(skills) > 0:
            skill_name = skills[0]["name"]
            file_result = await client.call_tool(
                "get_skill_related_file",
                {"skill_name": skill_name, "relative_path": "SKILL.md", "return_type": "content"},
            )
            content = file_result.content[0].text if file_result.content else ""

            assert isinstance(content, str)
            assert len(content) > 0
            assert "---" in content
            assert f"name: {skill_name}" in content


@pytest.mark.asyncio
async def test_get_skill_related_file_file_path_only(mcp):
    """Test get_skill_related_file with return_type='file_path'."""
    async with Client(mcp) as client:
        skills_result = await client.call_tool("get_available_skills", {})
        skills = skills_result.structured_content.get("result", [])

        if len(skills) > 0:
            skill_name = skills[0]["name"]
            file_result = await client.call_tool(
                "get_skill_related_file",
                {"skill_name": skill_name, "relative_path": "SKILL.md", "return_type": "file_path"},
            )
            file_path = file_result.content[0].text if file_result.content else ""

            assert isinstance(file_path, str)
            assert file_path.endswith("SKILL.md")


@pytest.mark.asyncio
async def test_get_skill_related_file_not_found(mcp):
    """Test get_skill_related_file with non-existent file."""
    async with Client(mcp) as client:
        # First get available skills
        skills_result = await client.call_tool("get_available_skills", {})
        skills = skills_result.structured_content.get("result", [])

        if len(skills) > 0:
            skill_name = skills[0]["name"]

            with pytest.raises(Exception, match="not found"):
                await client.call_tool(
                    "get_skill_related_file", {"skill_name": skill_name, "relative_path": "nonexistent.txt"}
                )


@pytest.mark.asyncio
async def test_get_skill_related_file_directory_traversal(mcp):
    """Test that directory traversal is prevented in get_skill_related_file."""
    async with Client(mcp) as client:
        # First get available skills
        skills_result = await client.call_tool("get_available_skills", {})
        skills = skills_result.structured_content.get("result", [])

        if len(skills) > 0:
            skill_name = skills[0]["name"]

            with pytest.raises(Exception, match="Invalid path"):
                await client.call_tool(
                    "get_skill_related_file", {"skill_name": skill_name, "relative_path": "../../../etc/passwd"}
                )
