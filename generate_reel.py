import json
import os
from gtts import gTTS

# Read slide_plan.json
with open('ai_grading/slide_plan.json', 'r', encoding='utf-8') as f:
    plan = json.load(f)

if isinstance(plan, list):
    slides = plan
elif isinstance(plan, dict):
    slides = plan.get("slides", plan.get("plan", []))
else:
    slides = []

print(f"🎬 Found {len(slides)} slides. Generating voiceover with gTTS...")

for i, slide in enumerate(slides, 1):
    narration = slide.get("narration", f"Slide {i} presentation")
    speech_path = f"slides/audio_{i}.mp3"
    
    print(f"🎙️ Generating voice for Slide {i}...")
    
    # Generate high-quality English voiceover
    tts = gTTS(text=narration, lang='en', tld='com')
    tts.save(speech_path)
            
    print(f"✅ Created: {speech_path}")

print("\n🎉 All audio files generated successfully in slides/ folder!")
