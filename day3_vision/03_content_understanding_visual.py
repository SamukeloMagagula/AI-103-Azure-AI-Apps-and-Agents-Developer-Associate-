"""Day 3 · Script 3 — Content Understanding for images and video.

Exam objective → "Implement visual understanding by configuring Azure
Content Understanding in Foundry Tools" + video segment analysis +
single-task vs pro-mode pipelines.

Content Understanding analyzer kinds
------------------------------------
    document  → OCR + layout + field extraction
    image     → visual features, embedded text, objects
    video     → scene segmentation, transcript, visual summary
    audio     → transcript + speaker diarization + sentiment

Modes
    standard    → single-task, cheap, quick
    pro         → multi-step reasoning, higher quality, slower
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

show("Image analyzer (mock)",
     mock_azure.content_understanding_analyze("image-generic", "./photo.jpg"))

show("Video analyzer (mock)",
     mock_azure.content_understanding_analyze("video-scene", "./clip.mp4"))

print("\nAnalyzer schema → you define 'fields' with types (string, number,")
print("                  date, array<object>) in Foundry's Analyzer Studio.")
