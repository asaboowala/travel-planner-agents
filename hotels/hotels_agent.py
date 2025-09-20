import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.agents import Agent
from tools import hotels_toolset

print("hotels_toolset", hotels_toolset)

hotels_agent = Agent(
    name="hotels_agent",
    model="gemini-2.0-flash", 
    description="Provides hotel booking information given the user's request.",
    instruction="You are a helpful hotel booking assistant. "
                "When the user asks for the hotel booking information, "
                "use the 'hotels_toolset' toolkit to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the hotel booking information clearly.",
    tools=[hotels_toolset], 
)



async def debug_list_mcp_tools():
    # ADK’s MCPToolset fetches schemas asynchronously
    tools = await hotels_toolset.get_tools(None)  # read-only context
    print("[MCP] Discovered tools:")
    for t in tools:
        print(f" - {t.name}: {getattr(t, 'description', '')}")

asyncio.get_event_loop().run_until_complete(debug_list_mcp_tools())