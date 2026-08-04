import os
import subprocess
import asyncio
import imageio_ffmpeg
from playwright.async_api import async_playwright

os.makedirs('slides', exist_ok=True)

# 1. ปรับดีไซน์สไลด์เป็นโทนสีสันสดใส ดูสนุกสนาน (Vibrant Playful Theme)
s1 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; background: linear-gradient(135deg, #1e1b4b, #311042); color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; text-align: center; padding: 60px; box-sizing: border-box; }
  .badge { background: linear-gradient(90deg, #ff007a, #7928ca); color: #ffffff; padding: 14px 36px; border-radius: 40px; font-weight: 900; font-size: 26px; letter-spacing: 2px; margin-bottom: 35px; box-shadow: 0 10px 25px rgba(255, 0, 122, 0.4); }
  h1 { font-size: 56px; line-height: 1.25; margin: 0 0 25px 0; background: linear-gradient(to right, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
  p { font-size: 30px; color: #e0e7ff; max-width: 900px; line-height: 1.5; margin: 0; font-weight: 600; }
</style>
</head>
<body>
  <div class="badge">🚀 AI AGENT PROJECT</div>
  <h1>Multimodal Fine Dining Consumer Insight Observer</h1>
  <p>Transforming traditional manual reviews into real-time, deep sentiment analytics.</p>
</body>
</html>"""

s2 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; background: linear-gradient(135deg, #0f172a, #1e1b4b); color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 60px; box-sizing: border-box; }
  .title { font-size: 46px; font-weight: 900; margin-bottom: 45px; text-align: center; background: linear-gradient(to right, #fbbf24, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .grid { display: flex; flex-direction: column; gap: 30px; }
  .card { border-radius: 28px; padding: 35px; box-sizing: border-box; }
  .card.prob { background: linear-gradient(135deg, #450a0a, #7f1d1d); border: 3px solid #f87171; box-shadow: 0 10px 20px rgba(239, 68, 68, 0.2); }
  .card.target { background: linear-gradient(135deg, #0c4a6e, #0369a1); border: 3px solid #38bdf8; box-shadow: 0 10px 20px rgba(56, 189, 248, 0.2); }
  .card-title { font-size: 34px; font-weight: 900; margin-bottom: 12px; }
  .card-text { font-size: 26px; color: #ffffff; line-height: 1.4; margin: 0; font-weight: 500; }
</style>
</head>
<body>
  <div class="title">✨ Bangkok Fine Dining Market</div>
  <div class="grid">
    <div class="card prob">
      <div class="card-title" style="color: #fca5a5;">⚠️ Problem</div>
      <div class="card-text">High acquisition costs & unorganized customer feedback leave operators blind to real issues.</div>
    </div>
    <div class="card target">
      <div class="card-title" style="color: #7dd3fc;">🎯 Target Audience</div>
      <div class="card-text">Fine dining owners needing deeper emotional & real-time sentiment analysis.</div>
    </div>
  </div>
</body>
</html>"""

s3 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; background: linear-gradient(135deg, #022c22, #0f172a); color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 60px; box-sizing: border-box; }
  .title { font-size: 44px; font-weight: 900; text-align: center; margin-bottom: 40px; background: linear-gradient(to right, #34d399, #00f2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .dashboard { background: rgba(30, 41, 59, 0.8); border-radius: 28px; border: 3px solid #334155; padding: 40px; backdrop-filter: blur(10px); }
  .bar-group { margin-bottom: 28px; }
  .bar-group:last-child { margin-bottom: 0; }
  .tag { font-size: 26px; color: #f8fafc; margin-bottom: 12px; font-weight: 700; display: block; }
  .bar-bg { background-color: #0f172a; height: 32px; border-radius: 16px; overflow: hidden; border: 1px solid #475569; }
  .bar-fill { height: 100%; border-radius: 16px; }
</style>
</head>
<body>
  <div class="title">📊 AI Real-Time Emotion Analysis</div>
  <div class="dashboard">
    <div class="bar-group">
      <span class="tag">Video Metadata Analysis (85%)</span>
      <div class="bar-bg"><div class="bar-fill" style="width: 85%; background: linear-gradient(90deg, #38bdf8, #818cf8);"></div></div>
    </div>
    <div class="bar-group">
      <span class="tag">Webcam Facial Tracking (92%)</span>
      <div class="bar-bg"><div class="bar-fill" style="width: 92%; background: linear-gradient(90deg, #f43f5e, #fb7185);"></div></div>
    </div>
    <div class="bar-group">
      <span class="tag">Qualitative Chat Sentiment (78%)</span>
      <div class="bar-bg"><div class="bar-fill" style="width: 78%; background: linear-gradient(90deg, #c084fc, #e879f9);"></div></div>
    </div>
  </div>
</body>
</html>"""

s4 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; background: linear-gradient(135deg, #1e1b4b, #0f172a); color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 50px; box-sizing: border-box; }
  .title { font-size: 46px; font-weight: 900; text-align: center; margin-bottom: 45px; background: linear-gradient(to right, #f472b6, #fb923c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
  .metric-card { background: rgba(30, 41, 59, 0.9); border-radius: 28px; padding: 35px 20px; text-align: center; border: 3px solid #475569; }
  .icon { font-size: 55px; margin-bottom: 10px; }
  .label { font-size: 26px; color: #cbd5e1; font-weight: 700; }
  .val { font-size: 42px; font-weight: 900; color: #34d399; margin-top: 8px; }
</style>
</head>
<body>
  <div class="title">🎉 Expected Outcomes</div>
  <div class="grid">
    <div class="metric-card">
      <div class="icon">🍽️</div>
      <div class="label">Food</div>
      <div class="val">+24%</div>
    </div>
    <div class="metric-card">
      <div class="icon">🍷</div>
      <div class="label">Ambience</div>
      <div class="val">+35%</div>
    </div>
    <div class="metric-card">
      <div class="icon">🤝</div>
      <div class="label">Service</div>
      <div class="val">+40%</div>
    </div>
    <div class="metric-card">
      <div class="icon">📈</div>
      <div class="label">Retention</div>
      <div class="val">BOOST</div>
    </div>
  </div>
</body>
</html>"""

with open('slides/slide_1.html', 'w', encoding='utf-8') as f: f.write(s1)
with open('slides/slide_2.html', 'w', encoding='utf-8') as f: f.write(s2)
with open('slides/slide_3.html', 'w', encoding='utf-8') as f: f.write(s3)
with open('slides/slide_4.html', 'w', encoding='utf-8') as f: f.write(s4)

# 2. แคปภาพสไลด์
async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        for i in range(1, 5):
            await page.goto(f"file://{os.path.abspath(f'slides/slide_{i}.html')}")
            await page.wait_for_timeout(800)
            await page.screenshot(path=f"slides/slide_{i}.png")
        await browser.close()

asyncio.run(capture())

ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

# 3. สร้างวิดีโอแยกส่วน
for i in range(1, 5):
    cmd = [
        ffmpeg_bin, "-y",
        "-loop", "1", "-i", f"slides/slide_{i}.png",
        "-i", f"slides/audio_{i}.mp3",
        "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-shortest",
        f"slides/part_{i}.mp4"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 4. ใส่ Transition แบบ Crossfade จางสลับ 0.3 วินาที (กำลังพอดี เนียน ไม่กวนตา)
filter_complex = (
    "[0:v][1:v]xfade=transition=fade:duration=0.3:offset=7[v12];"
    "[v12][2:v]xfade=transition=fade:duration=0.3:offset=14[v123];"
    "[v123][3:v]xfade=transition=fade:duration=0.3:offset=21[vout];"
    "[0:a][1:a][2:a][3:a]concat=n=4:v=0:a=1[aout]"
)

cmd_final = [
    ffmpeg_bin, "-y",
    "-i", "slides/part_1.mp4",
    "-i", "slides/part_2.mp4",
    "-i", "slides/part_3.mp4",
    "-i", "slides/part_4.mp4",
    "-filter_complex", filter_complex,
    "-map", "[vout]",
    "-map", "[aout]",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "reel.mp4"
]

subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("🎨 สำเร็จแล้วครับ! reel.mp4 ปรับสีสันสดใสสนุกขึ้น พร้อม Transition จางสลับฉากอย่างเนียนเรียบร้อยครับ!")
