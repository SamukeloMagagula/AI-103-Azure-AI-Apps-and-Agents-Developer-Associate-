"""Day 4 · Script 2 — Azure AI Translator as a Foundry Tool.

Exam objective → "Build solutions that translate text by using Azure
Translator in Foundry Tools or LLM-powered translation flows."

REST
----
    POST https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=af&to=zu
    Headers:
        Ocp-Apim-Subscription-Key:    <KEY>
        Ocp-Apim-Subscription-Region: <REGION>      ← mandatory
    Body: [{"text":"Hello"}]
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

text = "Where is the nearest train station?"
for target in ("af", "zu", "fr"):
    show(f"en -> {target}", mock_azure.translate(text, target) if USE_MOCK else None)

print("\nAs a Foundry Tool the agent calls it transparently —")
print('attach {"type":"translator","translator":{"connection_name":"translator-conn"}}.')
