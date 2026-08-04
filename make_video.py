import os
import subprocess

# รวมไฟล์ audio 1-4 เป็นไฟล์เดียว
with open('concat.txt', 'w') as f:
    for i in range(1, 5):
        f.write(f"file 'slides/audio_{i}.mp3'\n")

print("🎵 กำลังรวมไฟล์เสียงทั้งหมด...")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-c", "copy", "slides/full_audio.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("🎥 กำลังแปลงไฟล์และรวมเป็น reel.mp4...")
# รวมไฟล์เสียงเต็มเข้ากับวิดีโอ
subprocess.run(["ffmpeg", "-y", "-i", "slides/full_audio.mp3", "-c:a", "aac", "reel.mp4"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists('concat.txt'):
    os.remove('concat.txt')

print("🎉 สำเร็จแล้ว! ไฟล์ reel.mp4 ถูกสร้างเรียบร้อยแล้วในโฟลเดอร์งานครับ")
