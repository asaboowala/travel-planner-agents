# executor_adk.py
from typing import AsyncGenerator, Optional

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import get_message_text, new_agent_text_message
from a2a.types import (
    CancelTaskRequest, CancelTaskResponse, JSONRPCErrorResponse,
    UnsupportedOperationError, Task,
)

from google.genai import types as genai_types
from google.adk.runners import Runner

class ADKRunnerExecutor(AgentExecutor):
    """Bridge A2A -> ADK Runner: read A2A Message, run ADK once, reply as A2A Message."""

    def __init__(self, runner: Runner, user_id: str = "a2a_user"):
        self.runner = runner
        self.user_id = user_id

    async def _ensure_session(self, session_id: str):
        # Create the session if it doesn't exist (safe to call repeatedly)
        await self.runner.session_service.create_session(
            app_name=self.runner.app_name,
            user_id=self.user_id,
            session_id=session_id,
        )

    async def _run_once(self, user_text: str, session_id: str) -> str:
        content = genai_types.Content(role="user", parts=[genai_types.Part(text=user_text)])
        final_text = ""
        async for event in self.runner.run_async(
            user_id=self.user_id,
            session_id=session_id,
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    for p in event.content.parts:
                        if getattr(p, "text", None):
                            final_text += p.text
                break
        return (final_text or "No response.").strip()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        try:
            # 1) Read the user's message safely from RequestContext
            if context.message is None:
                await event_queue.enqueue_event(
                    new_agent_text_message("No message provided.", context_id=context.context_id, task_id=context.task_id)
                )
                return

            user_text = get_message_text(context.message).strip()
            # Prefer the message's context_id so multi-turn threads keep history
            session_id = (context.message.context_id or context.context_id or "session_flights_a2a")
            await self._ensure_session(session_id)

            # 2) Run your ADK agent once (non-streaming demo)
            final_text = await self._run_once(user_text, session_id)

            # 3) Emit a single A2A Message back to the client
            await event_queue.enqueue_event(
                new_agent_text_message(
                    final_text,
                    context_id=context.message.context_id or context.context_id,
                    task_id=context.task_id,
                )
            )
        finally:
            # Close the queue so SSE/handler can finish cleanly
            await event_queue.close()

    async def cancel(self, request: CancelTaskRequest, task: Task) -> CancelTaskResponse:
        # Minimal demo: no cancellable tasks
        return CancelTaskResponse(
            root=JSONRPCErrorResponse(id=request.id, error=UnsupportedOperationError())
        )