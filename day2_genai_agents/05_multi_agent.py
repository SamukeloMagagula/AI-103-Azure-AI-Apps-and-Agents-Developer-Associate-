"""Day 2 · Script 5 — Orchestrated multi-agent workflow.

Exam objective → "Implement orchestrated multi-agent solutions" +
"Build autonomous or semiautonomous workflows with safeguards and
approval flow controls."

Pattern: one LEAD agent decomposes the task, delegates to SPECIALIST
agents, then AGGREGATES. The lead owns conversation memory (the thread).

Approval flow: mark a tool with {"requires_approval": true}. The run
returns status=requires_action with an approval step; a human (or
policy engine) submits approve/reject before execution resumes.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

lead     = mock_azure.agents_create("lead",      "gpt-4.1",       "Decompose and route.")
analyst  = mock_azure.agents_create("analyst",   "gpt-4o-mini",   "Do the numeric analysis.")
writer   = mock_azure.agents_create("writer",    "gpt-4o-mini",   "Turn findings into a memo.")

trace = mock_azure.multi_agent_handoff(
    agents=[lead["name"], analyst["name"], writer["name"]],
    task="Draft a weekly ops report from this CSV")
show("Handoff trace", trace)

show("Approval-gated tool example", {
    "type": "function",
    "function": {"name": "send_email", "description": "Send an email",
                 "parameters": {"type": "object",
                                "properties": {"to": {"type": "string"},
                                               "body": {"type": "string"}}}},
    "requires_approval": True,
})

print("\nTrap → multi-agent memory lives on the SHARED thread; specialists")
print("        append to it so the lead can see what each produced.")
