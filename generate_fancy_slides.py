import os
import subprocess
import asyncio
import imageio_ffmpeg
from playwright.async_api import async_playwright

os.makedirs('slides', exist_ok=True)

s1 = """<!DOCTYPE html>
<html>
<head>
<style>
  body { margin: 0; background: #0B0F19; color: #fff; font-family: 'Segoe UI', system-ui, sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; text-align: center; padding: 40px; box-sizing: border-box; overflow: hidden; }
  .badge { background: linear-gradient(135deg, #FF007A, #7928CA); padding: 12px 28px; border-radius: 30px; font-weight: 800; font-size: 24px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 30px; box-shadow: 0 0 20px rgba(255,0,122,0.5); }
  h1 { font-size: 52px; line-height: 1.2; margin: 0 0 20px 0; background: linear-gradient(to right, #00F2FE, #4FACFE); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
  p { font-size: 28px; color: #94A3B8; max-width: 800px; line-height: 1.5; margin: 0; }
</style>
</head>
<body>
<div class="badge">AI AGENT PROJECT</div>
<h1>Multimodal Fine Dining Consumer Insight Observer</h1>
<p>Transforming traditional manual reviews into real-time, deep sentiment analytics.</p>
</body>
</html>"""

s2 = """<!DOCTYPE html>
<html>
<head>
<style>
  body { margin: 0; background: #0B0F19; color: #fff; font-family: 'Segoe UI', system-ui, sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 60px; box-sizing: border-box; }
  .title { font-size: 40px; font-weight: 800; margin-bottom: 40px; color: #F8FAFC; text-align: center; }
  .grid { display: flex; flex-direction: column; gap: 30px; }
  .card { background: rgba(255,255,255,0.03); border: 2px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 35px; }
  .card.prob { border-color: #FF4B4B; background: rgba(255,75,75,0.08); }
  .card.target { border-color: #00E5FF; background: rgba(0,229,255,0.08); }
  .card-title { font-size: 32px; font-weight: 800; margin-bottom: 12px; }
  .card-text { font-size: 24px; color: #CBD5E1; line-height: 1.4; margin: 0; }
</style>
</head>
<body>
<div class="title">Bangkok Fine Dining Market</div>
<div class="grid">
  <div class="card prob">
    <div class="card-title" style="color: #FF4B4B;">⚠️ Problem</div>
    <div class="card-text">High acquisition costs & unorganized customer feedback leave operators blind to real issues.</div>
  </div>
  <div class="card target">
    <div class="card-title" style="color: #00E5FF;">🎯 Target Audience</div>
    <div class="card-text">Fine dining owners needing deeper emotional & real-time sentiment analysis.</div>
  </div>
</div>
</body>
</html>"""

s3 = """<!DOCTYPE html>
<html>
<head>
<style>
  body { margin: 0; background: #0B0F19; color: #fff; font-family: 'Segoe UI', system-ui, sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 50px; box-sizing: border-box; }
  .title { font-size: 38px; font-weight: 800; text-align: center; margin-bottom: 30px; background: linear-gradient(to right, #00FF87, #60EFFF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .dashboard { background: #1E293B; border-radius: 20px; border: 2px solid #334155; padding: 30px; }
  .dash-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 15px; border-bottom: 1px solid #334155; margin-bottom: 25px; }
  .dots { display: flex; gap: 8px; }
  .dot { width: 14px; height: 14px; border-radius: 50%; }
  .bar-chart { display: flex; flex-direction: column; gap: 15px; }
  .bar-bg { background: #0F172A; height: 24px; border-radius: 12px; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 12px; }
  .tag { font-size: 20px; color: #CBD5E1; margin-bottom: 5px; font-weight: 600; }
</style>
</head>
<body>
<div class="title">AI Real-Time Emotion Analysis</div>
<div class="dashboard">
  <div class="dash-header">
    <div class="dots">
      <div class="dot" style="background:#FF5F56"></div>
      <div class="dot" style="background:#FFBD2E"></div>
      <div class="dot" style="background:#27C93F"></div>
    </div>
    <span style="font-size: 18px; color: #00FF87; font-weight: bold;">LIVE TRACKING</span>
  </div>
  <div class="bar-chart">
    <div class="tag">Video Metadata Analysis</div>
    <div class="bar-bg"><div class="bar-fill" style="width: 85%; background: #00E5FF;"></div></div>
    <div class="tag">Webcam Facial Tracking</div>
    <div class="bar-bg"><div class="bar-fill" style="width: 92%; background: #FF007A;"></div></div>
    <div class="tag">Qualitative Chat Sentiment</div>
    <div class="bar-bg"><div class="bar-fill" style="width: 78%; background: #7928CA;"></div></div>
  </div>
</div>
</body>
</html>"""

s4 = """<!DOCTYPE html>
<html>
<head>
<style>
  body { margin: 0; background: #0B0F19; color: #fff; font-family: 'Segoe UI', system-ui, sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 50px; box-sizing: border-box; }
  .title { font-size: 40px; font-weight: 800; text-align: center; margin-bottom: 40px; color: #F8FAFC; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .metric-card { background: #1E293B; border-radius: 20px; padding: 30px; text-align: center; border: 2px solid #334155; }
  .icon { font-size: 45px; margin-bottom: 10px; }
  .label { font-size: 22px; color: #94A3B8; font-weight: 600; }
  .val { font-size: 36px; font-weight: 800; color: #00FF87; margin-top: 5px; }
</style>
</head>
<body>
<div class="title">Expected Outcomes</div>
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

print("🎨 1. อัปเดตสไลด์ HTML ชุดใหม่เรียบร้อย!")

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        for i in range(1, 5):
            await page.goto(f"file://{os.path.abspath(f'slides/slide_{i}.html')}")
            await page.screenshot(path=f"slides/slide_{i}.png")
            print(f"📸 2. แคปภาพสไลด์ {i} โฉมใหม่สำเร็จ")
        await browser.close()

asyncio.run(capture())

ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

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

with open('list.txt', 'w') as f:
    for i in range(1, 5):
        f.write(f"file 'slides/part_{i}.mp4'\n")

subprocess.run([
    ffmpeg_bin, "-y", "-f", "concat", "-safe", "0",
    "-i", "list.txt", "-c", "copy", "reel.mp4"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists('list.txt'):
    os.remove('list.txt')

print("\n🎉 3. รวมวิดีโอสร้างไฟล์ reel.mp4 โฉมใหม่สำเร็จ 100%!")
