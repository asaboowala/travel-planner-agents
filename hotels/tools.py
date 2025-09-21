import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StdioServerParameters
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# --- Hotels MCP (Python stdio via npx) ---
HOTELS_CMD = os.getenv("HOTELS_MCP_CMD", "npx")
HOTELS_ARGS = os.getenv("HOTELS_MCP_ARGS", "jinko-mcp-dev@latest").split()
hotels_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=HOTELS_CMD,          
            args=HOTELS_ARGS,          
        )
    ),
)