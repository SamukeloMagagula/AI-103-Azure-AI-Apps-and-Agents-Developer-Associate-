"""Day 2 · Script 6 — Evaluators: groundedness, fluency, relevance, safety.

Exam objective → "Evaluate models and apps, including detecting
fabrications, relevance, quality, and safety."

Live code
---------
from azure.ai.evaluation import (evaluate, GroundednessEvaluator,
                                 RelevanceEvaluator, FluencyEvaluator,
                                 ContentSafetyEvaluator)
result = evaluate(
    data="eval_data.jsonl",
    evaluators={"groundedness": GroundednessEvaluator(model_config),
                "relevance":    RelevanceEvaluator(model_config),
                "fluency":      FluencyEvaluator(model_config),
                "safety":       ContentSafetyEvaluator(project_scope)},
    azure_ai_project=project)
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

dataset = [
    {"query": "What is the Responses API?",
     "response": "The Responses API is Foundry's unified inference endpoint.",
     "context":  "Responses is the unified protocol that supersedes Chat Completions."},
    {"query": "Best embedding model?",
     "response": "(mock) The mock model is best.",
     "context":  "text-embedding-3-small is the Foundry default."},
]
show("Eval result", mock_azure.evaluate(dataset) if USE_MOCK else None)

print("\nMetrics you must know (all 1-5 or 0-1 scored):")
print("  groundedness · relevance · coherence · fluency · similarity")
print("  + safety scores: hate · self_harm · sexual · violence")
print("  + fabrication / protected_material / indirect_attack")
