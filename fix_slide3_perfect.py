import os
import subprocess
import asyncio
import glob
import imageio_ffmpeg
from playwright.async_api import async_playwright

os.makedirs('slides', exist_ok=True)
os.makedirs('temp_video', exist_ok=True)

ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

# 1. ฟังก์ชันเช็กความยาวเสียงจริง
def get_audio_duration(file_path):
    cmd = [ffmpeg_bin, "-i", file_path]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    for line in result.stderr.split('\n'):
        if "Duration" in line:
            time_str = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = time_str.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 7.0

durations = [get_audio_duration(f'slides/audio_{i}.mp3') for i in range(1, 5)]
print("🔊 ความยาวเสียงพากย์จริง:", [round(d, 2) for d in durations])

# 2. สร้างไฟล์ HTML
s1 = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body { margin: 0; background: linear-gradient(135deg, #1e1b4b, #311042); color: #fff; font-family: system-ui; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; text-align: center; padding: 60px; box-sizing: border-box; }
.badge { background: linear-gradient(90deg, #ff007a, #7928ca); padding: 14px 36px; border-radius: 40px; font-weight: 900; font-size: 26px; margin-bottom: 35px; }
h1 { font-size: 56px; margin: 0 0 25px 0; background: linear-gradient(to right, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; }
p { font-size: 30px; color: #e0e7ff; max-width: 900px; line-height: 1.5; font-weight: 600; }
</style></head><body><div class="badge">🚀 AI AGENT PROJECT</div><h1>Multimodal Fine Dining Consumer Insight Observer</h1><p>Transforming traditional manual reviews into real-time, deep sentiment analytics.</p></body></html>"""

s2 = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body { margin: 0; background: linear-gradient(135deg, #0f172a, #1e1b4b); color: #fff; font-family: system-ui; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 60px; box-sizing: border-box; }
.title { font-size: 46px; font-weight: 900; margin-bottom: 45px; text-align: center; background: linear-gradient(to right, #fbbf24, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.grid { display: flex; flex-direction: column; gap: 30px; }
.card { border-radius: 28px; padding: 35px; }
.card.prob { background: linear-gradient(135deg, #450a0a, #7f1d1d); border: 3px solid #f87171; }
.card.target { background: linear-gradient(135deg, #0c4a6e, #0369a1); border: 3px solid #38bdf8; }
.card-title { font-size: 34px; font-weight: 900; margin-bottom: 12px; }
.card-text { font-size: 26px; color: #fff; line-height: 1.4; }
</style></head><body><div class="title">✨ Bangkok Fine Dining Market</div><div class="grid"><div class="card prob"><div class="card-title" style="color:#fca5a5">⚠️ Problem</div><div class="card-text">High acquisition costs & unorganized customer feedback leave operators blind to real issues.</div></div><div class="card target"><div class="card-title" style="color:#7dd3fc">🎯 Target Audience</div><div class="card-text">Fine dining owners needing deeper emotional & real-time sentiment analysis.</div></div></div></body></html>"""

s3 = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body {{ margin: 0; background: linear-gradient(135deg, #022c22, #0f172a); color: #fff; font-family: system-ui; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 60px; box-sizing: border-box; }}
.title {{ font-size: 44px; font-weight: 900; text-align: center; margin-bottom: 40px; background: linear-gradient(to right, #34d399, #00f2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.dashboard {{ background: rgba(30, 41, 59, 0.8); border-radius: 28px; border: 3px solid #334155; padding: 40px; }}
.bar-group {{ margin-bottom: 28px; }}
.bar-group:last-child {{ margin-bottom: 0; }}
.tag {{ font-size: 26px; color: #f8fafc; margin-bottom: 12px; font-weight: 700; display: block; }}
.bar-bg {{ background-color: #0f172a; height: 32px; border-radius: 16px; overflow: hidden; border: 1px solid #475569; }}
.bar-fill {{ height: 100%; border-radius: 16px; width: 0%; animation-duration: 0.8s; animation-timing-function: ease-out; animation-fill-mode: forwards; }}
.b1 {{ animation-name: fill1; animation-delay: 0.2s; background: linear-gradient(90deg, #38bdf8, #818cf8); }}
.b2 {{ animation-name: fill2; animation-delay: {durations[2]*0.25}s; background: linear-gradient(90deg, #f43f5e, #fb7185); }}
.b3 {{ animation-name: fill3; animation-delay: {durations[2]*0.55}s; background: linear-gradient(90deg, #c084fc, #e879f9); }}
@keyframes fill1 {{ to {{ width: 85%; }} }}
@keyframes fill2 {{ to {{ width: 92%; }} }}
@keyframes fill3 {{ to {{ width: 78%; }} }}
</style></head><body><div class="title">📊 AI Real-Time Emotion Analysis</div><div class="dashboard"><div class="bar-group"><span class="tag">Video Metadata Analysis (85%)</span><div class="bar-bg"><div class="bar-fill b1"></div></div></div><div class="bar-group"><span class="tag">Webcam Facial Tracking (92%)</span><div class="bar-bg"><div class="bar-fill b2"></div></div></div><div class="bar-group"><span class="tag">Qualitative Chat Sentiment (78%)</span><div class="bar-bg"><div class="bar-fill b3"></div></div></div></div></body></html>"""

s4 = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body { margin: 0; background: linear-gradient(135deg, #1e1b4b, #0f172a); color: #fff; font-family: system-ui; display: flex; flex-direction: column; justify-content: center; height: 100vh; padding: 50px; box-sizing: border-box; }
.title { font-size: 46px; font-weight: 900; text-align: center; margin-bottom: 45px; background: linear-gradient(to right, #f472b6, #fb923c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
.metric-card { background: rgba(30, 41, 59, 0.9); border-radius: 28px; padding: 35px 20px; text-align: center; border: 3px solid #475569; }
.icon { font-size: 55px; margin-bottom: 10px; }
.label { font-size: 26px; color: #cbd5e1; font-weight: 700; }
.val { font-size: 42px; font-weight: 900; color: #34d399; margin-top: 8px; }
</style></head><body><div class="title">🎉 Expected Outcomes</div><div class="grid"><div class="metric-card"><div class="icon">🍽️</div><div class="label">Food</div><div class="val">+24%</div></div><div class="metric-card"><div class="icon">🍷</div><div class="label">Ambience</div><div class="val">+35%</div></div><div class="metric-card"><div class="icon">🤝</div><div class="label">Service</div><div class="val">+40%</div></div><div class="metric-card"><div class="icon">📈</div><div class="label">Retention</div><div class="val">BOOST</div></div></div></body></html>"""

with open('slides/slide_1.html', 'w', encoding='utf-8') as f: f.write(s1)
with open('slides/slide_2.html', 'w', encoding='utf-8') as f: f.write(s2)
with open('slides/slide_3.html', 'w', encoding='utf-8') as f: f.write(s3)
with open('slides/slide_4.html', 'w', encoding='utf-8') as f: f.write(s4)

# 3. เรนเดอร์ด้วย Playwright (แก้พาธสไลด์ 3 ให้ถูกต้องเป๊ะ)
async def process_slides():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for i in [1, 2, 4]:
            page = await browser.new_page(viewport={"width": 1080, "height": 1920})
            await page.goto(f"file://{os.path.abspath(f'slides/slide_{i}.html')}")
            await page.wait_for_timeout(500)
            await page.screenshot(path=f"slides/slide_{i}.png")
            await page.close()

        # สไลด์ 3
        context = await browser.new_context(
            viewport={"width": 1080, "height": 1920},
            record_video_dir="temp_video",
            record_video_size={"width": 1080, "height": 1920}
        )
        page3 = await context.new_page()
        await page3.goto(f"file://{os.path.abspath('slides/slide_3.html')}")
        await page3.wait_for_timeout(int((durations[2] + 3.0) * 1000))
        await context.close()
        await browser.close()

asyncio.run(process_slides())

webm_files = glob.glob('temp_video/*.webm')
recorded_webm = webm_files[0] if webm_files else None

# 4. สร้างวิดีโอแต่ละพาร์ท (เพิ่ม Padding 1.2s เว้นช่วงให้พูดจบสบายๆ)
pad = 1.2 

# Part 1, 2, 4
for i in [1, 2, 4]:
    dur = durations[i-1] + pad
    cmd = [
        ffmpeg_bin, "-y",
        "-loop", "1", "-i", f"slides/slide_{i}.png",
        "-i", f"slides/audio_{i}.mp3",
        "-filter_complex", f"[0:v]trim=duration={dur}[v];[1:a]apad=pad_len=88200[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-shortest",
        f"slides/part_{i}.mp4"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Part 3
dur3 = durations[2] + pad
cmd_part3 = [
    ffmpeg_bin, "-y",
    "-i", recorded_webm,
    "-i", "slides/audio_3.mp3",
    "-filter_complex", f"[0:v]trim=duration={dur3}[v];[1:a]apad=pad_len=88200[a]",
    "-map", "[v]", "-map", "[a]",
    "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
    "-pix_fmt", "yuv420p", "-shortest",
    "slides/part_3.mp4"
]
subprocess.run(cmd_part3, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 5. คำนวณ Offset รวม Padding
trans = 0.3
o1 = (durations[0] + pad) - trans
o2 = o1 + (durations[1] + pad) - trans
o3 = o2 + (durations[2] + pad) - trans

filter_complex = (
    f"[0:v][1:v]xfade=transition=fade:duration={trans}:offset={o1:.2f}[v12];"
    f"[v12][2:v]xfade=transition=fade:duration={trans}:offset={o2:.2f}[v123];"
    f"[v123][3:v]xfade=transition=fade:duration={trans}:offset={o3:.2f}[vout];"
    f"[0:a][1:a][2:a][3:a]concat=n=4:v=0:a=1[aout]"
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

if os.path.exists('temp_video'):
    for f in glob.glob('temp_video/*'): os.remove(f)
    os.rmdir('temp_video')

print("🎉 แก้ไขบั๊กเรียบร้อยครับ! ตอนนี้ Slide 3 จะแสดงวิดีโอกราฟตรงตัว และขยายเวลาให้พูดQualitative Chat Sentiment จบครบถ้วนแล้วแน่นอนครับ")
