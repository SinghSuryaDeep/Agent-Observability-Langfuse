

import asyncio
import logging
import os
import sys
import traceback
from typing import Any
from dotenv import load_dotenv
from beeai_framework.agents import AgentExecutionConfig
from beeai_framework.agents.react import ReActAgent, ReActAgentRunOutput
from beeai_framework.emitter import EmitterOptions, EventMeta
from beeai_framework.errors import FrameworkError
from beeai_framework.logger import Logger
from beeai_framework.memory import TokenMemory
from beeai_framework.tools import AnyTool
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.tools.weather import OpenMeteoTool
from beeai_framework.adapters.watsonx import WatsonxChatModel
from beeio import ConsoleReader
from openinference.instrumentation.beeai import BeeAIInstrumentor
from langfuse import get_client, observe

class Config:
    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.model_id = os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-3-8b-instruct")
        self.url = os.getenv("WATSONX_URL")
load_dotenv()

langfuse = get_client()
assert langfuse.auth_check(), "Langfuse auth failed - check your keys ✋"

BeeAIInstrumentor().instrument()
logger = Logger("app", level=logging.DEBUG)
reader = ConsoleReader()


def create_agent(config: Config) -> ReActAgent:
    """Create and configure the agent with Watsonx and tools."""

    llm = WatsonxChatModel(
        api_key=config.api_key,
        project_id=config.project_id,
        model=config.model_id,
        url=config.url,
    )

    tools: list[AnyTool] = [
        WikipediaTool(),
        OpenMeteoTool(),
        DuckDuckGoSearchTool(),
    ]

    memory = TokenMemory(llm=llm)

    return ReActAgent(llm=llm, tools=tools, memory=memory)


def process_agent_events(data: Any, event: EventMeta) -> None:
    """Log agent lifecycle events."""
    if event.name == "error":
        reader.write("Agent 🤖 : ", FrameworkError.ensure(data.error).explain())
    elif event.name == "retry":
        reader.write("Agent 🤖 : ", "retrying the action...")
    elif event.name == "update":
        reader.write(f"Agent({data.update.key}) 🤖 : ", data.update.parsed_value)
    elif event.name == "start":
        reader.write("Agent 🤖 : ", "starting new iteration")
    elif event.name == "success":
        reader.write("Agent 🤖 : ", "success")


@observe()
async def run_agent(agent: ReActAgent, prompt: str) -> ReActAgentRunOutput:
    """Run the agent on the user's prompt."""
    response = await agent.run(
        prompt=prompt,
        execution=AgentExecutionConfig(
            max_retries_per_step=3,
            total_max_retries=10,
            max_iterations=20,
        ),
    ).on("*", process_agent_events, EmitterOptions(match_nested=False))

    return response


async def main() -> None:
    """Main interaction loop."""
    config = Config()
    agent = create_agent(config)

    reader.write("🛠️ System: ", "Agent initialized with Wikipedia, DuckDuckGo, and Weather tools.")
    reader.write("🛠️ System: ", "\n🔁 Now you can ask your own questions.")

    for prompt in reader:
        response = await run_agent(agent=agent, prompt=prompt)
        reader.write("Agent 🤖 : ", response.result.text)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
