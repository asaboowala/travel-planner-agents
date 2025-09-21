import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.agents import Agent
from tools import activities_search_tool

print("activities_search_tool", activities_search_tool)

activities_agent = Agent(
    name="activities_agent",
    model="gemini-2.0-flash", 
    description="Provides activities information given the user's request to build a travel plan.",
    instruction="You are a helpful activities assistant. "
                "When the user asks for the activities information, "
                "use the 'activities_search_tool' toolkit to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the activities information clearly to help the user build a travel plan.",
    tools=[activities_search_tool], 
)


async def debug_list_mcp_tools():
    # ADK’s MCPToolset fetches schemas asynchronously
    tools = await activities_search_tool.get_tools(None)  # read-only context
    print("[MCP] Discovered tools:")
    for t in tools:
        print(f" - {t.name}: {getattr(t, 'description', '')}")

asyncio.get_event_loop().run_until_complete(debug_list_mcp_tools())