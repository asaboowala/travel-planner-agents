from google.adk.agents import Agent
from tools import flights_toolset

print("flights_toolset", flights_toolset)

flights_agent = Agent(
    name="flights_agent",
    model="gemini-2.0-flash", 
    description="Provides flight information given the user's request.",
    instruction="You are a helpful flight assistant. "
                "When the user asks for the flight information, "
                "use the 'flights_toolset' toolkit to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the flight information clearly.",
    tools=[flights_toolset], 
)

import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

async def debug_list_mcp_tools():
    # ADK’s MCPToolset fetches schemas asynchronously
    tools = await flights_toolset.get_tools(None)  # read-only context
    print("[MCP] Discovered tools:")
    for t in tools:
        print(f" - {t.name}: {getattr(t, 'description', '')}")

asyncio.get_event_loop().run_until_complete(debug_list_mcp_tools())