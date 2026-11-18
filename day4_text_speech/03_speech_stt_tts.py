"""Day 4 · Script 3 — Speech: STT + TTS + custom speech.

Exam objective → "Implement workflows to convert speech to text and text
to speech for agentic interactions" + custom speech models.

Live code
---------
import azure.cognitiveservices.speech as speechsdk
cfg = speechsdk.SpeechConfig(subscription=key, region=region)
cfg.speech_recognition_language = "en-US"

# STT
reco = speechsdk.SpeechRecognizer(speech_config=cfg,
            audio_config=speechsdk.audio.AudioConfig(filename="in.wav"))
r = reco.recognize_once_async().get()

# TTS
cfg.speech_synthesis_voice_name = "en-US-AvaNeural"
synth = speechsdk.SpeechSynthesizer(speech_config=cfg)
synth.speak_text_async("Hello from Foundry").get()
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

show("STT", mock_azure.speech_to_text("./in.wav") if USE_MOCK else None)
show("TTS", {k: v for k, v in (mock_azure.text_to_speech("Hello from Foundry").items()
                               if USE_MOCK else []) if k != "audioBytes"})

print("\nCustom Speech → upload transcripts + audio in Speech Studio, train a")
print("                custom model, deploy to an endpoint id, then:")
print('                cfg.endpoint_id = "<deployment-guid>"')
