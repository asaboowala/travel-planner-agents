import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StdioServerParameters


# --- Flights MCP (Python stdio via uv) ---
# Update this path to your local clone
FLIGHTS_DIR = os.path.expanduser("/Users/alishasaboowala/Desktop/GenAI_Projects/Medium/google-adk/flights-mcp")
flights_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uv",
            args=["--directory", FLIGHTS_DIR, "run", "flights-mcp"],
            env={"DUFFEL_API_KEY_LIVE": os.environ.get("DUFFEL_API_KEY_LIVE", "")},
        )
    )
)
