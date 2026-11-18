"""Day 4 · Script 4 — Speech as an agent modality.

Exam objective → "Integrate speech as an agent modality" + audio-in
multimodal reasoning + speech translation.

Pattern: voice UI → STT → agent run → TTS → voice reply.
For low-latency voice, use the Realtime API (gpt-4o-realtime) which
handles audio streams directly without the STT/TTS hop.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

# 1. User speaks → STT
stt = mock_azure.speech_to_text("./user.wav") if USE_MOCK else None
show("User transcription", stt)

# 2. Agent processes text
agent = mock_azure.agents_create("voice-bot", "gpt-4o-mini",
                                 "Reply in <=2 short sentences.")
thread = mock_azure.threads_create()
mock_azure.messages_add(thread["id"], "user", stt["DisplayText"])
run = mock_azure.runs_create_and_process(thread["id"], agent["id"])
show("Agent run", run)

# 3. Reply → TTS
tts = mock_azure.text_to_speech("Here's your answer.") if USE_MOCK else None
show("TTS (metadata only — audioBytes omitted)",
     {k: v for k, v in tts.items() if k != "audioBytes"})

print("\nRealtime alternative: Azure OpenAI Realtime WebSocket endpoint")
print("                      /openai/realtime?deployment=gpt-4o-realtime.")
