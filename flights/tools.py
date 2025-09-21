import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StdioServerParameters
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# --- Flights MCP (Python stdio via uv) ---
FLIGHTS_DIR = os.path.expanduser(os.getenv("FLIGHTS_MCP_DIR"))
flights_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=["--directory", FLIGHTS_DIR, "run", "flights-mcp"],
            env={"DUFFEL_API_KEY_LIVE": os.environ.get("DUFFEL_API_KEY_LIVE", "")},
        )
    )
)
