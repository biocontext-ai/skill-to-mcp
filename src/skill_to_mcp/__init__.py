from importlib.metadata import version

from skill_to_mcp.main import run_app
from skill_to_mcp.mcp import mcp

__version__ = version("skill_to_mcp")

__all__ = ["mcp", "run_app", "__version__"]


if __name__ == "__main__":
    run_app()
