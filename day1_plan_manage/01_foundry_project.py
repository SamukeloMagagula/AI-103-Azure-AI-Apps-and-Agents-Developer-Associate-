"""Day 1 · Script 1 — Foundry project, deployments, connections.

Exam objective → "Set up AI solutions in Foundry"

Live code
---------
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

client = AIProjectClient(
    endpoint="https://<proj>.services.ai.azure.com/api/projects/<proj>",
    credential=DefaultAzureCredential())

# List model deployments attached to the project
for d in client.deployments.list():
    print(d.name, d.model.name, d.model.version, d.sku.capacity)

# List connections (Search, Storage, Content Understanding, custom APIs)
for c in client.connections.list():
    print(c.name, c.type, c.target)
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import need, show

show("Project endpoint", need("AZURE_FOUNDRY_PROJECT_ENDPOINT"))
show("Deployments (mock)", [
    {"name": "gpt-4o-mini",             "sku": "GlobalStandard", "capacity_tpm": 150_000},
    {"name": "text-embedding-3-small",  "sku": "Standard",       "capacity_tpm":  60_000},
    {"name": "gpt-image-1",             "sku": "Standard",       "capacity_tpm":   5_000},
])
show("Connections (mock)", [
    {"name": "aisearch-conn",        "type": "AzureAISearch"},
    {"name": "storage-conn",         "type": "AzureStorageAccount"},
    {"name": "content-understanding","type": "AzureAIServices"},
])

print("\nExam trap → agents/tools reference a CONNECTION name, not a raw endpoint.")
