#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, subprocess

OUTDIR = os.path.dirname(os.path.abspath(__file__))
manifest = json.load(open(os.path.join(OUTDIR, "manifest_v2.json"), encoding="utf-8"))
AUDIO = "/Users/karen/Documents/Sunny Words.m4a"

concat_path = os.path.join(OUTDIR, "concat_v2.txt")
with open(concat_path, "w", encoding="utf-8") as f:
    for item in manifest:
        f.write(f"file '{item['file']}'\n")
        f.write(f"duration {item['duration']}\n")
    f.write(f"file '{manifest[-1]['file']}'\n")

OUT = os.path.join(OUTDIR, "sunny_words_v2_musicplayer.mp4")
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_path,
    "-i", AUDIO,
    "-map", "0:v", "-map", "1:a",
    "-vf", "scale=1080:1920,format=yuv420p",
    "-c:v", "libx264", "-r", "30", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    OUT,
]
subprocess.run(cmd, check=True)
print(f"✅ 输出 → {OUT}")
