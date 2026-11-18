"""Day 5 · Script 3 — End-to-end RAG ingestion pipeline.

Exam objective → "Configure RAG ingestion flow, including documents and
using optical character recognition (OCR)" + enrichment skills.

Pipeline
--------
    blob storage ─┐
                  ├─► Indexer ─► Skillset (OCR + CU + embed)
    documents ────┘            │
                               └─► AI Search index ──► Agent tool
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show
import mock_azure

skillset = {
    "name": "docs-skillset",
    "skills": [
        {"@odata.type": "#Microsoft.Skills.Util.ContentUnderstandingSkill",
         "connectionName": "content-understanding",
         "analyzerId": "invoice-markdown",
         "inputs":  [{"name": "file", "source": "/document/content"}],
         "outputs": [{"name": "markdown", "targetName": "md"},
                     {"name": "fields",   "targetName": "fields"}]},
        {"@odata.type": "#Microsoft.Skills.Text.SplitSkill",
         "textSplitMode": "pages", "maximumPageLength": 2000,
         "inputs":  [{"name": "text", "source": "/document/md"}],
         "outputs": [{"name": "textItems", "targetName": "chunks"}]},
        {"@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
         "resourceUri": "https://<aoai>.openai.azure.com/",
         "deploymentId": "text-embedding-3-small",
         "inputs":  [{"name": "text", "source": "/document/chunks/*"}],
         "outputs": [{"name": "embedding", "targetName": "vector"}]},
    ],
    "indexProjections": {
        "selectors": [{
            "targetIndexName": "docs-index",
            "parentKeyFieldName": "parent_id",
            "sourceContext": "/document/chunks/*",
            "mappings": [
                {"name": "chunk",     "source": "/document/chunks/*"},
                {"name": "embedding", "source": "/document/chunks/*/vector"},
            ]}]
    },
}
show("Skillset", skillset)

indexer = {
    "name": "docs-indexer",
    "dataSourceName": "blob-ds",
    "targetIndexName": "docs-index",
    "skillsetName":   "docs-skillset",
    "schedule": {"interval": "PT1H"},
    "parameters": {"configuration": {"dataToExtract": "contentAndMetadata"}},
}
show("Indexer", indexer)

# A query against the resulting index
mock_azure.search_index_docs([
    {"id": "inv-1", "chunk": "Invoice 42 total R1250", "embedding": mock_azure.embed("inv-1")},
])
show("Sample query", mock_azure.search_query(q="invoice total", top=1))
