"""Day 3 · Script 2 — Multimodal understanding: captions, Q&A over images.

Exam objective → "Build a solution that analyzes visual context by using
multimodal models" + alt-text generation + visual Q&A.

Live code
---------
r = client.responses.create(
    model="gpt-4o",
    input=[{"role":"user","content":[
        {"type":"input_text","text":"Describe this for a screen reader."},
        {"type":"input_image","image_url":"https://..."}]}])
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

request = [{"role": "user", "content": [
    {"type": "input_text",  "text": "Produce alt-text (<125 chars)."},
    {"type": "input_image", "image_url": "https://example.com/photo.jpg"}]}]

r = mock_azure.responses_create(model="gpt-4o", input_=request) if USE_MOCK else None
show("Multimodal response", r)

print("\nAlt-text rules → describe FUNCTION, not every pixel; omit 'image of'.")
print("For long descriptions use `aria-describedby` with the extended text.")
