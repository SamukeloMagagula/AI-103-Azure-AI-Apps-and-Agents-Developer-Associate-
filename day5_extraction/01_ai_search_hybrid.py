"""Day 5 · Script 1 — AI Search: hybrid + semantic reranker + vector.

Exam objective → "Configure semantic search, hybrid search, and vector
search for grounding."

REST body
---------
POST /indexes/<name>/docs/search?api-version=2024-07-01
{
  "search": "azure openai",
  "vectorQueries": [{"kind":"vector","vector":[...],
                     "fields":"embedding","k":5}],
  "queryType": "semantic",
  "semanticConfiguration": "default-semantic",
  "captions": "extractive",
  "answers":  "extractive|count-3",
  "top": 5
}
Hybrid = both `search` and `vectorQueries` set. Fusion = RRF.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

docs = [
    {"id": "1", "title": "Agent Framework",
     "content": "Foundry Agent Framework defines agents, threads and runs.",
     "embedding": mock_azure.embed("Foundry Agent Framework defines agents, threads and runs.")},
    {"id": "2", "title": "Content Understanding",
     "content": "Content Understanding extracts fields from documents, images and video.",
     "embedding": mock_azure.embed("Content Understanding extracts fields from documents, images and video.")},
    {"id": "3", "title": "Private endpoints",
     "content": "Private endpoints protect AI resources from the public internet.",
     "embedding": mock_azure.embed("Private endpoints protect AI resources from the public internet.")},
]
mock_azure.search_index_docs(docs)

q = "how does the Foundry agent orchestrate tools"
qv = mock_azure.embed(q)
show("Hybrid + semantic result",
     mock_azure.search_query(q=q, vector=qv, top=3, semantic=True))

print("\nField attributes: searchable · filterable · sortable · facetable · retrievable · key.")
print("Vector field type: Collection(Edm.Single) with dimensions + vectorSearchProfile.")
