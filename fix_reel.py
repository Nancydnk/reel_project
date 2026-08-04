import os
import subprocess
import asyncio
import imageio_ffmpeg
from playwright.async_api import async_playwright

os.makedirs('slides', exist_ok=True)

# 1. เขียนไฟล์ HTML ใหม่ที่เน้นความคมชัด อ่านง่าย 100% (High Contrast)
s1 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; background-color: #0d1117; color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; text-align: center; padding: 60px; box-sizing: border-box; }
  .badge { background-color: #8b5cf6; color: #ffffff; padding: 14px 32px; border-radius: 40px; font-weight: 800; font-size: 26px; letter-spacing: 2px; margin-bottom: 40px; text-transform: uppercase; }
  h1 { font-size: 56px; line-height: 1.25; margin: 0 0 30px 0; color: #38bdf8; font-weight: 900; }
  p { font-size: 32px; color: #e2e8f0; max-width: 900px; line-height: 1.6; margin: 0; font-weight: 500; }
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
<meta charset="utf-8">
<style>
  body { margin: 0; background-color: #0d1117; color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 60px; box-sizing: border-box; }
  .title { font-size: 46px; font-weight: 800; margin-bottom: 50px; color: #ffffff; text-align: center; }
  .grid { display: flex; flex-direction: column; gap: 35px; }
  .card { border-radius: 24px; padding: 40px; box-sizing: border-box; }
  .card.prob { background-color: #2a1215; border: 3px solid #f87171; }
  .card.target { background-color: #0c2a38; border: 3px solid #38bdf8; }
  .card-title { font-size: 36px; font-weight: 800; margin-bottom: 16px; }
  .card-text { font-size: 28px; color: #f1f5f9; line-height: 1.5; margin: 0; }
</style>
</head>
<body>
  <div class="title">Bangkok Fine Dining Market</div>
  <div class="grid">
    <div class="card prob">
      <div class="card-title" style="color: #f87171;">⚠️ Problem</div>
      <div class="card-text">High acquisition costs & unorganized customer feedback leave operators blind to real issues.</div>
    </div>
    <div class="card target">
      <div class="card-title" style="color: #38bdf8;">🎯 Target Audience</div>
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
  body { margin: 0; background-color: #0d1117; color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 60px; box-sizing: border-box; }
  .title { font-size: 44px; font-weight: 800; text-align: center; margin-bottom: 40px; color: #4ade80; }
  .dashboard { background-color: #161b22; border-radius: 24px; border: 3px solid #30363d; padding: 40px; }
  .bar-group { margin-bottom: 30px; }
  .bar-group:last-child { margin-bottom: 0; }
  .tag { font-size: 26px; color: #ffffff; margin-bottom: 12px; font-weight: 700; display: block; }
  .bar-bg { background-color: #21262d; height: 32px; border-radius: 16px; overflow: hidden; border: 1px solid #484f58; }
  .bar-fill { height: 100%; border-radius: 16px; }
</style>
</head>
<body>
  <div class="title">AI Real-Time Emotion Analysis</div>
  <div class="dashboard">
    <div class="bar-group">
      <span class="tag">Video Metadata Analysis (85%)</span>
      <div class="bar-bg"><div class="bar-fill" style="width: 85%; background-color: #38bdf8;"></div></div>
    </div>
    <div class="bar-group">
      <span class="tag">Webcam Facial Tracking (92%)</span>
      <div class="bar-bg"><div class="bar-fill" style="width: 92%; background-color: #f43f5e;"></div></div>
    </div>
    <div class="bar-group">
      <span class="tag">Qualitative Chat Sentiment (78%)</span>
      <div class="bar-bg"><div class="bar-fill" style="width: 78%; background-color: #a855f7;"></div></div>
    </div>
  </div>
</body>
</html>"""

s4 = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { margin: 0; background-color: #0d1117; color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 50px; box-sizing: border-box; }
  .title { font-size: 46px; font-weight: 800; text-align: center; margin-bottom: 50px; color: #ffffff; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
  .metric-card { background-color: #161b22; border-radius: 24px; padding: 35px 20px; text-align: center; border: 3px solid #30363d; }
  .icon { font-size: 55px; margin-bottom: 12px; }
  .label { font-size: 26px; color: #94a3b8; font-weight: 700; }
  .val { font-size: 42px; font-weight: 900; color: #4ade80; margin-top: 8px; }
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

# 2. แคปภาพสไลด์โดยสั่งให้รอ 1 วินาทีเต็ม เพื่อให้เรนเดอร์สีสมบูรณ์
async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        for i in range(1, 5):
            await page.goto(f"file://{os.path.abspath(f'slides/slide_{i}.html')}")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=f"slides/slide_{i}.png")
        await browser.close()

asyncio.run(capture())

# 3. รวมสไลด์ภาพนิ่งเข้ากับไฟล์เสียงพากย์เดิม
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

print("✅ สำเร็จแล้วครับ! สร้างไฟล์ reel.mp4 แบบตัวอักษรและกราฟิกสว่าง คมชัด อ่านง่าย 100% เรียบร้อยครับ")
