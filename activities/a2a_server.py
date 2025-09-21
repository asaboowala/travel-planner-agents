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

from activities_agent import activities_agent
from executor import ADKRunnerExecutor
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")


PORT = int(os.getenv("PORT", "10003"))
PUBLIC_URL = os.getenv("PUBLIC_URL", f"http://localhost:{PORT}")

# 1. Create a Runner for the ADK agent
runner = Runner(
        app_name=activities_agent.name,
        agent=activities_agent,
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
    )

# 2. Create an AgentCard for the ADK agent (contains capabilities, skills, etc.)
capabilities = AgentCapabilities(streaming=True)
skill = AgentSkill(
    id="activities_search",
    name="Search & summarize activities",
    description="Given a city, finds activities and returns an itinerary.",
    tags=["travel", "activities"],
    examples=["Make a travel plan for Tokyo"],
)
agent_card = AgentCard(
    name="Activities Planner Agent",
    description="This activities agent helps you search for activities and provide activities information to help the user build a travel plan.",
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
    