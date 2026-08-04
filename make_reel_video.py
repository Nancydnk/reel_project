import os
import subprocess
import imageio_ffmpeg

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
    print(f"🎬 รวมคลิปส่วนที่ {i} สำเร็จ")

with open('list.txt', 'w') as f:
    for i in range(1, 5):
        f.write(f"file 'slides/part_{i}.mp4'\n")

subprocess.run([
    ffmpeg_bin, "-y", "-f", "concat", "-safe", "0",
    "-i", "list.txt", "-c", "copy", "reel.mp4"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists('list.txt'):
    os.remove('list.txt')

print("\n🎉 เรียบร้อย! ได้ไฟล์ reel.mp4 ในโฟลเดอร์ reel_project พร้อมส่งงานแล้วครับ!")
