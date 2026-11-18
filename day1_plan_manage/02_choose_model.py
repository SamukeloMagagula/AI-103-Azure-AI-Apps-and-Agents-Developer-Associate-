"""Day 1 · Script 2 — Pick the right Foundry model for each task.

Exam objective → "Choose an appropriate model for each task"

Memorise this decision table. The exam phrases it as:
"A customer needs X. Which model family do you choose?"
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show

MATRIX = [
    ("Long-form reasoning, planning for an agent",  "gpt-4.1 / gpt-5 (LLM, reasoning)"),
    ("Cheap high-throughput text classification",   "gpt-4o-mini / gpt-5-mini (SLM)"),
    ("Edge / on-device inference",                  "Phi-4 (SLM)"),
    ("Image + text understanding",                  "gpt-4o (multimodal)"),
    ("Audio in, text out (transcription + reason)", "gpt-4o-audio / Speech STT"),
    ("Text-to-image generation",                    "gpt-image-1 / DALL-E 3"),
    ("Video understanding / scene summary",         "Content Understanding (video analyzer)"),
    ("Embedding text for RAG",                      "text-embedding-3-small / -3-large"),
    ("Code generation in an agent tool",            "gpt-4.1 + code_interpreter tool"),
    ("Translation inside an agent",                 "Translator Foundry Tool (not an LLM)"),
]

for task, pick in MATRIX:
    show(task, pick)

print("\nTrap → model id (gpt-4o-mini) vs deployment name (my-mini-dep).")
print("        Code calls use the DEPLOYMENT NAME everywhere.")
