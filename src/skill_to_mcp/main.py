import enum
import logging
import sys

import click

from .tools import *  # noqa: F403 import all tools to register them


class EnvironmentType(enum.Enum):
    """Enum to define environment type."""

    PRODUCTION = enum.auto()
    DEVELOPMENT = enum.auto()


@click.command(name="run")
@click.option(
    "-t",
    "--transport",
    "transport",
    type=str,
    help="MCP transport option. Defaults to 'stdio'.",
    default="stdio",
    envvar="MCP_TRANSPORT",
)
@click.option(
    "-p",
    "--port",
    "port",
    type=int,
    help="Port of MCP server. Defaults to '8000'",
    default=8000,
    envvar="MCP_PORT",
    required=False,
)
@click.option(
    "-h",
    "--host",
    "hostname",
    type=str,
    help="Hostname of MCP server. Defaults to '0.0.0.0'",
    default="0.0.0.0",
    envvar="MCP_HOSTNAME",
    required=False,
)
@click.option("-v", "--version", "version", is_flag=True, help="Get version of package.")
@click.option(
    "-e",
    "--env",
    "environment",
    type=click.Choice(["development", "production"], case_sensitive=False),
    default="development",
    envvar="MCP_ENVIRONMENT",
    help="MCP server environment. Defaults to 'development'.",
)
@click.option(
    "-s",
    "--skills-dir",
    "skills_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Path to skills directory containing SKILL.md files.",
    envvar="SKILLS_DIR",
    required=False,
)
def run_app(
    transport: str = "stdio",
    port: int = 8000,
    hostname: str = "0.0.0.0",
    environment: str = "development",
    version: bool = False,
    skills_dir: str | None = None,
):
    """Run the MCP server "skill-to-mcp".

    Convert AI Skills (following Claude Skills format) into MCP server resources.
    This server exposes skills as MCP tools, allowing LLM applications to discover and access
    specialized knowledge and workflows stored in SKILL.md files.

    Configuration options:
    - Skills directory: Set via "-s/--skills-dir" or SKILLS_DIR environment variable (required)
    - Transport: Set via "-t/--transport" or MCP_TRANSPORT environment variable (default: "stdio")
    - Port: Set via "-p/--port" or MCP_PORT environment variable (default: 8000)
    - Hostname: Set via "-h/--host" or MCP_HOSTNAME environment variable (default: "0.0.0.0")
    - Environment: Set via "-e/--env" or MCP_ENVIRONMENT environment variable (default: "development")
    """
    if version is True:
        from skill_to_mcp import __version__

        click.echo(__version__)
        sys.exit(0)

    # Validate skills directory
    if not skills_dir:
        click.echo(
            "Error: Skills directory is required. Set via --skills-dir or SKILLS_DIR environment variable.", err=True
        )
        sys.exit(1)

    logger = logging.getLogger(__name__)
    logger.info(f"Using skills directory: {skills_dir}")

    # Initialize MCP server with skills directory
    from skill_to_mcp.mcp import initialize_mcp

    mcp = initialize_mcp(skills_dir)

    if environment == "development":
        logger.info("Starting MCP server (DEVELOPMENT mode)")
        if transport == "http":
            mcp.run(transport=transport, port=port, host=hostname)
        else:
            mcp.run(transport=transport)
    else:
        raise NotImplementedError()
        # logger.info("Starting Starlette app with Uvicorn in PRODUCTION mode.")
        # uvicorn.run(app, host=hostname, port=port)


if __name__ == "__main__":
    run_app()
