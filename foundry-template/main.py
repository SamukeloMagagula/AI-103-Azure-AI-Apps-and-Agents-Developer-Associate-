# Copyright (c) Microsoft. All rights reserved.
"""
Microsoft Foundry agent — minimal Agent Framework scaffold.

This is the `foundry-template` branch of the AI-103 study repo. It stands
up a single agent, attaches one locally-implemented tool (`get_weather`),
and serves it over the Foundry Responses hosting layer on port 8088.

AI-103 mapping
--------------
Objective: "Build agents by using Foundry — define agent roles, goals,
conversation-tracking approach, and tool schemas." (section weight: 30-35%)

Three Foundry objects to recognise when reading this file
    * Agent    — persona + model + tools + instructions (defined below).
    * Thread   — conversation memory; created by the hosting layer per request.
    * Run      — one execution of an agent against a thread; also managed by
                 the hosting layer when you use ResponsesHostServer.

Authentication
--------------
Uses `DefaultAzureCredential`, which walks a credential chain:
  1. Environment variables (AZURE_CLIENT_ID / _SECRET / _TENANT_ID)
  2. Workload identity / managed identity (in Azure Container Apps, etc.)
  3. `az login` token (local dev)
  4. Visual Studio / Visual Studio Code sign-in
The code never sees an API key — this is the keyless pattern the exam
prefers. Grant the identity the role `Cognitive Services OpenAI User`
on the target Azure OpenAI resource, or `Azure AI Developer` on the
Foundry project.
"""

import os
from random import randint

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from pydantic import Field
from typing_extensions import Annotated

# Pull FOUNDRY_PROJECT_ENDPOINT + AZURE_AI_MODEL_DEPLOYMENT_NAME from `.env`.
# In production (Container Apps / App Service) these should come from app
# settings instead — `.env` is for local dev only and is gitignored.
load_dotenv()


# ---------------------------------------------------------------------------
# Tool definition
# ---------------------------------------------------------------------------
# `@tool(...)` turns this Python function into a callable the agent can invoke.
# Full type hints (`Annotated[..., Field(description=...)]`) are mandatory —
# the Agent Framework introspects them to build the JSON Schema the LLM
# sees, so a missing hint means the model can't fill that parameter.
#
# `approval_mode="never_require"` lets the agent call this tool without a
# human approval step. For anything with real-world side effects (send_email,
# run_sql, execute_payment), use `approval_mode="always_require"` instead —
# the run will then pause in `requires_action` until an operator approves.
@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    # Fake implementation so the template runs without a real weather API.
    # Swap this out for a requests.get(...) call in a real deployment.
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return (
        f"The weather in {location} is {conditions[randint(0, 3)]} "
        f"with a high of {randint(10, 30)}°C."
    )


# ---------------------------------------------------------------------------
# Agent + server bootstrap
# ---------------------------------------------------------------------------
def main() -> None:
    # Chat client wired to a Foundry project. `model=` takes the DEPLOYMENT
    # NAME you chose in the Foundry portal, not the model id (gpt-4o-mini etc.)
    # — this is one of the classic AI-103 traps.
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )

    # Build the agent. `instructions` is the system prompt — keep it tight.
    # `tools=[...]` is where you register everything the agent can call;
    # see day2_genai_agents/04_agent_tools.py in the main branch for the
    # full catalog (file_search, azure_ai_search, content_understanding,
    # openapi, bing_grounding, code_interpreter, and plain function tools).
    agent = Agent(
        client=client,
        instructions="You are a friendly assistant. Keep your answers brief.",
        tools=[get_weather],
        # `store=False` → the hosting layer manages conversation memory per
        # request; the chat service does NOT persist the thread server-side.
        # Flip to True if you want Foundry to remember state across sessions.
        # Reference:
        # https://developers.openai.com/api/reference/resources/responses/methods/create
        default_options={"store": False},
    )

    # Serve the agent over the Responses API. The hosting layer handles
    # thread + run lifecycle, tool-call orchestration, and the HTTP surface.
    # Default bind address is 0.0.0.0:8088 — matches the EXPOSE 8088 in the
    # Dockerfile.
    server = ResponsesHostServer(agent)
    server.run()


if __name__ == "__main__":
    main()
