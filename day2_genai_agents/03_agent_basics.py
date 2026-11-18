"""Day 2 · Script 3 — Agent Framework: create agent, thread, run.

Exam objective → "Build agents by using Foundry: define roles, goals,
conversation-tracking approach, and tool schemas."

Live code
---------
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient

agents = AgentsClient(endpoint=project_endpoint, credential=DefaultAzureCredential())

agent = agents.create_agent(
    model="gpt-4o-mini",
    name="support-bot",
    instructions="You are a terse Azure AI support agent.",
    tools=[{"type":"file_search"}])

thread = agents.threads.create()
agents.messages.create(thread_id=thread.id, role="user",
                       content="Summarise the attached ticket.")
run = agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
for m in agents.messages.list(thread_id=thread.id):
    print(m.role, m.content[0].text.value)
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

agent = mock_azure.agents_create(
    name="support-bot",
    model="gpt-4o-mini",
    instructions="You are a terse Azure AI support agent.",
    tools=[{"type": "file_search"}]) if USE_MOCK else None
show("Agent", agent)

thread = mock_azure.threads_create() if USE_MOCK else None
mock_azure.messages_add(thread["id"], "user", "What is the Responses API?")
run = mock_azure.runs_create_and_process(thread["id"], agent["id"])
show("Run", run)

print("\nLifecycle → queued → in_progress → requires_action (tool) → completed | failed.")
