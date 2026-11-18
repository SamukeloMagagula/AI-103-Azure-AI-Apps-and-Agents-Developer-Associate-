"""Day 4 · Script 1 — Text analysis via LLM prompting (structured outputs).

Exam objective → "Implement solutions to extract entities, topics,
summaries, and structured JSON outputs by using generative prompting
and Foundry Tools."

The exam prefers LLM-powered structured outputs over the classic
Language service. Use `response_format={"type":"json_schema", ...}` to
force a schema.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "ticket",
        "schema": {
            "type": "object",
            "properties": {
                "sentiment":  {"type": "string", "enum": ["positive", "neutral", "negative"]},
                "intent":     {"type": "string"},
                "entities":   {"type": "array", "items": {"type": "string"}},
                "summary":    {"type": "string"},
            },
            "required": ["sentiment", "intent", "summary"],
        },
        "strict": True,
    },
}

input_text = "I need to cancel my Azure subscription — the billing from last month is wrong."
show("Request", {"model": "gpt-4o-mini", "input": input_text, "response_format": SCHEMA})

r = mock_azure.responses_create(model="gpt-4o-mini", input_=input_text) if USE_MOCK else None
show("Response (would be valid JSON matching the schema)", r)

print("\nTrap → strict=True forbids additional properties; the model errors")
print("        rather than invent fields.")
