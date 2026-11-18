"""Deterministic fake responses shaped like the real Foundry / Azure AI APIs.

Reshaped for AI-103 (Azure AI Apps and Agents Developer Associate):
Foundry Agent Framework, Responses API, Content Understanding, AI Search,
Translator, Speech, Content Safety. Every function mirrors the real JSON
schema so the calling code is portable — swap USE_MOCK=0 and keep going.
"""
from __future__ import annotations
import hashlib
import json
import math
import time
import uuid
from typing import Any


# =========================================================================
# Azure OpenAI / Foundry — Responses API
# =========================================================================
def responses_create(model: str, input_: str | list[dict], *,
                     tools: list[dict] | None = None,
                     tool_choice: str = "auto",
                     instructions: str | None = None) -> dict[str, Any]:
    """POST {endpoint}/openai/responses?api-version=2025-03-01-preview."""
    user_text = input_ if isinstance(input_, str) else next(
        (c.get("content", "") for c in reversed(input_) if c.get("role") == "user"), "")
    output: list[dict[str, Any]] = []

    if tools and "weather" in user_text.lower():
        output.append({"type": "function_call", "id": "call_1",
                       "call_id": "call_1", "name": "get_weather",
                       "arguments": json.dumps({"city": "Johannesburg"})})
    else:
        output.append({"type": "message", "role": "assistant",
            "content": [{"type": "output_text",
                         "text": f"(mock) grounded answer to: {user_text!r}"}]})

    return {"id": f"resp_{uuid.uuid4().hex[:12]}", "object": "response",
            "created_at": int(time.time()), "model": model, "status": "completed",
            "instructions": instructions, "output": output,
            "usage": {"input_tokens": 50, "output_tokens": 20, "total_tokens": 70}}


# =========================================================================
# Foundry Agent Framework
# =========================================================================
_AGENTS: dict[str, dict] = {}
_THREADS: dict[str, list[dict]] = {}


def agents_create(name: str, model: str, instructions: str,
                  tools: list[dict] | None = None,
                  tool_resources: dict | None = None) -> dict[str, Any]:
    """Foundry Agent Framework — POST /agents."""
    aid = f"asst_{uuid.uuid4().hex[:12]}"
    _AGENTS[aid] = {"id": aid, "name": name, "model": model,
                    "instructions": instructions, "tools": tools or [],
                    "tool_resources": tool_resources or {}}
    return _AGENTS[aid]


def threads_create() -> dict[str, Any]:
    tid = f"thread_{uuid.uuid4().hex[:12]}"
    _THREADS[tid] = []
    return {"id": tid, "object": "thread", "created_at": int(time.time())}


def messages_add(thread_id: str, role: str, content: str) -> dict[str, Any]:
    msg = {"id": f"msg_{uuid.uuid4().hex[:8]}", "thread_id": thread_id,
           "role": role, "content": [{"type": "text", "text": {"value": content}}]}
    _THREADS.setdefault(thread_id, []).append(msg)
    return msg


def runs_create_and_process(thread_id: str, agent_id: str) -> dict[str, Any]:
    """Run an agent against a thread; may emit a tool-call step."""
    agent = _AGENTS[agent_id]
    history = _THREADS.get(thread_id, [])
    user_text = next((m["content"][0]["text"]["value"]
                      for m in reversed(history) if m["role"] == "user"), "")

    steps = []
    if any(t.get("type") == "function" and "weather" in user_text.lower()
           for t in agent["tools"]):
        steps.append({"type": "tool_calls",
                      "tool_calls": [{"id": "call_1", "type": "function",
                                       "function": {"name": "get_weather",
                                                    "arguments": '{"city":"Johannesburg"}'}}]})
        reply = "Tool call issued — submit the result with submit_tool_outputs."
        status = "requires_action"
    else:
        reply = f"(mock agent '{agent['name']}') grounded reply to: {user_text!r}"
        status = "completed"
        messages_add(thread_id, "assistant", reply)

    return {"id": f"run_{uuid.uuid4().hex[:8]}", "thread_id": thread_id,
            "agent_id": agent_id, "status": status, "steps": steps,
            "usage": {"prompt_tokens": 80, "completion_tokens": 30, "total_tokens": 110}}


def multi_agent_handoff(agents: list[str], task: str) -> dict[str, Any]:
    """Pretend a lead agent routes work between specialists."""
    trace = [{"agent": agents[0], "action": "plan",
              "note": f"decompose task: {task!r}"}]
    for a in agents[1:]:
        trace.append({"agent": a, "action": "execute",
                      "note": f"{a} handled a subtask"})
    trace.append({"agent": agents[0], "action": "aggregate",
                  "note": "merged specialist outputs into final answer"})
    return {"task": task, "trace": trace,
            "final_answer": "(mock) consolidated answer from the agent team."}


# =========================================================================
# Evaluation (Foundry Evaluators)
# =========================================================================
def evaluate(outputs: list[dict]) -> dict[str, Any]:
    """Mimics azure-ai-evaluation metric aggregation."""
    def score(text: str, kind: str) -> float:
        if kind == "groundedness":
            return 0.3 if "mock" in text.lower() else 0.85
        if kind == "fluency":        return 0.9
        if kind == "relevance":      return 0.8
        if kind == "coherence":      return 0.85
        if kind == "safety":         return 1.0 if "attack" not in text else 0.1
        return 0.5

    rows = []
    for o in outputs:
        rows.append({k: score(o["response"], k)
                     for k in ("groundedness", "fluency", "relevance",
                               "coherence", "safety")})
    agg = {k: sum(r[k] for r in rows) / len(rows) for k in rows[0]}
    return {"rows": rows, "metrics": agg}


# =========================================================================
# Content Safety (Prompt Shield + category analysis)
# =========================================================================
def content_safety(text: str) -> dict[str, Any]:
    bad = any(w in text.lower() for w in ("kill", "hate", "attack"))
    sev = 4 if bad else 0
    return {"categoriesAnalysis": [
        {"category": "Hate",     "severity": sev},
        {"category": "SelfHarm", "severity": 0},
        {"category": "Sexual",   "severity": 0},
        {"category": "Violence", "severity": sev},
    ]}


def prompt_shield(user_prompt: str, documents: list[str]) -> dict[str, Any]:
    jailbreak = "ignore previous" in user_prompt.lower()
    indirect  = any("ignore previous" in d.lower() for d in documents)
    return {"userPromptAnalysis": {"attackDetected": jailbreak},
            "documentsAnalysis": [{"attackDetected": indirect} for _ in documents]}


# =========================================================================
# Content Understanding (Foundry Tools)
# =========================================================================
def content_understanding_analyze(analyzer_id: str, source: str) -> dict[str, Any]:
    """POST {endpoint}/contentunderstanding/analyzers/{id}:analyze."""
    if analyzer_id == "invoice-markdown":
        return {"status": "succeeded", "result": {"analyzerId": analyzer_id,
            "markdown": "# Invoice INV-00042\n\n**Vendor:** Contoso Ltd\n**Total:** R 1 250.00\n",
            "fields": {
                "VendorName":   {"value": "Contoso Ltd",  "confidence": 0.97},
                "InvoiceId":    {"value": "INV-00042",    "confidence": 0.99},
                "InvoiceTotal": {"value": "R 1 250.00",   "confidence": 0.92}}}}
    if analyzer_id == "video-scene":
        return {"status": "succeeded", "result": {
            "segments": [
                {"startTime": 0,  "endTime": 12, "summary": "Opening landscape shot"},
                {"startTime": 12, "endTime": 48, "summary": "Presenter discusses Foundry agents"},
            ], "transcript": "(mock) Welcome to the AI-103 demo..."}}
    return {"status": "succeeded", "result": {"analyzerId": analyzer_id,
            "content": f"(mock) understood {source!r}", "fields": {}}}


# =========================================================================
# Image generation (dall-e / gpt-image)
# =========================================================================
def images_generate(prompt: str, size: str = "1024x1024", n: int = 1) -> dict[str, Any]:
    return {"created": int(time.time()),
            "data": [{"url": f"https://mock.blob/{uuid.uuid4().hex}.png",
                      "revised_prompt": f"(mock revised) {prompt}"} for _ in range(n)]}


# =========================================================================
# Translator (Foundry Tool)
# =========================================================================
def translate(text: str, target: str) -> list[dict[str, Any]]:
    return [{"detectedLanguage": {"language": "en", "score": 1.0},
             "translations": [{"text": f"[{target}] {text}", "to": target}]}]


# =========================================================================
# Speech
# =========================================================================
def speech_to_text(audio_path: str, language: str = "en-US") -> dict[str, Any]:
    return {"RecognitionStatus": "Success",
            "DisplayText": "Hello, this is a mocked transcription.",
            "Language": language, "Offset": 0, "Duration": 15_000_000}


def text_to_speech(text: str, voice: str = "en-US-AvaNeural") -> dict[str, Any]:
    return {"audioBytes": b"<mock-wav-bytes>", "voice": voice, "length": len(text)}


# =========================================================================
# AI Search (index / hybrid / vector)
# =========================================================================
_INDEX: list[dict[str, Any]] = []


def search_index_docs(docs: list[dict[str, Any]]) -> dict[str, Any]:
    _INDEX.extend(docs)
    return {"value": [{"key": d.get("id"), "status": True, "statusCode": 201}
                      for d in docs]}


def search_query(q: str = "", vector: list[float] | None = None,
                 top: int = 3, semantic: bool = False) -> dict[str, Any]:
    def cos(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a)) or 1
        nb = math.sqrt(sum(x * x for x in b)) or 1
        return dot / (na * nb)

    scored = []
    for d in _INDEX:
        text_score = 0.0
        if q:
            text = " ".join(str(v) for k, v in d.items() if k != "embedding").lower()
            text_score = float(sum(term in text for term in q.lower().split()))
        vec_score = cos(vector, d.get("embedding", vector)) if vector else 0.0
        combined = 0.6 * text_score + 0.4 * vec_score if (q and vector) else (text_score or vec_score)
        if combined:
            row = {"@search.score": combined, **{k: v for k, v in d.items() if k != "embedding"}}
            if semantic:
                row["@search.reranker_score"] = combined * 1.2
                row["@search.captions"] = [{"text": str(d.get("content", ""))[:80],
                                            "highlights": q}]
            scored.append(row)
    scored.sort(key=lambda x: -x.get("@search.reranker_score", x["@search.score"]))
    return {"value": scored[:top]}


# =========================================================================
# Embeddings
# =========================================================================
def embed(text: str) -> list[float]:
    h = hashlib.sha256(text.encode()).digest()
    return [((b / 255) - 0.5) for b in h[:16]]
