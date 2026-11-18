"""Day 5 · Script 4 — Rapid-fire exam drill for AI-103.

Run until you answer every question cold. Each item maps to a real
exam objective.
"""
QUESTIONS = [
    # --- Plan & manage ---
    ("Which Azure role lets an app read documents from an AI Search index?",
     "Search Index Data Reader"),
    ("Keyless auth to Azure OpenAI uses which scope?",
     "https://cognitiveservices.azure.com/.default"),
    ("Reserved AOAI capacity with predictable latency is which SKU?",
     "Provisioned (PTU)"),
    ("Severity scale for Content Safety categories (default)?",
     "0, 2, 4, 6"),
    # --- GenAI + Agents (biggest) ---
    ("Which API supersedes Chat Completions in Foundry?",
     "The Responses API"),
    ("In the Agent Framework, what three objects model a conversation?",
     "Agent, Thread, Run"),
    ("Which run status indicates the agent is waiting for a tool result?",
     "requires_action"),
    ("Which tool type exposes a REST API via its OpenAPI spec to an agent?",
     "{'type':'openapi', ...}"),
    ("Which parameter forces a strict JSON schema on a Responses output?",
     "response_format={'type':'json_schema', ..., strict:true}"),
    ("Which evaluator detects answers unsupported by the provided context?",
     "GroundednessEvaluator"),
    ("Prompt Shield protects against two attack types — which?",
     "User-prompt jailbreaks AND indirect (document) prompt injections"),
    # --- Vision ---
    ("Which deployment handles text-to-image?",
     "gpt-image-1 (or dall-e-3)"),
    ("For an image edit, what is a transparent pixel on the mask?",
     "A region the model should re-paint"),
    ("Which CU mode is slower but reasons across multiple steps?",
     "pro-mode"),
    # --- Text + speech ---
    ("Which Translator header is mandatory besides the key?",
     "Ocp-Apim-Subscription-Region"),
    ("How do you point the Speech SDK at a custom speech deployment?",
     "set speech_config.endpoint_id = '<deployment-guid>'"),
    # --- Info extraction ---
    ("What is the Edm type for a vector field in AI Search?",
     "Collection(Edm.Single) with 'dimensions' and 'vectorSearchProfile'"),
    ("Which search queryType returns captions and extractive answers?",
     "semantic (with semanticConfiguration set)"),
    ("What algorithm fuses BM25 and vector rankings in hybrid search?",
     "Reciprocal Rank Fusion (RRF)"),
    ("Which Content Understanding analyzer kinds exist?",
     "document, image, video, audio"),
]

if __name__ == "__main__":
    for q, a in QUESTIONS:
        input(f"\nQ: {q}\n[Enter for answer] ")
        print(f"A: {a}")
