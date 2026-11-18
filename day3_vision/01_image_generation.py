"""Day 3 · Script 1 — Image generation (text-to-image + mask edits).

Exam objective → "Implement a solution that generates images from text
prompts and reference media" + "image-editing workflows, including
inpainting, mask-based edits, and prompt-driven modifications."

Live code
---------
from openai import AzureOpenAI
client = AzureOpenAI(...)

# Generate
img = client.images.generate(model="gpt-image-1", prompt="...",
                             size="1024x1024", n=1)

# Edit with a mask (inpainting)
with open("original.png","rb") as src, open("mask.png","rb") as mask:
    edit = client.images.edit(model="gpt-image-1",
                              image=src, mask=mask,
                              prompt="replace the sky with a sunset")
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import show, USE_MOCK
import mock_azure

show("Generate", mock_azure.images_generate(
    prompt="A serene Table Mountain sunrise, photorealistic", size="1024x1024"))

show("Edit (mask inpainting) request shape", {
    "model": "gpt-image-1",
    "image": "<original.png bytes>",
    "mask":  "<mask.png bytes — transparent where you want the edit>",
    "prompt": "Replace the sky with a sunset"})

print("\nTrap → mask is TRANSPARENT where you want the model to paint.")
print("Trap → video generation is a separate model (Sora) wired through Foundry.")
