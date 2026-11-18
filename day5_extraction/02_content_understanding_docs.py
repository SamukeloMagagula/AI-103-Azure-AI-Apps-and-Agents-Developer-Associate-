"""Day 5 · Script 2 — Content Understanding for documents.

Exam objective → "Extract information by using multimodal pipelines that
combine OCR, layout analysis, and field extraction" + "Implement
analyzers for generating structured or markdown outputs."

Content Understanding REPLACES Document Intelligence in the AI-103
skill set — same capabilities, unified under one Foundry Tool with
configurable analyzers.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

show("Prebuilt invoice-markdown analyzer",
     mock_azure.content_understanding_analyze("invoice-markdown", "./invoice.pdf"))

show("Custom analyzer schema (what you POST when creating one)", {
    "analyzerId": "medical-claim",
    "baseAnalyzerId": "prebuilt-documentAnalyzer",
    "config": {"returnDetails": True, "enableOcr": True, "enableLayout": True},
    "fieldSchema": {
        "fields": {
            "PatientName":  {"type": "string"},
            "ClaimAmount":  {"type": "number"},
            "ServiceDate":  {"type": "date"},
            "LineItems":    {"type": "array",
                             "items": {"type": "object",
                                       "properties": {"code":  {"type": "string"},
                                                       "price": {"type": "number"}}}},
        }
    }
})

print("\nPrebuilt analyzers to recognise:")
print("  prebuilt-documentAnalyzer · prebuilt-imageAnalyzer ·")
print("  prebuilt-videoAnalyzer    · prebuilt-audioAnalyzer ·")
print("  invoice-markdown · receipt · businessCard · idDocument")
