import os
import uvicorn
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from flights_agent import flights_agent
from executor import ADKRunnerExecutor
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")


PORT = int(os.getenv("PORT", "10001"))
PUBLIC_URL = os.getenv("PUBLIC_URL", f"http://localhost:{PORT}")

# 1. Create a Runner for the ADK agent
runner = Runner(
        app_name=flights_agent.name,
        agent=flights_agent,
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
    )

# 2. Create an AgentCard for the ADK agent (contains capabilities, skills, etc.)
capabilities = AgentCapabilities(streaming=True)
skill = AgentSkill(
    id="flights_search",
    name="Search & summarize flights",
    description="Given city/dates/budget, finds flights via MCP and returns a tidy shortlist.",
    tags=["travel", "flights"],
    examples=["Find 3 flights froßm Tokyo to London for Nov 10 to 13"],
)
agent_card = AgentCard(
    name="Flights Planner Agent",
    description="This flights agent helps you search for flights and provide flight information.",
    url=f"{PUBLIC_URL}",
    version="1.0.0",
    defaultInputModes=["text", "text/plain"],
    defaultOutputModes=["text", "text/plain"],
    capabilities=capabilities,
    skills=[skill],
)

# 3) Wire the executor into the default handler and start the Starlette app
request_handler = DefaultRequestHandler(
    agent_executor=ADKRunnerExecutor(runner),
    task_store=InMemoryTaskStore(),
)
server = A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)
app = server.build()

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
    except Exception as e:
        print(f"An error occurred during server startup: {e}")
        exit(1)
    