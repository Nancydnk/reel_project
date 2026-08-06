#!/usr/bin/env python3
"""Build reel.mp4 from existing slides/*.html and slides/audio_*.mp3 files.

Reads slide HTML (never overwrites them), records animated slides with
Playwright, muxes each clip with narration audio, then stitches parts
together with varied smooth xfade transitions.
"""

from __future__ import annotations

import asyncio
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_PLAYWRIGHT_CACHE = Path.home() / "Library/Caches/ms-playwright"
if not os.environ.get("PLAYWRIGHT_BROWSERS_PATH") and DEFAULT_PLAYWRIGHT_CACHE.exists():
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(DEFAULT_PLAYWRIGHT_CACHE)

import imageio_ffmpeg
from playwright.async_api import async_playwright

SLIDES_DIR = ROOT / "slides"
TEMP_DIR = ROOT / "temp_video"
OUTPUT = ROOT / "reel.mp4"

VIEWPORT = {"width": 1080, "height": 1920}
AUDIO_PAD_S = 0.5
XFADE_S = 0.55

# Varied transitions between consecutive slides (ffmpeg xfade names).
TRANSITIONS = ["smoothleft", "zoomin", "slideright", "circleopen", "dissolve"]


def discover_slides() -> list[tuple[int, Path, Path]]:
    """Return sorted (index, html_path, audio_path) tuples."""
    html_files = sorted(
        SLIDES_DIR.glob("slide_*.html"),
        key=lambda p: int(re.search(r"slide_(\d+)\.html$", p.name).group(1)),
    )
    if not html_files:
        raise FileNotFoundError(f"No slide HTML files found in {SLIDES_DIR}")

    pairs: list[tuple[int, Path, Path]] = []
    for html_path in html_files:
        match = re.search(r"slide_(\d+)\.html$", html_path.name)
        if not match:
            continue
        idx = int(match.group(1))
        audio_path = SLIDES_DIR / f"audio_{idx}.mp3"
        if not audio_path.exists():
            raise FileNotFoundError(f"Missing narration audio: {audio_path}")
        pairs.append((idx, html_path, audio_path))

    print(f"Found {len(pairs)} slide(s):")
    for idx, html_path, audio_path in pairs:
        print(f"  slide {idx}: {html_path.name} + {audio_path.name}")
    return pairs


def get_ffmpeg() -> str:
    return imageio_ffmpeg.get_ffmpeg_exe()


def get_audio_duration(ffmpeg_bin: str, audio_path: Path) -> float:
    result = subprocess.run(
        [ffmpeg_bin, "-i", str(audio_path)],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        check=False,
    )
    for line in result.stderr.splitlines():
        if "Duration:" in line:
            time_str = line.split("Duration:")[1].split(",")[0].strip()
            hours, minutes, seconds = time_str.split(":")
            return float(hours) * 3600 + float(minutes) * 60 + float(seconds)
    raise RuntimeError(f"Could not read duration for {audio_path}")


def run_ffmpeg(cmd: list[str], label: str) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"ffmpeg failed while {label}")


async def record_slide_videos(
    slides: list[tuple[int, Path, Path]],
    durations: list[float],
) -> list[Path]:
    """Record each animated HTML slide as a WebM clip via Playwright."""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    recorded: list[Path] = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        for (idx, html_path, _), duration in zip(slides, durations):
            slide_temp = TEMP_DIR / f"capture_{idx}"
            if slide_temp.exists():
                shutil.rmtree(slide_temp)
            slide_temp.mkdir(parents=True)

            clip_duration = duration + AUDIO_PAD_S
            context = await browser.new_context(
                viewport=VIEWPORT,
                record_video_dir=str(slide_temp),
                record_video_size=VIEWPORT,
            )
            page = await context.new_page()
            url = html_path.resolve().as_uri()
            print(f"Recording {html_path.name} ({clip_duration:.2f}s)")
            await page.goto(url, wait_until="load")
            await page.wait_for_timeout(int(clip_duration * 1000))
            await context.close()

            webm_files = list(slide_temp.glob("*.webm"))
            if not webm_files:
                raise RuntimeError(f"No video captured for slide {idx}")
            dest = SLIDES_DIR / f"slide_{idx}.webm"
            shutil.move(str(webm_files[0]), str(dest))
            recorded.append(dest)
            shutil.rmtree(slide_temp, ignore_errors=True)

        await browser.close()

    return recorded


def build_slide_parts(
    ffmpeg_bin: str,
    slides: list[tuple[int, Path, Path]],
    webm_paths: list[Path],
    durations: list[float],
) -> list[Path]:
    parts: list[Path] = []
    for (idx, _, audio_path), webm_path, duration in zip(slides, webm_paths, durations):
        part_path = SLIDES_DIR / f"part_{idx}.mp4"
        clip_duration = duration + AUDIO_PAD_S
        cmd = [
            ffmpeg_bin,
            "-y",
            "-i",
            str(webm_path),
            "-i",
            str(audio_path),
            "-filter_complex",
            f"[0:v]trim=duration={clip_duration:.3f},setpts=PTS-STARTPTS,"
            f"scale=1080:1920:force_original_aspect_ratio=decrease,"
            f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v];"
            f"[1:a]apad=pad_dur={AUDIO_PAD_S}[a]",
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "20",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-pix_fmt",
            "yuv420p",
            "-shortest",
            str(part_path),
        ]
        print(f"Rendering part {idx} ({clip_duration:.2f}s)")
        run_ffmpeg(cmd, f"building {part_path.name}")
        parts.append(part_path)
    return parts


def concat_with_transitions(
    ffmpeg_bin: str,
    parts: list[Path],
    durations: list[float],
) -> None:
    if len(parts) == 1:
        shutil.copy2(parts[0], OUTPUT)
        return

    clip_lengths = [d + AUDIO_PAD_S for d in durations]
    inputs: list[str] = []
    for part in parts:
        inputs.extend(["-i", str(part)])

    filters: list[str] = []
    current_v = "0:v"
    offset = clip_lengths[0] - XFADE_S

    for i in range(1, len(parts)):
        transition = TRANSITIONS[(i - 1) % len(TRANSITIONS)]
        out_v = f"v{i}" if i < len(parts) - 1 else "vout"
        filters.append(
            f"[{current_v}][{i}:v]xfade=transition={transition}:duration={XFADE_S:.3f}:"
            f"offset={offset:.3f}[{out_v}]"
        )
        print(f"  transition {i}: {transition} at {offset:.2f}s")
        current_v = out_v
        offset += clip_lengths[i] - XFADE_S

    audio_concat = "".join(f"[{i}:a]" for i in range(len(parts)))
    filters.append(f"{audio_concat}concat=n={len(parts)}:v=0:a=1[aout]")

    cmd = [
        ffmpeg_bin,
        "-y",
        *inputs,
        "-filter_complex",
        ";".join(filters),
        "-map",
        "[vout]",
        "-map",
        "[aout]",
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        str(OUTPUT),
    ]
    print(f"Stitching {len(parts)} parts into {OUTPUT.name}")
    run_ffmpeg(cmd, "stitching final reel")


def cleanup_temp() -> None:
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR, ignore_errors=True)


def main() -> None:
    SLIDES_DIR.mkdir(exist_ok=True)
    cleanup_temp()

    slides = discover_slides()
    ffmpeg_bin = get_ffmpeg()
    durations = [get_audio_duration(ffmpeg_bin, audio_path) for _, _, audio_path in slides]
    print("Audio durations (s):", [round(d, 2) for d in durations])

    webm_paths = asyncio.run(record_slide_videos(slides, durations))
    parts = build_slide_parts(ffmpeg_bin, slides, webm_paths, durations)

    if OUTPUT.exists():
        OUTPUT.unlink()
    concat_with_transitions(ffmpeg_bin, parts, durations)
    cleanup_temp()

    print(f"Done — wrote {OUTPUT}")


if __name__ == "__main__":
    main()
