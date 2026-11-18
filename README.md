# AI-103 — 5-Day Practical Kit

Hands-on scripts for **Exam AI-103: Developing AI Apps and Agents on
Azure** (Microsoft Certified: Azure AI Apps and Agents Developer
Associate). Every script runs locally against mock Foundry endpoints so
you can learn the SDK shapes without burning tokens or waiting on quota.
Flip `USE_MOCK=0` in `.env` and point at real Foundry resources when ready.

## Weighting the exam actually uses

| Section                                            | Weight    | Folder                 |
|----------------------------------------------------|-----------|------------------------|
| Plan and manage an Azure AI solution               | 25-30 %   | `day1_plan_manage/`    |
| **Implement generative AI and agentic solutions**  | **30-35 %** | `day2_genai_agents/`  |
| Implement computer vision solutions                | 10-15 %   | `day3_vision/`         |
| Implement text analysis solutions                  | 10-15 %   | `day4_text_speech/`    |
| Implement information extraction solutions         | 10-15 %   | `day5_extraction/`     |

Day 2 is deliberately the largest — the agents section is the biggest
block on the exam.

## Layout

```
.
├── .env.example           → copy to .env, fill in when you have real keys
├── common.py              → env loader + mock/live switch
├── mock_azure.py          → stub responses shaped like real Foundry APIs
├── day1_plan_manage/      → Foundry setup, models, quotas, RBAC, RAI
├── day2_genai_agents/     → Responses API, Agent Framework, RAG, multi-agent, evals
├── day3_vision/           → image/video gen, multimodal understanding, CU visual
├── day4_text_speech/      → LLM-driven text analysis, Translator, Speech
└── day5_extraction/       → AI Search hybrid/vector, Content Understanding, drill
```

## Running anything

```powershell
python day2_genai_agents/03_agent_basics.py
```

Every file opens with:
1. A docstring naming the **real SDK class + REST route** the exam tests.
2. The `USE_MOCK` call pattern.
3. A short "Exam trap" line at the end — a common gotcha.

## Prerequisites (when going live)

```powershell
pip install azure-ai-projects azure-ai-agents azure-ai-evaluation ^
            azure-ai-contentsafety azure-search-documents openai ^
            azure-identity python-dotenv requests
```

## Core services the exam names

- **Microsoft Foundry** (projects, deployments, connections)
- **Azure OpenAI** via Foundry (Responses API, Chat Completions, embeddings, images)
- **Foundry Agent Framework** — `azure-ai-agents`
- **Azure AI Content Understanding** — Foundry Tool for docs/images/video/audio
- **Azure AI Search** — hybrid + semantic + vector grounding
- **Azure AI Content Safety** — categories, Prompt Shield, groundedness
- **Azure AI Translator** — as a Foundry Tool
- **Azure AI Speech** — STT, TTS, custom speech
- **Azure AI Evaluation** — groundedness, fluency, safety, fabrication detection
