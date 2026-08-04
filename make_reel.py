import json
import os
import subprocess
from gtts import gTTS

# Load slide plan
with open('ai_grading/slide_plan.json', 'r', encoding='utf-8') as f:
    plan = json.load(f)

# Convert HTML slides to Images or text video layout using ffmpeg/python
slides = plan.get("slides", [])

print("🎬 Generating voiceover and video components...")

for i, slide in enumerate(slides, 1):
    narration = slide.get("narration", "Slide " + str(i))
    tts = gTTS(text=narration, lang='en')
    tts.save(f"slides/audio_{i}.mp3")
    print(f"✅ Generated audio for Slide {i}")

print("✨ Processing video layout for reel.mp4...")
