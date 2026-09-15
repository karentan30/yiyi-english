#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sunny Words · 音乐播放器风格样式(仿小红书爆款) · 双语歌词滚动条
"""
import os, sys, json

sys.path.insert(0, "/Users/karen/projects/yiyi-english/docs/card-templates")
from gen_cards import render

IMG_PATH = "/Users/karen/projects/yiyi-english/docs/card-templates/生成/一诺妈/素材-唱歌小孩/唱歌小孩_02.png"
OUTDIR = os.path.dirname(os.path.abspath(__file__))
FRAMES_DIR = os.path.join(OUTDIR, "frames_v2")
os.makedirs(FRAMES_DIR, exist_ok=True)

FONT = '"PingFang SC","Microsoft YaHei",Arial,sans-serif'
W, H = 1080, 1920
TOTAL = 51.2

# (start, end, english, chinese)
LINES = [
    (0.00, 5.28, None, None),
    (5.28, 8.18, "One little duck goes for a walk", "一只小鸭去散步"),
    (8.18, 11.08, "Quack, quack, quack, hear it talk", "嘎嘎嘎，听它说话"),
    (11.08, 13.85, "Two little birds up in a tree", "两只小鸟在树上"),
    (13.85, 16.62, "Singing songs for you and me", "为你我唱着歌"),
    (16.62, 19.32, "La, la, la, come and play", "啦啦啦，一起玩耍"),
    (19.32, 22.02, "Sunny words for a sunny day", "阳光的日子说阳光的话"),
    (22.56, 25.16, "La, la, la, hand in hand", "啦啦啦，手拉手"),
    (25.16, 27.76, "Learning together, isn't it grand", "一起学习，多美好"),
    (27.76, 30.56, "Three little cats jump on the mat", "三只小猫跳上垫子"),
    (30.56, 33.36, "Clap your hands and pat, pat, pat", "拍拍手，啪啪啪"),
    (33.36, 36.16, "Four little frogs go hop, hop, hop", "四只青蛙跳跳跳"),
    (36.16, 38.96, "Dancing till they cannot stop", "跳舞跳到停不下来"),
    (38.96, 41.64, "La, la, la, come and play", "啦啦啦，一起玩耍"),
    (41.64, 44.32, "Sunny words for a sunny day", "阳光的日子说阳光的话"),
    (44.32, 47.18, "La, la, la, hand in hand", "啦啦啦，手拉手"),
    (47.18, 50.04, "Learning together, isn't it grand", "一起学习，多美好"),
    (50.04, 51.20, None, None),
]


def esc(s):
    if s is None:
        return ""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt_t(sec):
    m = int(sec // 60)
    s = int(sec % 60)
    return f"{m}:{s:02d}"


OPACITY_STEPS = [1.0, 0.92, 0.82, 0.72, 0.6, 0.48]


def lyric_stack_html(idx):
    """当前行 + 前面最多5行，做渐隐堆叠向上滚动的效果——歌词区域要占大半屏，方便照着唱"""
    history = [l for l in LINES[:idx + 1] if l[2] is not None]
    show = history[-6:]  # 最多显示6行(含当前行)
    rows = []
    n = len(show)
    for i, (_, _, en, zh) in enumerate(show):
        depth = n - 1 - i  # 0 = 当前行
        opacity = OPACITY_STEPS[depth] if depth < len(OPACITY_STEPS) else 0.4
        size_en = 62 if depth == 0 else 50
        size_zh = 38 if depth == 0 else 31
        cls = "cur" if depth == 0 else ""
        rows.append(
            f'<div class="lyric-line {cls}" style="opacity:{opacity}">'
            f'<div class="en" style="font-size:{size_en}px">{esc(en)}</div>'
            f'<div class="zh" style="font-size:{size_zh}px">{esc(zh)}</div>'
            f'</div>'
        )
    return "".join(rows)


def frame_html(idx, start, end):
    progress_pct = min(100, max(0, start / TOTAL * 100))
    lyric_html = lyric_stack_html(idx)
    return f'''<style>
* {{ margin:0; padding:0; box-sizing:border-box; font-family:{FONT}; }}
body {{ width:{W}px; height:{H}px; position:relative; overflow:hidden; background:#0a0a1a; }}
.bg-photo {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:top center; filter:brightness(0.92); }}
.top-scrim {{
  position:absolute; top:0; left:0; right:0; height:620px;
  background:linear-gradient(to bottom, rgba(8,10,30,0.88) 0%, rgba(8,10,30,0.72) 45%, rgba(8,10,30,0.25) 80%, transparent 100%);
}}
.header {{ position:absolute; top:56px; left:0; right:0; text-align:center; padding:0 50px; }}
.title-row {{ display:flex; align-items:center; justify-content:center; gap:16px; }}
.title {{
  font-size:52px; font-weight:900; letter-spacing:1px;
  background:linear-gradient(180deg,#eaf6ff,#8fd3ff);
  -webkit-background-clip:text; background-clip:text; color:transparent;
  text-shadow:0 0 18px rgba(90,180,255,0.55);
}}
.disc {{
  width:64px; height:64px; border-radius:50%;
  background:radial-gradient(circle at 50% 50%, #222 0 8px, #444 9px 12px, #111 13px 30px, #333 31px 32px);
  border:2px solid rgba(255,255,255,0.25);
  flex:none;
}}
.subtitle {{ margin-top:14px; font-size:30px; font-weight:700; color:#7CFFB2; text-shadow:0 0 10px rgba(60,255,150,0.4); }}
.progress-wrap {{ margin-top:38px; padding:0 30px; }}
.progress-times {{ display:flex; justify-content:space-between; font-size:24px; color:rgba(255,255,255,0.75); margin-bottom:10px; }}
.progress-bar {{ position:relative; height:6px; border-radius:3px; background:rgba(255,255,255,0.28); }}
.progress-fill {{ position:absolute; left:0; top:0; bottom:0; width:{progress_pct:.1f}%; background:#fff; border-radius:3px; }}
.progress-dot {{ position:absolute; top:50%; left:{progress_pct:.1f}%; transform:translate(-50%,-50%); width:20px; height:20px; border-radius:50%; background:#fff; box-shadow:0 0 10px rgba(255,255,255,0.7); }}
.controls {{ margin-top:36px; display:flex; align-items:center; justify-content:center; gap:56px; }}
.controls .icon {{ font-size:40px; color:#fff; opacity:0.85; }}
.controls .play-btn {{
  width:110px; height:110px; border-radius:50%; background:#fff;
  display:flex; align-items:center; justify-content:center; font-size:46px; color:#111;
  box-shadow:0 8px 24px rgba(0,0,0,0.35);
}}
.lyrics-scrim {{
  position:absolute; left:0; right:0; top:840px; bottom:170px;
  background:linear-gradient(to bottom,
    transparent 0%,
    rgba(6,8,20,0.45) 10%,
    rgba(6,8,20,0.72) 30%,
    rgba(6,8,20,0.88) 55%,
    rgba(6,8,20,0.94) 100%);
}}
.lyrics-wrap {{
  position:absolute; left:0; right:0; top:840px; bottom:170px; padding:0 60px;
  display:flex; flex-direction:column; justify-content:flex-end; gap:22px;
}}
.lyric-line {{ text-align:center; transition:none; }}
.lyric-line .en {{ font-weight:900; color:#fff; line-height:1.22; text-shadow:0 2px 10px rgba(0,0,0,0.9), 0 0 22px rgba(0,0,0,0.6); }}
.lyric-line .zh {{ font-weight:600; color:rgba(255,255,255,0.92); margin-top:6px; text-shadow:0 2px 8px rgba(0,0,0,0.85); }}
.lyric-line.cur .zh {{ border-bottom:3px solid #FF8C42; padding-bottom:6px; display:inline-block; }}
.bottom-bar {{
  position:absolute; bottom:0; left:0; right:0; height:110px; padding:0 60px;
  display:flex; align-items:center; justify-content:space-between;
  background:rgba(10,10,26,0.9);
}}
.account-name {{ font-size:28px; font-weight:700; color:#fff; }}
.aigc-label {{ font-size:22px; font-weight:400; color:rgba(180,180,200,0.75); }}
</style>
<img class="bg-photo" src="file://{IMG_PATH}" alt="">
<div class="top-scrim"></div>
<div class="header">
  <div class="title-row"><div class="title">每天一首磨耳朵英文歌</div><div class="disc"></div></div>
  <div class="subtitle">坚持每天跟唱，脱口而出</div>
  <div class="progress-wrap">
    <div class="progress-times"><span>{fmt_t(start)}</span><span>{fmt_t(TOTAL)}</span></div>
    <div class="progress-bar"><div class="progress-fill"></div><div class="progress-dot"></div></div>
  </div>
  <div class="controls">
    <span class="icon">🔀</span><span class="icon">⏮</span>
    <span class="play-btn">⏸</span>
    <span class="icon">⏭</span><span class="icon">🔁</span>
  </div>
</div>
<div class="lyrics-scrim"></div>
<div class="lyrics-wrap">{lyric_html}</div>
<div class="bottom-bar">
  <span class="account-name">@一诺妈说启蒙</span>
  <span class="aigc-label">AI生成 · AIGC</span>
</div>'''


manifest = []
for i, (start, end, en, zh) in enumerate(LINES):
    out = os.path.join(FRAMES_DIR, f"frame_{i:02d}.png")
    render(frame_html(i, start, end), out, W, H)
    dur = round(end - start, 3)
    manifest.append({"file": out, "duration": dur, "start": start, "end": end, "en": en, "zh": zh})
    print(f"✅ frame_{i:02d}.png  {start:.2f}-{end:.2f}s  {en or ''}")

with open(os.path.join(OUTDIR, "manifest_v2.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print(f"\n共 {len(manifest)} 帧")
