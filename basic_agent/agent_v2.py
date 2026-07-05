import logging

from livekit import agents
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    TurnHandlingOptions,
    MetricsCollectedEvent,
    metrics,
    room_io
)
from livekit.agents.beta import EndCallTool
from livekit.plugins import openai, cartesia
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

class GenericAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=("You are a conversational agent you can talk with user on any topic that user initiate with you."
                          "You dont have any boundaries or restrictions on the topics that you can speak. "
                          "but the conversation should be very polite and the topic oriented and topic bounded."),
            tools=[EndCallTool()]
        )

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions="Greet the user and introduce yourself.")

server = AgentSession()

async def entrypoint(ctx: JobContext) -> None:
    # each log entry will include these fields
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    session: AgentSession = AgentSession(
        stt=cartesia.STT(),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(),
        turn_handling=TurnHandlingOptions(
            interruption={
                # sometimes background noise could interrupt the agent session, these are considered false positive
                # interruptions when it's detected, you may resume the agent's speech
                "resume_false_interruption": True,
                "false_interruption_timeout": 1.0,
            },
            # allow the LLM to generate a response while waiting for the end of turn
            preemptive_generation={"enabled": True, "max_retries": 3},
        )
    )

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent) -> None:
        if ev.metrics.type == "stt_metrics":
            return
        metrics.log_metrics(ev.metrics)

    async def log_usage():
        logger.info(f"Usage: {session.usage}")

    # shutdown callbacks are triggered when the session is over
    ctx.add_shutdown_callback(log_usage)

    await session.start(
        agent=GenericAgent(),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                # uncomment to enable the Krisp BVC noise cancellation
                # noise_cancellation=noise_cancellation.BVC(),
            ),
        ),
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint)) # agent_name="<YOUR NAME>"