import os
import subprocess
import asyncio
import imageio_ffmpeg
from playwright.async_api import async_playwright

os.makedirs('slides', exist_ok=True)

# 1. HTML สไลด์พร้อม CSS Keyframe Animation
s1 = """<!DOCTYPE html>
<html>
<head>
<style>
  @keyframes fadeInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
  @keyframes pulseGlow { 0% { box-shadow: 0 0 15px rgba(255,0,122,0.4); } 50% { box-shadow: 0 0 35px rgba(255,0,122,0.8); } 100% { box-shadow: 0 0 15px rgba(255,0,122,0.4); } }
  body { margin: 0; background: #0B0F19; color: #fff; font-family: 'Segoe UI', system-ui, sans-serif; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; text-align: center; padding: 40px; box-sizing: border-box; overflow: hidden; }
  .badge { background: linear-gradient(135deg, #FF007A, #7928CA); padding: 12px 28px; border-radius: 30px; font-weight: 800; font-size: 24px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 30px; animation: fadeInDown 1s ease-out, pulseGlow 2s infinite; }
  h1 { font-size: 52px; line-height: 1.2; margin: 0 0 20px 0; background: linear-gradient(to right, #00F2FE, #4FACFE); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; animation: fadeInDown 1.2s ease-out; }
  p { font-size: 28px; color: #94A3B8; max-width: 800px; line-height: 1.5; margin: 0; animation: fadeInDown 1.4s ease-out; }
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
  @keyframes slideInLeft { from { opacity: 0; transform: translateX(-50px); } to { opacity: 1; transform: translateX(0); } }
  @keyframes slideInRight { from { opacity: 0; transform: translateX(50px); } to { opacity: 1; transform: translateX(0); } }
  body { margin: 0; background: #0B0F19; color: #fff; font-family: 'Segoe UI', system-ui, sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 60px; box-sizing: border-box; }
  .title { font-size: 40px; font-weight: 800; margin-bottom: 40px; color: #F8FAFC; text-align: center; }
  .grid { display: flex; flex-direction: column; gap: 30px; }
  .card { background: rgba(255,255,255,0.03); border: 2px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 35px; }
  .card.prob { border-color: #FF4B4B; background: rgba(255,75,75,0.08); animation: slideInLeft 1s ease-out; }
  .card.target { border-color: #00E5FF; background: rgba(0,229,255,0.08); animation: slideInRight 1s ease-out; }
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
  @keyframes growBar { from { width: 0%; } }
  body { margin: 0; background: #0B0F19; color: #fff; font-family: 'Segoe UI', system-ui, sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 50px; box-sizing: border-box; }
  .title { font-size: 38px; font-weight: 800; text-align: center; margin-bottom: 30px; background: linear-gradient(to right, #00FF87, #60EFFF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .dashboard { background: #1E293B; border-radius: 20px; border: 2px solid #334155; padding: 30px; }
  .dash-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 15px; border-bottom: 1px solid #334155; margin-bottom: 25px; }
  .dots { display: flex; gap: 8px; }
  .dot { width: 14px; height: 14px; border-radius: 50%; }
  .bar-chart { display: flex; flex-direction: column; gap: 15px; }
  .bar-bg { background: #0F172A; height: 24px; border-radius: 12px; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 12px; animation: growBar 1.5s ease-out; }
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
  @keyframes popIn { 0% { transform: scale(0.8); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
  body { margin: 0; background: #0B0F19; color: #fff; font-family: 'Segoe UI', system-ui, sans-serif; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 50px; box-sizing: border-box; }
  .title { font-size: 40px; font-weight: 800; text-align: center; margin-bottom: 40px; color: #F8FAFC; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .metric-card { background: #1E293B; border-radius: 20px; padding: 30px; text-align: center; border: 2px solid #334155; animation: popIn 0.8s ease-out; }
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

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        for i in range(1, 5):
            await page.goto(f"file://{os.path.abspath(f'slides/slide_{i}.html')}")
            await page.screenshot(path=f"slides/slide_{i}.png")
        await browser.close()

asyncio.run(capture())

ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

print("🎥 กำลังสร้างวิดีโอที่มีทั้ง Camera Zoom In Motion และ Transition Effect...")

# สร้างคลิปที่มีการค่อยๆ Zoom In (Ken Burns Effect) ตลอดเวลา
for i in range(1, 5):
    cmd = [
        ffmpeg_bin, "-y",
        "-loop", "1", "-i", f"slides/slide_{i}.png",
        "-i", f"slides/audio_{i}.mp3",
        "-filter_complex", "zoompan=z='min(zoom+0.0015,1.15)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920",
        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-shortest",
        f"slides/part_{i}.mp4"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

filter_complex = (
    "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=7[v12];"
    "[v12][2:v]xfade=transition=fade:duration=0.5:offset=14[v123];"
    "[v123][3:v]xfade=transition=fade:duration=0.5:offset=21[vout];"
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

print("\n🎉 เรียบร้อย! ไฟล์ reel.mp4 มี Motion และกล้องซูมลื่นไหลสุดๆ แล้วครับ!")
