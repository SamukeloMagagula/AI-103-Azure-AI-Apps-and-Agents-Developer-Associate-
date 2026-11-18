"""Day 2 · Script 2 — RAG via Foundry "On Your Data".

Exam objective → "Implement retrieval-augmented generation (RAG)
in an application."

Two approaches on the exam
--------------------------
(A) Server-side RAG — let Foundry handle retrieval:
    client.chat.completions.create(
        model=deployment,
        messages=[...],
        extra_body={"data_sources":[{
            "type":"azure_search",
            "parameters":{
                "endpoint": search_endpoint,
                "index_name": "docs-index",
                "authentication":{"type":"system_assigned_managed_identity"},
                "embedding_dependency":{"type":"deployment_name",
                                        "deployment_name":"text-embedding-3-small"},
                "query_type":"vector_semantic_hybrid"}}]})

(B) Build-your-own — embed → search → stuff → generate (shown below).
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

# Seed KB
kb = [("agents", "Foundry agents use threads, runs and tools."),
      ("resp",   "The Responses API supersedes Chat Completions."),
      ("cu",     "Content Understanding extracts fields from docs/images/video.")]
docs = [{"id": k, "title": k, "content": v,
         "embedding": mock_azure.embed(v)} for k, v in kb]
mock_azure.search_index_docs(docs)

question = "What API replaced chat completions?"
retrieved = mock_azure.search_query(q=question, vector=mock_azure.embed(question),
                                    top=2, semantic=True)
show("Retrieved (hybrid + semantic)", retrieved)

context = "\n".join(d["content"] for d in retrieved["value"])
r = mock_azure.responses_create(
    model="gpt-4o-mini",
    instructions=f"Answer ONLY from this context:\n{context}",
    input_=question) if USE_MOCK else None
show("Grounded answer", r)

print("\nquery_type options → simple · semantic · vector · vector_semantic_hybrid.")
