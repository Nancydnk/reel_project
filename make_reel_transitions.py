import os
import subprocess
import imageio_ffmpeg

ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

print("🎬 กำลังสร้างวิดีโอพร้อม Transition Effect (Fade / Crossfade)...")

# คำสั่ง FFmpeg Filter Complex สำหรับเชื่อม 4 คลิปเข้าด้วยกันพร้อมเอฟเฟกต์ Crossfade 0.5 วินาที
filter_complex = (
    "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=7[v12];"
    "[v12][2:v]xfade=transition=fade:duration=0.5:offset=14[v123];"
    "[v123][3:v]xfade=transition=fade:duration=0.5:offset=21[vout];"
    "[0:a][1:a][2:a][3:a]concat=n=4:v=0:a=1[aout]"
)

cmd = [
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

subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("\n🎉 เรียบร้อย! เพิ่ม Transition Effect ใส่ใน reel.mp4 สำเร็จแล้วครับ!")
