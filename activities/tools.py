import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StdioServerParameters
from dotenv import load_dotenv, find_dotenv
from langchain_tavily import TavilySearch

load_dotenv(find_dotenv())

activities_search_tool = TavilySearch(
    max_results=10, 
    topic="general", 
    include_images=True, 
    search_depth="advanced"
)