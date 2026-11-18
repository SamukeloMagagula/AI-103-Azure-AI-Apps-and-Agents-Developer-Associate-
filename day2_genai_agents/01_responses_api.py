"""Day 2 · Script 1 — Foundry Responses API (unified protocol).

Exam objective → "Deploy and consume LLMs ... integrate generative workflows
by using Foundry SDKs and connectors."

Live code
---------
from openai import AzureOpenAI
client = AzureOpenAI(api_key=..., api_version="2025-03-01-preview",
                     azure_endpoint="https://<aoai>.openai.azure.com/")
r = client.responses.create(
    model="<DEPLOYMENT_NAME>",           # deployment, not model id
    instructions="You are a terse Azure tutor.",
    input="Explain embeddings in one sentence.")
print(r.output_text)

Streaming:
    with client.responses.stream(model=..., input=...) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="")
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import need, show, USE_MOCK
import mock_azure

show("Request", {
    "endpoint": need("AZURE_OPENAI_ENDPOINT"),
    "deployment": need("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    "api_version": need("AZURE_OPENAI_API_VERSION"),
    "instructions": "You are a terse Azure tutor.",
    "input": "Explain embeddings in one sentence.",
})

r = mock_azure.responses_create(
    model=need("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    instructions="You are a terse Azure tutor.",
    input_="Explain embeddings in one sentence.") if USE_MOCK else None
show("Response", r)

print("\nTrap → `input=` accepts a string OR a list of role-tagged items.")
print("Trap → Chat Completions is the LEGACY path; Responses is the exam default.")
