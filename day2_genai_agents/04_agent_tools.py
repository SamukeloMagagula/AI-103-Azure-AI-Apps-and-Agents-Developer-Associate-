"""Day 2 · Script 4 — Agent tools: function calling + file_search + code_interpreter.

Exam objective → "Integrate agent tools including APIs, knowledge stores,
search, content understanding, and custom functions."

Built-in tool types the exam asks about
---------------------------------------
    {"type":"file_search"}                  — RAG over uploaded files
    {"type":"code_interpreter"}             — sandboxed Python
    {"type":"azure_ai_search", ...}         — AI Search index as a tool
    {"type":"openapi", ...}                 — any REST API via OpenAPI spec
    {"type":"function", "function":{...}}   — your own Python function
    {"type":"bing_grounding"} / {"type":"browser_automation"}
    {"type":"content_understanding", ...}   — CU analyzer as a tool
"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

tools = [
    {"type": "function",
     "function": {"name": "get_weather",
                  "description": "Get current weather for a city",
                  "parameters": {"type": "object",
                                 "properties": {"city": {"type": "string"}},
                                 "required": ["city"]}}},
    {"type": "azure_ai_search",
     "azure_ai_search": {"connection_name": "aisearch-conn",
                         "index_name": "docs-index",
                         "query_type": "vector_semantic_hybrid"}},
    {"type": "content_understanding",
     "content_understanding": {"connection_name": "content-understanding",
                               "analyzer_id": "invoice-markdown"}},
]

agent = mock_azure.agents_create(
    name="ops-bot", model="gpt-4o-mini",
    instructions="Use tools; don't guess.", tools=tools)
thread = mock_azure.threads_create()
mock_azure.messages_add(thread["id"], "user", "What's the weather in Johannesburg?")
run = mock_azure.runs_create_and_process(thread["id"], agent["id"])
show("Run (expect requires_action)", run)

# Submit the tool output back
tc = run["steps"][0]["tool_calls"][0]
args = json.loads(tc["function"]["arguments"])
tool_output = {"tool_call_id": tc["id"],
               "output": json.dumps({"city": args["city"], "tempC": 24, "sky": "clear"})}
show("submit_tool_outputs payload", tool_output)

print("\nTrap → runs.submit_tool_outputs_and_process polls to completion;")
print("        plain submit_tool_outputs returns immediately — you must poll.")
